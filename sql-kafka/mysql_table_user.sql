CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    customer_id INT,
    transaction_date DATE,
    amount INT
);

GRANT ALL PRIVILEGES ON logs.* TO 'digitoon'@'%';
FLUSH PRIVILEGES;

CREATE USER 'metabase'@'%' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON logs.* TO 'metabase'@'%';
FLUSH PRIVILEGES;
