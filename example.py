import qzapi
from getpass import getpass

def menu(qz):
    help = '1.查看个人信息\n2.查询本周课表\n3.获取空自习室\n'
    help += '4.查询成绩\n'
    choice = input(help)
    while choice != 'quit':
        if choice is '1':
            info = qz.get_user_info()
            formatInfo = f'{info["name"]}, {info["sex"]}, {info["grade"]}, '
            formatInfo += f'{info["college"]}, {info["major"]}, {info["class"]}'
            print(formatInfo)
        elif choice is '2':
            sch = qz.get_schedule()
            for i in sch:
                formatSch = f'{i["weekday"]}, {i["daySequence"]}, {i["subjectName"]}, '
                formatSch += f'{i["roomName"]}, {i["teacherName"]}, {i["teachWeek"]}'
                print(formatSch)
        elif choice is '3':
            period = input('输入时间段("am","pm","night","allday"):')
            room = qz.get_empty_classroom('am')
            for i in room:
                print(f'{i["floorName"]}:')
                for j in i['roomList']:
                    print(f'{j["roomName"]}, {j["roomSize"]}, {j["floorName"]}')
        elif choice is '4':
            semester = input('输入学期(例:2018-2019-1):')
            score = qz.get_exam_score(semester)
            for i in score:
                formatScore = f'{i["subjectProp"]}, {i["subjectCategory"]}, '
                formatScore += f'{i["subjectEngName"]}, {i["subjectName"]}, '
                formatScore += f'{i["score"]}, {i["credit"]}'
                print(formatScore)
        choice = input(help)

if __name__ == '__main__':
    idNumber = input('输入账号:')
    password = getpass('输入密码:')

    qz = qzapi.qzapi(idNumber, password)
    menu(qz)
