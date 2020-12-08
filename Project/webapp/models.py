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
    Male = 2
    Orther = 3


class ETypeGoal(Enum):
    A = 1
    B = 2
    C = 3


class EPosition(Enum):
    HLV = "Huấn luyện viên"
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


class Team(BaseModel, UserMixin):
    __tablename__ = "Team"

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
    players = relationship("Player", backref="team", lazy=True)
    teamselected = relationship('TeamsInRound', backref=backref('team', lazy=True))


class Position(BaseModel):
    __tablename = "Position"
    symbol = Column(String(10))
    detail = Column(String(300))
    players = relationship('Player', backref=backref('position'), lazy=True)


# Danh sach cau thu
class Player(BaseModel):
    __tablename__ = "Player"
    lastname = Column(String(100))
    firstname = Column(String(100))
    birthdate = Column(DATETIME, nullable=False)
    nationality = Column(String(100), default="")
    # loai cầu thủ
    typeplayer = Column(EnumSQL(ETyEpePlayer), nullable=False, default=ETyEpePlayer.localplayer)
    #  Tổng số bàn thắng
    scorecount = Column(Integer, default=0)
    note = Column(String(100))
    gender = Column(EnumSQL(EGender), default=EGender.Orther)
    # anh cau thu
    avatar = Column(String(200))
    # relationship
    player_goal = relationship("Goal", backref="player", lazy=True)
    # ForeignKey
    # Vị trí thi đấu(Tiền vệ trái, hậu vệ phải...) Có thể để dạng Enum
    position_id = Column(UUIDType(binary=True), ForeignKey(Position.id), nullable=False)
    team_id = Column(UUIDType(binary=True), ForeignKey(Team.id), nullable=False)


class TypeGoals(BaseModel):
    __tablename__ = "TypeGoals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    value = Column(String(500), nullable=False)

    goal_Type = relationship('Goal', backref=backref('typeGoal'), lazy=True)


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
    round_match = relationship("Match", backref="round", lazy=True)
    # team đc chọn
    teamselected = relationship('TeamsInRound', backref=backref('round', lazy=True))

    def __str__(self):
        return self.groupname


class TeamsInRound(db.Model):
    __tablename__ = "TeamsInRound"
    round_id = Column(UUIDType(binary=True), ForeignKey('Round.id'), primary_key=True)
    team_id = Column(UUIDType(binary=True), ForeignKey('Team.id'), primary_key=True)
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
    hometeam_id = Column(UUIDType(binary=True), ForeignKey(Team.id), nullable=False)
    # Đội khách
    awayteam_id = Column(UUIDType(binary=True), ForeignKey(Team.id), nullable=False)

    hometeams = relationship('Team', foreign_keys=[hometeam_id], backref=backref('hometeam'))
    awayteams = relationship('Team', foreign_keys=[awayteam_id], backref=backref('awayteam'))

    def __str__(self):
        return self.hometeams.name + " - " + self.awayteams.name


class Config(BaseModel):
    __tablename__ = "Config"
    name = None
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
    diem = Column(Integer, nullable=False, default=1)
    hieuSo = Column(Integer, nullable=False, default=2)
    tongBanThang = Column(Integer, nullable=False, default=3)
    doiKhang = Column(Integer, nullable=False, default=4)
    prioritySort_Config = relationship('Config', backref=backref('prioritySort'), lazy=True)


# Bán thắng
class Goal(BaseModel):
    # thời gian ghi bàn
    time = Column(DATETIME, nullable=False)  # Kết quả
    name = None
    # relationship
    # ForeignKey
    result_id = Column(UUIDType(binary=True), ForeignKey("Result.id"))
    player_id = Column(UUIDType(binary=True), ForeignKey(Player.id), nullable=False)
    type_id = Column(Integer, ForeignKey(TypeGoals.id), nullable=False)
    def __str__(self):
        return "goal " + str(time)

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
    # team_id = Column(UUIDType(binary=True), ForeignKey(Team.id), nullable=False)
    # số bàn thắng của đội thắng
    winnergoals = Column(Integer, nullable=False)
    # Số bàn thắng đội thua
    losergoals = Column(Integer, nullable=False)

    def __str__(self):
        return "Result " + str(Match.query.get(self.match_id))


