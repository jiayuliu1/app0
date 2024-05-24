import json
import os
import streamlit as st
from pypinyin import lazy_pinyin
from datastruct import Trie


@st.cache_data
def load_data(filename):
    data = {}
    if os.path.exists(filename):
        with open(os.path.join(os.getcwd(), filename), encoding='utf-8') as file:
            data = json.load(file)
    return data


def save_data(filename, data):
    with open(os.path.join(os.getcwd(), filename), 'w', encoding='utf-8') as file:
        json.dump(data, file)


def get_trie(keys):
    t = Trie()
    for loc, key in enumerate(keys):
        pin_yin = ''.join(lazy_pinyin(key))
        t.insert(pin_yin, key, loc)
    return t


disease_trie = Trie()
with open(os.path.join(os.getcwd(), 'resources/data/disease_cn_medicine.txt'), encoding='utf-8') as file:
    for f in file:
        row = f.strip()
        if row != '':
            disease, drugs = row.split('】')
            disease = disease.removeprefix('【')
            drugs = drugs.split('、')
            disease_trie.insert(''.join(lazy_pinyin(disease)), drugs, None)
