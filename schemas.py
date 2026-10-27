from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError


class DemandeChat(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=2000,
        description="La question posée par l'utilisateur"
    )
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

    @field_validator("message")
    @classmethod
    def message_non_vide(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("le message ne peut pas être uniquement des espaces")
        return v.strip()


class Periode(BaseModel):
    jour_arrivee: int = Field(ge=1, le=31)
    jour_depart: int = Field(ge=1, le=31)

    @model_validator(mode="after")
    def depart_apres_arrivee(self):
        if self.jour_depart <= self.jour_arrivee:
            raise ValueError("le départ doit être après l'arrivée")
        return self

class ReponseChat(BaseModel):
    texte: str
    modele: str
    nb_caracteres: int
    
def essayer(libelle, fonction):
    print(f"\n--- {libelle} ---")
    try:
        resultat = fonction()
        print("OK :", resultat)
    except ValidationError as e:
        print("REFUSÉ :")
        print(e)


