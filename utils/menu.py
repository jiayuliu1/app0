import streamlit as st


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.switch_page('pages/login.py')


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        unauthenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("app.py")
    menu()


def sidebar_menu():
    st.sidebar.page_link('pages/home.py', label='首页')
    st.sidebar.page_link('pages/profile.py', label='个人信息')
    st.sidebar.page_link('pages/materials.py', label='药材库')
    st.sidebar.page_link('pages/prescriptions.py', label='药方库')
    st.sidebar.page_link('pages/drugs.py', label='中成药库')
    st.sidebar.page_link('pages/knowledge.py', label='中医基础知识库')
    st.sidebar.page_link('pages/exam.py', label='考试中心')
    st.sidebar.page_link('pages/logout.py', label='退出登录')

