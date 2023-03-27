from pydantic import BaseModel


class postCountryBody(BaseModel):
    """Pydantic BaseModel for the body of postCountryBody"""

    country: str
    date: str
