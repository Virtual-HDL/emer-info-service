import streamlit as st
import json
import crawl
import pandas as pd
from streamlit.components.v1 import html

def re_var(var:str):   
    return var if var != None else '-'

def app_init() -> None:
    st.set_page_config(
        page_title="응급행 (실시간 응급실 정보 확인)",
        page_icon='🚨'
    )
    st.title('응급행 (실시간 응급실 정보 확인)')
    return

def app_contents() -> None:
    st.info('실시간 응급실 정보 확인 사이트 응급행 입니다.', icon='❕')
    st.markdown('''
        ### 주소 입력
        > **현재 응급 상황이 발생한 위치를 입력해주세요.**  
    ''')
    col1, col2 = st.columns(2)
    col3, _ = st.columns(2)

    with open('./citys.json', 'r', encoding='UTF8') as f:
        citys_data = json.load(f)

    with col1:
        state = st.selectbox(
            label='시/도 선택',
            options=list(citys_data.keys())
        )

    with col2:
        city = st.selectbox(
            label='시/군/구 선택',
            options=citys_data[state]
        )

    with col3:
        isAdult = st.selectbox(
            label='성인 여부',
            options=['성인','소아']
        )

    if st.button('Done'):
        st.markdown('''
            <br/>  

            ### 결과  
            <br/>
        ''',unsafe_allow_html=True)

        if isAdult == '소아':
            emer_data = crawl.emer_crawl(state, city, False)
            moon_data = crawl.moon_crawl(state, city)
        else:
            emer_data = crawl.emer_crawl(state, city, True)
            moon_data = ''


        if len(emer_data) + len(moon_data) == 0: 
            st.info('결과가 없습니다.', icon='❕'); return
        
        for d in emer_data:
            emer_emoji, emer_sec = st.columns([5,95])

            emer_emoji.write('💓')
            info_expender = emer_sec.expander(d['name'])

            info_expender.markdown(f'''
                주소 : {d['addr']}  
                전화번호 : {d['tel']}  
                최근 갱신시간 : {d['hvidate'][:4] + '년 ' +
                    d['hvidate'][4:6] + '월 ' + d['hvidate'][6:8] + '일 ' +
                    d['hvidate'][8:10] + '시 ' + d['hvidate'][10:12] + '분 ' +
                    d['hvidate'][12:14] + '초'
                }
                <br/>  
            ''', unsafe_allow_html=True)

            if isAdult == '소아':
                info_expender.markdown(f'''
                    **응급실 정보**  
                    - 당직의 전화번호 : {re_var(d['hv12'])}  
                    - 소아진료 가능여부 : {re_var(d['hv10'])}  
                    - 소아 가용 병상 : {re_var(d['hv28'])} / {re_var(d['hvs02'])}
                    - 소아 중환자실 : {re_var(d['hv32'])} / {re_var(d['hvs09'])}
                    - [응급] 소아 중환자실 : {re_var(d['hv33'])} / {re_var(d['hvs10'])}
                    - [응급] 소아 입원실 : {re_var(d['hv37'])} / {re_var(d['hvs20'])}
                ''', unsafe_allow_html=True)
            else:
                info_expender.markdown(f'''
                    **응급실 기본 정보**
                    - 일반 입원실 : {re_var(d['hvgc'])} / {re_var(d['hvs38'])}
                    - 일반 병상 : {re_var(d['hvec'])} / {re_var(d['hvs01'])}
                    - [기타] 수술실 : {re_var(d['hvoc'])} / {re_var(d['hvs22'])}
                      
                    **중환자실 정보**  
                    - 신경과 중환자실 : {re_var(d['hvcc'])} / {re_var(d['hvs11'])}
                    - 흉부외과 중환자실 : {re_var(d['hvccc'])} / {re_var(d['hvs16'])}
                    - 일반 중환자실 : {re_var(d['hvicc'])} / {re_var(d['hvs17'])}
                    - 내과 중환자실 : {re_var(d['hv2'])} / {re_var(d['hvs06'])}
                    - 외과 중환자실 : {re_var(d['hv3'])} / {re_var(d['hvs07'])} 
                    - 신경 외과 중환자실 : {re_var(d['hv6'])} / {re_var(d['hvs12'])}
                    - 화상 중환자실 : {re_var(d['hv8'])} / {re_var(d['hvs13'])}
                    - 외상 중환자실 : {re_var(d['hv9'])} / {re_var(d['hvs14'])} 
                ''', unsafe_allow_html=True)

            info_expender.map(pd.DataFrame({'lat': [d['lat']], 'lon': [d['lon']]}))

        
        for d in moon_data:
            moon_emoji, moon_sec = st.columns([5,95])

            moon_emoji.write('🌛')
            info_expender = moon_sec.expander(d['name'])
            if d['info'] != None: info_expender.info(d['info'], icon='❕')
            info_expender.markdown(f'''
                주소 : {d['addr']}  
                전화번호 : {d['tel']}  
                
            ''')
            info_expender.map(pd.DataFrame({'lat': [d['lat']], 'lon': [d['lon']]}))
    return
