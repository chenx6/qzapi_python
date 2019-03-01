import qzAPI

idNumber = input('输入账号')
password = input('输入密码')

qz = qzAPI.qzapi(idNumber, password)

sch = qz.get_schedule()
for i in sch:
    print('%s %s %s %s %s %s' % (i['weekday'], i['daySequence'], i['subjectName'], i['roomName'],
                                 i['teacherName'],  i['teachWeek']))

info = qz.get_user_info()
print('%s %s %s %s %s %s' %
      (info['name'], info['sex'], info['grade'], info['college'], info['major'], info['class']))

score = qz.get_exam_score('2018-2019-1')
for i in score:
    print('%s %s %s %s %s %s' % (
        i['subjectProp'], i['subjectCategory'], i['subjectEngName'], i['subjectName'], i['score'], i['credit']))

room = qz.get_empty_classroom('am')
for i in room:
      print('%s:'%i['floorName'])
      for j in i['roomList']:
            print('%s %s %s'%(j['roomName'], j['roomSize'], j['floorName']))