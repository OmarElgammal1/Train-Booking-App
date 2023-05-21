use TrainBooking;
-- empty tables data
delete [USER];
delete [ADMIN];
delete [CUSTOMER];
delete [TRAIN];
delete [SEAT];
delete [TRIP];
-- reset identity keys
DBCC CHECKIDENT ('Train', RESEED, 0);
DBCC CHECKIDENT ('Admin', RESEED, 0);
DBCC CHECKIDENT ('Customer', RESEED, 0);
DBCC CHECKIDENT ('Seat', RESEED, 0);
DBCC CHECKIDENT ('Trip', RESEED, 0);

-- add admins
insert into [USER](email,password) values ('amgad@admin.com','1234')
insert into [USER](email,password) values ('seif@admin.com','1234')
insert into [USER](email,password) values ('zayat@admin.com','1234')
insert into [USER](email,password) values ('omar@admin.com','1234')

insert into [ADMIN] (email)
select [USER].email from [USER]
where [USER].email = 'amgad@admin.com';

insert into [ADMIN] (email)
select [USER].email from [USER]
where [USER].email = 'seif@admin.com';

insert into [ADMIN] (email)
select [USER].email from [USER]
where [USER].email = 'zayat@admin.com';

insert into [ADMIN] (email)
select [USER].email from [USER]
where [USER].email = 'omar@admin.com';

-- add Customers
insert into [USER](email,password) values ('mahmoud@gmail.com','1234')
insert into [USER](email,password) values ('fatma@gmail.com','1234')
insert into [USER](email,password) values ('samer@gmail.com','1234')
insert into [USER](email,password) values ('salah@gmail.com','1234')


insert into [CUSTOMER] (name,email,phoneNum)
select 'Mahmoud',[USER].email,'01206212820' from [USER]
where [USER].email = 'mahmoud@gmail.com';


insert into [CUSTOMER] (name,email,phoneNum)
select 'Fatma',[USER].email,'01206212820' from [USER]
where [USER].email = 'fatma@gmail.com';

insert into [CUSTOMER] (name,email,phoneNum)
select 'Samer',[USER].email,'01206212820' from [USER]
where [USER].email = 'samer@gmail.com';

insert into [CUSTOMER] (name,email,phoneNum)
select 'Salah',[USER].email,'01206212820' from [USER]
where [USER].email = 'salah@gmail.com';

--add Trains
insert into TRAIN values (60,'Express');
insert into TRAIN values (30,'Local');
insert into TRAIN values (80,'Freight');
insert into TRAIN values (100,'High-Speed');



--add Trips
insert into TRIP (trainID,fromLocation,toLocation,depTime,price)
select [TRAIN].trainID, 'Alexandria','SharmElsheikh','2023-04-15 20:00:00',250 from TRAIN
where [TRAIN].trainID = 1;

insert into TRIP (trainID,fromLocation,toLocation,depTime,price)
select [TRAIN].trainID, 'Cairo','SharmElsheikh','2023-04-15 20:00:00',250 from TRAIN
where [TRAIN].trainID = 2;

insert into TRIP (trainID,fromLocation,toLocation,depTime,price)
select [TRAIN].trainID, 'Cairo','Alexandria','2023-05-16 20:00:00',250 from TRAIN
where [TRAIN].trainID = 3;

insert into TRIP (trainID,fromLocation,toLocation,depTime,price)
select [TRAIN].trainID, 'Alexandria','SharmElsheikh','2023-06-11 15:00:00',150 from TRAIN
where [TRAIN].trainID = 4;

insert into TRIP (trainID,fromLocation,toLocation,depTime,price)
select [TRAIN].trainID, 'Alexandria','Aswan','2023-07-21 20:00:00',500 from TRAIN
where [TRAIN].trainID = 1;


-- add Seats
Declare @i int = 0
declare @seatCount int;

select @seatCount = TRAIN.seatCount from TRAIN
where [TRAIN].trainID = 1
while @i < @seatCount
begin
set @i = @i + 1
insert into SEAT (Seat.tripID)
select TRIP.tripID from TRIP
where TRIP.tripID = 1;
end

set @i = 0
select @seatCount = TRAIN.seatCount from TRAIN
where [TRAIN].trainID = 2
while @i < @seatCount
begin
set @i = @i + 1
insert into SEAT (Seat.tripID)
select TRIP.tripID from TRIP
where TRIP.tripID = 2;
end

set @i = 0
select @seatCount = TRAIN.seatCount from TRAIN
where [TRAIN].trainID = 3
while @i < @seatCount
begin
set @i = @i + 1
insert into SEAT (Seat.tripID)
select TRIP.tripID from TRIP
where TRIP.tripID = 3;
end

set @i = 0
select @seatCount = TRAIN.seatCount from TRAIN
where [TRAIN].trainID = 4
while @i < @seatCount
begin
set @i = @i + 1
insert into SEAT (Seat.tripID)
select TRIP.tripID from TRIP
where TRIP.tripID = 4;
end

--add customer to seats
update SEAT
set customerID = 1
where seatNum = 1;

update SEAT
set customerID = 1
where seatNum = 2;

update SEAT
set customerID = 1
where seatNum = 3;

update SEAT
set customerID = 2
where seatNum = 61;

update SEAT
set customerID = 2
where seatNum = 62;

update SEAT
set customerID = 2
where seatNum = 63;

update SEAT
set customerID = 4
where seatNum = 95;

update SEAT
set customerID = 4
where seatNum = 104;

update SEAT
set customerID = 4
where seatNum = 120;

update SEAT
set customerID = 4
where seatNum = 121;

update SEAT
set customerID = 3
where seatNum = 183;

update SEAT
set customerID = 3
where seatNum = 184;