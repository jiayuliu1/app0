import math
import os
import streamlit as st
from utils.menu import menu_with_redirect, sidebar_menu

menu_with_redirect()
sidebar_menu()


@st.cache_data
def get_knowledge():
    datas = []
    with open(os.path.join(os.getcwd(), 'resources/data/base_knowledge.txt'), encoding='utf-8') as file:
        for f in file:
            datas.append(f.removesuffix('\n'))
    return datas


rows = 20
knowledge = get_knowledge()
length = len(knowledge)
max_page = math.ceil(length / rows)
curr_page = st.sidebar.number_input('页码', step=1, min_value=0, max_value=max_page)
start = curr_page * rows
end = length if (curr_page + 1) * rows > length else (curr_page + 1) * rows
left, right = st.columns(2)
count = 0
for i in range(start, end):
    if count < 10:
        with left:
            st.write(f'{i}. {knowledge[i]}')
    else:
        with right:
            st.write(f'{i}. {knowledge[i]}')
    count += 1
