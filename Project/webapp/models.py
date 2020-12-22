from webapp import db
from sqlalchemy import Column, Integer, String, DATETIME, Float, ForeignKey, BigInteger, Boolean, Unicode, UnicodeText, \
    Enum as EnumSQL, ForeignKeyConstraint
import uuid
from sqlalchemy_utils import UUIDType, ChoiceType, IPAddressType, PasswordType, Password
from datetime import datetime, time
from flask_login import UserMixin
from enum import Enum
from sqlalchemy.orm import relationship, backref


class BaseEnum(Enum):
    print()

class Role(Enum):
    admin = 2
    manager = 1


class ETypeResult(Enum):
    Win = 1
    Lose = 2
    Tie = 3


# Danh sach loai cau thu
class ETyEpePlayer(Enum):
    localplayer = "Trong Nước"
    foreignplayer = "Nước Ngoài"


class EGender(Enum):
    Female = 'Nữ'
    Male = 'Nam'
    Orther = "Khác"


class ETypeGoal(Enum):
    A = 1
    B = 2
    C = 3


class EActive(Enum):
    Active = True
    InActive = False


class EStatusValidation(Enum):
    InValid = False
    Validity = True


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
    stadium = Column(String(200))
    active = Column(Boolean, nullable=False, default=True)
    logo = Column(String(200))
    description = Column(String(600))
    # Được duyệt hay chưa
    invalid = Column(Boolean, default=False)
    # relationship
    players = relationship("Player", backref="team", lazy=True)
    team_group = relationship('TeamsInGroup', backref=backref('team', lazy=True))
    results = relationship('Result', backref=backref('team', lazy=True))

class Position(BaseModel):
    __tablename = "Position"
    symbol = Column(String(10))
    detail = Column(String(300))
    players = relationship('Player', backref=backref('position'), lazy=True)


# Danh sach cau thu
class Player(BaseModel):
    __tablename__ = "Player"
    birthdate = Column(DATETIME, nullable=False)
    nationality = Column(String(100), default="")
    lastname = Column(String(100))
    firstname = Column(String(100))
    number = Column(String(100))
    # loai cầu thủ
    typeplayer = Column(EnumSQL(ETyEpePlayer), nullable=False, default=ETyEpePlayer.localplayer)
    #  Tổng số bàn thắng
    scorecount = Column(Integer, default=0)
    note = Column(String(100))

    gender = Column(EnumSQL(EGender), default=EGender.Orther)
    # anh cau thu
    avatar = Column(String(200))

    # relationship

    goals = relationship("Goal", backref="player", lazy=True)

    # ForeignKey
    # Vị trí thi đấu(Tiền vệ trái, hậu vệ phải...) Có thể để dạng Enum
    position_id = Column(UUIDType(binary=True), ForeignKey(Position.id), nullable=False)
    team_id = Column(UUIDType(binary=True), ForeignKey(Team.id), nullable=False)


class TypeGoals(BaseModel):
    __tablename__ = "TypeGoals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    value = Column(String(500), nullable=False)

    goals = relationship('Goal', backref='typeGoal', lazy=True)

# Bảng đấu
class Round(BaseModel):
    __tablename__ = "Round"
    name = None
    roundname = Column(String(10))
    # Số lượng các đội trong vòng
    numberteamin = Column(Integer, nullable=False)
    # Số lượng các đội trong vòng
    numberteamout = Column(Integer, nullable=False)
    # Thể thức
    format = Column(String(100))
    # relationship
    groups = relationship("Groups", backref="round", lazy=True)


    def __str__(self):
        return self.roundname

#Bảng đấu trong vòng bảng
class Groups(BaseModel):
    __tablename__ = "Groups"
    # Số lượng các đội trong bảng
    numberteamin = Column(Integer, nullable=False)
    # Số lượng các đội trong bảng thắng
    numberteamout = Column(Integer, nullable=False)
    round_id = Column(UUIDType(binary=True), ForeignKey(Round.id),nullable=False)
    matchs = relationship('Match', backref=backref('groups'), lazy=True)
    teams = relationship('TeamsInGroup', backref=backref('groups', lazy=True))

