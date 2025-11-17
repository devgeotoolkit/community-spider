from locations.models import ServicesModel
from locations.attributes import FuelTypesEnum
import json
import pytest
from pydantic import ValidationError

class TestServices:
    def test_services_base_model_incorrect_fuel_types(self):
        with pytest.raises(ValidationError):
            fuel_types = [1,1]
            ServicesModel(FuelTypes=fuel_types)
    
    def test_services_base_model_empty(self):
        services = ServicesModel()
        services_dict = json.loads(services.model_dump_json())
        assert services_dict == {"FuelTypes": None, 'Accessibility': None, 'Amenities': None}
    
    def test_services_base_model_fuel_types(self):
        fuel_types = [FuelTypesEnum.Octane_87]
        services = ServicesModel(FuelTypes=fuel_types)
        
        services_dict = json.loads(services.model_dump_json())
        assert services_dict == {"FuelTypes": ["Octane-87"], 'Accessibility': None, 'Amenities': None}
    
    def test_services_base_model_fuel_types_empty(self):
        fuel_types = []
        services = ServicesModel(FuelTypes=fuel_types)
        
        services_dict = json.loads(services.model_dump_json())
        assert services_dict == {"FuelTypes": [], 'Accessibility': None, 'Amenities': None}
