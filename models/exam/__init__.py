class Exam:
    EASY = 0
    MID = 1
    HARD = 2

    def __init__(self, eid, start_time, level=EASY, questions=None):
        self.eid = eid
        self.start_time = start_time
        self.level = level
        self.questions = questions