class TeamsInGroup(db.Model):
    __tablename__ = "TeamsInGroup"
    group_id = Column(UUIDType(binary=True), ForeignKey('Groups.id'), primary_key=True)
    team_id = Column(UUIDType(binary=True), ForeignKey('Team.id'), primary_key=True)
    timeJoinRound = Column(DATETIME, default=datetime.now())

# Trận đấu
class Match(BaseModel):
    __tablename__ = "Match"

    name = None
    datetime = Column(DATETIME, nullable=False)
    # relationship
    results = relationship("Result", backref=backref("match", uselist=False), lazy=True)
    # ForeignKey
    group_id = Column(UUIDType(binary=True), ForeignKey(Groups.id), nullable=False)
    # đội nhà
    hometeam_id = Column(UUIDType(binary=True), ForeignKey(Team.id), nullable=False)
    # Đội khách
    awayteam_id = Column(UUIDType(binary=True), ForeignKey(Team.id), nullable=False)
    #Sân
    stadium_id = Column(UUIDType(binary=True),ForeignKey(Team.id),nullable=False)

    hometeams = relationship('Team', foreign_keys=[hometeam_id], backref=backref('homematch'))
    awayteams = relationship('Team', foreign_keys=[awayteam_id], backref=backref('awaymatch'))
    stadiumofteam = relationship('Team',foreign_keys=[stadium_id],backref=backref('stadiummatch'))

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
    diem = Column(Integer, nullable=False)
    hieuSo = Column(Integer, nullable=False)
    tongBanThang = Column(Integer, nullable=False)
    doiKhang = Column(Integer, nullable=False)

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
    goals = relationship('Goal', backref='result', lazy=True)

    # ForeignKey
    # kết quả của trận đấu nào
    match_id = Column(UUIDType(binary=True), ForeignKey(Match.id), nullable=False, primary_key=True)
    # đội thắng
    winteam = Column(UUIDType(binary=True), ForeignKey(Team.id))
    # team_id = Column(UUIDType(binary=True), ForeignKey(Team.id), nullable=False)
    # số bàn thắng của đội thắng
    winnergoals = Column(Integer, nullable=False)
    # Số bàn thắng đội thua
    losergoals = Column(Integer, nullable=False)

    def __str__(self):
        return "Results " + str(Match.query.get(self.match_id))


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

    config = Config(amountForeignPlayer=3, minAgePlayer=18, maxAgePlayer=20, diem=1,tongBanThang=2,hieuSo=3,doiKhang=4, loseScore=1,
                    winScore=3,
                    tieScore=2, thoiDiemGhiBanToiDa=96, maxPlayer=18, minPlayer=12)
    admin = Team(id=uuid.uuid4(), name="Admin",
                 email='vutandat29092000@gmail.com',
                 role=Role.admin,
                 username='admin',
                 invalid=True,
                 password='d047de6de9348ed903f6ac3631731f26dc3795e09b07f6d3ac993d5f48045558')
    team1 = Team(id=uuid.uuid4(),
                 name='TPHCM',
                 username='team1',
                 password='d047de6de9348ed903f6ac3631731f26dc3795e09b07f6d3ac993d5f48045558',
                 email="vutandat29092000@gmail.com",
                 phonenumber='098765433456',
                 invalid=True,
                 stadium="Phường 3,Phú Nhuận,TPHCM",

                 )
    team2 = Team(id=uuid.uuid4(),
                 name='HN',
                 username='team2',
                 password='d047de6de9348ed903f6ac3631731f26dc3795e09b07f6d3ac993d5f48045558',
                 email="vutandat29092000@gmail.com",
                 phonenumber='098765433456',
                 invalid=True,
                 stadium="Phường 3,Phú Nhuận,HN",
                 )
    team3 = Team(id=uuid.uuid4(),
                 name='GJ',
                 username='team3',
                 password='d047de6de9348ed903f6ac3631731f26dc3795e09b07f6d3ac993d5f48045558',
                 email="vutandat29092000@gmail.com",
                 phonenumber='098765433456',
                 invalid=True,
                 stadium="Phường 3,Phú Nhuậđn,HN",
                 )
    player1 = Player(id=uuid.uuid4(),
                     name="Công Phượng",
                     team_id=team1.id,
                     typeplayer=ETyEpePlayer.localplayer,
                     birthdate=datetime.now(),
                     gender=EGender.Male,
                     position_id=Position.query.filter(Position.symbol == EPosition.RS._name_).first().id
                     )
    player2 = Player(id=uuid.uuid4(),
                     name="Rô béo",
                     team_id=team2.id,
                     typeplayer=ETyEpePlayer.foreignplayer,
                     birthdate=datetime.now(),
                     gender=EGender.Female,
                     position_id=Position.query.filter(Position.symbol == EPosition.ST.name).first().id
                     )
    tuket = Round(id=uuid.uuid4(), roundname="Tứ kết", numberteamin=4, numberteamout = 2)
    chungket = Round(id=uuid.uuid4(), roundname="Chung kết", numberteamin=2, numberteamout = 1)
    tuketGroup = Groups(id=uuid.uuid4(), name = 'Tứ kết',round_id=tuket.id,numberteamin=tuket.numberteamin, numberteamout = tuket.numberteamout)
    teamintuke = TeamsInGroup(group_id=tuketGroup.id, team_id=team1.id)
    team1intuke = TeamsInGroup(group_id=tuketGroup.id, team_id=team2.id)
    match1 = Match(id=uuid.uuid4(), hometeam_id=team1.id, awayteam_id=team2.id, group_id=tuketGroup.id,
                   datetime=datetime.now(),stadium_id=team1.id)
    match2 = Match(id=uuid.uuid4(), hometeam_id=team2.id, awayteam_id=team1.id, group_id=tuketGroup.id,
                   datetime=datetime.now(),stadium_id=team2.id)
    match3 = Match(id=uuid.uuid4(), hometeam_id=team2.id, awayteam_id=team3.id, group_id=tuketGroup.id,
                   datetime=datetime.now(), stadium_id=team2.id)
    match4 = Match(id=uuid.uuid4(), hometeam_id=team3.id, awayteam_id=team2.id, group_id=tuketGroup.id,
                   datetime=datetime.now(), stadium_id=team3.id)
    resultmatch1 = Result(id=uuid.uuid4(), match_id=match1.id, winnergoals=3, losergoals=2, typeresult=ETypeResult.Win, winteam=team1.id)
    resultmatch2 = Result(id=uuid.uuid4(), match_id=match2.id, winnergoals=3, losergoals=3, typeresult=ETypeResult.Tie, )
    resultmatch3 = Result(id=uuid.uuid4(), match_id=match3.id, winnergoals=3, losergoals=2, typeresult=ETypeResult.Win, winteam=team2.id)
    resultmatch4 = Result(id=uuid.uuid4(), match_id=match4.id, winnergoals=3, losergoals=3, typeresult=ETypeResult.Tie, )

    goal1 = Goal(id=uuid.uuid4(), result_id=resultmatch1.id, player_id=player1.id, time=datetime.now(), type_id=1)
    goal2 = Goal(id=uuid.uuid4(), result_id=resultmatch1.id, player_id=player2.id, time=datetime.now(), type_id=2)
    goal3 = Goal(id=uuid.uuid4(), result_id=resultmatch1.id, player_id=player1.id, time=datetime.now(), type_id=3)

    listcommit = [
        config,
        admin,team1, team2,team3,
        player1, player2,
        tuket, chungket,
        tuketGroup,
        team1intuke, teamintuke,
        match1, match2,match3,match4,
        resultmatch1,resultmatch2,resultmatch3,resultmatch4,
        goal1, goal2, goal3

    ]
    db.session.add_all(listcommit)
    db.session.commit()
    print("Thành công")
