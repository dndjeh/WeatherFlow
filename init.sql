-- Kafka → Spark → MySQL 적재용 DB 생성
CREATE DATABASE IF NOT EXISTS weatherflow
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE weatherflow;

-- 테이블 생성
CREATE TABLE IF NOT EXISTS weather_data (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    temp FLOAT NOT NULL,
    humidity INT NOT NULL,
    weather VARCHAR(50) NOT NULL,
    timestamp datetime NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Airflow 전용 DB 생성
CREATE DATABASE IF NOT EXISTS airflow_db
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- 사용자 생성 및 권한 부여
CREATE USER IF NOT EXISTS 'user'@'%' IDENTIFIED BY 'userpass';
GRANT ALL PRIVILEGES ON weatherflow.* TO 'user'@'%';
GRANT ALL PRIVILEGES ON airflow_db.* TO 'user'@'%';
FLUSH PRIVILEGES;
