import pandas as pd
import streamlit as st

from utils.data_handler import save_data
from utils.database import user_db, user_exam_db
from utils.menu import menu_with_redirect, sidebar_menu

menu_with_redirect()
sidebar_menu()

st.title('个人信息')
user = st.session_state['role']
st.subheader('昵称')
st.write(user.nickname)
st.subheader('账号')
st.write(user.username)
st.subheader('学习时长')
hours = user.learn_time // 3600
minutes = user.learn_time % 3600 // 60
seconds = user.learn_time % 60
st.write(f'{hours}小时{minutes}分{seconds}秒')
st.subheader('考核成绩')
st.markdown('---')
df = pd.DataFrame(columns=['试卷号', '开始时间', '考试时长', '成绩'])
for k, v in user_exam_db.items():
    if user.username in k:
        eid = eval(k)[1]
        row = {'试卷号': eid, '开始时间': v[0], '考试时长': v[1], '成绩': v[2]}
        df.loc[len(df)] = row

st.table(df)

col1, col2 = st.columns([2, 1])
with col1:
    with st.popover('修改昵称'):
        with st.form('update_nickname'):
            nickname = st.text_input('请输入新的昵称').strip()
            submit = st.form_submit_button('确定', type='primary')
            if submit:
                if nickname == '':
                    st.toast('请输入昵称')
                else:
                    user.nickname = nickname
                    user_db[user.username] = user.__dict__
                    save_data('resources/data/user_db.json', user_db)
                    st.rerun()

with col2:
    with st.popover('修改密码'):
        with st.form('update_password'):
            password = st.text_input('请输入旧密码', type='password').strip()
            new_password = st.text_input('请输入新的密码', type='password').strip()
            check_password = st.text_input('请再次输入新的密码', type='password').strip()
            submit = st.form_submit_button('确定', type='primary')
            if submit:
                if password == '' or new_password == '' or check_password == '':
                    st.toast('请填写表单内容！')
                elif password != user.password:
                    st.toast('旧密码输入错误！')
                elif new_password != check_password:
                    st.toast('密码输入不一致！')
                else:
                    user.password = new_password
                    user_db[user.username] = user.__dict__
                    save_data('resources/data/user_db.json', user_db)
                    st.toast('密码修改成功！')
