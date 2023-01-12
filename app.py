# 2022-07-17 PinkB가 최초 작성.
# 자유로운 이용과 수정, 재배포가 가능합니다.

import os
import re

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import list
import sp
import korean
import strCommon
import container

# Initialize App with bot token
# 봇 토큰을 환경변수에서 읽어와서 앱을 초기화합니다.
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

singleSpObj  = sp.singleSp(f"sp/singleSp.json")
forceSpObj   = sp.forceSp(f"sp/forceSp.json")
passiveSpObj = sp.forceSp(f"sp/passiveSp.json")

smootherObj = korean.Smoother(f"korean/smoother.json")
containerObj = container.Container()


# Listens to incoming messages that contain "!나오쟝"
# "!나오쟝"을 포함하는 메시지를 인식합니다.
@app.message(re.compile("!나오쟝"))

# 반응하여 메시지를 보냅니다
def message_respond(message, say):
    print("receiving!")

    # uid 취득
    user = message['user']

    # message의 텍스트 값으로부터 최대 4개의 선택지를 읽어들이는 매치 오브젝트를 생성합니다. 4개의 그룹이 생성됩니다
    keyword = re.compile('\!나오쟝')
    cmdString = keyword.sub('', message['text'], count=1)

    # 공백제거
    cmdString = strCommon.stripAll(cmdString)

    if not cmdString:
        sayGuide(say)
        return True

    # 선택지를 포함하는 객체 생성
    question = list.ChoiceList(re.finditer(r'(?:([^\,]*),?)', cmdString))

    # 랜덤 처리 전, 특정 패턴을 검사한다.
    if saySp(say,singleSpObj,question.list,message):
        return True
    elif saySp(say,forceSpObj,question.list,message):
        return True

    # 특정 패턴에 매치하지 않았을 경우, 리스트의 길이가 2 미만일 때 안내 메시지 출력
    if len(question.list) < 2:
        sayGuide(say)
        return True
    
    # 랜덤 값 생성
    answer = question.choiceRand()
    # 공백제거
    answer = strCommon.stripAll(answer)

    # 답변한 값을 container 오브젝트에 보존
    containerObj.addA(user,answer)

    # 질문 목록을 container 오브젝트에 보존
    # 무작위 답을 구하지 않는 질문의 경우 질문을 저장하지 않음
    containerObj.addQ(user, question)

    # 랜덤 값 전달 전 특정 패턴 검사
    if saySp(say,passiveSpObj,[answer],message):
        return True
    else:        
        # 랜덤 값 전달
        answer = combineAnswer(answer)
        say(answer)
        return True

# 특수 패턴 출력 함수
def saySp(say,spObj,choiceList,message):
    value = spObj.search(choiceList)

    value = runSingleSp(value,choiceList,message)
    if value:
        say(value)
        return True
    else:
        return False

def runSingleSp(value,choiceList,message):
    # choiceelse (딴거 선택) singeSp 메서드 실행
    if value == "@selectelse":
        user = message['user']
        try:
            value = containerObj.selectelse(user)
            value = combineAnswer(value)
        except KeyError or ValueError:
            value = '죄송한데예, 뭐라 하셨는지 까먹어뿟심다'
    else:
        pass
    return value

def sayGuide(say):
    # 답변할 수 있는 질문이 아닐 때 출력하는 기본 메시지이다.
    say('부르셨심니껴? 뭔가 못 정하겠으면 \"!나오쟝 짜장면,짬뽕\"과 같이 말씀해주이소.')
    return True

def combineAnswer(answer):
    # 주 답변 내용의 앞 뒤는 일단 보류한다
    prephrase = '제 생각엔'

    # Smoother 오브젝트의 메서드 .convert() 실행하여
    # 부드럽게 다듬기 알맞은 문자열이 포함되어있는지, 검색하고 변환한다
    mainAnswer = smootherObj.convert(answer)
    postphrase = ''

    # 만일 변환한 내용이 없다면 기본적인 조사처리만 한다
    if mainAnswer is False:
        mainAnswer = f'{answer}{korean.post(answer)}'
        postphrase = '맞는 것 같심니더.'

    fused = f'{prephrase} {mainAnswer} {postphrase}'
    # 조합한 문장을 반환
    return fused

# Start App
# 앱 기동
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()