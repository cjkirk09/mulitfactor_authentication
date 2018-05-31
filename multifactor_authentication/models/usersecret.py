from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base


class UserSecret(Base):
    __tablename__ = 'usersecret'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Text)


Index('my_index', UserSecret.name, unique=True, mysql_length=255)
