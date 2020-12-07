from webapp import db
from sqlalchemy import Column, Integer, String, DATETIME, Float, ForeignKey, BigInteger, Boolean, Unicode, UnicodeText, \
    Enum as EnumSQL, ForeignKeyConstraint
import uuid
from sqlalchemy_utils import UUIDType, ChoiceType, IPAddressType, PasswordType, Password
from datetime import datetime, time
from flask_login import UserMixin
from enum import Enum
from sqlalchemy.orm import relationship, backref



class Role(Enum):
    admin = 2
    manager = 1


class ETypeResult(Enum):
    Win = 1
    Lose = 2
    Tie = 3


# Danh sach loai cau thu
class ETyEpePlayer(Enum):
    localplayer = 1
    foreignplayer = 2


class EGender(Enum):
    Female = 1
    Mate = 2
    Orther = 3


class ETypeGoal(Enum):
    A = 1
    B = 2
    C = 3


class EPosition(Enum):
    GK = "Thủ môn"
    LF = "Tiền đạo cánh trái"
    RF = "Tiền đạo cánh phải"
    CF = "Tiền đạo trung tâm"
    SW = "Trung vệ thòng"
    ST = "Tiền đạo cắm / Trung Phong"
    CB = "Trung vệ"
    LB = "Hậu vệ trái"
    RB = "Hậu vệ phải"
    RS = "Hậu vệ phải"
    LS = "Hậu vệ trái"
    LM = "Tiền vệ trái"
    RM = "Tièn vệ phải"


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(UUIDType(binary=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    __tablename__ = "User"

    username = Column(String(50), nullable=False)
    password = Column(String(600), nullable=False)
    joindate = Column(DATETIME, nullable=False, default=datetime.now())
    role = Column(EnumSQL(Role), nullable=False, default=Role.manager)
    email = Column(String(100), nullable=False)
    phonenumber = Column(String(20), nullable=True)
    active = Column(Boolean, nullable=False, default=True)
    # relationship
    team_user = relationship("Team", backref=backref('users'), lazy=True)


# Danh sach doi bong
class Team(BaseModel):
    __tablename__ = "ListTeam"
    stadium = Column(String(50), nullable=False)
    # Được duyệt hay chưa
    invalid = Column(Boolean, default=False)
    # relationship
    player_team = relationship("Player", backref="teams", lazy=True)
    match_team = relationship('Match', backref=backref('teams'), lazy=True)
    # ForeignKey
    user_id = Column(UUIDType(binary=True), ForeignKey(User.id), nullable=False)


# Danh sach cau thu
class Player(BaseModel):
    __tablename__ = "Player"
    birthdate = Column(DATETIME, nullable=False)
    nationality = Column(String(100), default="")
    # Vị trí thi đấu(Tiền vệ trái, hậu vệ phải...) Có thể để dạng Enum
    position = Column(EnumSQL(EPosition), nullable=False, default="")
    # loai cau
    typeplayer = Column(EnumSQL(ETyEpePlayer), nullable=False, default=ETyEpePlayer.localplayer)
    #  Tổng số bàn thắng
    scorecount = Column(Integer)
    note = Column(String(100))
    # Được duyệt hay chưa
    invalid = Column(Boolean, default=False)
    gender = Column(EnumSQL(EGender), default=EGender.Orther)
    # anh cau thu
    avatar = Column(String(200))

    # relationship

    player_result = relationship("Result", backref="players", lazy=True)

    # ForeignKey

    team_id = Column(UUIDType(binary=True), ForeignKey(Team.id), nullable=False)


# Bảng đấu
class Round(BaseModel):
    __tablename__ = "Round"
    name = None
    groupname = Column(String(10))
    # Số lượng các dội
    numberofteam = Column(Integer, nullable=False)
    # Số lượn team được chọn
    teamselected = Column(Integer, nullable=False)
    # Thể thức
    format = Column(String(100))
    # relationship
    round_match = relationship("Match", backref="rounds", lazy=True)


# Trận đấu
class Match(BaseModel):
    __tablename__ = "Match"

    name = None
    datetime = Column(DATETIME, nullable=False)
    # relationship
    match_result = relationship("Result", backref=backref("matchs", uselist=False), lazy=True)
    # ForeignKey
    stadium_id = Column(UUIDType(binary=True), ForeignKey(Team.id), nullable=False, )
    round_id = Column(UUIDType(binary=True), ForeignKey(Round.id), nullable=False)
    # đội nhà
    hometeam = Column(UUIDType(binary=True), ForeignKey(Team.id), nullable=False)
    # Đội khách
    awayteam = Column(UUIDType(binary=True), ForeignKey(Team.id), nullable=False)


# Bán thắng
class Goal(BaseModel):
    # cầu thủ ghi bàn

    type = Column(EnumSQL(ETypeGoal), nullable=False)
    # thời gian ghi bàn
    time = Column(DATETIME, nullable=False)  # Kết quả

    # relationship
    result_goal = relationship('Result', backref=backref('goals'), lazy=True)
    #ForeignKey
    player = Column(UUIDType(binary=True), ForeignKey(Player.id), nullable=False)

class Result(BaseModel):
    __tablename__ = "Result"
    name = None
    # loại kết quả thắng thua hoa
    typeresult = Column(EnumSQL(ETypeResult), nullable=False)

    # ForeignKey
    # kết quả của trận đấu nào
    match_id = Column(UUIDType(binary=True), ForeignKey(Match.id), nullable=False, )
    # đội thắng
    team_id = Column(UUIDType(binary=True), ForeignKey(Team.id), nullable=False)
    # số bàn thắng của đội thắng
    winnergoals_id = Column(UUIDType(binary=True), ForeignKey(Goal.id), nullable=False)
    # Số bàn thắng đội thua (???)
    losergoals_id = Column(UUIDType(binary=True), ForeignKey(Goal.id), nullable=False)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