def inserPosition():
    for k in EPosition._member_names_:
        p1 = Position(symbol=k, name=EPosition.__getitem__(k).value)
        db.session.add(p1)


def insertypegoals():
    for k in ETypeGoal._member_names_:
        p1 = TypeGoals(name=k, value=ETypeGoal.__getitem__(k).value)
        db.session.add(p1)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    # ==========insert data============#
    inserPosition()
    insertypegoals()
    prisort = PrioritySort(id =1,name='DHTD', diem=1, hieuSo=2, tongBanThang=3, doiKhang=4)
    prisort1 = PrioritySort(id = 2,name='DTHD', diem=1, hieuSo=3, tongBanThang=2, doiKhang=4)
    config = Config(amountForeignPlayer=3, minAgePlayer=18, maxAgePlayer=20, prioritySort_id=prisort.id, loseScore=1,
                    winScore=3,
                    tieScore=2, thoiDiemGhiBanToiDa=96, maxPlayer=18, minPlayer=12)
    team1 = Team(id= uuid.uuid4(),
                 name='TPHCM',
                 username='team1',
                 password='team1',
                 email="vutandat29092000@gmail.com",
                 phonenumber='098765433456',
                 invalid=True,
                 stadium="Phường 3,Phú Nhuận,TPHCM",

                 )
    team2 = Team(id= uuid.uuid4(),
                 name='HN',
                 username='team2',
                 password='team2',
                 email="vutandat29092000@gmail.com",
                 phonenumber='098765433456',
                 invalid=True,
                 stadium="Phường 3,Phú Nhuận,HN",
                 )
    player1 = Player(id = uuid.uuid4(),
                     name="Công Phượng",
                     team_id=team1.id,
                     typeplayer=ETyEpePlayer.localplayer,
                     birthdate=datetime.now(),
                     gender=EGender.Male,
                     position_id=Position.query.filter(Position.symbol == EPosition.RS._name_).first().id
                     )
    player2 = Player(id = uuid.uuid4(),
                     name="Rô béo",
                     team_id=team2.id,
                     typeplayer=ETyEpePlayer.foreignplayer,
                     birthdate=datetime.now(),
                     gender=EGender.Female,
                     position_id=Position.query.filter(Position.symbol == EPosition.ST.name).first().id
                     )
    tuket = Round(id = uuid.uuid4(),groupname="Tứ kết", numberofteam=4)
    chungket = Round(id = uuid.uuid4(),groupname="Chung kết", numberofteam=2)
    teamintuke = TeamsInRound(round_id=tuket.id, team_id=team1.id)
    team1intuke = TeamsInRound(round_id=tuket.id, team_id=team2.id)
    team2intuke = TeamsInRound(round_id=chungket.id, team_id=team1.id)
    team3intuke = TeamsInRound(round_id=chungket.id, team_id=team2.id)
    match1 = Match(id = uuid.uuid4(),hometeam_id=team1.id, awayteam_id=team2.id, round_id=chungket.id, datetime=datetime.now())
    match2 = Match(id = uuid.uuid4(),hometeam_id=team2.id, awayteam_id=team1.id, round_id=chungket.id, datetime=datetime.now())
    resultmatch1 = Result(id = uuid.uuid4(),match_id=match1.id, winnergoals=3, losergoals=2, typeresult=ETypeResult.Win)
    goal1 = Goal(id = uuid.uuid4(),result_id=resultmatch1.id, player_id=player1.id, time=datetime.now(), type_id=1)
    goal2 = Goal(id = uuid.uuid4(),result_id=resultmatch1.id, player_id=player2.id, time=datetime.now(), type_id=2)
    goal3 = Goal(id = uuid.uuid4(),result_id=resultmatch1.id, player_id=player1.id, time=datetime.now(), type_id=3)

    listcommit = [
        prisort,prisort1,
        config,
        team1,team2,
        player1,player2,
        tuket,chungket,
        team1intuke,teamintuke,team2intuke,team3intuke,
        match1,match2,
        resultmatch1,
        goal1,goal2,goal3

    ]
    db.session.add_all(listcommit)
    db.session.commit()
    print("Thành công")
