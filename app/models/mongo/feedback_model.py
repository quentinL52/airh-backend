from pydantic import Field
from app.models.mongo.base import BaseMongoModel
from app.config import settings

class FeedbackModel(BaseMongoModel):
    collection_name: str = settings.MONGO_FEEDBACK_COLLECTION

    user_id: str | None = None
    interview_id: str | None = None
    feedback_content: dict = Field(default_factory=dict)
    feedback_date: str | None = None # ISO format string
