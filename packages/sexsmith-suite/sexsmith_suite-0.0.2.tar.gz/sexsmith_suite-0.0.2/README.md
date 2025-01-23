# Sexsmith Suite
Sexsmith Suite is an engineering toolbox designed to assist engineers, particularly those working in ERPL (Engineering Rocket Propulsion Laboratory), with essential calculations and unit conversions.

This suite is built to save time by providing a core set of effective functions, allowing experienced developers to quickly implement analysis and design calculations without reinventing the wheel. Instead of re-writing functions for every new project (like your 5 billionth rocket calculator), leverage the Sexsmith Suite for initial calculations and unit conversions, while focusing on key design decisions.

The suite is also a fantastic resource for young engineers, providing easy access to basic equations for rocket engine analysis and design.

## Key Features of Sexsmith Suite:
Simple Unit Conversions: The core module provides simple, effective unit conversion functions that are easy to use for those unfamiliar with object-oriented programming or intimidated by more complex libraries like Pint.
Lightweight and Efficient: Unlike other libraries, Sexsmith Suite doesn't overcomplicate things with unit-tied objects. It directly returns raw magnitudes, making it fast and flexible, even for complex calculations (e.g., square roots, complex equations like Bartz).
Designed for Engineers: Ideal for both seasoned developers and beginner engineers, providing a clean and intuitive way to perform unit conversions and basic calculations.

## Installation
You can easily install the Sexsmith Suite via pip:

```
pip install sexsmith-suite
```
Once installed, you can start using Sexsmith Suite in your Python code. 


## Why Use Sexsmith Suite?
Reduced Complexity: While Pint is an excellent library for unit conversions, Sexsmith Suite is a simpler, more approachable solution for those who don't need all the complexity that comes with unit-tied objects. If you're performing quick conversions and don't want to deal with the overhead, this is the package for you.

Note On Better Coding Practices: Although Sexsmith Suite provides raw magnitudes, it's highly recommended that you use a unit-aware library like Pint for more robust, production-grade applications to maintain correct unit consistency and improve overall coding practices.

## Examples

### Using Sexsmith Core
Sexsmith Core is the section of the package intended for basic engineering conversions and calculations. For now, this is primarily an non-objected-oriented unit converter.
The convert function allows you to easily convert values between units.Unlike more complex libraries, Sexsmith Suite does not tie values to unit objects, returning raw magnitudes to avoid unnecessary complexity. This was designed for Quick, Accurate Conversions, which is especially useful for engineers needing quick calculations without diving into more complex libraries like Pint.
 Here's a quick example of how to use the core unit conversion functionality:

Example:
```
import sexsmith_suite.core as sexcore

# Initialize the core Units class
units = sexcore.Units()

# Convert a value (e.g., 1 foot to meters)
initial_value = 1  # in feet
new_value = units.convert(initial_value, from_unit='ft', to_unit='m')  # result in meters

print(f"{initial_value} ft = {new_value} m")
```

## Development and Contributing
If you'd like to contribute to the development of Sexsmith Suite, feel free to fork the repository and submit pull requests. Any improvements to the code or documentation are always welcome!

## License
Sexsmith Suite is licensed under the MIT License.