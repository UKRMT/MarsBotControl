create database Rover;
create user 'openmct'@'localhost' identified by 'trashcan';
grant  select,insert,update,delete,create,drop on Rover.* to 'openmct'@'localhost';
