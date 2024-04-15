CREATE TABLE ElectricityPrices (
    id INT PRIMARY KEY,
    DKK_per_kWh DECIMAL(10, 4),
    time_start DATETIME,
    time_end DATETIME
);


INSERT INTO ElectricityPrices (id, DKK_per_kWh, time_start, time_end)
VALUES