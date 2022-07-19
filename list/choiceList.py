import random

# sre.match Object를 요소로 포함시킨다
class choiceList:
    def __init__(self, iter):
        # 객체 생성 시, iterator를 요구한다. (re.finditer()로 생성한 것)
        # iterator의 문자열 요소를 포함하는 리스트를 보존한다.
        self.list = []

        for m in iter:
            if m.group(1) != '':
                self.list.append(m.group(1))

    # 제외할 선택지를 전달하면 그것을 제외하고 다시 결정한다.
    def choiceRand(self, *args):
        # 차집합을 구해서 임시 리스트 생성
        tempList = list(set(self.list)
                        - set(args))
        # 임시 리스트에서 랜덤한 값을 반환
        randKey = random.randrange(0,len(tempList))
        return tempList[randKey]