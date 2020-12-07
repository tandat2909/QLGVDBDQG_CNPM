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


class UuTienSapXep(Enum):
    Diem = 1
    HieuSo = 2
    TongBanThang = 3
    DoiKhang = 4


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(UUIDType(binary=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class Team(BaseModel, UserMixin):
    __tablename__ = "team"

    username = Column(String(50), nullable=False)
    password = Column(String(600), nullable=False)
    joindate = Column(DATETIME, nullable=False, default=datetime.now())
    role = Column(EnumSQL(Role), nullable=False, default=Role.manager)
    email = Column(String(100), nullable=False)
    phonenumber = Column(String(20), nullable=True)
    stadium = Column(String(200), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    # Được duyệt hay chưa
    invalid = Column(Boolean, default=False)
    # relationship
    player_team = relationship("Player", backref="team", lazy=True)
    match_team = relationship('Match', backref=backref('team'), lazy=True)


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

    gender = Column(EnumSQL(EGender), default=EGender.Orther)
    # anh cau thu
    avatar = Column(String(200))

    # relationship

    player_result = relationship("Result", backref="player", lazy=True)

    # ForeignKey

    team_id = Column(UUIDType(binary=True), ForeignKey(Team.id), nullable=False)


class TypeGoals(db.Model):
    __tablename__ = "TypeGoals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    value = Column(String(500), nullable=False)

    goal_Type = relationship('Goal', backref=backref('TypeGoals'), lazy=True)


# Bảng đấu
class Round(BaseModel):
    __tablename__ = "Round"
    name = None
    groupname = Column(String(10))
    # Số lượng các dội
    numberofteam = Column(Integer, nullable=False)
    # Thể thức
    format = Column(String(100))
    # relationship
    round_match = relationship("Match", backref="rounds", lazy=True)
    # team đc chọn
    teamselected = relationship('team', secondary="TeamsInRound", lazy='subquery', backref=backref('round', lazy=True))


class TeamsInRound(BaseModel):
    __tablename__ = "TeamsInRound"
    id = None
    name = None
    round_id = Column(UUIDType(binary=True), ForeignKey(Round.id), primary_key=True)
    team_id = Column(UUIDType(binary=True), ForeignKey(Team.id), primary_key=True)
    timeJoinRound = Column(DATETIME, default=datetime.now())


# Trận đấu
class Match(BaseModel):
    __tablename__ = "Match"

    name = None
    datetime = Column(DATETIME, nullable=False)
    # relationship
    match_result = relationship("Result", backref=backref("match", uselist=False), lazy=True)
    # ForeignKey

    round_id = Column(UUIDType(binary=True), ForeignKey(Round.id), nullable=False)
    # đội nhà
    hometeam = Column(UUIDType(binary=True), ForeignKey(Team.id), nullable=False)
    # Đội khách
    awayteam = Column(UUIDType(binary=True), ForeignKey(Team.id), nullable=False)


class Config(BaseModel):
    __tablename__ = "Config"
    winScore = Column(Integer, nullable=False)
    tieScore = Column(Integer, nullable=False)
    loseScore = Column(Integer, nullable=False)
    maxPlayer = Column(Integer, nullable=False)
    minPlayer = Column(Integer, nullable=False)
    amountForeignPlayer = Column(Integer, nullable=False)
    maxAgePlayer = Column(Integer, nullable=False)
    minAgePlayer = Column(Integer, nullable=False)
    thoiDiemGhiBanToiDa = Column(Integer, nullable=False)
    prioritySort_id = Column(Integer, ForeignKey('PrioritySort.id'))


class PrioritySort(BaseModel):
    __tablename__ = "PrioritySort"
    """
        thứ tự ưu tiên sắp xếp
    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = None
    Diem = Column(Integer, nullable=False, default=1)
    HieuSo = Column(Integer, nullable=False, default=2)
    TongBanThang = Column(Integer, nullable=False, default=3)
    DoiKhang = Column(Integer, nullable=False, default=4)
    PrioritySort_Config = relationship('Config', backref=backref('prioritySort'), lazy=True)


# Bán thắng
class Goal(BaseModel):
    # thời gian ghi bàn
    time = Column(DATETIME, nullable=False)  # Kết quả
    # relationship
    # ForeignKey
    result_id = Column(UUIDType(binary=True), ForeignKey("Result.id"))
    player = Column(UUIDType(binary=True), ForeignKey(Player.id), nullable=False)
    type_id = Column(Integer, ForeignKey(TypeGoals.id), nullable=False)


class Result(BaseModel):
    __tablename__ = "Result"
    name = None
    # loại kết quả thắng thua hoa
    typeresult = Column(EnumSQL(ETypeResult), nullable=False)

    # relationship
    result_goal = relationship('Goal', backref=backref('result'), lazy=True)

    # ForeignKey
    # kết quả của trận đấu nào
    match_id = Column(UUIDType(binary=True), ForeignKey(Match.id), nullable=False, primary_key=True)
    # đội thắng
    team_id = Column(UUIDType(binary=True), ForeignKey(Team.id), nullable=False)
    # số bàn thắng của đội thắng
    winnergoals = Column(Integer, nullable=False)
    # Số bàn thắng đội thua
    losergoals = Column(Integer, nullable=False)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
