from pydantic import BaseModel, AfterValidator, ValidationError, field_validator
from typing import Annotated, Optional
from decimal import Decimal, InvalidOperation

def name_validator(username):
    try:
        str(username)
    except:
        raise ValidationError('username validation error')

def score_validator(score):
    try:
        float(score)
    except:
        raise ValidationError('score validation error')

class User(BaseModel):
    username: Annotated[Optional[str], AfterValidator(name_validator)] = None
    best_score: Annotated[Optional[str], AfterValidator(score_validator)] = None
    jwt: Optional[str] = None

    @field_validator('best_score')
    def format_score(cls, v):
        if v is None:
            return "0.00"
        try:
            return f"{float(v):.2f}"
        except (ValueError, TypeError, InvalidOperation):
            return "0.00"