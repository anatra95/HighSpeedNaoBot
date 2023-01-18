# 사용자 입력 및 봇의 결정을 기록하기 위한 용도의 컨테이너 클래스
class Container:
    def __init__(self):
        self.questionDictionary = {}
        self.answerDictionary = {}
        # 각각 마지막 질문 리스트와 마지막 답변을 저장한다
        # 양쪽 다 사용자 이름을 key로 한다

    # 
    def addQ(self, user, choicelist):
        self.questionDictionary[user] = choicelist
    
    def addA(self, user, answer):
        self.answerDictionary[user] = answer

    def getQ(self, user):
        return self.questionDictionary[user]
    
    def getA(self, user):
        return self.answerDictionary[user]

    # selectelse, 딴거 골라줘 라는 기능을 구현하기 위한 목적의 메서드
    def selectelse(self,user):
        question = self.getQ(user)

        try:
            question.list.remove(self.getA(user))
        except:
            pass
        
        try:
            answer = question.choiceRand()
            self.addA(user,answer)
        except ValueError:
            answer = "@noanswerremains"

        return answer