# The main repository of Praxis Bot can be found at: <https://github.com/TheCuriousNerd/Praxis-Bot>.
# Copyright (C) 2021

# Author Info Examples:
#   Name / Email / Website
#       Twitter / Twitch / Youtube / Github

# Authors:
#   Alex Orid / inquiries@thecuriousnerd.com / TheCuriousNerd.com
#       Twitter: @TheCuriousNerd / Twitch: TheCuriousNerd / Youtube: thecuriousnerd / Github: TheCuriousNerd

# This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.

#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import numexpr as ne

class Mathematician():
    def __init__(self):
        pass

    def solve_problem(self, problem):
        # Replace "^" with "**"
        problem = problem.replace("^", "**")
        return self.doMath(problem)

    def solve_unitConversion(self, value, fromUnit, toUnit):
        converter = self.UnitConverter()
        return converter.convertUnit(value, fromUnit, toUnit)

    def doMath(self, problem):
        answer = ne.evaluate(problem)
        return answer

    class UnitConverter():
        def __init__(self):
            self.imperial_distanceUnitsToMeters = [
                ("in", 0.0254),
                ("ft", 0.3048),
                ("yd", 0.9144),
                ("mi", 1609.344)
                ]
            self.imperial_volumeUnitsToLiters = [
                ("qt", 0.946352946),
                ("gal", 3.785411784),
                ("pt", 0.4731762915),
                ("cup", 0.2365882365),
                ("fl oz", 0.02957352956),
                ("tsp", 0.00492892159),
                ("tbsp", 0.0147867648)
                ]
            self.imperial_weightUnitsToGrams = [
                ("lb", 453.59237),
                ("oz", 28.349523125),
                ("st", 6350.29318),
                ("t", 907185.0),
                ("ton", 1016046.9088),
                ("tonne", 1000000)
                ]

            self.FarenheitToCelsius = lambda x: (x - 32) * 5/9
            self.CelsiusToFarenheit = lambda x: (x * 9/5) + 32
            self.CelsiusToKelvin = lambda x: x + 273.15
            self.KelvinToCelsius = lambda x: x - 273.15

            self.metric_distanceUnitsConversion = [
                ("m", 1),
                ("km", 0.001),
                ("cm", 100),
                ("mm", 1000)
                ]
            self.metric_volumeUnitsConversion = [
                ("l", 1),
                ("ml", 1000),
                ("cl", 100),
                ("dl", 10),
                ("m^3", 0.001)
                ]
            self.metric_weightUnitsConversion = [
                ("g", 1),
                ("mg", 1000),
                ("kg", 0.001)
                ]
            #self.timeUnitsConversion = [("s", 1), ("min", 60), ("hr", 3600)]

            self.temp_prefixes = ["C", "F", "K"]
            self.metric_prefixes = ["da", "h" ,"k", "M", "G", "T", "P", "E", "Z", "Y"]
            self.metric_subUnits = ["d", "c", "m", "μ", "n", "p", "f", "a", "z", "y"]

        def convertUnit(self, value, fromUnit, toUnit):
            # Convert the value from one unit to another
            # Example: convertUnit(1, "m", "ft")
            # 1 m = 3.28084 ft

            value = self.convert_to_unit(value, fromUnit, toUnit)

            # Return the converted value
            return value

        def convert_to_unit(self, value, fromUnit, toUnit):
            """
            Convert a value from one unit to another.

            :param value: The value to convert.
            :param fromUnit: The unit to convert from.
            :param toUnit: The unit to convert to.
            :return: The converted value.
            """

            # Convert the value to the base unit
            value = self.convert_to_base_unit(value, fromUnit)

            # Convert the value to the new unit
            value = self.convert_from_base_unit(value, toUnit)

            # Return the converted value
            return value

        def convert_to_base_unit(self, value, fromUnit):
            """
            Convert a value from one unit to the base unit.

            :param value: The value to convert.
            :param fromUnit: The unit to convert from.
            :return: The converted value.
            """
            conversionType_Distance = False
            for u_ in self.metric_distanceUnitsConversion:
                if fromUnit == u_[0]:
                    conversionType_Distance = True
                    print("conversion: " + str(u_[0]) + " fromu nit: " + fromUnit)
                    print("conversion: " + str(u_[1]))
                    print("conversionType_Distance metric:", conversionType_Distance)
            for u_ in self.imperial_distanceUnitsToMeters:
                if fromUnit == u_[0]:
                    conversionType_Distance = True
                    print("conversion: " + str(u_[0]) + " from unit: " + fromUnit)
                    print("conversion: " + str(u_[1]))
                    print("conversionType_Distance imperial:", conversionType_Distance)

            conversionType_Volume = False
            for u_ in self.metric_volumeUnitsConversion:
                if fromUnit == u_[0]:
                    conversionType_Volume = True
                    print("conversionType_Volume:", conversionType_Volume)
            for u_ in self.imperial_volumeUnitsToLiters:
                if fromUnit == u_[0]:
                    conversionType_Volume = True
                    print("conversionType_Volume:", conversionType_Volume)

            conversionType_Weight = False
            for u_ in self.metric_weightUnitsConversion:
                if fromUnit == u_[0]:
                    conversionType_Weight = True
                    print("conversionType_Weight:", conversionType_Weight)
            for u_ in self.imperial_weightUnitsToGrams:
                if fromUnit == u_[0]:
                    conversionType_Weight = True
                    print("conversionType_Weight:", conversionType_Weight)

            # Convert the value to the base unit
            if conversionType_Distance:
                # Convert distance to meters
                for unit in self.metric_distanceUnitsConversion:
                    if fromUnit == unit[0]:
                        value = float(value) / float(unit[1])
                for unit in self.imperial_distanceUnitsToMeters:
                    if fromUnit == unit[0]:
                        value = float(value) * float(unit[1])
            elif conversionType_Volume:
                # Convert volume to liters
                for unit in self.metric_volumeUnitsConversion:
                    if fromUnit == unit[0]:
                        value = float(value) / float(unit[1])
                for unit in self.imperial_volumeUnitsToLiters:
                    if fromUnit == unit[0]:
                        value = float(value) * float(unit[1])
            elif conversionType_Weight:
                # Convert weight to Grams
                for unit in self.metric_weightUnitsConversion:
                    if fromUnit == unit[0]:
                        value = float(value) / float(unit[1])
                for unit in self.imperial_weightUnitsToGrams:
                    if fromUnit == unit[0]:
                        value = float(value) * float(unit[1])

            # Return the converted value
            return value

        def convert_from_base_unit(self, value, toUnit):
            """
            Convert a value from the base unit to another unit.

            :param value: The value to convert.
            :param toUnit: The unit to convert to.
            :return: The converted value.
            """

            conversionType_Distance = False
            for u_ in self.metric_distanceUnitsConversion:
                if toUnit == u_[0]:
                    conversionType_Distance = True
                    print("conversionType_Distance metric:", conversionType_Distance)
            for u_ in self.imperial_distanceUnitsToMeters:
                if toUnit == u_[0]:
                    conversionType_Distance = True
                    print("conversionType_Distance imperial:", conversionType_Distance)

            conversionType_Volume = False
            for u_ in self.metric_volumeUnitsConversion:
                if toUnit == u_[0]:
                    conversionType_Volume = True
                    print("conversionType_Volume:", conversionType_Volume)
            for u_ in self.imperial_volumeUnitsToLiters:
                if toUnit == u_[0]:
                    conversionType_Volume = True
                    print("conversionType_Volume:", conversionType_Volume)

            conversionType_Weight = False
            for u_ in self.metric_weightUnitsConversion:
                if toUnit == u_[0]:
                    conversionType_Weight = True
                    print("conversionType_Weight:", conversionType_Weight)
            for u_ in self.imperial_weightUnitsToGrams:
                if toUnit == u_[0]:
                    conversionType_Weight = True
                    print("conversionType_Weight:", conversionType_Weight)

            # Convert the value from the base unit
            if conversionType_Distance:
                # Convert meters to distance
                for unit in self.imperial_distanceUnitsToMeters:
                    if unit[0] == toUnit:
                        print("imperial")
                        print("unit[0] unit[1]:", unit[0], unit[1])
                        print("value:", value)
                        value = float(value) / float(unit[1])
                for unit in self.metric_distanceUnitsConversion:
                    if unit[0] == toUnit:
                        print("metric")
                        print("unit[0] unit[1]:", unit[0], unit[1])
                        print("value:", value)
                        value = float(value) * float(unit[1])
            elif conversionType_Volume:
                # Convert liters to volume
                for unit in self.imperial_volumeUnitsToLiters:
                    if unit[0] == toUnit:
                        value = float(value) / float(unit[1])
                for unit in self.metric_volumeUnitsConversion:
                    if unit[0] == toUnit:
                        value = float(value) * float(unit[1])
            elif conversionType_Weight:
                # Convert kilograms to weight
                for unit in self.imperial_weightUnitsToGrams:
                    if unit[0] == toUnit:
                        value = float(value) / float(unit[1])
                for unit in self.metric_weightUnitsConversion:
                    if unit[0] == toUnit:
                        value = float(value) * float(unit[1])

            # Return the converted value
            return value




if __name__ == "__main__":

    math = Mathematician()

    answer = ""
    conversionProblem = input("Is this a unit conversion problem? (y/n) ")
    if conversionProblem == "y":
        fromUnit = input("What is the unit you are converting from? ")
        toUnit = input("What is the unit you are converting to? ")
        value = input("What is the value you are converting? ")
        answer = math.solve_unitConversion(value, fromUnit, toUnit)
    else:
        problem = input("What is the problem? ")
        answer = math.solve_problem(problem)
    print("The answer is: " + str(answer))
