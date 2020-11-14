# qzapi_python 文档

## 初始化

所有对强智教务系统的使用都从实例化一个`Qzapi`类开始，通过`Qzapi`类中的方法来使用教务系统的功能。

参数列表:

| 参数名字 | 参数类型 | 描述 | 备注 |
| :-: | :-: | :-: | :-: |
|idNumber|str|学号| |
|password|str|密码| |

返回值:

无

例:

```python
>>> import qzapi
>>> qz = qzapi.Qzapi('******', '******')
>>> qz.get_user_info()
{'name': '***', 'sex': '*', 'grade': '****', 'college': '********', 'major': '********', 'class': '********'}
```

## 获取用户信息

可以通过`get_user_info()`方法获取当前登录用户的信息。

参数列表:无

返回类型:

Python dict 类型

返回值:

| 键 | 值类型 | 描述 | 备注 |
| :-: | :-: | :-: | :-: |
|'name'|str|学生姓名| |
|'sex'|str|性别| |
|'grade'|str|年级| |
|'college'|str|院校名称| |
|'major'|str|专业名称| |
|'class'|str|班级| |

例:

```python
>>> qz.get_user_info()
{'name': '***', 'sex': '*', 'grade': '****', 'college': '********', 'major': '********', 'class': '********'}
```

## 获取课程表

可以通过`get_schedule()`方法获得当周或者其他周次的课程表。

参数列表:

| 参数名字 | 参数类型 | 描述 | 备注 |
| :-: | :-: | :-: | :-: |
|queryWeek|int|查询周次|如为空则查询当周课表|

返回类型:

Python list 类型

返回值:

| 键 | 值类型 | 描述 | 备注 |
| :-: | :-: | :-: | :-: |
|'weekday'|str|星期||
|'daySequence'|str|排课时间|'0102'代表第一第二节课|
|'subjectName'|str|科目名字||
|'teacherName'|str|教师名字||
|'roomName'|str|教室名字||
|'teachWeek'|str|教学周次||

例:

```python
>>> qz.get_schedule(1)
[{'weekday': 'Tuesday', 'daySequence': '0102', 'subjectName': '大学英语(A）（2-2）', 'teacherName': '***', 'roomName': 'J1-207室', 'teachWeek': '1-20'}, {'weekday': 'Tuesday', 'daySequence': '0304', 'subjectName': '计算机程序设计（C语言）', 'teacherName': '***', 'roomName': 'J14-303室', 'teachWeek': '1-12'}, {'weekday': 'Tuesday', 'daySequence': '0506', 'subjectName': '高等数学（A）（2-2）', 'teacherName': '***', 'roomName': 'J14-219室', 'teachWeek': '1-16'}]
```

## 获取今日的空教室

智校园重要功能。可以通过`get_empty_classroom()`方法获取空教室列表。

参数列表:

| 参数名字 | 参数类型 | 描述 | 备注 |
| :-: | :-: | :-: | :-: |
|idleTime|str|空闲时间段|可以是 'am', 'pm', 'night'|
|currDate|str|空闲日期|格式:'2019-08-01'|

返回类型:

Python list 类型

返回值:

| list中类型 | 描述 | 备注 |
| :-: | :-: | :-: |
|dict|教学楼信息|包含如下dict|

| 键 | 值类型 | 描述 | 备注 |
| :-: | :-: | :-: | :-: |
|floorName|str|教学楼名字||
|roomList|list|教室列表|包含如下dict|

| 键 | 值类型 | 描述 | 备注 |
| :-: | :-: | :-: | :-: |
|roomName|str|空教室名字||
|roomSize|str|空教室大小||
|floorName|str|教学楼名字||

例:

```python
>>>qz.get_empty_classroom('am', '2019-07-01')
[{'floorName': '青岛校区-7号楼', 'roomList': [{'roomName': 'J7-105室', 'roomSize': 126, 'floorName':'7号楼'}]},
{'floorName': '青岛校区-14号楼', 'roomList': [{'roomName': 'J14-328室', 'roomSize': 126, 'floorName': '14号楼'}]}]
```

## 获取个人成绩

可通过`get_exam_score()`方法获取令人悲伤的成绩

参数列表:

| 参数名字 | 参数类型 | 描述 | 备注 |
| :-: | :-: | :-: | :-: |
|semester|str|指定学期|例如: '2018-2019-1'|

返回值:

| 键 | 值类型 | 描述 | 备注 |
| :-: | :-: | :-: | :-: |
|subjectProp|str|课程性质||
|subjectCategory|str|课程属性||
|subjectEngName|str|课程英语名||
|subjectName|str|课程名字||
|score|int/float|分数|值类型得看实际分数，如果带小数的话就是float类型|
|credit|float|学分||

例:

```python
[{'subjectProp': '公共选修课', 'subjectCategory': '公选', 'subjectEngName': 'Career development and employment guidance for College Students', 'subjectName': '大学生职业发展与就业创业指导', 'score': '-1', 'credit': -1}, {'subjectProp': '通识教育课', 'subjectCategory': '必修', 'subjectEngName': 'College English (A)（2-1）', 'subjectName': '大学英语(A）（2-1）', 'score': '-1', 'credit': -1}]
```
