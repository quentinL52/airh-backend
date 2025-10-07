from pydantic import Field
from app.models.mongo.base import BaseMongoModel
from app.config import settings

class CVModel(BaseMongoModel):
    collection_name: str = settings.MONGO_CV_COLLECTION

    user_id: str | None = None
    parsed_data: dict = Field(default_factory=dict)
    raw_text: str | None = None
    upload_date: str | None = None # ISO format string
