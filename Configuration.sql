create schema if not exists Hotel_Management;

use Hotel_Management;

-- drop table if exists Guest;
-- truncate table Guest;

CREATE TABLE if not exists Guest (
    GuestID INT AUTO_INCREMENT PRIMARY KEY,
    GuestName VARCHAR(100) NOT NULL,
    Address_City VARCHAR(50),
    Address_State VARCHAR(50),
    Address_Street VARCHAR(100),
    Address_Zipcode VARCHAR(10),
    Email VARCHAR(100)
);
select * from guest;

-- Drop table if exists guest_phone;
-- truncate table guest_phone;

CREATE TABLE if not exists guest_phone (
    PhoneID INT AUTO_INCREMENT PRIMARY KEY,
    GuestID INT NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    FOREIGN KEY (GuestID) REFERENCES Guest(GuestID) ON DELETE CASCADE
);
select * from guest_phone;

-- Drop table if exists staff;
-- truncate table staff;

CREATE TABLE if not exists Staff (
    StaffID INT AUTO_INCREMENT PRIMARY KEY,
    StaffName VARCHAR(50) NOT NULL,
    Role VARCHAR(100),
    ContactInfo VARCHAR(20)
);
select * from Staff;

-- drop table if exists room;
-- truncate table room;

create table if not exists room(
	roomnumber int auto_increment PRIMARY KEY,
    roomtype varchar(10) NOT NULL,
    price int NOT NULL,
    capacity int NOT NULL,
    status varchar(15)
);

select * from room;

-- drop table if exists service;
-- truncate table service;

CREATE TABLE Service (
    ServiceID INT PRIMARY KEY,
    ServiceType VARCHAR(30),
    Description VARCHAR(255),
    Cost DECIMAL(10, 2)
);
select * from service;

-- drop table if exists reservation;
-- truncate table reservation;

CREATE TABLE Reservation (
    ReservationID INT AUTO_INCREMENT PRIMARY KEY,
    CheckInDate DATE NOT NULL,
    CheckOutDate DATE NOT NULL,
    ReservationStatus VARCHAR(20),
    TotalCost DECIMAL(10, 2),
    StaffID INT,
    GuestID INT NOT NULL,
    RoomNumber INT NOT NULL,
    FOREIGN KEY (GuestID) REFERENCES Guest(GuestID),
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID),
    FOREIGN KEY (RoomNumber) REFERENCES Room(RoomNumber)
);
select * from reservation;

-- drop table if exists payment;
-- truncate table payment;

create table if not exists Payment (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    PaymentMethod VARCHAR(20) NOT NULL, 
    PaymentDate DATE NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    ReservationID INT NOT NULL,
    FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID)
);
select * from payment;

-- drop table if exists amenity;
-- truncate table amenity;

CREATE TABLE Amenity (
    AmenityID varchar(10) PRIMARY KEY,
    Name VARCHAR(50),
    Description VARCHAR(255),
    RoomNumber INT,
    FOREIGN KEY (RoomNumber) REFERENCES Room(RoomNumber)
);
select * from amenity;

-- drop table if exists roomreservation;
-- truncate table roomreservation;

create table if not exists roomreservation(
	id INT AUTO_INCREMENT PRIMARY KEY,
	RoomNumber INT,
    ReservationID INT,
    FOREIGN KEY (RoomNumber) REFERENCES Room(RoomNumber),
    FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID)
);
select * from roomreservation;

-- drop table if exists reservationservice;
-- truncate table reservationservice;

create table if not exists reservationservice(
	ReservationID INT,
    ServiceID INT,
    PRIMARY KEY (ReservationID, ServiceID),
    FOREIGN KEY (ServiceID) REFERENCES Service(ServiceID),
    FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID)
);
select * from reservationservice;

-- drop table if exists roomamenity;
-- truncate table roomamenity;

create table if not exists roomamenity(
	RoomNumber INT,
    AmenityID VARCHAR(10),
    PRIMARY KEY (RoomNumber, AmenityID),
    FOREIGN KEY (RoomNumber) REFERENCES Room(RoomNumber),
    FOREIGN KEY (AmenityID) REFERENCES Amenity(AmenityID)
);
select * from roomamenity;

CREATE VIEW all_services AS
SELECT * FROM service;