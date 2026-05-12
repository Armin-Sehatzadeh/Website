from datetime import date, datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Float, Date


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


# DATABASE USER
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


# DATABASE TEACHER
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


# DATABASE STUDENT
class Student(db.Model):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), nullable=True)
    manager_id: Mapped[int] = mapped_column(ForeignKey("managers.id"), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20))
    birth_date: Mapped[date] = mapped_column(Date)
    address: Mapped[str] = mapped_column(String(255))
    score: Mapped[float] = mapped_column(Float)
    grade_level: Mapped[int] = mapped_column(Integer, nullable=False)

    user = relationship("User", back_populates="student")
    teacher = relationship("Teacher", back_populates="students")
    manager = relationship("Manager", back_populates="students")
  
    
# DATABASE MANAGER
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


# DATABASE BLOCKLIST
class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    jti: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))