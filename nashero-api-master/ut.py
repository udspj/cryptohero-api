import requests
import json
import logging
import pymongo

db = pymongo.MongoClient(port=27014)["tt"]

s = requests.session()
s.headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
}
s1 = requests.session()
s1.headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
}


def getMaxhash():
    """获取最大的hash"""
    if db["ttt"].count():
        return (
            db["ttt"]
            .find({}, {"hash": 1, "_id": 0})
            .sort("createdAt", pymongo.DESCENDING)[0]["hash"]
        )

    else:
        return ""


def getalldata(hash, page=1, datas=[]):
    print("get tx page ...", page)
    url = "https://explorer.nebulas.io/main/api/tx?a=n1gDfiiQLEBu95xDWHGxNi4qToyXjD2vE4D&p={}".format(
        page
    )
    z = s.get(url)
    data = z.json()["data"]["txnList"]
    hashs = [i["hash"] for i in data]
    if hash in hashs:
        for i in data:
            if i["hash"] == hash:
                for i in datas:
                    i["data"] = json.loads(i["data"])
                return save2db(
                    sorted(datas, key=lambda x: x["createdAt"], reverse=False)
                )

            else:
                datas.append(i)
    else:
        datas.extend(data)

        totalPage = z.json()["data"]["totalPage"]
        currentPage = z.json()["data"]["currentPage"]
        if currentPage < totalPage:
            getalldata(hash, currentPage + 1, datas=datas)
        else:
            for i in datas:
                i["data"] = json.loads(i["data"])
            save2db(sorted(datas, key=lambda x: x["createdAt"], reverse=False))


def save2db(data):
    if data:
        if not isinstance(data, list):
            data = [data]
        f_data = filter(lambda a: a["data"]["Function"] == "setTokenPrice", data)
        buyToken_data = filter(lambda a: a["data"]["Function"] == "buyToken", data)
        # 过滤掉调用异常的
        f_data = filter(lambda a: a["executeError"] == "", f_data)
        for i in f_data:
            # print(i)
            tokenid, price = json.loads(i["data"]["Args"])
            createdAt = i["createdAt"]  # 现在的时间
            if not isTokenClaimed(tokenid):
                heroId = getHeroIdByTokenId(tokenid)
                db["hero"].update_one(
                    {"tokenId": tokenid},
                    {
                        "$set": {
                            "tokenId": str(tokenid),
                            "heroId": heroId,
                            "price": price,
                            "createdAt": createdAt,
                        }
                    },
                    upsert=True,
                )
        for i in buyToken_data:
            tokenid = json.loads(i["data"]["Args"])[0]
            nowCreatedAt = i["createdAt"]  # 购买的时间
            d = db["hero"].find_one(
                {"tokenId": str(tokenid)}, {"createdAt": 1, "_id": 0}
            )
            print(tokenid, d, nowCreatedAt)
            if d:
                createdAt = d["createdAt"]
                if nowCreatedAt > createdAt:
                    db["hero"].delete_one({"tokenId": str(tokenid)})

        db["ttt"].insert_many(data)


def getHeroIdByTokenId(tokenid):
    print("getHeroIdByTokenId", tokenid)
    url = "https://mainnet.nebulas.io/v1/user/call"
    data = {
        "from": "n1Z6SbjLuAEXfhX1UJvXT6BB5osWYxVg3F3",
        "to": "n1gDfiiQLEBu95xDWHGxNi4qToyXjD2vE4D",
        "value": "0",
        "nonce": 0,
        "gasPrice": "1000000",
        "gasLimit": "20000000",
        "contract": {"function": "getHeroIdByTokenId", "args": "[{}]".format(tokenid)},
    }
    z = s1.post(url, json=data)
    try:
        return z.json()["result"]["result"]
    except:
        print(z.text)
        logging.exception("getHeroIdByTokenId error")
        return getHeroIdByTokenId(tokenid)


def isTokenClaimed(tokenid):
    print("isTokenClaimed", tokenid)
    url = "https://mainnet.nebulas.io/v1/user/call"
    data = {
        "from": "n1Z6SbjLuAEXfhX1UJvXT6BB5osWYxVg3F3",
        "to": "n1gDfiiQLEBu95xDWHGxNi4qToyXjD2vE4D",
        "value": "0",
        "nonce": 0,
        "gasPrice": "1000000",
        "gasLimit": "20000000",
        "contract": {"function": "isTokenClaimed", "args": "[{}]".format(tokenid)},
    }
    z = s1.post(url, json=data)
    try:
        # print(z.json()["result"]["result"])
        return json.loads(z.json()["result"]["result"])
    except:
        print(z.text)
        logging.exception("isTokenClaimed")
        return isTokenClaimed(tokenid)


def run():
    print("run...")
    hash = getMaxhash()
    getalldata(hash)


if __name__ == "__main__":
    run()
    # print(hash)
    # getTx(hash)
    # print(getHeroIdByTokenId(11739))
    # print(
    # print(type(isTokenClaimed(123)))
    # tokenid = 12345
    # while True:
    #     print(isTokenClaimed(tokenid))
    #     tokenid += 1
