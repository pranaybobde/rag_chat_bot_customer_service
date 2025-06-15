import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
import uvicorn
from models import Complaint, SessionLocal


class ComplaintCreate(BaseModel):
    name: constr(min_length=2)
    phone_number: constr(min_length=10, max_length=15, pattern=r'^\d{10,15}$')
    email: EmailStr
    complaint_details: str


app = FastAPI()

@app.get("/")
async def home():
    return "Server is Live !!!"


@app.post("/complaints")
def create_complaint(complaint: ComplaintCreate):
    
    try:
        complaint_id = str(uuid.uuid4())
        created_at = datetime.now()
        
        with SessionLocal() as session:
            try:
                db_complaint = Complaint(
                    complaint_id=complaint_id,
                    name=complaint.name,
                    phone_number=complaint.phone_number,
                    email=complaint.email,
                    complaint_details=complaint.complaint_details,
                    created_at=created_at
                )
                
                session.add(db_complaint)
                session.commit()
                session.refresh(db_complaint)
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erro while adding complaint data to db: {str(e)}")
        
        return {"complaint_id": complaint_id, "message": "Complaint created successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro while processing request: {str(e)}")

@app.get("/complaints/{complaint_id}")
def get_complaint(complaint_id: str):
    with SessionLocal() as session:
        try:
            db_complaint = session.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro while adding complaint data to db: {str(e)}")
    if not db_complaint:
        raise HTTPException(status_code=404, detail=f"Complaint not found with complaint id {complaint_id}")
    
    return {
        "complaint_id": db_complaint.complaint_id,
        "name": db_complaint.name,
        "phone_number": db_complaint.phone_number,
        "email": db_complaint.email,
        "complaint_details": db_complaint.complaint_details,
        "created_at": db_complaint.created_at.isoformat()
    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8002)