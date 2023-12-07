import openai
import glob
import os
import time
# import urllib
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
import streamlit as st


from sender import Sender
from receiver import Receiver

file_list = []

class Sender_Reciver : 
    def __init__(self, 
                 params,
                 local_path,
                 prompt,
                 run_name):
        
        self.params = params
        self.local_path = local_path
        self.prompt = prompt + ' --ar 16:9 --niji 5 -Upscaled (4x)'
        self.run_name = run_name
        self.file_list = []

    def Run_create_image(self):
        sender = Sender(params = self.params)
        sender.send(self.prompt)
        time.sleep(30)
        receiver = Receiver(params = self.params, 
                    local_path = self.local_path, run_name=self.run_name )
        file_name = receiver.main()
        print("파일네임을 생성했습니다.")
        print(file_name)
        return file_name


    def Crop_image(self, file_list): 
        for i,file_name in enumerate(file_list):
            print('인덱스랑 파일네임 ')
            print(i)
            print(file_name)
            
            if len(file_list)==1:
                img_path = os.path.join(self.local_path, str(self.run_name), str(file_name))
                print(img_path)
                img = Image.open(img_path)     
            else : 
                new_file_name = file_list[0]
                img_path = os.path.join(self.local_path, str(self.run_name), str(new_file_name))
                print(img_path)
                img = Image.open(img_path) 
            
            grid_w, grid_h = 1024, 1024    
            range_w, range_h = img.size[0] // grid_w, img.size[1] // grid_h
            for j, (w, h) in enumerate([(w, h) for w in range(range_w) for h in range(range_h)]):
                bbox = (h * grid_h, w * grid_w, (h + 1) * grid_h, (w + 1) * grid_w)         
                crop_img = img.crop(bbox)       
                fname = f"/{self.run_name}_{i}.png"        
                save_name = '/Users/yula0/data_analytics/langchain/fairytale_book/Midjourney_api-main/story-book-runs/'+ self.run_name+ '/' +fname         
                if j ==2 : 
                    crop_img.save(save_name)         
                    print(f"Saved file: {save_name}")

    def Overlaid_image(self,img, overlay_text):
        # 이미지에 텍스트 오버레이
        draw = ImageDraw.Draw(img)
        
        font_size = 100
        font = ImageFont.truetype("arial.ttf", font_size)
        
        
        text_color = "white"  # 텍스트 색상 설정
        text_position = (30, img.height - 900)  # 텍스트 위치 설정
        
        draw.text(text_position, overlay_text, fill=text_color, font=font)
        
        return img
    
    def Create_cover_image(self,story_title):
        local_path = '/Users/yula0/data_analytics/langchain/fairytale_book/Midjourney_api-main/story-book-runs'
        

        image_path = os.path.join(local_path, f"{self.run_name}",f"{self.run_name}_0.png")
        img = Image.open(image_path)
            
        # 오버레이된 이미지 생성
        SR = Sender_Reciver(self.params, self.local_path, self.prompt,self.run_name)
        new_img = SR.Overlaid_image(img, story_title)
        new_img.save(os.path.join(self.local_path, self.run_name,f"{self.run_name}_cover.png"))
        return new_img, local_path    
        

                





def generate_cover_image(run_name, story_title,  art_style, params, local_path):
    
    prompt = f'{run_name} as {art_style} style, {story_title}'
    SR = Sender_Reciver(params, local_path,prompt, run_name)
    file_name = SR.Run_create_image()
    
    print(run_name)
    print(file_name)
    if run_name in file_name : 
        file_list.append(file_name)


    SR.Crop_image(file_list)
