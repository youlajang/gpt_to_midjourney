
from create_prompt import *
from create_img import *
import create_img as ci
from create_pdf import * 
import streamlit as st
import time
    

def main():
    st.title("동화 만들기!!")
    
    nickname = st.text_input("사용할 닉네임을 영문으로 입력하세요:",placeholder='ex:olivia')
    story_page = ""
    
    num_characters = st.number_input("원하는 스토리의 주인공 수를 입력하세요:", min_value=1, max_value = 4, step=1)
    
    characters_list = []  
    character_info = {}
    for i in range(num_characters):

        st.subheader(f"주인공 {i+1} 정보를 입력하세요")
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
    params ='/Users/yula0/data_analytics/langchain/fairytale_book/Midjourney_api-main/sender_params.json'
    #folder of saved image
    local_path = '/Users/yula0/data_analytics/langchain/fairytale_book/Midjourney_api-main/discord_images/'
    #run_name : using foler name & image file name
    run_name = nickname + str(int(time.time()))
    # Get the number of main characters from the user
    num_main_characters = num_characters    
    art_style = 'cute illustration '  
    
    if st.button("동화 생성"):
        # Create the story prompt
        story_prompt = Create_book.create_story_prompt(num_main_characters, characters_list,story)
        #create story
        story_title, story_full_text,character_summary = Create_book.create_story(run_name,story_prompt,art_style)

        #create images
        print('표지 제작중')
        with st.spinner('표지제작중...'):
            generate_cover_image(run_name, story_title, art_style, params, local_path)
        
        st.success('표지 제작 완성!')
        
        story_title = Create_book.transrate_text(story_title, n=1)
        SR = Sender_Reciver(params, local_path, story_title,run_name)
        cover_img, image_path = SR.Create_cover_image(story_title)
        story_full_text = Create_book.transrate_text(story_full_text,n=2)
        st.subheader("동화가 만들어 졌습니다!")
        # 오버레이된 이미지 출력
        st.image(cover_img, caption='표지', use_column_width=True)
        st.write(story_full_text)
        #Generate_PDF(story_full_text, image_path)
        if st.button("PDF로 저장"):
            generated_pdf = create_pdf(image_path, story_full_text)
            with open(generated_pdf, "rb") as pdf_file:
                st.download_button(label="Download PDF", data=pdf_file, file_name="Mystory.pdf", mime="application/pdf")


       
 



if __name__ == "__main__":
    main()
    





