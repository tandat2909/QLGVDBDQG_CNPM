import base64, hashlib, os, random, yagmail
import datetime

from sqlalchemy import or_, select, not_, and_
from sqlalchemy.sql.functions import count

from webapp import Config, db, models, config_main


def check_password(pw_hash='', pw_check=''):
    pw_check_hash = hashlib.sha256((pw_check + str(Config.KEYPASS)).encode("utf-8")).hexdigest()
    if pw_hash == pw_check_hash:
        return True
    return False


def check_password_first(pw='', pw_check=''):
    pw_check_base64 = base64.urlsafe_b64encode(pw_check.encode('utf-8')).decode('utf-8')
    return True if pw_check_base64 == pw else False


def generate_password(pw):
    pw_hash = hashlib.sha256((pw + str(Config.KEYPASS)).encode("utf-8")).hexdigest()
    return pw_hash


def encodeID(input="-"):
    """

    :param input:
    :return:
    :exception Exception
    """

    # print("input:",input)
    temp = str(input)
    output = ""
    try:
        # tạo chuỗi gây nhiễu
        rac = str(os.urandom(20).hex())
        # random vị trí cắt chuỗi gây nhiễu
        a = random.randint(4, len(rac) - 8)
        # cắt lấy 4-8 ký tự gây nhiễu
        rac = rac[a: a + random.randint(4, 8)]  # "xngfff"
        # cắt chuỗi theo lý tự '- "83319B1A-2EF83FB-4A753-75CECA824D17" [83319B1A,2EF83FB,4753,75CECA824D17]
        blocks = temp.split('-')
        # random vị trí thêm rac
        vt = random.randint(1, len(blocks) - 1)
        # thêm chuỗi gây nhiễu
        blocks.insert(vt, rac)  # [83319B1A,2EF83FB,"xngfff",4753,75CECA824D17]
        # nối lại chuỗi vừa cắt
        temp = "-".join(blocks)
        # thêm vị trí của chuỗi gây nhiễu vào chuỗi vừa nối
        temp = str(vt) + temp
        # đảo ngược chuỗi và in hoa các ký tự thường
        temp = temp[::-1].upper()  # 83319B1A-2EF83FB-"xngfff"-4753-75CECA824D17
        # mã hóa đoạn chuỗi trên bằng thuật toán base64
        output = base64.urlsafe_b64encode((temp).encode('utf-8')).decode("utf-8").replace('=', '')
        # đảo ngược chuỗi mã hóa
        output = output[::-1]
        # thêm 4 ký tự gây nhiễu vào cuối chuỗi mã hóa
        output += rac[:4].upper()

        return output

    except Exception as ex:
        print("Error EncodeID:", ex)
        raise ex


def decodeID(input):
    """

    :param input:
    :return:
    :exception Exception
    """
    temp = str(input)
    try:
        temp = temp[:-4]
        temp = temp[::-1]
        decode_temp = ''

        for i in range(3):
            try:
                decode_temp = base64.urlsafe_b64decode(temp).decode('utf-8').lower()
                break
            except:
                temp += '='
                continue

        decode_temp = decode_temp[::-1]
        vt_block = int(decode_temp[:1])
        decode_temp = decode_temp[1:]
        blocks = decode_temp.split('-')
        blocks.pop(vt_block)
        result = '-'.join(blocks)

        return result

    except Exception as ex:
        print('Error decodeID:', ex)
        raise ex


def change_password(user=None, pwold: str = None, pwnew: str = None, invalid=True):
    try:
        if user and pwnew and pwold:
            if check_password(user.password, pwold) or check_password_first(user.password, pwold):
                user.password = generate_password(pwnew)
                user.invalid = invalid
                # print("pw hashmới: " + user.password)
                db.session.add(user)
                db.session.commit()
                return True
        raise
    except:
        return False


def lock_account(current_user, user_id, lock: bool = None):
    try:
        if current_user.role == models.Role.admin and user_id and lock is not None:
            if current_user.id != decodeID(user_id):
                user = models.Team.query.get(decodeID(user_id))
                user.active = models.EActive.InActive.value if lock else models.EActive.Active.value
                db.session.add(user)
                db.session.commit()
                return True
        return False
    except:
        return False


