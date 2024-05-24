import os

import streamlit as st
from pypinyin import lazy_pinyin
from models.material import Material
from utils.data_handler import get_trie
from utils.database import material_db
from utils.menu import menu_with_redirect, sidebar_menu


@st.cache_data
def get_materials():
    datas = []
    for value in material_db.values():
        data = value
        datas.append(Material(*data.values()))
    return datas


menu_with_redirect()
sidebar_menu()
materials = get_materials()  # 药材数据
trie = get_trie(material_db.keys())  # 字典树
length = len(materials)  # 药材数据数量
curr_page = st.sidebar.number_input('页码', step=1, max_value=length - 1, min_value=0)  # 当前页码

if 'curr_page_material' in st.session_state:
    curr_page = st.session_state['curr_page_material']
    del st.session_state['curr_page_material']

input_text = st.sidebar.text_input('搜索框', placeholder='输入要搜索的药材').strip()  # 搜索框内容
if input_text != '':
    pinyin = ''.join(lazy_pinyin(input_text))
    results = trie.get_start_with(pinyin)
    for r_name, r_loc in results:
        if r_name.startswith(input_text):
            button = st.sidebar.button(r_name)
            if button:
                st.session_state['curr_page_material'] = r_loc
                st.rerun()


material = materials[curr_page]
col1, col2 = st.columns(2)
with col2:
    st.image(os.path.join(os.getcwd(), material.img))
with col1:
    st.title(material.name)
    st.write(f'【别名】：{material.alias}')
    st.write(f'【药性】：{material.drug_property}')
    st.write(f'【入药部分】：{material.part}')
    st.write(f'【药材使用方法】：{material.produce}')
    st.write(f'【产地分布】：{material.area}')
    st.write(f'【功效】：{material.effects}')
    st.write(f'【禁忌】：{material.taboo}')
