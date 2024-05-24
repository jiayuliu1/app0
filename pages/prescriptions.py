import streamlit as st
from pypinyin import lazy_pinyin
from models.prescription import Prescription
from utils.data_handler import get_trie
from utils.database import prescription_db
from utils.menu import menu_with_redirect, sidebar_menu


@st.cache_data
def get_prescriptions():
    datas = []
    for value in prescription_db.values():
        data = value
        datas.append(Prescription(*data.values()))
    return datas


menu_with_redirect()
sidebar_menu()
cols = 1
rows = 1
prescriptions = get_prescriptions()
trie = get_trie(prescription_db.keys())
length = len(prescriptions)
max_pages = length // (cols * rows)
curr_page = st.sidebar.number_input('页码', step=1, max_value=max_pages, min_value=0)

if 'curr_page_prescription' in st.session_state:
    curr_page = st.session_state['curr_page_prescription']
    del st.session_state['curr_page_prescription']

columns = st.columns(cols, gap='large')
start = curr_page * rows * cols
end = length if (curr_page + 1) * rows * cols > length else (curr_page + 1) * rows * cols
input_text = st.sidebar.text_input('搜索框', placeholder='输入要搜索的处方名').strip()
if input_text != '':
    pinyin = ''.join(lazy_pinyin(input_text))
    results = trie.get_start_with(pinyin)
    for r_name, r_loc in results:
        if r_name.startswith(input_text):
            button = st.sidebar.button(r_name)
            if button:
                st.session_state['curr_page_prescription'] = r_loc
                st.rerun()

for i in range(start, end):
    index = i % cols
    with columns[index]:
        p = prescriptions[i]
        st.title(p.name)
        st.markdown('---')
        st.write(f'【来源】：{p.source}')
        st.write(f'【配方】：{p.formula}')
        st.write(f'【制法】：{p.produce}')
        st.write(f'【功效】：{p.effects}')
        st.write(f'【禁忌】：{p.taboo}')
