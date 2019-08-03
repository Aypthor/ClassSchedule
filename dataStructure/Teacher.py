from dataStructure.CourseTable import CourseTable
from tools.ExcelParser import ExcelParser


class Teacher:
    def __init__(self, *args):
        if len(args) == 9:
            self.name, self.subject, self.Class, self.teachHour, \
            self.Exception, self.Continue, self.continueLength, self.continueTimes, self.originTeachHour = args
            #记录老师一天的上课节数 超过四节则在运行算法时尽量不在这一天排课
            self.tired = [0, 0, 0, 0, 0, 0, 0, 0]
            self.allocated = []
