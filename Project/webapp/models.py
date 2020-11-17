from webapp import db
from sqlalchemy import Column, Integer, String,DATETIME, Float, ForeignKey,BigInteger,Boolean,Unicode,UnicodeText,Enum as EnumSQL, ForeignKeyConstraint
import uuid
from sqlalchemy_utils import UUIDType, ChoiceType, IPAddressType,PasswordType,Password
from datetime import datetime, time
from flask_login import UserMixin
from enum import Enum
from sqlalchemy.orm import relationship, backref


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(UUIDType(binary=False),primary_key=True,default=uuid.uuid4)
    name = Column(String,nullable=False)

    def __str__(self):
        return self.name

class Role(Enum):
    admin = 2
    manager = 1


class User(BaseModel,UserMixin):
    __tablename__ = "User"

    username = Column(String(50), nullable=False)
    password = Column(String,nullable=False)
    joindate = Column(DATETIME,nullable=False,default=datetime.now())
    role = Column(EnumSQL(Role),nullable=False,default=Role.manager)
    email = Column(String, nullable=False)
    phonenumber = Column(String(20), nullable=True)
    active = Column(Boolean,nullable=False,default=True)
    team_user = relationship("Team",backref= backref('users'),lazy = True)

#Danh sach doi bong
class Team(BaseModel):
    __tablename__ = "ListTeam"

    stadium = Column(String(50), nullable= False)
    #Được duyệt hay chưa
    invalid = Column(Boolean, default=False)
    player_team = relationship("Player", backref= "teams", lazy= True)

    user_id = Column(UUIDType,ForeignKey(User.id),nullable=False)

#Danh sach loai cau thu
class TypePlayer(Enum):
    localplayer = 1
    foreignplayer = 2

#Danh sach cau thu
class Player(BaseModel):
    __tablename__ = "Player"
    birthdate = Column(DATETIME, nullable= False)
    typeplayer = Column(EnumSQL(TypePlayer), nullable= False, default= TypePlayer.localplayer)
    team_id = Column(UUIDType,ForeignKey(Team.id),nullable=False)
    #  Tổng số bàn thắng
    scorecount = Column(Integer)
    note = Column(String(100))
    # Được duyệt hay chưa
    invalid = Column(Boolean, default=False)

    player_result = relationship("Result", backref="players", lazy=True)

#Bảng đấu
class Round(BaseModel):
    __tablename__ = "Round"

    groupname = Column(String(10))
    # Số lượng các dội
    numberofteam = Column(Integer, nullable=False)
    # Số lượn team được chọn
    teamselected = Column(Integer, nullable=False)
    #Thể thức
    format = Column(String)
    round_match = relationship("Match", backref= "rounds", lazy= True)

#Trận đấu
class Match(BaseModel):
    __tablename__ = "Match"

    name = None
    teamA = Column(String, nullable= False)
    teamB = Column(String, nullable= False)
    datetime = Column(DATETIME, nullable=False)
    stadium = Column(UUIDType, ForeignKey(Team.id),nullable= False, )
    round = Column(UUIDType, ForeignKey(Round.id), nullable=False)

    match_result = relationship("Result", backref= backref("matchs",uselist = False), lazy= True )

#Danh sach loai ban thang
class TypeScores(Enum):
    A = 1
    B = 2
    C = 3
class TypeResult(Enum):
    Win = 1
    Lose = 2
    Tie = 3

#Kết quả
class Result(BaseModel):
    __tablename__ = "Result"
    name = None
    typeresult = Column(EnumSQL(TypeResult), nullable= False)
    match = Column(UUIDType,  ForeignKey(Match.id),nullable=False,)
    #cầu thủ ghi bàn
    player = Column(UUIDType,  ForeignKey(Player.id),nullable=False)
    #đội thắng
    team = Column(UUIDType, ForeignKey(Team.id),nullable=False)
    typescore = Column(EnumSQL(TypeScores), nullable=False)
    #Thoi diem ghi ban
    time = Column(String, nullable=False)



if __name__=='__main__':
    db.drop_all()
    db.create_all()





