import os
import re

from dataStructure.Class import Class
from tools.ExcelParser import ExcelParser
from tools.ExcelWriter import write_excel_xlsx


class ClassList:
    def __init__(self, *args):
        if len(args) == 2:
            #从文件中读取信息
            parser = ExcelParser(args[0])
            classInfo = parser.parse_excel()
            self.classNum = classInfo[0][0]
            if not isinstance(self.classNum, float) or self.classNum < 0:
                raise Exception("班级数为非数字或包含0或负数，请修改！！")
            self.dayNum = classInfo[0][1]
            if not isinstance(self.dayNum, float) or self.dayNum < 0:
                raise Exception("上课天数为非数字或包含0或负数，请修改！！")
            self.lessonNum = classInfo[0][2]
            if not isinstance(self.lessonNum, float) or self.lessonNum < 0:
                raise Exception("每日课时数为非数字或包含0或负数，请修改！！")
            self.list = []

            #初始化Class类
            for i in range(0, round(self.classNum)):
                classEntity = Class(i + 1, round(self.dayNum), round(self.lessonNum))
                self.list.append(classEntity)
            #检查老师列表中是否包含非法班级号
            for teacher in args[1]:
                for clsNum in teacher.Class:
                    if int(clsNum) > round(self.classNum):
                        raise Exception(teacher.name + "的班级中包含超过总班级数的序号，请检查总班级数或此老师所带的班是否正确")
                for exp in teacher.Exception:
                    day, time = exp
                    day = int(day)
                    time = int(time)
                    if not((0 < day <= round(self.dayNum) and 0 < time <= round(self.lessonNum)) or (day == 0 and time == 0)):
                        raise Exception((teacher.name + "的特殊需求中包含超出上课天数或上课节数的项，请检查"))
            Class.setTeacherList(args[1])
            result = self._getNoSchedule(classInfo[0][3])
            if result == -1:
                raise Exception("集体自习中有中文分号，请修改！！")
            elif result == -2:
                raise Exception("集体自习中有中文逗号，请修改！！")
            elif result == -3:
                raise Exception("集体自习中有非数字部分，请修改！！")
            elif result == -4:
                raise Exception("集体自习中有时间超出上课天数或节数超过上课节数，请修改！！")
            else:
                Class.setNoSchedule(result)

            self._getTeachersOfEveryClass()

    def _getNoSchedule(self, str):
        if str.find("；") != -1:
            # 含有中文分号时返回-1
            return -1
        rawInfo = str.split(';')
        info = []
        result = []
        #对字符串处理

        #分割每一个不能上课的条目
        for i in rawInfo:
            i = i.strip()
            info.append(i)
        #对每一个条目进行处理
        for i in info:
            #含有中文逗号返回-2
            if i.find('，') != -1:
                return -2
            else:
                #去掉括号
                i = i.lstrip("(")
                i = i.lstrip("（")
                i = i.rstrip(")")
                i = i.rstrip("）")
                #将括号项转换成list
                rawException = i.split(',')
                if rawException != [""]:
                    day = rawException[0]
                    time = rawException[1]
                    day = day.strip()
                    time = time.strip()
                    day = re.compile(r'[0-9]\d*').findall(day)
                    time = re.compile(r'[0-9]\d*').findall(time)
                    if day and time:
                        if (0 < int(day[0]) <= round(self.dayNum) and 0 < int(time[0]) <= round(self.lessonNum)) or (day == 0 and time == 0):
                            result.append((int(day[0]), int(time[0])))
                        else:
                            return -4
                    else:
                        return -3

        return result
    def _getTeachersOfEveryClass(self):
        for cls in self.list:
            try:
                cls.getTeachers(self.dayNum * self.lessonNum)
            except Exception as e:
                print(e)
                os._exit(0)

    def generateClassTableForEveryClass(self):
        for cls in self.list:
            path = "./documents/class/" + str(cls.classNo) + ".xlsx"
            name = "course table"

            write_excel_xlsx(path, name, cls.getCourseTable())

if __name__ == "__main__":
    aaa = ClassList("../documents/ClassInfo.xlsx")
    print(aaa.list)