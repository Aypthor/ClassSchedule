from dataStructure.Class import Class
from dataStructure.CourseTable import CourseTable
from dataStructure.Teacher import Teacher
from tools.ExcelParser import ExcelParser
from tools.ExcelWriter import write_excel_xlsx


class TeacherList:
    def __init__(self, *args):
        self.list = []
        if len(args) == 1:
            # construct form excel
            parser = ExcelParser(args[0])
            info = parser.parse_excel()
            for teacherInfo in info:
                #从excel中读取数据
                name = teacherInfo[0]
                subject = teacherInfo[1]
                teachHour = teacherInfo[3]
                continueTimes = teacherInfo[7]
                continueLength = teacherInfo[6]
                classInfo = self._getClassInfo(teacherInfo[2])
                if classInfo == -1:
                    raise Exception(name + "的班级中含有中文分号，请修改！！")
                exception = self._getExceptions(teacherInfo[4])
                if exception == -1:
                    raise Exception(name + "的特殊要求中有中文分号，请修改！！")
                elif exception == -2:
                    raise Exception(name + "的特殊要求中有中文逗号，请修改！！")
                Continue = teacherInfo[5]
                self.list.append(Teacher(name, subject, classInfo, teachHour, exception, Continue, continueLength, continueTimes, teachHour))

    def _getClassInfo(self, str):
        if str.find("；") != -1:
            #含有中文分号时返回-1
            return -1
        rawinfo = str.split(';')
        info = []
        #对每一个班的数据进行去掉前后空格处理并且添加到list
        for i in rawinfo:
            i = i.strip()
            info.append(i)
        return info

    def _getExceptions(self, str):
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
                    result.append((day, time))

        return result

    def generateClassTableForEveryTeacher(self):
        for teacher in self.list:
            dayNum = CourseTable.dayNum
            lessonNum = CourseTable.lessonNum
            courseTable = CourseTable(dayNum, lessonNum)
            #生成每个班的课表
            for i in range(0, len(teacher.Class)):
                for j in range(0 + i * int(teacher.originTeachHour), int(teacher.originTeachHour) + i * int(teacher.originTeachHour)):
                    day, lesson = teacher.allocated[j]
                    courseTable.table[lesson][day] = teacher.Class[i]

            table = []
            for i in range(1, courseTable.lessonNum + 1):
                day = []
                for j in range(1, courseTable.dayNum + 1):
                    day.append(courseTable.table[i][j])
                table.append(day)
            path = "./documents/teacher/" + teacher.name + ".xlsx"
            name = "course table"

            write_excel_xlsx(path, name, table)

if __name__ == '__main__':
    try:
        list = TeacherList("../documents/Teachers.xlsx")
        print("aaa")
    except Exception as e:
        print(e)
