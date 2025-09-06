from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
import models1 # Updated import
from database1 import engine, SessionLocal # Updated import
from sqlalchemy.orm import Session

# Creating the FastAPI application instance
app = FastAPI()

# Creating the database tables defined in the models1.py file
models1.Base.metadata.create_all(bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        # Yielding the session to the route function
        yield db
    finally:
        # Closeing the session after the request is completed
        db.close()

# Pydantic model for a Student, used for request body validation
class Student(BaseModel):
    name: str = Field(min_length=1, description="Full name of the student.")
    age: int = Field(gt=0, description="Age of the student.")
    email_id: EmailStr = Field(description="Email address of the student.")

# Retrieving all students from the database
@app.get("/")
def read_api(db: Session = Depends(get_db)):
    # Query the database for all student records
    return db.query(models1.Students).all()

# Creating a new student record
@app.post("/")
def create_student(student: Student, db: Session = Depends(get_db)):
    # Create a new instance of the Students SQLAlchemy model
    student_model = models1.Students()
    student_model.name = student.name
    student_model.age = student.age
    student_model.email_id = student.email_id

    # Adding the new student record to the database and commit the transaction
    db.add(student_model)
    db.commit()
    
    # Returning the created student object
    return student

# Updating an existing student record by ID
@app.put("/{student_id}")
def update_student(student_id: int, student: Student, db: Session = Depends(get_db)):
    # Query the database to find the student by ID
    student_model = db.query(models1.Students).filter(models1.Students.id == student_id).first()
    
    # Raising a 404 error if the student is not found
    if student_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {student_id} : Student does not exist"
        )
    
    # Updating the student model's attributes with the new data
    student_model.name = student.name
    student_model.age = student.age
    student_model.email_id = student.email_id
    
    # Commiting the changes to the database
    db.add(student_model)
    db.commit()
    
    # Returning the updated student object
    return student

# Deleting a student record by ID
@app.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    # Query the database to find the student by ID
    student_model = db.query(models1.Students).filter(models1.Students.id == student_id).first()
    
    # Raising a 404 error if the student is not found
    if student_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {student_id} : Student does not exist"
        )
    
    # Deleting the student record from the database
    db.query(models1.Students).filter(models1.Students.id == student_id).delete()
    
    # Commiting the deletion to the database
    db.commit()
    
    # Returning a success message
    return {"message": f"Student with ID {student_id} has been deleted successfully."}
