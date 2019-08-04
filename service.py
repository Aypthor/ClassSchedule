import os

from dataStructure.ClassList import ClassList
from dataStructure.Teacher import Teacher
from dataStructure.TeacherList import TeacherList
from tools.ExcelWriter import write_excel_xlsx


def mainProcess():
    #从文件中获取老师信息
    try:
        teacherList = TeacherList("./documents/Teachers.xlsx")
    except Exception as e:
        print(e)
        os._exit(0)

    #从文件中获取班级信息
    try:
        classList = ClassList("./documents/ClassInfo.xlsx", teacherList.list)
    except Exception as e:
        print(e)
        os._exit(0)
    #在课表上标出不分配课的地方
    ETeacher = Teacher(0, "E", 0, 0, 0, 0, 0, 0, 0)
    for Class in classList.list:
        for i in Class.noSchedule:
            day, lesson = i
            Class.courseTable.table[lesson][day] = ETeacher

    #处理算法
    #给每个班先分配连堂课

    #策略：一个班一天最多上三节同样的课，老师一天最多上四节课，按照此原则排课完成后若有空缺就遍历备选列表随意填满
    for Class in classList.list:
        print("allocating class " + str(Class.classNo))
        allocateTeacherC(Class)
        num = 0
        for i in range(1, Class.courseTable.lessonNum + 1):
            for j in range(1, Class.courseTable.dayNum + 1):
                if Class.courseTable.table[i][j] == 0:
                    allocateTeacher(j, i, Class)
    #产生班级课表
    classList.generateClassTableForEveryClass()
    teacherList.generateClassTableForEveryTeacher()
    print("finished")

    # for i in range(1, classList.list[1].courseTable.lessonNum + 1):
    #     for j in range(1, classList.list[1].courseTable.dayNum + 1):
    #         print(classList.list[1].courseTable.table[i][j].name)

def allocateTeacher(day, lesson, Class):
    teachers = Class.teachers
    teacher, index = Class.getARandomTeacher()
    errTime = 0
    #首先在一个位置上按老师喜好随机老师，若尝试20此无法随到有效老师就从老师列表中找出一个没有被分配时间的老师
    while teacher.tired[day] >= len(teacher.Class) * 2 or (day, lesson) in teacher.allocated or (str(day), str(lesson)) in\
            teacher.Exception or not Class.allocatable(day, teacher):
        errTime += 1
        teacher, index = Class.getARandomTeacher()
        if errTime >= 5000:
            for tea in teachers:
                if not (day, lesson) in tea.allocated:
                    teacher = tea
                    break
            break
    teacher.tired[day] += 1
    teacher.allocated.append((day, lesson))
    Class.allocate(day, lesson, teacher)
    teacher.teachHour -= 1
    if teacher.teachHour == 0:
        teacher.teachHour = teacher.originTeachHour
        Class.teachers.pop(index)

def allocateTeacherC(Class):
    teachers = Class.teachers
    for teacher in teachers:
        #判断这位老师是否需要连堂课
        if int(teacher.Continue) == 1:
            length = teacher.continueLength
            times = teacher.continueTimes
            for j in range(0, int(times)):
                day, lesson = Class.courseTable.getAvailablePositionForC()
                errTime = 0
                while teacher.tired[day] >= (len(teacher.Class) * 2) - 1 or (str(day), str(lesson)) in \
                        teacher.Exception or (str(day), str(lesson + 1)) in teacher.Exception:
                    errTime += 1
                    day, lesson = Class.courseTable.getAvailablePositionForC()
                    if errTime >= 10:
                        break
                teacher.tired[day] += 2
                teacher.allocated.append((day, lesson))
                teacher.allocated.append((day, lesson + 1))
                teacher.teachHour -= 2
                Class.allocate(day, lesson, teacher)
                Class.allocate(day, lesson + 1, teacher)
                if teacher.teachHour == 0:
                    teacher.teachHour = teacher.originTeachHour
                    Class.teachers.remove(teacher)


if __name__ == "__main__":
    mainProcess()
