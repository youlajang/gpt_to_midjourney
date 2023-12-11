
from create_prompt import *
from create_img import *
from create_pdf import * 
import streamlit as st

import time

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet


from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import os

def main():
    st.title("	:ribbon: :rainbow[동화] 만들기!!:ribbon:")
    
    nickname = st.text_input("사용할 닉네임을 영문으로 입력하세요:",placeholder='ex:olivia')
    story_page = ""
    
    num_characters = st.number_input("원하는 스토리의 주인공 수를 입력하세요:", min_value=1, max_value = 4, step=1)
    
    characters_list = []  
    character_info = {}
    for i in range(int(num_characters)):

        st.subheader(f"주인공 {i+1} 정보를 입력하세요 :lower_left_ballpoint_pen:")
        #gender = st.selectbox("성별을 선택하세요:", ("남자", "여자"), key=f"gender_{i}")
        if i ==0 :
            gender1 = st.radio(label = '성별을 입력하세요', options = ['남자', '여자'], key="gender_1")
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            # character_gender[i] = st.text_input("성별을 입력하세요(예: 남자/여자):")
            name1 = st.text_input("이름을 입력하세요:", key="name_1")
            character_info = {
            '성별': gender1,
            '이름': name1
            }
            characters_list.append(character_info)
            # name = st.text_input("이름을 입력하세요:",key=f"name_{i}")
        if i ==1 :
            gender2 = st.radio(label = '성별을 입력하세요', options = ['남자', '여자'], key="gender_2")
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            # character_gender[i] = st.text_input("성별을 입력하세요(예: 남자/여자):")
            name2 = st.text_input("이름을 입력하세요:", key="name_2")
            character_info = {
            '성별': gender2,
            '이름': name2
            }
            characters_list.append(character_info)
        if i ==2 :
            gender3 = st.radio(label = '성별을 입력하세요', options = ['남자', '여자'], key="gender_3")
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            # character_gender[i] = st.text_input("성별을 입력하세요(예: 남자/여자):")
            name3 = st.text_input("이름을 입력하세요:", key="name_3")
            character_info = {
            '성별': gender3,
            '이름': name3
            }
            characters_list.append(character_info)
        if i ==3:
            gender4 = st.radio(label = '성별을 입력하세요', options = ['남자', '여자'], key="gender_4")
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            # character_gender[i] = st.text_input("성별을 입력하세요(예: 남자/여자):")
            name4 = st.text_input("이름을 입력하세요:", key="name_4")
            character_info = {
            '성별': gender4,
            '이름': name4
            }
            characters_list.append(character_info)
 

    story = st.text_area("원하는 스토리를 입력하세요:", 
                         placeholder='ex: 못생긴 데니와 장난끼 많은 소피아의 로미오와 줄리엣 같은 이룰수 없는 사랑이야기.')
    
    #midjourney_api info
    params ='sender_params.json'
    #folder of saved image
    
    local_path = './discord_images/'
    os.makedirs(local_path, exist_ok=True)
    #run_name : using foler name & image file name
    run_name = nickname + str(int(time.time()))
    # Get the number of main characters from the user
    num_main_characters = num_characters    
    art_style = 'cute illustration '  
    
    if st.button("동화 생성"):
        # Create the story prompt
        story_prompt = Create_book.create_story_prompt(num_main_characters, characters_list,story)
        #create story
        story_title, story_full_text = Create_book.create_story(run_name,story_prompt,art_style)

        #create images
        print('표지 제작중')
        with st.spinner('표지제작중...'):
            generate_cover_image(run_name, story_title, art_style, params, local_path)
        
        st.success('표지 제작 완성!')
        with st.spinner("동화 제작중..."):
            story_title = Create_book.transrate_text(story_title, n=1)
            SR = Sender_Reciver(params, local_path, story_title,run_name)
            cover_img, image_path = SR.Create_cover_image(story_title)
            story_full_text = Create_book.transrate_text(story_full_text,n=2)
            st.subheader(":rainbow[동화]가 만들어 졌습니다!&mdash;\:tulip:")
            # 오버레이된 이미지 출력
            st.image(cover_img, caption='표지', use_column_width=True)
            st.write(story_full_text)
        with st.spinner("pdf제작중..."):
            pdf_buffer = BytesIO()
            #==================================================
            font_path = "./NanumGothic-Regular.ttf"  # 폰트 파일의 경로를 설정!
            pdfmetrics.registerFont(TTFont("NanumGothic-Regular", font_path))  # 한글 폰트 등록
            # Add story text to PDF
            styles = getSampleStyleSheet()
            style = styles["Normal"]
            style.wordWrap = 'CJK'
            style.fontName = "NanumGothic-Regular"  # 한글 폰트 적용
            #==================================================
            style.fontSize = 16  # 적절한 크기로 조절
            style.leading = style.fontSize * 2  # 더블 스페이스
            #========================


        
            # 이미지를 먼저 불러와서 cover_img에 저장
            cover_img_data = open(image_path + '/' + run_name + '/' + run_name + '_cover.png', 'rb').read()
            cover_img = Image(BytesIO(cover_img_data), width=456.0, height=636.0)  # 이미지 크기 조절
    
            # 텍스트를 파라그래프로 변환
            story_paragraphs = []
            story_paragraphs.append(cover_img)
    
            # 텍스트를 줄 단위로 파싱하고, 각 줄을 파라그래프로 추가
            story_full_text = Create_book.transrate_text(story_full_text, n=2)
            for para in story_full_text.split('\n'):
                story_paragraphs.append(Paragraph(para, style))
    
            # PDF를 생성하고 이미지와 텍스트를 추가
            pdf_buffer = BytesIO()
            pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
            pdf.build(story_paragraphs)
    
        # PDF 생성 완료 메시지 출력
        st.success('PDF 생성 완료!')
    
        # Add a download button for the PDF
        st.download_button("PDF 저장", pdf_buffer.getvalue(), file_name=f"{run_name}_Myfairytale_book.pdf", key="download_button")
            #==================================================


if __name__ == "__main__":
    main()
    




