from webapp import db
from sqlalchemy import Column, Integer, String,DATETIME, Float, ForeignKey,BigInteger,Boolean,Unicode,UnicodeText,Enum as EnumSQL
import uuid
from sqlalchemy_utils import UUIDType, ChoiceType, IPAddressType,PasswordType,Password
from datetime import datetime
from flask_login import UserMixin
from enum import Enum
class BaseModel(db.Model):
    __abstract__ = True
    id = Column(UUIDType(binary=False),primary_key=True,default=uuid.uuid4())
    name = Column(String,nullable=False)

    def __str__(self):
        return self.name

class Role(Enum):
    admin = 2
    manager = 1


class User(BaseModel,UserMixin):
    __tablename__ = "User"

    username = Column(String(50), nullable=False)
    password = Column(String, nullable=False)
    joindate = Column(DATETIME,nullable=False,default=datetime.now())
    role = Column(EnumSQL(Role),nullable=False,default=Role.manager)
    email = Column(String, nullable=False)
    phonenumber = Column(String(20), nullable=True)
    active = Column(Boolean,nullable=False,default=True)

if __name__=='__main__':
    db.drop_all()
    db.create_all()





