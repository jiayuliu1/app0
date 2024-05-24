class Question:
    SINGLE_CHOICE = 0  # 单选
    FILL_IN_THE_BLANKS = 1  # 填空

    def __init__(self, qid, description, kind, option_list, file_url=''):
        self.qid = qid
        self.description = description
        self.kind = kind
        self.option_list = option_list
        self.file_url = file_url
