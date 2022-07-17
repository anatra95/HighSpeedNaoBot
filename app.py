# 2022-07-17 PinkB가 작성함.
# 자유로운 이용과 수정, 재배포가 가능합니다.

import os
import re
import random

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

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
    matchObj = re.search('\!나오쟝\s(\S*)\s(\S*)\s?(\S*)?\s?(\S*)?', message['text'])

    print(f"starting read each match of matchObj ({matchObj})")

    if not matchObj:
        say('부르셨심니껴? 뭔가 못 정하겠으면 \"!나오쟝 짜장면 짬뽕\"과 같이 말씀해주이소.')
        return

    # 빈 문자열이 아닌 그룹의 갯수를 세어 matchCount에 저장합니다.    
    matchCount = 0
    for i in range(1, 5):
        if matchObj.group(i) != '':
            matchCount = min(matchCount + 1, 4)
        else:
            print(f'Oops! match string ({matchObj.group(i)}) ({i}) is empty')

    if matchCount < 2:
        # 2개 미만의 그룹이 발견된 경우, 랜덤값을 출력할 수 없습니다.
        say(f'오류가 발생했습니다, <@{user}>! \
            필요한 수에 미달하는 매치 ({matchCount}) 가 발견되었습니다.\
            \n\"!나오쟝 짜장면 짬뽕\"과 같은 형태로 말해주이소. 4개까지니깐요.')
    else:
        # 랜덤값을 출력합니다.
        answer = matchObj.group(random.randrange(1,matchCount + 1))
        say(f'제 생각엔 {answer}이(가) 좋을 것 같심니더.')
    return

# Start App
# 앱 기동
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()