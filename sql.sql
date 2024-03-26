use project;
create table department
(
dept_name varchar(20),
building varchar(20),
budget varchar(20),
primary key(dept_name)
);
create table instructor
(
ID varchar(20),
instructor_name varchar(20),
salary int(20),
dept_name varchar(20) NOT NULL,
primary key(ID),
foreign key(dept_name) references department(dept_name)
);
create table student
(
ID varchar(20),
stu_name varchar(20),
MENTOR varchar(20),
dept_name varchar(20) NOT NULL,
total_cred int(20),
foreign key(dept_name) references department(dept_name),
foreign key(FID) references instructor(ID),
primary key(ID)
);
create table attendance
(
	aid int(6),
	Dld int(10),
    dbms int(10),
    primary key (aid)
);
create table student_login
(
	ID varchar(20),
	username varchar(20),
    password1 varchar(20),
    primary key(username),
    foreign key(ID) references student(ID)
    
);
create table instructor_login
(
	username1 varchar(20),
    password2 varchar(20),
    primary key(username1)
);
drop table student_login;
insert into student_login values("NIKHIL","N");
select username1 from student_login where username1 =student_loginstudent_login "NIKHIL";
