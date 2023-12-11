# Midjourney_api
비공식 Midjourney API
# sample url : https://myjourneystory-yula0910.streamlit.app/

이것은 맞춤형 Midjourney API입니다. 이를 사용하면 코드로 이미지를 생성할 수 있습니다. Discord API 작업 중입니다.

!! Modjourney TOS는 자동화를 허용하지 않으므로 이 프로젝트는 연구 목적으로만 사용된다는 점을 잊지 마세요!!

다음을 포함합니다:
- 발신자: Midjourney에게 메시지를 보내기 위해
- 수신기: 터미널에서 작동하며 완성된 모든 이미지를 로컬 폴더에 다운로드합니다.

설치:
1. Discord 계정을 생성하고 서버를 생성하세요(지침: https://discord.com/blog/starting-your-first-discord-server)
2. Midjourney 계정을 생성하고 Midjourney Bot을 서버에 초대합니다(지침: https://docs.midjourney.com/docs/invite-the-bot).
3. 서버에서 생성이 작동하는지 확인하세요.
4. Chrome 브라우저에서 Discord에 로그인하고 서버의 텍스트 채널을 열고 오른쪽 상단 모서리에 있는 세 점을 클릭한 다음 추가 도구, 개발자 도구를 차례로 클릭하세요.
네트워크 탭을 선택하면 페이지의 모든 네트워크 활동이 표시됩니다.
5. 이제 텍스트 채널에 생성할 프롬프트를 입력하고 Enter를 눌러 프롬프트가 포함된 메시지를 보내면 네트워크 활동에 "interaction"이라는 새 줄이 표시됩니다.
이를 누르고 Payload 탭을 선택하면 payload_json이 표시됩니다. 이것이 바로 우리에게 필요한 것입니다!
Channelid, application_id, guild_id, session_id, version 및 id 값을 복사하세요. 잠시 후에 필요합니다.
그런 다음 페이로드 탭에서 헤더 탭으로 이동하여 "인증" 필드를 찾아 해당 값도 복사합니다.
6. 이 저장소를 복제하세요.
7. "sender_params.json" 파일을 열고 5항의 모든 값을 여기에 입력합니다. 또한 프롬프트에 특수 플래그를 지정하려면 '플래그' 필드를 입력하세요.
8. 이제 파일을 실행할 준비가 되었습니다.
- 수신자 스크립트를 시작하려면 터미널을 열고 다음을 입력하세요.
파이썬 /path/to/cloned/dir/receiver.py --params /path/to/cloned/dir/sender_params.json --local_path '/path/to/folder/for/downloading/images'
이 스크립트는 모든 생성 진행 상황을 표시하고 이미지가 준비되는 즉시 이미지를 다운로드합니다.
- 생성 프롬프트를 보내려면 다른 터미널을 열고 다음을 입력하세요.
python //path/to/cloned/dir/sender.py --params /path/to/cloned/dir/sender_params.json --prompt '여기에 프롬프트'
9. 즐겨보세요 :)

병렬 요청 수를 제어하십시오. 일반적이고 가장 빠른 작업의 경우 3(기본 및 표준 계획에서는, Pro 계획에서는 12)보다 크지 않아야 합니다.


프로젝트 코멘트:

이것은 깃허브의Midjourney_api-main 파일을 참고하여 만들었습니다.

Contacts:

For proposals and cooperation:
email: Dev.youlajang@gmail.com

