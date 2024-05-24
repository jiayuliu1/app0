import os.path
import streamlit as st
from pypinyin import lazy_pinyin
from models.drug import Drug
from utils.data_handler import get_trie, disease_trie
from utils.database import drug_db
from utils.menu import menu_with_redirect, sidebar_menu

menu_with_redirect()
sidebar_menu()


@st.cache_data
def get_drugs():
    datas = []
    for value in drug_db.values():
        data = value
        datas.append(Drug(*data.values()))
    return datas


drugs = get_drugs()
trie = get_trie(drug_db.keys())
length = len(drugs)
curr_page = st.sidebar.number_input('页码', step=1, min_value=0, max_value=length - 1)

if 'curr_page_drug' in st.session_state:
    curr_page = st.session_state['curr_page_drug']
    del st.session_state['curr_page_drug']

input_text = st.sidebar.text_input('搜索框', placeholder='输入要搜索的药品')
flag = False
if input_text != '':
    pinyin = ''.join(lazy_pinyin(input_text))
    results = trie.get_start_with(pinyin)
    if len(results) == 0:
        dgs = disease_trie.get_start_with(pinyin)
        for drug in dgs:
            names = drug[0]
            for name in names:
                flag = True
                results += trie.get_start_with(''.join(lazy_pinyin(name)))
    results = list(set(results))
    for r_name, r_loc in results:
        if flag or r_name.startswith(input_text):
            button = st.sidebar.button(r_name, key=r_name)
            if button:
                st.session_state['curr_page_drug'] = r_loc
                st.rerun()

drug = drugs[curr_page]
left, right = st.columns(2)
with right:
    st.image(os.path.join(os.getcwd(), drug.img_url))

with left:
    st.title(drug.name)
    st.write(f'【主要成分】：{drug.ingredients}')
    st.write(f'【主   治】：{drug.usage}')
    st.write(f'【用法用量】：{drug.use_method}')
    st.write(f'【规   格】：{drug.scale}')
    st.write(f'【批准文号】：{drug.number}')
    st.write(f'【生产企业】：{drug.enterprise}')
