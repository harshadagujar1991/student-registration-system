# models.py
# SQLAlchemy models for Student Registration System

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Department(db.Model):
    __tablename__ = 'Departments'
    Dept_ID = db.Column(db.Integer, primary_key=True)
    Dept_Name = db.Column(db.String(100), unique=True, nullable=False)

class Student(db.Model):
    __tablename__ = 'Students'
    Student_ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    DOB = db.Column(db.Date, nullable=True)
    Email = db.Column(db.String(100), unique=True, nullable=True)
    Dept_ID = db.Column(db.Integer, db.ForeignKey('Departments.Dept_ID'), nullable=True)

class Faculty(db.Model):
    __tablename__ = 'Faculty'
    Faculty_ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Dept_ID = db.Column(db.Integer, db.ForeignKey('Departments.Dept_ID'))

class Course(db.Model):
    __tablename__ = 'Courses'
    Course_ID = db.Column(db.Integer, primary_key=True)
    Course_Name = db.Column(db.String(100), nullable=False)
    Credits = db.Column(db.Integer)
    Dept_ID = db.Column(db.Integer, db.ForeignKey('Departments.Dept_ID'))
    Faculty_ID = db.Column(db.Integer, db.ForeignKey('Faculty.Faculty_ID'))

class Registration(db.Model):
    __tablename__ = 'Registrations'
    Reg_ID = db.Column(db.Integer, primary_key=True)
    Student_ID = db.Column(db.Integer, db.ForeignKey('Students.Student_ID'))
    Course_ID = db.Column(db.Integer, db.ForeignKey('Courses.Course_ID'))
    Semester = db.Column(db.String(20), nullable=False)

class Payment(db.Model):
    __tablename__ = 'Payments'
    Pay_ID = db.Column(db.Integer, primary_key=True)
    Student_ID = db.Column(db.Integer, db.ForeignKey('Students.Student_ID'))
    Amount = db.Column(db.Numeric(10,2), nullable=False)
    Status = db.Column(db.String(20), nullable=False)  # Paid / Pending / Failed
    Date = db.Column(db.Date, nullable=False)
