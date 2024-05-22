-- Creating database 
CREATE DATABASE restaurant_reservations;

-- Selecting database
USE restaurant_reservations;

-- Creating customer table
CREATE TABLE Customers (
    customerId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    customerName VARCHAR(45) NOT NULL,
    contactInfo VARCHAR(200)
);

-- Creating reservations table
CREATE TABLE Reservations (
    reservationId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    customerId INT NOT NULL,
    reservationTime DATETIME NOT NULL,
    numberOfGuests INT NOT NULL,
    specialRequests VARCHAR(200),
    FOREIGN KEY (customerId) REFERENCES Customers(customerId)
);

-- Creating diningPreferences table
CREATE TABLE DiningPreferences (
    preferenceId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    customerId INT NOT NULL,
    preference VARCHAR(255),
    FOREIGN KEY (customerId) REFERENCES Customers(customerId)
);

-- Creating Stored Procedure to find reservations
DELIMITER //
CREATE PROCEDURE findReservations(IN custId INT)
BEGIN
    SELECT * FROM Reservations WHERE customerId = custId;
END //
DELIMITER ;

-- Adding special requests
DELIMITER //
CREATE PROCEDURE addSpecialRequest(IN resId INT, IN requests VARCHAR(200))
BEGIN
    UPDATE Reservations
    SET specialRequests = requests
    WHERE reservationId = resId;
END //
DELIMITER ;

-- Adding reservations with customer check or creation
DELIMITER //
CREATE PROCEDURE addReservation(IN custId INT, IN resTime DATETIME, IN numGuests INT, IN specialReq VARCHAR(200))
BEGIN
    INSERT INTO Reservations (customerId, reservationTime, numberOfGuests, specialRequests)
    VALUES (custId, resTime, numGuests, specialReq);
END //
DELIMITER ;

-- Inserting data into Customers table
INSERT INTO Customers (customerName, contactInfo) VALUES 
('Rick James', 'RickJames@gmail.com'),
('Will Ferrel', 'WillFerrel@gmail.com'),
('Jack Black', 'JackBlack@gmail.com');

-- Inserting data into Reservations table
INSERT INTO Reservations (customerId, reservationTime, numberOfGuests, specialRequests) VALUES 
(1, '2024-05-16 9:30', 4, 'Peanut Allergy'),
(2, '2024-05-16 10:00', 2, 'Balcony Seats'),
(3, '2024-05-16 10:30', 2, 'No Special Request');

-- Inserting data into DiningPreferences table
INSERT INTO DiningPreferences (customerId, preference) VALUES 
(1, 'A5 Wagyu'),
(2, 'Vegan'),
(3, 'Lamb Shank');


