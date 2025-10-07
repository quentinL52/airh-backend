from pydantic import BaseModel, Field
from typing import Optional

class JobOffer(BaseModel):
    id: str
    entreprise: Optional[str] = None
    ville: Optional[str] = None
    poste: Optional[str] = None
    contrat: Optional[str] = None
    description_poste: Optional[str] = Field(None, alias="description_poste")
    publication: Optional[str] = None
    lien: Optional[str] = None
    description_nettoyee: Optional[str] = Field(None, alias="description_nettoyee")
    mission: Optional[str] = None
    profil_recherche: Optional[str] = Field(None, alias="profil_recherche")
    competences: Optional[str] = None
    pole: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True