from pydantic import BaseModel
from locations.attributes import FuelTypesEnum
from typing import List, Union

class ServicesModel(BaseModel):
    Accessibility: Union[List[str], None] = None
    Amenities: Union[List[str], None] = None
    FuelTypes: Union[List[FuelTypesEnum], None] = None