USE TrainBooking
GO
-- Delete data from tables (optional if tables are already empty)
DELETE FROM [USER];
DELETE FROM [ADMIN];
DELETE FROM [CUSTOMER];
DELETE FROM [SEAT];
DELETE FROM [TRIP];
DELETE FROM [TRAIN];
GO
-- Reset identity columns to maintain the starting numbers of each column
DBCC CHECKIDENT ('[ADMIN]', RESEED, 0);
DBCC CHECKIDENT ('[CUSTOMER]', RESEED, 0);
DBCC CHECKIDENT ('[SEAT]', RESEED, 0);
DBCC CHECKIDENT ('[TRAIN]', RESEED, 0);
DBCC CHECKIDENT ('[TRIP]', RESEED, 0);
GO
-- Insert new users into the USER table
INSERT INTO [USER]
VALUES
    ('0000', 'seif@admin'),
    ('0000', 'amgad@admin'),
    ('0000', 'omar@admin'),
    ('0000', 'mohsen@admin'),
    ('0000', 'zayat@admin'),
    ('0000', 'fatma@admin'),
    ('0000', 'nour@admin'),
    ('0000', 'hoda@admin'),
    ('0000', 'ali@admin'),
    ('0000', 'john@admin'),
    ('1111', 'seif@user'),
    ('1111', 'amgad@user'),
    ('1111', 'omar@user'),
    ('1111', 'mohsen@user'),
    ('1111', 'zayat@user'),
    ('1111', 'fatma@user'),
    ('1111', 'nour@user'),
    ('1111', 'hoda@user'),
    ('1111', 'ali@user'),
    ('1111', 'john@user');
GO
-- Insert admins into the ADMIN table
INSERT INTO ADMIN
SELECT email FROM [USER]
WHERE email LIKE '%@admin%';
GO
-- Insert customers into the CUSTOMER table
INSERT INTO CUSTOMER
SELECT
	CONCAT(UPPER(LEFT(U.email, 1)), LOWER(SUBSTRING(U.email, 2, CHARINDEX('@', U.email) - 2))) AS name,
    '01234567890', -- Use a sample phone number
    U.email
FROM [USER] U
WHERE U.email LIKE '%@user%';
GO
-- Insert new trains into the TRAIN table
INSERT INTO TRAIN
VALUES
    (100, 'Bullet'),
    (200, 'Express'),
    (150, 'Local'),
    (120, 'Commuter'),
    (200, 'Electric'),
    (250, 'Freight'),
    (150, 'Maglev'),
    (100, 'Monorail'),
	(300, 'Regional'),
	(80, 'Tram');
GO
-- Insert new trips into the TRIP table
INSERT INTO TRIP (trainID, fromLocation, toLocation, depTime, price)
SELECT
    T.trainID,
    F.fromLocation,
    F.toLocation,
    DATEADD(DAY, ROW_NUMBER() OVER (PARTITION BY T.trainID ORDER BY NEWID()), DATEADD(MONTH, 2, GETDATE())) AS depTime,
    CAST((RAND(CHECKSUM(NEWID())) * 100 + 50) AS INT) AS price
FROM
    (SELECT DISTINCT trainID FROM TRAIN) AS T
    CROSS JOIN (VALUES ('Cairo', 'Alex'), ('Tanta', 'Sharm El Sheikh'), ('Aswan', 'Luxor'), ('Assiut', 'Matrouh'), ('Qena', 'Mansoura')) AS F(fromLocation, toLocation);
GO

-- Add seats to trips and assign seats to customers manually from the application

-- Output the inserted data (optional)
SELECT * FROM [ADMIN];
SELECT * FROM [CUSTOMER];
SELECT * FROM [SEAT];
SELECT * FROM [TRAIN];
SELECT * FROM [TRIP];
SELECT * FROM [USER];
GO