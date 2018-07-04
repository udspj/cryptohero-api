<?php

class SampleClass {

    protected $cache;
    public function __construct($cache) {
        $this->cache = $cache;
    }

    public function doSomething() {
        $item = $this->cache->getItem('unique-cache-key');
        if ($item->isHit()) {
            return 'I was previously called at ' . $item->get();
        }
        else {
            $item->set(time());
            $item->expiresAfter(3600);
            $this->cache->save($item);

            return 'I am being called for the first time, I will return results from cache for the next 3600 seconds.';
        }
    }
}