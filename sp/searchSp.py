# 특정 패턴과 매치할 경우

import json

# 특정 패턴에 일치하면 특수 답변을 전달하는 기능 - 부모 클래스
class Sp:
    def __init__(self, filepath):
        # json 데이터 생성 후 보존
        f = open(filepath, encoding="UTF-8")
        self.jsonData = json.loads(f.read())

    # 검색 메서드
    def search(self, choiceList):

        # 우선도를 계산하기 위한 반복문
        for j in range(0,4):
            # jsonData 내부를 검색하는 반복문
            for i in self.jsonData:

                # 현재 검색 중인 우선도가 아니라면 넘긴다
                if self.jsonData[i]["priority"] != j:
                    continue

                # 교집합의 리스트 생성
                comparisonList = list(set(self.jsonData[i]["key"]).intersection(choiceList))
                # 교집합이 존재한다면 특수 답변 전달
                if comparisonList:
                    return self.jsonData[i]["answer"]
        return

class singleSp(Sp):
    pass
class forceSp(Sp):
    pass
class passiveSp(Sp):
    pass