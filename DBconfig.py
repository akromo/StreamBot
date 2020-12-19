from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import utils, config
from requests import post


engine = create_engine('sqlite:///Data.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_login = Column(String)
    date = Column(String)
    twitchApiToken = Column(String)
    #twitchApiRefreshToken = Column(String)

    def __init__(self, user_login, date, token):
        self.user_login = user_login
        self.date = date
        self.twitchApiToken = token
        #self.twitchApiRefreshToken = refreshToken
    def __repr__(self):
        return "<User('%s','%s','%s')>" % (self.id, self.user_login, self.date)

Base.metadata.create_all(engine)

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter(User.user_login.in_(["rocksun_wow"])).first()
    scopes = "channel_subscriptions+channel:read:redemptions+bits:read"
    postAcsess = "https://id.twitch.tv/oauth2/token?client_id=" + config.CLIENT_ID_TW \
                 + "&client_secret=" + config.SECRET_TW + "&grant_type=client_credentials&scope=" + scopes
    user.twitchApiToken = "none"
    session.commit()
    print(session.query(User).all())

    session.close()
