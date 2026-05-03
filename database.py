from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Float, Date


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    student = relationship("Student", back_populates="user", uselist=False)
    teacher = relationship("Teacher", back_populates="user", uselist=False)
    manager = relationship("Manager", back_populates="user", uselist=False)


class Teacher(db.Model):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    manager_id: Mapped[int] = mapped_column(ForeignKey("managers.id"))
    phone_number: Mapped[str] = mapped_column(String(20))
    birth_date: Mapped[date] = mapped_column(Date)
    address: Mapped[str] = mapped_column(String(255))

    user = relationship("User", back_populates="teacher")
    students = relationship("Student", back_populates="teacher")
    manager = relationship("Manager", back_populates="teachers")


class Student(db.Model):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    manager_id: Mapped[int] = mapped_column(ForeignKey("managers.id"))
    phone_number: Mapped[str] = mapped_column(String(20))
    birth_date: Mapped[date] = mapped_column(Date)
    address: Mapped[str] = mapped_column(String(255))
    score: Mapped[float] = mapped_column(Float)
    grade_level: Mapped[int] = mapped_column(Integer, nullable=False)

    user = relationship("User", back_populates="student")
    teacher = relationship("Teacher", back_populates="students")
    manager = relationship("Manager", back_populates="students")
    

class Manager(db.Model):
    __tablename__ = "managers"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20))
    birth_date: Mapped[date] = mapped_column(Date)
    address: Mapped[str] = mapped_column(String(255))
    
    user = relationship("User", back_populates="manager")
    teachers = relationship("Teacher", back_populates="manager")
    students = relationship("Student", back_populates="manager")
