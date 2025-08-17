CREATE DATABASE IF NOT EXISTS weatherflow;
USE weatherflow;

CREATE TABLE IF NOT EXISTS weather_data (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    temp FLOAT NOT NULL,
    humidity INT NOT NULL,
    weather VARCHAR(50) NOT NULL,
    timestamp datetime NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);