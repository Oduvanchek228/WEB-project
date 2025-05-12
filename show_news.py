from data import db_session
from data.news import News
from data.users import User

db_session.global_init(f'db/blogs.db')
# db_session.global_init(f'db/users.db')
session = db_session.create_session()
for article in session.query(News).all():
    print(article)