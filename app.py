# 2022-07-17 PinkB가 최초 작성.
# 자유로운 이용과 수정, 재배포가 가능합니다.

import os
import re
import random

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import list

# Initialize App with bot token
# 봇 토큰을 환경변수에서 읽어와서 앱을 초기화합니다.
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Listens to incoming messages that contain "!나오쟝"
# "!나오쟝"을 포함하는 메시지를 인식합니다.
@app.message(re.compile("!나오쟝"))

# 반응하여 메시지를 보냅니다
def message_respond(message, say):
    # 유저의 이름을 보존
    user = message['user']
    # message의 텍스트 값으로부터 최대 4개의 선택지를 읽어들이는 매치 오브젝트를 생성합니다. 4개의 그룹이 생성됩니다
    keyword = re.compile('\!나오쟝\s')
    cmdString = keyword.sub('', message['text'], count=1)

    # 선택지를 포함하는 객체 생성
    question = list.choiceList(re.finditer(r'([\w|\s]+|^\,)+', cmdString))

    if not question.list:
        say('부르셨심니껴? 뭔가 못 정하겠으면 \"!나오쟝 짜장면,짬뽕\"과 같이 말씀해주이소.')
        return

    # 랜덤 값 반환
    say(f'제 생각엔 {question.choiceRand()}이(가) 좋을 것 같심니더.')
    return

# Start App
# 앱 기동
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()