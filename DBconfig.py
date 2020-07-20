from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///Data.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_login = Column(String)
    date = Column(String)

    def __init__(self, user_login, date):
        self.user_login = user_login
        self.date = date
    def __repr__(self):
        return "<User('%s','%s','%s')>" % (self.id, self.user_login, self.date)

Base.metadata.create_all(engine)

if __name__ == '__main__' :
    Session = sessionmaker(bind=engine)
    session = Session()
    #session.add(User('mrprovokator', 'none'))
    #session.commit()
    #user = session.query(User).filter(User.id.in_([2]))
    #for i in session.query(User).all():
    #    session.delete(i)
    #    session.commit()
    print(session.query(User).all())
    session.close()
