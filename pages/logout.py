import time
from datetime import datetime

import streamlit as st

from utils.data_handler import save_data
from utils.database import user_db
from utils.menu import menu_with_redirect, sidebar_menu

menu_with_redirect()
sidebar_menu()

st.markdown('<style>body{text-align:center;}</style>', unsafe_allow_html=True)
with st.form('logout'):
    st.title('退出登录')
    submit = st.form_submit_button('确定', type='primary')
    if submit:
        start = datetime.strptime(st.session_state['learning_start_time'], "%Y-%m-%d %H:%M:%S")
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        end = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
        delta = end - start
        st.session_state['learning_start_time'] = None
        user = st.session_state['role']
        user.learn_time += delta.seconds
        user_db[user.username] = user.__dict__
        save_data('resources/data/user_db.json', user_db)
        st.session_state['role'] = None
        st.rerun()
