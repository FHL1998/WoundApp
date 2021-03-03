--
-- 由SQLiteStudio v3.2.1 产生的文件 周六 2月 20 19:55:00 2021
--
-- 文本编码：System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- 表：account
CREATE TABLE account (Username TEXT, Email TEXT, Password TEXT);
INSERT INTO account (Username, Email, Password) VALUES ('FHL', '17222032@bjtu.edu.cn', 'fhl19981101');

-- 表：Patient
CREATE TABLE Patient (PatientName TEXT PRIMARY KEY, Age INT, Gender TEXT, CreationDate DATE, Image VARCHAR, Swelling STRING, Redness STRING, Pus STRING, Area DOUBLE, Infection STRING);
INSERT INTO Patient (PatientName, Age, Gender, CreationDate, Image, Swelling, Redness, Pus, Area, Infection) VALUES ('FanHaolin', 22, 'Male', '2020/12/12', 'D:\newimage.png', 'Positive', 'Positive', 'Positive', 22.0, 'Negative');
INSERT INTO Patient (PatientName, Age, Gender, CreationDate, Image, Swelling, Redness, Pus, Area, Infection) VALUES ('LiuYoujie', 21, 'Male', '2021/01/06', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO Patient (PatientName, Age, Gender, CreationDate, Image, Swelling, Redness, Pus, Area, Infection) VALUES ('', '', '', '', NULL, NULL, NULL, NULL, NULL, NULL);

-- 表：User
CREATE TABLE User (id INTEGER PRIMARY KEY, name VARCHAR (20), head_image VARCHAR (200));
INSERT INTO User (id, name, head_image) VALUES (1, 'FHL', 'image/c0c.jpg');

-- 表：Wound
CREATE TABLE Wound (ID INTEGER, Swelling CHAR, Redness CHAR, Pus CHAR, Area DOUBLE, Infection CHAR);
INSERT INTO Wound (ID, Swelling, Redness, Pus, Area, Infection) VALUES (1, 'True', 'True', 'False', 22.0, 'True');
INSERT INTO Wound (ID, Swelling, Redness, Pus, Area, Infection) VALUES (2, 'False', 'True', 'True', 50.0, 'False');

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
