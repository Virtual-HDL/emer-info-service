import streamlit as st
#from PIL import Image

def re_var(var:str):   
    return var if var != None else '-'

def cpr_init():
    st.set_page_config(
        page_title="응급행 - CPR 방법",
        page_icon='🚨'
    )
    st.title('CPR(심폐소생술) 방법')
    return

def cpr_contents():
    st.header('CPR 가이드 (BPM 110)')
    st.info('CPR은 분당 100~120회의 속도를 유지하면서 가슴압박을 실시합니다.')
    st.video('https://youtu.be/6W_Oy80gGBU')
    return

cpr_init()
cpr_contents()