from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt



from io import BytesIO
import streamlit as st


def register_korean_font():
    font_path = "./NanumGothic-Regular.ttf"  # 폰트 파일의 경로를 설정!
    pdfmetrics.registerFont(TTFont("NanumGothic-Regular", font_path))


# 이미지와 텍스트 정보
image_path = "./"  # 이미지 파일 경로

# PDF 생성 함수
def create_pdf(story_full_text, image_path):
    # PDF 생성
    pdf_filename = "Mystory.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    register_korean_font()  # 한글 폰트 등록
    
    # 이미지 추가
    img = Image.open(image_path)
    c.drawImage(image_path, 100, 400,width=700)  # 이미지 위치 및 크기 조절
    
    # 텍스트 추가
    c.drawString(100, 300, story_full_text)  # 텍스트 위치 조절
    
    c.save()
    return pdf_filename





# Generate PDF
def Generate_PDF(story_full_text, image_path):
    pdf_buffer = BytesIO()
    register_korean_font()  # 한글 폰트 등록
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.wordWrap = 'CJK'
    style.fontName = "NanumGothic-Regular"  # 한글 폰트 적용
    story = []
            
    # Adding cumulative answers to the PDF
    story.append(Paragraph("동화", styles['Title']))
    story.append(Spacer(1, 12))
    cover_image = Image.open(image_path)
    story.append(image_path, 100, 400,width=700)

    cover_image = Image(cover_image, width=300, height=300)
    #cover_image = Image.open(image_path)
    story.append(cover_image)

    paragraph = Paragraph(story_full_text, style)
    story.append(paragraph)
    story.append(Spacer(1, 12))
    

    # Save the PDF
    pdf.build(story)

    # Download the PDF
    st.download_button("PDF 저장", pdf_buffer.getvalue(), file_name="Myfairytale_book.pdf")

    