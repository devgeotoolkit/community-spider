from locations.models import ServicesModel
from locations.attributes import FuelTypesEnum
from locations.exporters import convert_attrs

class TestExporters:
    # --- PHONE TESTS ---

    def test_convert_attrs_phone_with_list(self):
        result = convert_attrs("phone", ["+381 889934593", "+381 889934593"])
        assert result == {"Store": ["+381 889934593", "+381 889934593"]}

    def test_convert_attrs_phone_with_string(self):
        result = convert_attrs("phone", "+381 889934593")
        assert result == {"Store": ["+381 889934593"]}

    def test_convert_attrs_phone_with_invalid_type(self):
        result = convert_attrs("phone", 123)
        assert result == {"Store": []}
    
    # --- EMAIL TESTS ---

    def test_email_with_list(self):
        result = convert_attrs("email", ["a@test.com", "b@test.com"])
        assert result == {"Customer Service": ["a@test.com", "b@test.com"]}

    def test_email_with_string(self):
        result = convert_attrs("email", "a@test.com")
        assert result == {"Customer Service": ["a@test.com"]}

    def test_email_with_invalid_type(self):
        result = convert_attrs("email", None)
        assert result == {"Customer Service": []}

    # --- OPENING HOURS TESTS ---

    def test_opening_hours_with_string(self):
        result = convert_attrs("opening_hours", "Mo-Fr 08:00-17:00")
        assert result == {"Store": "Mo-Fr 08:00-17:00"}

    def test_opening_hours_with_dict(self):
        val = {"Store": "24/7"}
        result = convert_attrs("opening_hours", val)
        assert result == val

    def test_opening_hours_with_empty_value(self):
        result = convert_attrs("opening_hours", None)
        assert result == {"Store": []}

    # --- SERVICES TESTS ---

    def test_services_fuel_types(self):
        services = ServicesModel(FuelTypes=[FuelTypesEnum.Octane_100])
        result = convert_attrs("services", services)
        assert result == {
                        "Fuel Types": ["Octane-100"]
                    }
    
    def test_services_fuel_types_empty(self):
        services = ServicesModel()
        result = convert_attrs("services", services)
        assert result == {}

    # --- DEFAULT / FALLBACK ---

    def test_default_attribute_type(self):
        result = convert_attrs("unknown", "some_value")
        assert result == "some_value"