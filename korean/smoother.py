import json
import re

# 답변 생성 중, 한국어 표현을 보다 정교하게 다듬어 자연스럽게 하는 기능
# ex) 먹을까, 말까 -> 먹을까가 좋을 것 같습니다x 먹는 게 좋을 것 같습니다o
class Smoother:
    def __init__(self,filepath):
        f = open(filepath, encoding="UTF-8")
        self.jsonData = json.loads(f.read())

    # 검색 및 변환 메서드
    # 변환은 json 데이터에 쓰여진 대로 한다
    def convert(self, answer):

        for i in self.jsonData:
        
            for j in self.jsonData[i]["key"]:
                # r".*먹을까\Z"와 같은 정규식 패턴 생성
                pattern = r".*" + re.escape(j) + r"\?*\Z"
                m = re.match(pattern, answer)
                if bool(m):
                    # 매치하는 경우, 매치한 key 부분을
                    # smoothen으로 치환하여 반환한다
                    newAnswer = answer.replace(j, self.jsonData[i]["smoothen"])
                    return newAnswer
                else:
                    continue
        
        # 매치하는 결과가 없는 경우 False를 리턴하여,
        # 기본적인 조사처리만 실행
        return False