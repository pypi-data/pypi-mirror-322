import pint

class Units:
    def __init__(self):
        # Initialize a Pint UnitRegistry, which holds all unit definitions
        self.ureg = pint.UnitRegistry()

    def get(self, unit_string):
        """
        Given a unit string (e.g., 'meter', 'second', 'kg'), returns the unit object.
        """
        return self.ureg(unit_string)
    
    def convert(self, value, from_unit, to_unit):
        """
        Convert a value from one unit to another.
        
        Args:
        - value (float): The numerical value to convert.
        - from_unit (str): The unit to convert from (e.g., 'meter', 'kg').
        - to_unit (str): The unit to convert to (e.g., 'foot', 'lb').

        Returns:
        - Converted value.
        """
        # Get the unit objects for from_unit and to_unit
        from_unit_obj = self.ureg(from_unit)
        to_unit_obj = self.ureg(to_unit)
        
        # Perform the conversion
        return (value * from_unit_obj).to(to_unit_obj).magnitude

    def list_units(self):
        """
        List some example units available in Pint.
        """
        return self.ureg.get_available_units()


# Example Usage:
if __name__ == "__main__":
    # Create an instance of UnitConverter
    converter = Units()
    
    # Accessing a unit directly
    meter = converter.get('meter')
    second = converter.get('second')
    kilogram = converter.get('kilogram')

    print(f"1 meter = {meter}")
    print(f"1 second = {second}")
    print(f"1 kilogram = {kilogram}")
    
    # Convert from meters to feet
    length_in_meters = 10
    length_in_feet = converter.convert(length_in_meters, 'meter', 'foot')
    print(f"{length_in_meters} meters = {length_in_feet} feet")
    
    # List available units
    units = converter.list_units()
    print(f"Some available units: {list(units)[:10]}")  # Print first 10 units
