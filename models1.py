from sqlalchemy import Column, Integer, String
from database1 import Base # Updated import

# Define the SQLAlchemy model for the students table
class Students(Base):
    __tablename__ = "students"
    
    # Define columns for the table
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    email_id = Column(String)
