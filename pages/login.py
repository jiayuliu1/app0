# streamlit: hide-page

import streamlit as st
from utils.database import user_db
from models.user import User

st.sidebar.page_link('pages/register.py', label='注册')
st.markdown("---", unsafe_allow_html=True)


with st.form("login_form"):
    st.title("登录")
    username = st.text_input("账号", placeholder='请输入你的账号',value='user').strip()
    password = st.text_input("密码", placeholder='请输入你的密码', type='password',value='user').strip()
    submit = st.form_submit_button(label='登录', type='primary')

    if submit:
        if username == '' or password == '':
            st.toast('请填写表单内容！')
        elif username in user_db:
            data = user_db[username]
            if password == data['password']:
                user = User(username, password, data['nickname'], data['learn_time'])
                st.session_state['role'] = user
                st.toast('登录成功！')
                st.switch_page('pages/home.py')
            else:
                st.toast('密码错误！')
        else:
            st.toast('不存在该用户！')
