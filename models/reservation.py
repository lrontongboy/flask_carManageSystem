from .mysql_connector import execute_query
from datetime import datetime

class Reservation:
    def __init__(self, id, user_id, car_id, start_time, end_time, status='pending') -> None:
        self._id = id
        self._user_id = user_id
        self._car_id = car_id
        self._start_time = start_time
        self._end_time = end_time
        self._status = status

    def getID(self):
        return self._id

    def getUserID(self):
        return self._user_id
    
    def getCarID(self):
        return self._car_id
    
    def getStartTime(self):
        return self._start_time
    
    def getEndTime(self):
        return self._end_time
    
    def getStatus(self):
        return self._status
    
    def setStatus(self, status):
        self._status = status

    def save(self):
        if self._id == None: # create new record
            query = "INSERT INTO reservations (user_id, car_id, start_time, end_time, status) VALUES (%s, %s, %s, %s, %s);"
            params = (self._user_id, self._car_id, self._start_time, self._end_time, self._status)
            self._id = execute_query(query, params)
        else: # update existing record
            query = "UPDATE reservations SET user_id = %s, car_id = %s, start_time = %s, end_time = %s, status = %s WHERE id = %s;"
            params = (self._user_id, self._car_id, self._start_time, self._end_time, self._status, self._id)
            execute_query(query, params)
    
    @classmethod
    def find(cls, id):
        records = execute_query('SELECT * FROM reservations WHERE id=%s', (id,))
        reservation = Reservation(*records[0])
        return reservation
    
    @classmethod
    def all(cls):
        records = execute_query('SELECT * FROM reservations;')
        reservations = []
        for record in records:
            reservation = Reservation(*record)
            reservations.append(reservation)
        return reservations

    @classmethod
    def findByUserID(cls, user_id):
        records = execute_query('SELECT * FROM reservations WHERE user_id=%s', (user_id,))
        reservations = []
        for record in records:
            reservation = Reservation(*record)
            reservations.append(reservation)
        return reservations