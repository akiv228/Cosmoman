from pydantic import BaseModel, AfterValidator, ValidationError
from typing import Annotated, Optional


def name_validator(username):
    try: str(username)
    except: raise ValidationError('username validation error')

def score_validator(score):
    try: int(score)
    except: raise ValidationError('password validation error')

class User(BaseModel):
    username: Annotated[Optional[str], AfterValidator(name_validator)] = None
    best_score: Annotated[Optional[str], AfterValidator(score_validator)] = None
    jwt: Optional[str] = None
