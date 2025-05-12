from data import db_session
from data.users import User

db_session.global_init(f'db/users.db')
session = db_session.create_session()
for user in session.query(User).all():
    print(user)
