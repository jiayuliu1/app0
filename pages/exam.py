from matplotlib import pyplot as plt
import json
import math
import random
import time
from datetime import datetime

import streamlit as st

from models.exam import Exam
from models.option import Option
from models.question import Question
from utils.data_handler import save_data
from utils.database import exam_db, question_db, option_db, user_exam_db
from utils.menu import menu_with_redirect, sidebar_menu

menu_with_redirect()
sidebar_menu()
sidebar_placeholder = st.sidebar.empty()
placeholder = st.empty()

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签 微软雅黑-
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def end_exam():
    st.session_state['bad_answer_radio'] = []
    st.session_state['bad_answer_fill'] = []
    st.session_state['good_answer_radio'] = []
    st.session_state['good_answer_fill'] = []
    count = 0
    # 选项与正确答案进行比较
    for k, v in st.session_state['answer'].items():
        if k in st.session_state['radios'] and v == st.session_state['radios'][k]:
            count += 1
            st.session_state['good_answer_radio'].append(str(k + 1))
        else:
            st.session_state['bad_answer_radio'].append(str(k + 1))
    # 比较填空题答案
    for k, v in st.session_state['blank'].items():
        if k in st.session_state['answer_fill_the_blank'] \
                and v.strip() == st.session_state['answer_fill_the_blank'][k].strip():
            count += 1
            st.session_state['good_answer_fill'].append(str(k + 1))
        else:
            st.session_state['bad_answer_fill'].append(str(k + 1))

    # 获取考试对象
    exam_obj = st.session_state['exam']
    # 计算成绩
    if exam_obj.level == Exam.EASY:
        score = count * 5
    elif exam_obj.level == Exam.MID:
        score = count * 2
    else:
        score = count

    # 页面清空
    placeholder.empty()
    # 绘制成绩
    st.session_state['score'] = score
    st.session_state['radios'] = None
    st.session_state['answer'] = None
    st.session_state['fill_the_blank'] = None
    st.session_state['answer_fill_the_blank'] = None
    user = st.session_state['role']
    start = datetime.strptime(exam_obj.start_time, "%Y-%m-%d %H:%M:%S")
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    end = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
    duration = end - start
    user_exam_db[str((user.username, exam_obj.eid))] = [exam_obj.start_time, str(duration), str(score)]
    save_data('resources/data/user_exam_db.json', user_exam_db)
    st.rerun()


def show_exam(qid_lst):
    length = len(qid_lst)
    sidebar_placeholder.empty()
    with sidebar_placeholder.container():
        curr_page = st.number_input('页码', min_value=1, max_value=math.ceil(length / 10))
        if st.button('交卷'):
            end_exam()

    start = (curr_page - 1) * 10
    end = length if curr_page * 10 > length else curr_page * 10

    # 记录用户单选题答案
    if 'radios' not in st.session_state or st.session_state['radios'] is None:
        st.session_state['radios'] = {}

    # 记录用户输入的填空题答案    
    if 'answer_fill_the_blank' not in st.session_state \
            or st.session_state['answer_fill_the_blank'] is None:
        st.session_state['answer_fill_the_blank'] = {}

    with placeholder.container():
        for i in range(start, end):
            qid = qid_lst[i]
            data = question_db[str(qid)]
            question = Question(*data.values())

            if question.kind == Question.SINGLE_CHOICE:
                # 选项描述
                options = []
                for oid in question.option_list:
                    data_option = option_db[str(oid)]
                    option = Option(*data_option.values())
                    # 添加选项
                    options.append(option.description)

                # 题目描述
                radio = st.radio(f'{i + 1}.{question.description}', options=options,
                                 key=qid, index=None)
                st.session_state['radios'][i] = radio
                # 图片单选题
                # if question.file_url != '':
                #     st.image(os.path.join(os.getcwd(), question.file_url))
            elif question.kind == Question.FILL_IN_THE_BLANKS:
                data_option = option_db[str(question.option_list[0])]
                option = Option(*data_option.values())
                text_input = st.text_input(label=f'{i + 1}.{question.description}',
                                           key=f'{i + 1}')
                st.session_state['answer_fill_the_blank'][i] = text_input


