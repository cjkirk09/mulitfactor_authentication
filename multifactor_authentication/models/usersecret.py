from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base


class UserSecret(Base):
    __tablename__ = 'user_secrets'
    id = Column(Integer, primary_key=True)
    username = Column(Text)
    secret = Column(Text)


Index('my_index', UserSecret.username, unique=True, mysql_length=255)
