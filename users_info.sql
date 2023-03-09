DROP DATABASE IF EXISTS users_info;
CREATE DATABASE users_info;
USE users_info;

CREATE TABLE `users` (
  `pid` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `uuid` BINARY(16)  DEFAULT (UUID_TO_BIN(UUID())),
  `username` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `sms` varchar(25) DEFAULT NULL,
  `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `lastUpdated` TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO users (username, name, email, sms)
VALUES("reanderson89", "robert", "reanderson89@gmail.com", "5039279423");

SELECT * FROM users;