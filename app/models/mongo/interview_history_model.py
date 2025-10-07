from pydantic import Field
from app.models.mongo.base import BaseMongoModel
from app.config import settings

class InterviewHistoryModel(BaseMongoModel):
    collection_name: str = settings.MONGO_INTERVIEW_COLLECTION

    user_id: str | None = None
    cv_id: str | None = None
    conversation: list[dict] = Field(default_factory=list) # List of {role: str, content: str}
    start_time: str | None = None # ISO format string
    end_time: str | None = None # ISO format string
