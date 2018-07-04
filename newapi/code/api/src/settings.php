<?php
return [
    'settings' => [
        'displayErrorDetails' => true, // set to false in production
        'addContentLengthHeader' => false, // Allow the web server to send the content-length header

        // Renderer settings
        'renderer' => [
            'template_path' => __DIR__ . '/../templates/',
        ],

        // Monolog settings
        'logger' => [
            'name' => 'slim-app',
            'path' => __DIR__ . '/../logs/app.log',
            'level' => \Monolog\Logger::DEBUG,
        ],

        // DataBase(MySQL) settings
          'db' => [
              'host' => '127.0.0.1',
              'port' => '3306',
              'user' => 'root',
              'pass' => '123456',
              'dbname' => 'seichijunrei'//,
              // 'charset'   => 'utf-8',
              // 'collation' => 'utf8_unicode_ci'
          ],
    ],
];
