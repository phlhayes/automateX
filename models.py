from sqlalchemy import Column, Integer, String
from database import Base

# Set your classes here.
class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(30))

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)                        


class Job(Base):
    __tablename__ = 'Jobs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    title = Column(String(120))
    database = Column(String(120))
    host = Column(String(120))
    db_user = Column(String(120))
    db_pass = Column(String(120))
    spreadsheet = Column(String(120))
    sheet = Column(String(120))
    query = Column(String(10000))   
    schedule = Column(String(120))

    def __init__(self, title=None, database=None, host=None, db_user=None, db_pass=None,
        spreadsheet=None, sheet=None, query=None, schedule=None, user_id = None):
        self.title = title
        self.database = database
        self.host = host
        self.db_user = db_user
        self.db_pass = db_pass
        self.spreadsheet = spreadsheet
        self.sheet = sheet
        self.query = query
        self.schedule = schedule
        self.user_id = 0

    def __repr__(self):
        return [self.title, self.database, self.host, self.db_user, self.db_pass, self.spreadsheet, self.sheet, self.query, self.schedule, self.user_id, self.id]

