import base64,hashlib,os,random,yagmail
import datetime


from webapp import Config, db, models


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
        print("Error EncodeID:",ex)
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
        print('Error decodeID:',ex)
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
    print(team.__dict__,data)
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
        print('Error Sent_mail_login:',e)
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
    if form:
        newconfig = models.Config(
            winScore= form.get('winScore'),
            tieScore = form.get('tieScore'),
            loseScore = form.get('loseScore'),
            maxPlayer = form.get('maxPlayer'),
            minPlayer = form.get('minPlayer'),
            amountForeignPlayer = form.get('amountForeignPlayer'),
            maxAgePlayer = form.get('maxAgePlayer'),
            minAgePlayer = form.get('minAgePlayer'),
            thoiDiemGhiBanToiDa = form.get('thoiDiemGhiBanToiDa')
        )
        db.session.add(newconfig)
        db.session.commit()
        return True
    else: return False

def find_player_by_name(name: str):
    players = models.Player.query.filter(models.Player.name.contains(name)).all()
    return players
def find_team_by_name(name: str):
    teams = models.Team.query.filter(models.Team.name.contains(name)).all()
    return teams
def create_round_playoff(roundname,numberofteam,teamselected,fomat):
    if roundname and numberofteam and teamselected :
        newround = models.Round(roundname = roundname, numberofteam = numberofteam, teamselected = teamselected, format = fomat)
        db.session.add(newround)
        db.session.commit()
        return True
    else: return False
def create_round(roundname,numberofteam,teamselected,fomat,groups):
    if roundname and numberofteam and teamselected :
        newround = models.Round(roundname = roundname, numberofteam = numberofteam, teamselected = teamselected,groups = groups, fomat = fomat)
        db.session.add(newround)
        db.session.commit()
        return True
    else: return False
def create_match(datetime, round_id, hometeam_id, awayteam_id):
    if datetime and round_id and hometeam_id and awayteam_id :
        newround = models.Round(roundname = roundname, numberofteam = numberofteam, teamselected = teamselected,groups = groups, fomat = fomat)
        db.session.add(newround)
        db.session.commit()
        return True
    else: return False

if __name__ == '__main__':
    pw = generate_password("admin@123")
    print(pw)

    print(find_team_by_name("H"))
