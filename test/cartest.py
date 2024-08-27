import sys
import os
parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_folder)
from models.car import Car
car = Car.find(1)
print('car:', car.getID(), car.getColor(), car.getDetails(), car.isAvailable())

cars = Car.allAvailable()
print(car)