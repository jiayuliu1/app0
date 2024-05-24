import streamlit as st
from models.user import User
from utils.data_handler import save_data
from utils.database import user_db

st.sidebar.page_link('pages/login.py', label='登录')

st.markdown(
    "<style>body{text-align:center}</style>", unsafe_allow_html=True)

with st.form('register_form'):
    st.title('注册')
    username = st.text_input('账号', placeholder='请输入账号').strip()
    nickname = st.text_input('用户名', placeholder='请输入用户名').strip()
    password = st.text_input('密码', placeholder='请输入密码', type='password').strip()
    check_password = st.text_input('再次输入密码', placeholder='请再次输入密码', type='password').strip()
    submit = st.form_submit_button(label='注册', type='primary')

    if submit:
        if username == '' or password == '' or check_password == '' or nickname == '':
            st.toast('请填写表单内容！')
        elif password != check_password:
            st.toast('密码不一致')
        elif username in user_db:
            st.toast('该账号以存在')
        else:
            user = User(username, password, nickname)
            user_db[username] = user.__dict__
            save_data('resources/data/user_db.json', user_db)
            st.toast('注册成功！')
