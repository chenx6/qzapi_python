'''
智校园的targetAPI是16, 使用极其蛋疼
所以就参照'QZAPI_Archive'和手动抓包分析, 使用python重新封装了API
2019, chen_null
'''

import requests
import time


class QzapiExecption(Exception):
    pass


class qzapi:
    '''
    将强智教务系统的API封装成类，以方便调用
    '''

    session = requests.Session()
    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    host = 'jwgl.sdust.edu.cn'
    api = f'http://{host}/app.do'

    def __init__(self, idNumber, password):
        '''
        初始化

        :param idNumber: 学号
        :param password：账号密码
        '''
        self.loginParam = {'method': 'authUser'}
        self.dateParam = {'method': 'getCurrentTime'}
        self.scheduleParam = {'method': 'getKbcxAzc'}
        self.emptyRoomParam = {'method': 'getKxJscx'}
        self.userInfoParam = {'method': 'getUserInfo'}
        self.examParam = {'method': 'getCjcx'}
        self.currDate = time.strftime('%Y-%m-%d', time.localtime())

        if idNumber == '' or password == '':
            raise QzapiExecption('未输入参数', idNumber, password)
        self.idNumber = idNumber
        self.loginParam['xh'] = idNumber
        self.loginParam['pwd'] = password
        loginResp = self.session.post(
            self.api, params=self.loginParam)
        loginJson = loginResp.json()
        if loginJson['token'] == -1:
            raise QzapiExecption('账号或密码输入错误')
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
        self.userInfoParam['xh'] = self.idNumber
        userInfoResp = self.session.post(
            self.api, params=self.userInfoParam)
        userInfoJson = userInfoResp.json()
        if None in userInfoJson or len(userInfoJson) == 0:
            raise QzapiExecption('无法获取资料')
        sortedUserInfo = self.sort_user_info(userInfoJson)
        return sortedUserInfo

    def get_curr_time(self):
        '''
        获取当前周次和学期
        该函数没有return值, 只是将当前周次和当前学期存入类中
        '''
        self.dateParam['currDate'] = self.currDate
        dateResp = self.session.post(self.api, params=self.dateParam)
        dateJson = dateResp.json()
        if None in dateJson or len(dateJson) == 0:
            raise QzapiExecption('无法获取时间')
        # week is a number...
        self.week = dateJson['zc']
        self.currSemester = dateJson['xnxqh']

    def get_schedule(self, queryWeek=None):
        '''
        获取课程表

        :param queryWeek: 当前周次

        :return: 一个dict:
        {'weekday': 星期,'daySequence': 课程次序, \
            'subjectName': 课程名字, 'teacherName': 教师名字, \
            'roomName': 教室名字, 'teachWeek': 教学周次}
        '''
        if queryWeek == None:
            queryWeek = self.week
        self.scheduleParam['xh'] = self.idNumber
        self.scheduleParam['xnxqid'] = self.currSemester
        self.scheduleParam['zc'] = str(queryWeek)
        scheduleResp = self.session.post(
            self.api, params=self.scheduleParam)
        scheduleJson = scheduleResp.json()
        if None in scheduleJson or len(scheduleJson) == 0:
            raise QzapiExecption('无法获取课程表')
        sortedSchedule = self.sort_schedule(scheduleJson)
        return sortedSchedule

    def get_empty_classroom(self, idleTime, currDate=None):
        '''
        获取今日的空教室

        :param idleTime: 空闲时间段, 可以是 'am', 'pm', 'night'
        :param currDate: 空闲日期

        :return: 
        {'floorName': 教学楼名字, 'roomList': 空教室名单[{'roomName': 空教室名字, 'roomSize': 空教室大小, 'floorName': 教学楼名字}]}
        '''
        if currDate == None:
            currDate = self.currDate
        self.emptyRoomParam['time'] = currDate
        self.emptyRoomParam['idleTime'] = idleTime
        emptyClassResp = self.session.post(
            self.api, params=self.emptyRoomParam)
        emptyClassJson = emptyClassResp.json()
        if None in emptyClassJson or len(emptyClassJson) == 0:
            raise QzapiExecption('无空闲教室')
        elif type(emptyClassJson) == type({}) and emptyClassJson['msg'] == '请联系管理员生成教学周历':
            raise QzapiExecption('管理员未生成教学周历')
        sortedEmptyClassroom = self.sort_empty_classroom(emptyClassJson)
        return sortedEmptyClassroom

    def get_exam_score(self, semester=None):
        '''
        获取令人悲伤的成绩

        :eg: get_exam_score('2018-2019-1')

        :param semester: 指定学期

        :return 一个dict:
        {'subjectProp': 课程性质, 'subjectCategory': 课程属性, \
            'subjectEngName': 课程英语名, 'subjectName': 课程名字, \
            'score': 分数, 'credit': 学分}
        '''
        if semester == None:
            semester = self.currSemester
        self.examParam['xh'] = self.idNumber
        self.examParam['xnxqid'] = semester
        examResp = self.session.post(self.api, params=self.examParam)
        examJson = examResp.json()
        if None in examJson or len(examJson) == 0:
            raise QzapiExecption('无成绩')
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
