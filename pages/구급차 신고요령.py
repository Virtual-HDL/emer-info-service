import streamlit as st
from PIL import Image

def call_init():
    st.set_page_config(
        page_title='응급행 - 119 신고요령', 
        layout='wide', 
        page_icon='🚨'
    )
    st.title('119 신고요령 with 소방청')
    st.info('''
        **참고 사이트**  
        https://www.nfa.go.kr/nfa/publicrelations/emergencyservice/119emergencydeclaration/''',
        icon="🚨")
    return

def call_image():
    for i in range(4):
        col1, col2 = st.columns(2)
        col1.image(Image.open(f'images/call/119emergencydeclaration-{2*i+1}.jpg'), use_column_width='auto')
        col2.image(Image.open(f'images/call/119emergencydeclaration-{2*i+2}.jpg'), use_column_width='auto')
    return

call_init()
call_image()