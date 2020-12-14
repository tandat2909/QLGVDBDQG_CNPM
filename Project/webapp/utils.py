import base64, hashlib, os, random, yagmail
import datetime

from webapp import Config, db, models, config_main


def check_password(pw_hash='', pw_check=''):
    pw_check_hash = hashlib.sha256((pw_check + str(Config.KEYPASS)).encode("utf-8")).hexdigest()
    if pw_hash == pw_check_hash:
        return True
    return False


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


def change_password(user=None, pwold: str = None, pwnew: str = None):
    try:
        if user and pwnew and pwold:
            if check_password(user.password, pwold):
                user.password = generate_password(pwnew)
                # print("pw hashmới: " + user.password)
                db.session.add(user)
                db.session.commit()
                return True
        raise
    except:
        return False


def sent_mail_login(team, data):
    print(team.__dict__, data)
    try:
        if team and data:
            data["time"] = str(datetime.datetime.now().strftime("%X %p - %d %B %Y"))
            sender_email = "antoanhethongthongtin13@gmail.com"
            receiver_email = team.email
            password = decodeID("ETUXVUUXVUMyMDQtgjRwMEMClTL8F0C")[0:-1].capitalize()
            subject = f'[Blog] Successful Login From New IP  {data["ip"]} - {data["time"]}'

            prettify_html = f'<h1><strong>Successful Login <span style ="color:#0bff00"> {team.name} </span> From New IP</strong></h1>\
                            <h3><strong>We&#39;ve noticed that you accessed your account from IP address new</strong></h3>\
                            <p>Time: <strong style="color:red">' + data['time'] + '</strong></p>\
                            <p>IP Address: <strong style="color:red">' + data['ip'] + ' - ' + data['location'] + '</strong></p>\
                            <p>Application: <strong style="color:red">' + data[
                'user_agent'].lower().capitalize() + ' - ' + data['os'] + '</strong></p>\
                            '
            yag = yagmail.SMTP(user=sender_email, password=password)
            status = yag.send(
                to=receiver_email,
                subject=subject,
                contents=prettify_html
            )
            return False if status == False else True
        return False
    except Exception as e:
        print('Error Sent_mail_login:', e)
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
            prioritySort = models.PrioritySort(name=form.get('PriorityName'),diem=form.get('diem'), hieuSo=form.get('hieuso'),
                                               tongBanThang=form.get('tongbanthang'),doiKhang=form.get('doikhang'))
            config_main.prioritySort_id=prioritySort.id

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
        group = models.Groups.query.filter(models.Groups.id ==group_id).first()
        db.session.delete(group)
        db.session.commit()
        return True
    except Exception as e:
        print('Error delete_group:', e)
        return False
def delete_round(round_id):
    try:
        round = models.Round.query.filter(models.Round.id ==round_id).first()
        db.session.delete(round)
        db.session.commit()
        return True
    except Exception as e:
        print('Error delete_round:', e)
        return False

if __name__ == '__main__':
    delete_match('29625f47-2238-4899-81b4-adce25dfd23b')

    print(find_player_by_name('Rô')[0].name)
