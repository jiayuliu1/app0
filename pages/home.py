import os
import time
import streamlit as st
from utils.menu import menu_with_redirect, sidebar_menu

menu_with_redirect()
sidebar_menu()
user = st.session_state['role']

if 'learning_start_time' not in st.session_state or st.session_state['learning_start_time'] is None:
    st.session_state['learning_start_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader('关于本程序')
    st.write('学校：华南理工大学')
    st.write('学院：化学与化工学院')
    st.write('年级：2020级')
    st.write('专业：化学工程与工艺')
    st.write('毕设：基于python的中医药知识学习与水平考试系统开发')
    st.write('姓名：刘佳羽')
    st.write('github：https://github.com/jiayuliu1')
    st.write('联系方式：1142011631@qq.com')
    st.write('导师：方利国')
    st.write('github：https://github.com/gzlgfang')
    st.write('联系方式：lgfang@scut.edu.cn')
    st.image('resources/logo/school.png', width=500)

