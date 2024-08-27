from .mysql_connector import execute_query

class Car:
    def __init__(self, id, make, model, year, color, image_url, details, available=True) -> None:
        self._id = id
        self._make = make
        self._model = model
        self._year = year
        self._color = color
        self._image_url = image_url
        self._details = details
        self._available = available

    def getID(self):
        return self._id

    def getMake(self):
        return self._make
    
    def getModel(self):
        return self._model
    
    def getYear(self):
        return self._year
    
    def getColor(self):
        return self._color

    def getImageURL(self):
        return self._image_url

    def getDetails(self):
        return self._details
    
    def isAvailable(self):
        return self._available
    
    def setAvailable(self, available):
        self._available = available

    def save(self):
        if self._id == None: # create new record
            query = "INSERT INTO cars (make, model, year, color, image_url, details) VALUES (%s, %s, %s, %s, %s, %s);"
            params = (self._make, self._model, self._year, self._color, self._image_url, self._details)
            self._id = execute_query(query, params)
        else: # update existing record
            query = "UPDATE cars SET make = %s, model = %s, year = %s, color = %s, image_url = %s, details = %s, available = %s WHERE id = %s;"
            params = (self._make, self._model, self._year, self._color, self._image_url, self._details, self._available, self._id)
            execute_query(query, params)
    
    @classmethod
    def find(cls, id):
        records = execute_query('SELECT * FROM cars WHERE id=%s', (id,))
        car = Car(*records[0])
        return car
    
    @classmethod
    def all(cls):
        records = execute_query('SELECT * FROM cars;')
        cars = []
        for record in records:
            car = Car(*record)
            cars.append(car)
        return cars
    
    @classmethod
    def allAvailable(cls):
        records = execute_query('SELECT * FROM cars WHERE available = 1')
        cars = []
        for record in records:
            # print(record)
            car = Car(*record)
            # print(car.__dict__)
            cars.append(car)
        return cars