'''
智校园的targetAPI是16, 使用极其蛋疼
所以就参照'QZAPI_Archive'和手动抓包分析, 使用python重新封装了API
2019, chen_null
'''

import requests
import time


class qzapi:
    session = requests.Session()

    currDate = ''
    week = 0
    currSemester = ''

    httpHead = 'http://'
    host = 'jwgl.sdust.edu.cn'


    def __init__(self, idNumber, password):
        '''
        初始化

        :param idNumber: 学号
        :param password：账号密码
        '''
        try:
            if idNumber == '' or password == '':
                raise ValueError('未输入参数', idNumber, password)
            self.idNumber = idNumber
            self.loginUrl = '/app.do?method=authUser&xh={idNumber}&pwd={password}'
            self.dateUrl = '/app.do?method=getCurrentTime&currDate={currDate}'
            self.scheduleUrl = '/app.do?method=getKbcxAzc&xh={idNumber}&xnxqid={semester}&zc={week}'
            self.emptyRoomUrl = '/app.do?method=getKxJscx&time={currTime}&idleTime={idle}'
            self.userInfoUrl = '/app.do?method=getUserInfo&xh={idNumber}'
            self.examUrl = '/app.do?method=getCjcx&xh={idNumber}&xnxqid={semester}'
            self.idNumber = idNumber
            self.currDate += time.strftime('%Y-%m-%d', time.localtime())
            self.loginUrl = self.loginUrl.format(
                idNumber=self.idNumber, password=password)
            loginResp = self.session.post(
                self.httpHead + self.host + self.loginUrl)
            loginJson = loginResp.json()
            if loginJson['token'] == -1:
                raise ValueError('账号或密码输入错误')
        except requests.exceptions.ConnectionError as e:
            print('网络有问题', e)
        except ValueError as e:
            print('参数错误', e)
        else:
            header = {'token': loginJson['token']}
            self.session.headers.update(header)
            self.get_curr_time()

    def get_user_info(self):
        '''
        获取当前用户信息

        :return: 一个格式化的dict:
        {'name': 学生姓名, 'sex': 性别, 'grade': 年级, 'college': 院校名称, \
            'major': 专业名称, 'class': 班级}
        '''
        try:
            self.userInfoUrl = self.userInfoUrl.format(idNumber=self.idNumber)
            userInfoResp = self.session.post(
                self.httpHead+self.host+self.userInfoUrl)
            userInfoJson = userInfoResp.json()
        except requests.exceptions.ConnectionError as e:
            print('网络有问题:', e)
        else:
            sortedUserInfo = self.sort_user_info(userInfoJson)
            return sortedUserInfo

    def get_curr_time(self):
        '''
        获取当前周次和学期
        该函数没有return值, 只是将当前周次和当前学期存入类中
        '''
        try:
            self.dateUrl = self.dateUrl.format(currDate=self.currDate)
            dateResp = self.session.post(self.httpHead+self.host+self.dateUrl)
            dateJson = dateResp.json()
            if dateJson == '':
                raise ValueError('无法获取时间')
        except requests.exceptions.ConnectionError as e:
            print('网络有问题:', e)
        except ValueError as e:
            print('参数错误', e)
        else:
            # week is a number...
            self.week = dateJson['zc']
            self.currSemester = dateJson['xnxqh']

    def get_schedule(self, queryWeek):
        '''
        获取课程表

        :param week: 当前周次

        :return: 一个dict:
        {'weekday': 星期,'daySequence': 课程次序, \
            'subjectName': 课程名字, 'teacherName': 教师名字, \
            'roomName': 教室名字, 'teachWeek': 教学周次}
        '''
        try:
            if queryWeek == 0:
                queryWeek = self.week
            self.scheduleUrl = self.scheduleUrl.format(
                idNumber=self.idNumber, semester=self.currSemester, week=str(queryWeek))
            scheduleResp = self.session.post(
                self.httpHead + self.host + self.scheduleUrl)
            scheduleJson = scheduleResp.json()
        except requests.exceptions.ConnectionError as e:
            print('网络有问题:', e) 
        else:
            sortedSchedule = self.sort_schedule(scheduleJson)
            return sortedSchedule

    def get_empty_classroom(self, idleTime, currDate):
        '''
        获取今日的空教室

        :param idleTime: 空闲时间段, 可以是 'am', 'pm', 'night'
        :param currDate: 空闲日期

        :return: 
        {'floorName': 教学楼名字, 'roomList': 空教室名单[{'roomName': 空教室名字, 'roomSize': 空教室大小, 'floorName': 教学楼名字}]}
        '''
        try:
            if currDate == 0:
                currDate = self.currDate
            self.emptyRoomUrl = self.emptyRoomUrl.format(
                currTime=currDate, idle=idleTime)
            emptyClassResp = self.session.post(
                self.httpHead+self.host+self.emptyRoomUrl)
            emptyClassJson = emptyClassResp.json()
            if emptyClassJson == '':
                raise ValueError('无空闲教室')
        except requests.exceptions.ConnectionError as e:
            print('网络有问题:', e)
        except ValueError as e:
            print('无返回值', e)
        else:
            sortedEmptyClassroom = self.sort_empty_classroom(emptyClassJson)
            return sortedEmptyClassroom

    def get_exam_score(self, semester):
        '''
        获取令人悲伤的成绩

        :eg: get_exam_score('2018-2019-1')

        :param semester: 指定学期

        :return 一个dict:
        {'subjectProp': 课程性质, 'subjectCategory': 课程属性, \
            'subjectEngName': 课程英语名, 'subjectName': 课程名字, \
            'score': 分数, 'credit': 学分}
        '''
        try:
            if semester == 0:
                semester = self.currSemester
            self.examUrl = self.examUrl.format(
                idNumber=self.idNumber, semester=semester)
            examResp = self.session.post(self.httpHead+self.host+self.examUrl)
            examJson = examResp.json()
            if examJson == '':
                raise ValueError('无成绩')
        except requests.exceptions.ConnectionError as e:
            print('网络有问题:', e) 
        except ValueError as e:
            print('无返回值')
        else:
            sortedExam = self.sort_exam(examJson)
            return sortedExam

    def sort_user_info(self, userInfoJson):
        '''
        带'sort'前缀的都是把中文缩写键值变成能看懂的英文键值
        '''
        tempDict = {}
        tempDict['name'] = userInfoJson['xm']
        tempDict['sex'] = userInfoJson['xb']
        tempDict['grade'] = userInfoJson['nj']
        tempDict['college'] = userInfoJson['yxmc']
        tempDict['major'] = userInfoJson['zymc']
        tempDict['class'] = userInfoJson['bj']
        return tempDict

    def sort_schedule(self, scheduleJson):
        '''
        这个函数将'kcsj'这个值改写, 转为直接可用的值
        'kcsj'例子: {'kcsj': '20102'} 意思是这节课是星期二的第一第二小节的课
        在此函数转换为星期二第一大节的课
        '''
        sortedJson = []
        for i in scheduleJson:
            tempDict = {}
            if i['kcsj'][0] == '1':
                tempDict['weekday'] = 'Monday'
            elif i['kcsj'][0] == '2':
                tempDict['weekday'] = 'Tuesday'
            elif i['kcsj'][0] == '3':
                tempDict['weekday'] = 'Wednesday'
            elif i['kcsj'][0] == '4':
                tempDict['weekday'] = 'Thursday'
            elif i['kcsj'][0] == '5':
                tempDict['weekday'] = 'Friday'
            elif i['kcsj'][0] == '6':
                tempDict['weekday'] = 'Saturday'
            elif i['kcsj'][0] == '7':
                tempDict['weekday'] = 'Sunday'
            tempDict['daySequence'] = i['kcsj'][1:]
            tempDict['subjectName'] = i['kcmc']
            tempDict['teacherName'] = i['jsxm']
            tempDict['roomName'] = i['jsmc']
            tempDict['teachWeek'] = i['kkzc']
            sortedJson.append(tempDict)
        return sortedJson

    def sort_empty_classroom(self, emptyClassJson):
        # 修复完成
        sortedFloor = []
        for j in emptyClassJson:
            tempFloor = {}
            tempFloor['floorName'] = j['jxl']
            sortedRoom = []
            for i in j['jsList']:
                tempDict = {}
                tempDict['roomName'] = i['jsmc']
                tempDict['roomSize'] = i['zws']
                tempDict['floorName'] = i['jzwmc']
                sortedRoom.append(tempDict)
            tempFloor['roomList'] = sortedRoom
            sortedFloor.append(tempFloor)
        return sortedFloor

    def sort_exam(self, examJson):
        sortedExam = []
        for i in examJson:
            tempDict = {}
            tempDict['subjectProp'] = i['kcxzmc']
            tempDict['subjectCategory'] = i['kclbmc']
            tempDict['subjectEngName'] = i['kcywmc']
            tempDict['subjectName'] = i['kcmc']
            tempDict['score'] = i['zcj']
            tempDict['credit'] = i['xf']
            sortedExam.append(tempDict)
        return sortedExam
