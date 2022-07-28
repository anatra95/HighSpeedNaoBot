import re

# (이, 가)의 쌍만 우선 구현한다
def post(string):
    temp = ''
    if re.match('[ㄱ-힣]',string[-1:]) is None:
        # 숫자로 끝나는 정규식 패턴 매칭
        m = re.search(r'([\d]+$)', string)

        # m[0]가 참인 경우 한국어 한글 표기로 변환해 보존
        if m != None:
            k = inttoko(m.group(1))
        else:
            return '이(가)'
    else:
        k = string

    # 한글 표기의 종성 확인
    if getFinalConsonant(k[-1:]) == ' ':
        return '가'
    else:
        return '이'

# 한글의 종성 획득
def getFinalConsonant(c):
    INITIAL_CODE, FINAL_NUM = 0xAC00, 28
    FINAL_LIST =   [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ',
                    'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    if re.match('[가-힣]', c) is not None:
        return FINAL_LIST[(ord(c) - INITIAL_CODE) % FINAL_NUM]
    elif re.match('[ㄱ-ㅎ]', c) is not None:
        return c
    else:
        return ''

# 정수를 한국어 한글 표기로 변환
def inttoko(i):
    # 숫자의 한글 표기
    num_ko         = ('', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구')
    # 반복되는 자리수 표기
    digit_ko_small = ('', '십', '백', '천')
    # 큰 수의 자리 표기
    digit_ko_big   = {0: '', 4: '만', 8: '억', 12:'조', 16:'경', 20: '해', 24: '자',
                      28: '양', 32: '구', 36: '간', 40: '정', 44: '재', 48: '극', 52: '항하사',
                      56: '아승기', 60: '나유타', 64: '불가사의', 68: '무량대수'}
    # 자리 수로 슬라이싱하기 위해 숫자를 문자열으로 형변환
    s = str(i)

    # 반환하는 문자열
    r = ''

    # 0은 따로 예외로 보낸다
    if s == '0':
        return '영'

    # 백만삼십만 과 같은 모양을 방지하는 기록 변수
    big_key_log = 0

    # 주 반복문
    for c in range(len(s)-1, -1, -1):
        # 각 자리수마다 추가하는 문자열의 임시값 초기화
        temp = ''
        # 해당 자리수가 0이면 읽지 않는다
        if s[c] == '0':
            continue
        else:
            # n은 반복문 카운터 c에 해당하는 자리수의 숫자
            n = int(s[c])
            # digit은 c로 생성한 인간이 바로 읽을 수 있는 자리 수
            digit = len(s) - c
            # 자리 수가 10^68를 초과하지 않는다면......
            if n <= 68:
                if n == 1 and digit != 1:
                    pass
                else:
                    temp += num_ko[n]
                temp += digit_ko_small[(digit - 1) % 4]
                
                big_key = (digit - 1) // 4 * 4
                if big_key in digit_ko_big and big_key != big_key_log:
                    temp += digit_ko_big[(digit - 1) // 4 * 4]
                    big_key_log = big_key
            # 무량대수보다 크면 뱉는다
            else:
                print("큰 수 표기 중 범위를 벗어난 오류!")
                return
        r = temp + r

    return r