def change_config(form):
    try:
        if form and config_main:
            config_main.winScore = form.get('winScore'),
            config_main.tieScore = form.get('tieScore'),
            config_main.loseScore = form.get('loseScore'),
            config_main.maxPlayer = form.get('maxPlayer'),
            config_main.minPlayer = form.get('minPlayer'),
            config_main.amountForeignPlayer = form.get('amountForeignPlayer'),
            config_main.maxAgePlayer = form.get('maxAgePlayer'),
            config_main.minAgePlayer = form.get('minAgePlayer'),
            config_main.thoiDiemGhiBanToiDa = form.get('thoiDiemGhiBanToiDa')
            prioritySort = models.PrioritySort(name=form.get('PriorityName'), diem=form.get('diem'),
                                               hieuSo=form.get('hieuso'),
                                               tongBanThang=form.get('tongbanthang'), doiKhang=form.get('doikhang'))
            config_main.prioritySort_id = prioritySort.id

            db.session.add(config_main)
            db.session.commit()
            return True
        return False
    except Exception as e:
        print('Error change_config', e)
        return False


def find_player_by_name(name: str):
    players = models.Player.query.filter(models.Player.name.contains(name)).all()
    return players


def find_team_by_name(name: str):
    teams = models.Team.query.filter(models.Team.name.contains(name)).all()
    return teams


def create_group(groupname: str = None, numberteamin: int = 0, numberteamout: int = 0, round_id=None):
    """

    :param groupname:
    :param numberteamin:
    :param numberteamout:
    :param round_id:
    :return: type bool
    """
    try:
        if groupname and numberteamin > numberteamout and round_id:
            rd = models.Round.query.get(round_id).id
            newround = models.Groups(round_id=rd, name=groupname, numberteamin=numberteamin,
                                     numberteamout=numberteamout)
            db.session.add(newround)
            db.session.commit()
            return True
        return False
    except Exception as e:
        print('Error create_group: ', e)
        return False


def create_round(roundname: str = None, numberteamin: int = None, numberteamout: int = None, format=None):
    """
    :param roundname:
    :param numberteamin:
    :param numberteamout:
    :param format:
    :return: type bool
    """
    try:
        if roundname and numberteamin and numberteamout and numberteamin > numberteamout:
            newRound = models.Round(roundname=roundname, numberteamin=numberteamin, numberteamout=numberteamout,
                                    format=format)
            db.session.add(newRound)
            db.session.commit()
            return True
        return False
    except Exception as e:
        print('Error create_round:', e)
        return False


def add_result():
    pass


def create_match(datetime=None, group_id=None, hometeam_id=None, awayteam_id=None, stadium_id=None):
    """
    :param datetime:
    :param group_id:
    :param hometeam_id:
    :param awayteam_id:
    :param stadium_id:
    :return: type Bool
    """
    if datetime and group_id and hometeam_id and awayteam_id and stadium_id:
        newMatch = models.Match(datetime=datetime, group_id=group_id, hometeam_id=hometeam_id, awayteam_id=awayteam_id,
                                stadium_id=stadium_id)
        db.session.add(newMatch)
        db.session.commit()
        return True
    else:
        return False


def delete_match(match_id):
    try:
        match = models.Match.query.get(match_id)
        db.session.delete(match)
        db.session.commit()
        return True
    except Exception as e:
        print('Error delete_match:', e)
        return False


def delete_group(group_id):
    try:
        group = models.Groups.query.filter(models.Groups.id == group_id).first()
        db.session.delete(group)
        db.session.commit()
        return True
    except Exception as e:
        print('Error delete_group:', e)
        return False


def delete_round(round_id):
    try:
        round = models.Round.query.filter(models.Round.id == round_id).first()
        db.session.delete(round)
        db.session.commit()
        return True
    except Exception as e:
        print('Error delete_round:', e)
        return False


