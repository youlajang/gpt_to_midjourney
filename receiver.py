import requests
import json
import time
import pandas as pd
import os
import re
from datetime import datetime
import glob
import argparse
import sys

class Receiver:

    def __init__(self, 
                 params,
                 local_path,
                 run_name):
        
        self.params = params
        self.local_path = local_path
        self.run_name = run_name
        

        self.sender_initializer()

        self.df = pd.DataFrame(columns = ['prompt', 'url', 'filename', 'is_downloaded'])

    
    def sender_initializer(self):

        with open(self.params, "r") as json_file:
            params = json.load(json_file)

        self.channelid=params['channelid']
        self.authorization=params['authorization']
        self.headers = {'authorization' : self.authorization}

    def retrieve_messages(self):
        r = requests.get(
            f'https://discord.com/api/v10/channels/{self.channelid}/messages?limit={50}', headers=self.headers)
        jsonn = json.loads(r.text)
        return jsonn


    def collecting_results(self):
        
        filename = ''
        message_list  = self.retrieve_messages()
        self.awaiting_list = pd.DataFrame(columns = ['prompt', 'status'])
        #print("메시지 리스트 : ", message_list)

        for message in message_list:
            

            if (message['author']['username'] == 'Midjourney Bot') and ( '**' in message['content']) and (message['mentions'][0]['username']=='ori_pputi'):
                
                if len(message['attachments']) > 0:
                    
                    if (message['attachments'][0]['filename'][-4:] == '.png') or ('(Open on website for full quality)' in message['content']):
                        id = message['id']
                        prompt = message['content'].split('**')[1].split(' --')[0]
                        url = message['attachments'][0]['url']
                        filename = message['attachments'][0]['filename']
                        print('파일네임출력')
                        print(filename)
                        

                        if id not in self.df.index:
                            self.df.loc[id] = [prompt, url, filename, 0]
                        
                        return filename

                    else:
                        id = message['id']
                        print('숫자3')
                        prompt = message['content'].split('**')[1].split(' --')[0]
                        if ('(fast)' in message['content']) or ('(relaxed)' in message['content']):
                            try:
                                status = re.findall("(\w*%)", message['content'])[0]
                            except:
                                status = 'unknown status'
                        self.awaiting_list.loc[id] = [prompt, status]
                        return status
                        

                else:
                    print('숫자4')
                    id = message['id']
                    prompt = message['content'].split('**')[1].split(' --')[0]
                    if '(Waiting to start)' in message['content']:
                        status = 'Waiting to start'
                    return id
                        
            # else : 
            #     print('숫자5')
        
    
        

                    
    
    def outputer(self):
        if len(self.awaiting_list) > 0:
            print(datetime.now().strftime("%H:%M:%S"))
            print('prompts in progress:')
            print(self.awaiting_list)
            print('=========================================')

        waiting_for_download = [self.df.loc[i].prompt for i in self.df.index if self.df.loc[i].is_downloaded == 0]
        if len(waiting_for_download) > 0:
            print(datetime.now().strftime("%H:%M:%S"))
            print('waiting for download prompts: ', waiting_for_download)
            print('=========================================')

    def downloading_results(self):
        processed_prompts = []
        for i in self.df.index:
            if self.df.loc[i].is_downloaded == 0:
                response = requests.get(self.df.loc[i].url)
                local_path = os.path.join(self.local_path,self.run_name)
                os.makedirs(local_path, exist_ok=True)
                with open(os.path.join(local_path, self.df.loc[i].filename), "wb") as req:
                    req.write(response.content)
                self.df.loc[i, 'is_downloaded'] = 1
                print('셀프 데이터 프레임 다운로드 확인')
                print(local_path + '/' + self.df.loc[i].filename)
                processed_prompts.append(self.df.loc[i].prompt)
        if len(processed_prompts) > 0:
            print(datetime.now().strftime("%H:%M:%S"))
            print('processed prompts: ', processed_prompts)
            print('=========================================')
            
  
    def main(self):
        file_name = ''
        k =True
        while k:
            file_name = self.collecting_results()
            # self.outputer()
            # self.downloading_results()
            time.sleep(5)
            
            print('파일찾기중....')
            print("런네임 : ",self.run_name)
            print("파일네임 : ", file_name)
            
            if (str(self.run_name) in file_name) :
                print('파일 리스트 서치 끝 ')
                self.outputer()
                self.downloading_results()
                k=False
                return file_name
            
                
            
            

# def parse_args(args):
    
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--params',        help='Path to discord authorization and channel parameters', required=True)
#     parser.add_argument('--local_path',           help='Path to output images', required=True)
#     parser.add_argument('--prompt',required=True)
#     print("작동")
#     return parser.parse_args(args)


# if __name__ == "__main__":

#     args = sys.argv[1:]
#     args = parse_args(args)
#     print("args프린트", args)
#     params = args.params
#     local_path = args.local_path
#     prompt = args.prompt
#     print("로컬패스",local_path)
#     print('=========== listening started ===========')
#     receiver = Receiver(params, local_path,prompt )
#     receiver.main()