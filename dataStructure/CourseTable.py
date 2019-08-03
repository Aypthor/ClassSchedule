import random
class CourseTable:
    dayNum = 5
    lessonNum = 9

    def __init__(self, dayNum, lessonNum):
        # 读文件决定要不要调用set
        if dayNum != 5:
            self.dayNum = dayNum
        if lessonNum != 9:
            self.lessonNum = lessonNum
        self.table = []
        for i in range(0, lessonNum + 1):
            day = []
            for j in range(0, dayNum + 1):
                day.append(0)
            self.table.append(day)

    def getAvailablePositionForC(self):
        day = random.randint(1, self.dayNum)
        lesson = random.randint(1, self.lessonNum - 1)
        errTime = 0
        # 首先随机找连堂课位置，如果多次尝试不成功则顺序查找
        while self.table[lesson][day] != 0 or self.table[lesson + 1][day] != 0:
            errTime += 1
            day = random.randint(1, self.dayNum)
            lesson = random.randint(1, self.lessonNum - 1)
            if errTime >= 50:
                for i in range(1, self.dayNum + 1):
                    for j in range(1, self.lessonNum):
                        if self.table[j][i] == 0 and self.table[j + 1][i] == 0:
                            return i, j

        return day, lesson


