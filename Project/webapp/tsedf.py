from webapp import db
from sqlalchemy import Column, Integer, String, DATETIME, Float, ForeignKey, BigInteger, Boolean, Unicode, UnicodeText, \
    Enum as EnumSQL, ForeignKeyConstraint
import uuid
from sqlalchemy_utils import UUIDType, ChoiceType, IPAddressType, PasswordType, Password
from datetime import datetime, time
from flask_login import UserMixin
from enum import Enum
from sqlalchemy.orm import relationship, backref


class A(db.Model):
    id = Column(UUIDType(binary=True), primary_key=True,default=uuid.uuid4)
    da = Column(String(233))
    #acs = relationship('C', backref=backref('a',lazy =True))


class B(db.Model):
    id = Column(UUIDType(binary=True), primary_key=True,default=uuid.uuid4)
    da = Column(String(233))
    acs = relationship('A',secondary='C', backref=backref('b',lazy =True))

class C(db.Model):
    a_id = Column(UUIDType(binary=True), ForeignKey(A.id), primary_key=True)
    b_id = Column(UUIDType(binary=True), ForeignKey(B.id), primary_key=True)
    ass = Column(DATETIME, default=datetime.now())
if __name__ == '__main__':
    db.drop_all()
    db.create_all()