from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from uuid import uuid4

from app.models.feedback import Feedback, FeedbackPatch
from app.types.feedback import FeedbackCreate, FeedbackResponse
from app.database import get_session

router = APIRouter()

@router.post("/")
def create_feedback(user: FeedbackCreate, session: Session = Depends(get_session)):

    new_feedback = Feedback(**user.model_dump(), id=str(uuid4()))
    session.add(new_feedback)
    session.commit()
    session.refresh(new_feedback)

    response = FeedbackResponse(**new_feedback.model_dump())
    return response

@router.get("/", response_model=list[FeedbackResponse])
def list_feedback(session: Session = Depends(get_session)):

    feedbacks = session.exec(select(Feedback)).all()
    return [FeedbackResponse(**feedback.model_dump()) for feedback in feedbacks]

@router.get("/{feedback_id}")
def get_user(feedback_id: str, session: Session = Depends(get_session)):

    feedback = session.exec(select(Feedback).where(Feedback.id == feedback_id)).first()

    if not feedback:
        return HTTPException(status_code=404, detail="Feedback not found")

    return feedback

@router.patch("/{feedback_id}")
def update_feedback(feedback_id: str, data: FeedbackPatch, session: Session = Depends(get_session)):

    feedback = session.exec(select(Feedback).where(Feedback.id == feedback_id)).first()

    if not feedback:
        return HTTPException(status_code=404, detail="Feedback not found")

    user_data = data.model_dump(exclude_unset=True)

    for key, value in user_data.items():
        setattr(feedback, key, value)

    session.add(feedback)
    session.commit()
    session.refresh(feedback)

    return feedback

@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: str, session: Session = Depends(get_session)):

    feedback = session.exec(select(Feedback).where(Feedback.id == feedback_id)).first()

    if not feedback:
        return HTTPException(status_code=404, detail="Feedback not found")

    session.delete(feedback)
    session.commit()

    return {"message": "Feedback deleted successfully"}