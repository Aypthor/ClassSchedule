from dataStructure.Class import Class
from tools.ExcelParser import ExcelParser
from tools.ExcelWriter import write_excel_xlsx


class ClassList:

    def __init__(self, *args):
        if len(args) == 2:
            #从文件中读取信息
            parser = ExcelParser(args[0])
            classInfo = parser.parse_excel()
            self.classNum = int(classInfo[0][0])
            dayNum = int(classInfo[0][1])
            lessonNum = int(classInfo[0][2])
            self.list = []

            #初始化Class类
            for i in range(0, self.classNum):
                classEntity = Class(i + 1, dayNum, lessonNum)
                self.list.append(classEntity)
            Class.setTeacherList(args[1])
            Class.setNoSchedule(self._getNoSchedule(classInfo[0][3]))
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
                    result.append((int(day), int(time)))

        return result
    def _getTeachersOfEveryClass(self):
        for cls in self.list:
            try:
                cls.getTeachers()
            except Exception as e:
                print(e)

    def generateClassTableForEveryClass(self):
        for cls in self.list:
            path = "./documents/class/" + str(cls.classNo) + ".xlsx"
            name = "course table"

            write_excel_xlsx(path, name, cls.getCourseTable())

if __name__ == "__main__":
    aaa = ClassList("../documents/ClassInfo.xlsx")
    print(aaa.list)