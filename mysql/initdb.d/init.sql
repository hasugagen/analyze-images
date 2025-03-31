-- init.sql

-- Create the ai_analysis_log table
CREATE TABLE `ai_analysis_log` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `image_path` VARCHAR(255) DEFAULT NULL,
    `success` TINYINT(1) NOT NULL,
    `message` VARCHAR(255) DEFAULT NULL,
    `class` INT(11) DEFAULT NULL,
    `confidence` DECIMAL(5,4) DEFAULT NULL,
    `request_timestamp` DATETIME(6) DEFAULT NULL,
    `response_timestamp` DATETIME(6) DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
