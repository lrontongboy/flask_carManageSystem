from .mysql_connector import execute_query
from password_encryptor import check_password_hash

class User:
    def __init__(self, id=None, username=None, password=None, real_name=None, date_of_birth=None, address=None, is_admin=False):
        self._id = id
        self._username = username
        self._password = password
        self._real_name = real_name
        self._date_of_birth = date_of_birth
        self._address = address
        self._is_admin = is_admin
        

    def getID(self):
        return self._id

    def getUsername(self):
        return self._username
    
    def getPassword(self):
        return self._password
    
    def getRealName(self):
        return self._real_name
    
    def getDateOfBirth(self):
        return self._date_of_birth
    
    def getAddress(self):
        return self._address
    
    def isAdmin(self):
        return self._is_admin
    
    def setPassword(self, password):
        self._password = password


    def authenticate(self, password):
        return check_password_hash(self._password, password)

    def save(self):
        
        if self._id is None:  # 新用户注册
            query = "INSERT INTO users (username, password) VALUES (%s, %s);"
            params = (self._username, self._password)
            self._id = execute_query(query, params)
        else:  # 更新用户信息
            query = "UPDATE users SET username = %s, password = %s, real_name = %s, date_of_birth = %s, address = %s, is_admin = %s WHERE id = %s;"
            params = (self._username, self._password, self._real_name, self._date_of_birth, self._address, self._is_admin, self._id)
            execute_query(query, params)

    def update_profile(self, real_name, date_of_birth, address):
        self._real_name = real_name
        self._date_of_birth = date_of_birth
        self._address = address
        self.save()  # 保存更新后的信息
    
    @classmethod
    def find(cls, id):
        records = execute_query('SELECT * FROM users WHERE id=%s', (id,))
        user = User(*records[0])
        return user
    
    @classmethod
    def findByUsername(cls, username):
        records = execute_query('SELECT * FROM users WHERE username=%s', (username,))
        if records:
            user = User(*records[0])
            return user
        else:
            return None
    
    @classmethod
    def all(cls):
        records = execute_query('SELECT * FROM users;')
        users = []
        for record in records:
            user = User(*record)
            users.append(user)
        return users
    

    def to_dict(self):
        return {
            'id': self._id,
            'username': self._username,
            'real_name': self._real_name,
            'date_of_birth': self._date_of_birth.isoformat() if self._date_of_birth else None,  # 将日期转换为字符串
            'address': self._address,
            'is_admin': self._is_admin
        }

    def delete(self):
        if self._id:
            query = "DELETE FROM users WHERE id = %s"
            params = (self._id,)
            execute_query(query, params)
            self._id = None  # After deletion, set the ID to None, indicating that the user object is no longer associated with the database record.
        else:
            raise ValueError("Unable to delete user without ID.")