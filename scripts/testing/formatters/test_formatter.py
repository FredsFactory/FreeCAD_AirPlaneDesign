# Test du formateur Python Black
# Ce fichier est mal formaté intentionnellement


def test_function(x, y, z):
    if x > 0:
        result = x * y + z
        return result
    else:
        return None


class TestClass:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value


# Imports mal organisés
import os
import freecad_imports
import sys
from freecad_imports import App, Vector, Part

# Liste mal formatée
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

# Dictionnaire mal formaté
my_dict = {"key1": "value1", "key2": "value2", "key3": "value3", "key4": "value4"}

# Conditions mal formatées
if True:
    print("Hello")
if False:
    print("World")

# Fonction principale
if __name__ == "__main__":
    test = TestClass(42)
    print(test.get_value())