def check_hometeam_stadium(id_hometeam, id_awayteam, id_group):
    # các trận đấu trong bảng(trong vòng) đó:
    matchs = models.Match.query.filter(models.Match.group_id == id_group, models.Match.hometeam_id == id_hometeam,
                                       models.Match.awayteam_id == id_awayteam).first()
    if matchs:
        return False
    else:
        return True


def get_win_match(teamid):
    """
    đếm số lượng trận thắng của một đội bóng nhằm mục đích tính điểm
    :param teamid:
    :return:
    """
    # matchs = các trận đội bóng đó đã tham gia
    result = models.Result.query.filter(models.Result.winteam == teamid).all()
    return result


def get_tie_match(teamid):
    amountie = models.Result.query.join(models.Match).filter(
        or_(models.Match.awayteam_id == teamid, models.Match.hometeam_id == teamid),
        models.Result.typeresult == models.ETypeResult.Tie).all()
    return amountie


def get_lose_match(teamid):
    amountie = models.Result.query.join(models.Match).filter(
        or_(models.Match.awayteam_id == teamid, models.Match.hometeam_id == teamid),
        not_(or_(models.Result.typeresult == models.ETypeResult.Tie,
                 models.Result.typeresult == models.ETypeResult.Win))).all()
    return amountie


def check_form_register_account(form):
    """
     kiểm tra đầu vào form
    :param form:
    :return:
    :exception ValueError
    """
    if form:
        user = models.Team.query.filter(
            or_(models.Team.username == form.get('username'),
                models.Team.name == form.get('teamname'),
                models.Team.email == form.get('email'))
        ).first()
        # validate email, user
        if user:
            if user.username == form.get('username'):
                raise ValueError("Invalid Username")
            if user.email == form.get('email'):
                raise ValueError("Invalid Email")
            if user.name == form.get('teamname'):
                raise ValueError("Invalid team name")
        return True
    raise ValueError("Error Form")


def create_account(form):
    """
    :param form: type dict()
    :return: Return True if it commit to database success else False which commit or password hashing failde
    """

    try:
        if form and form.get('email'):
            password = base64.standard_b64encode(os.urandom(8))[:8]
            usernew = models.Team(username=form.get('username', None),
                                  password=base64.urlsafe_b64encode(password).decode('utf-8'),
                                  email=form.get('email', None),
                                  name=form.get('teamname', None),
                                  phonenumber=form.get('phone_number', None),
                                  invalid=False,
                                  )
            db.session.add(usernew)
            db.session.commit()
            return True
        raise Exception('email or form is empty')
    except Exception as e:
        print("Error create_account:", e)
        return False

def get_list_player(teamid):
    try:
        if teamid:
            lsplayer = models.Player.query.filter(models.Player.team_id == teamid).all()
            return lsplayer
        raise ValueError('teamid is empty or ' + teamid + ' invalid')
    except Exception as e:
        print('Error get_list_player',e)
        return None
if __name__ == '__main__':
    print("hòa", get_tie_match(decodeID("xATMyQDM4U0MtIzNDNTL1QzQx0CN3YzQtIUMFVTLyI0NGV0N1ADOFJDM27C3"))[0].match_id)
    print("thắng", get_win_match(decodeID("xATMyQDM4U0MtIzNDNTL1QzQx0CN3YzQtIUMFVTLyI0NGV0N1ADOFJDM27C3"))[0].match_id)
    print("Thua", get_win_match(decodeID("xATMyQDM4U0MtIzNDNTL1QzQx0CN3YzQtIUMFVTLyI0NGV0N1ADOFJDM27C3"))[0].match_id)
    x = base64.standard_b64encode(os.urandom(8))[:8]
    print(x)
    xencode = base64.urlsafe_b64encode('spoNHAn6'.encode('utf-8')).decode('utf-8')
    xdecode = base64.urlsafe_b64decode(xencode).decode('utf-8')
    print(xdecode, xencode)
    print(check_password_first('c3BvTkhBbjd=', 'spoNHAn6'))

