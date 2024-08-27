import sys
import os
parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_folder)
from models.user import User

user1 = User.find(1)
print('user1:', user1.getID(), user1.getUsername(), user1.authenticate('abcdef'))
rose = User.findByUsername('link')
print('Rose:', rose.getID(), rose.getUsername(), rose.authenticate('123456'))


new_user = User(None, 'Amanda', '123456')
new_user.save()
print(new_user.getID(), new_user.getUsername())