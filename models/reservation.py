from .mysql_connector import execute_query
from datetime import datetime
from .car import Car

class Reservation:
    def __init__(self, id, user_id, car_id, start_time, end_time, status='pending', car=None) -> None:
        self._id = id
        self._user_id = user_id
        self._car_id = car_id
        self._start_time = start_time
        self._end_time = end_time
        self._status = status
        self._car = car 

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
    
    def getCar(self):
        
        if self._car is None:
            
            self._car = Car.find(self._car_id)  
        return self._car
    
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
    
    @staticmethod
    def check_conflict(car_id, start_time, end_time):
        """
        检查预订时间冲突，如果存在冲突，返回冲突信息；否则返回 False。

        Args:
            car_id: 车辆 ID。
            start_time: 预订开始时间。
            end_time: 预订结束时间。

        Returns:
            冲突信息字符串，例如 "2024-12-24 10:00 - 12:00"，或者如果没有冲突，则返回 False。
        """
        query = """
            SELECT *
            FROM reservations
            WHERE car_id = %s
              AND (
                (start_time <= %s AND end_time >= %s) OR
                (start_time < %s AND end_time > %s) OR
                (start_time < %s AND end_time > %s) OR
                (start_time > %s AND end_time < %s)
              )
        """
        params = (car_id, start_time, end_time, start_time, end_time, end_time, start_time, start_time, end_time)
        result = execute_query(query, params)

        if result:
            conflict_reservation = result[0]
            start_time_str = conflict_reservation[3].strftime('%Y-%m-%d %H:%M')
            end_time_str = conflict_reservation[4].strftime('%Y-%m-%d %H:%M')
            return f"{start_time_str} - {end_time_str}"
        else:
            return False