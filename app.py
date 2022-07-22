# 2022-07-17 PinkB가 최초 작성.
# 자유로운 이용과 수정, 재배포가 가능합니다.

import os
import re

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import list
import sp

# Initialize App with bot token
# 봇 토큰을 환경변수에서 읽어와서 앱을 초기화합니다.
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

singleSpObj  = sp.singleSp(f"sp/singleSp.json")
forceSpObj   = sp.forceSp(f"sp/forceSp.json")
passiveSpObj = sp.forceSp(f"sp/passiveSp.json")
# Listens to incoming messages that contain "!나오쟝"
# "!나오쟝"을 포함하는 메시지를 인식합니다.
@app.message(re.compile("!나오쟝"))

# 반응하여 메시지를 보냅니다
def message_respond(message, say):
    # 유저의 이름을 보존
    user = message['user']
    # message의 텍스트 값으로부터 최대 4개의 선택지를 읽어들이는 매치 오브젝트를 생성합니다. 4개의 그룹이 생성됩니다
    keyword = re.compile('\!나오쟝')
    cmdString = keyword.sub('', message['text'], count=1)

    while cmdString[0] == ' ':
        cmdString = cmdString.lstrip()

    # 선택지를 포함하는 객체 생성
    question = list.ChoiceList(re.finditer(r'(?:([^\,]*),?)', cmdString))


    # 랜덤 처리 전, 특정 패턴을 검사한다.
    if saySp(say,singleSpObj,question.list):
        return True
    elif saySp(say,forceSpObj,question.list):
        return True

    # 특정 패턴에 매치하지 않았을 경우, 리스트의 길이가 2 미만일 때 안내 메시지 출력
    if len(question.list) < 2:
        say('부르셨심니껴? 뭔가 못 정하겠으면 \"!나오쟝 짜장면,짬뽕\"과 같이 말씀해주이소.')
        return True
    
    # 랜덤 값 생성
    answer = question.choiceRand()
    # 랜덤 값 전달 전 특정 패턴 검사
    if saySp(say,passiveSpObj,[answer]):
        return True
    # 랜덤 값 전달
    say(f'제 생각엔 {answer}이(가) 좋을 것 같심니더.')
    return True

# 특수 패턴 출력 함수
def saySp(say,spObj,choiceList):
    value = spObj.search(choiceList)
    if value:
        say(value)
        return True
    else:
        return False

# Start App
# 앱 기동
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()