def choice_question(diff_level, exam_obj):
    # 判断考试难度等级，分配单选题和填空题数量
    if diff_level == Exam.EASY:
        count_choice = 12
        count_fill_the_blank = 8
    elif diff_level == Exam.MID:
        count_choice = 35
        count_fill_the_blank = 15
    else:
        count_choice = 80
        count_fill_the_blank = 20

    temp = count_choice
    length = len(question_db)
    # 当选择题抽取数量大于零时，抽取选择题题目
    while temp > 0:
        key = str(random.randint(0, length - 1))
        data = question_db[key]
        question = Question(*data.values())
        if question.kind == Question.SINGLE_CHOICE and question.qid not in exam_obj.questions:
            exam_obj.questions.append(question.qid)
            temp -= 1

    temp = count_fill_the_blank
    while temp > 0:
        key = str(random.randint(0, length - 1))
        data = question_db[key]
        question = Question(*data.values())
        if question.kind == Question.FILL_IN_THE_BLANKS:
            exam_obj.questions.append(question.qid)
            temp -= 1

    # 记录单选题选项
    st.session_state['answer'] = {}

    # 记录填空题标准答案
    st.session_state['blank'] = {}

    for i, qid in enumerate(exam_obj.questions):
        data = question_db[str(qid)]
        question = Question(*data.values())
        if question.kind == Question.SINGLE_CHOICE:
            for oid in question.option_list:
                data_option = option_db[str(oid)]
                option = Option(*data_option.values())
                if option.is_right:
                    st.session_state['answer'][i] = option.description
        else:
            data_option = option_db[str(question.option_list[0])]
            option = Option(*data_option.values())
            st.session_state['blank'][i] = option.description

    # 保存考试对象
    exam_db[exam_obj.eid] = exam_obj.__dict__
    # 保存考试数据
    save_data('resources/data/exam_db.json', exam_db)
    # 显示考试题目
    show_exam(exam_obj.questions)
    # 在session中保存exam
    st.session_state['exam'] = exam_obj
    st.rerun()


def exam_custom(diff_level):
    # 试卷号
    eid = len(exam_db)
    # 将试卷号作为随机种子
    random.seed(eid)
    # 获取当前时间
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    exam_obj = Exam(str(eid), now, diff_level, [])  # 生成考试对象
    choice_question(diff_level, exam_obj)


def exam_by_id(eid: str):
    random.seed(int(eid))
    diff_level = random.choice([Exam.EASY, Exam.MID, Exam.HARD])
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    exam_obj = Exam(eid, now, diff_level, [])  # 生成考试对象
    choice_question(diff_level, exam_obj)


if 'exam' not in st.session_state or st.session_state['exam'] is None:
    dic_level = {
        '简单': Exam.EASY,
        '中等': Exam.MID,
        '困难': Exam.HARD
    }

    with sidebar_placeholder.container():
        type_selection = st.sidebar.selectbox('考试类型选择', ('自定义', '输入试卷号'))

    with placeholder.container():
        st.markdown(
            "<style>body{text-align:center}</style>", unsafe_allow_html=True)
        if type_selection == '自定义':
            with st.form('exam_form_custom'):
                st.title('考试选择')
                level = st.selectbox('请选择考试难度', dic_level.keys())
                submit = st.form_submit_button('开始考试', type='primary')
                if submit:
                    placeholder.empty()
                    exam_custom(dic_level[level])
        else:
            with st.form('exam_form_id'):
                st.title('考试选择')
                exam_id = st.text_input('请输入试卷号', placeholder='请输入数字')
                submit = st.form_submit_button('开始考试', type='primary')
                if submit:
                    if exam_id in exam_db:
                        data_exam = json.loads(exam_db[exam_id])
                        exam = Exam(*data_exam.values())
                        st.session_state['exam'] = exam
                        show_exam(exam.questions)
                        st.rerun()
                    else:
                        exam_by_id(exam_id)

elif 'score' in st.session_state:
    this_exam = st.session_state['exam']
    score = st.session_state['score']
    st.title('考试成绩分析')
    st.subheader(f'试卷号：{this_exam.eid}')
    st.subheader(f'成绩：{score}分')
    count_good_answer = len(st.session_state['good_answer_radio']) + len(st.session_state['good_answer_fill'])
    count_bad_answer = len(st.session_state["bad_answer_radio"]) + len(st.session_state["bad_answer_fill"])
    st.subheader(f'题目数：{count_good_answer + count_bad_answer}')
    st.subheader(f'答对题目：{count_good_answer}道')
    st.write(f'选择题：{"、 ".join(st.session_state["good_answer_radio"])}')
    st.write(f'填空题：{"、 ".join(st.session_state["good_answer_fill"])}')
    st.subheader(f'答错题目：{count_bad_answer}道')
    st.write(f'选择题：{"、 ".join(st.session_state["bad_answer_radio"])}')
    st.write(f'填空题：{"、 ".join(st.session_state["bad_answer_fill"])}')
    plt.figure(figsize=(2, 2))
    plt.pie([score, 100 - score], labels=['正确率', '错误率'], autopct='%.1f%%')
    plt.legend(fontsize=3, loc='upper right')
    st.pyplot(plt)

    del st.session_state['score']
    st.session_state['exam'] = None
    st.button('确定', type='primary')
else:
    exam = st.session_state['exam']
    show_exam(exam.questions)
