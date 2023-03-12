import smtplib
from email.message import EmailMessage

# STMP 서버의 url과 port 번호
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465

# 1. SMTP 서버 연결
smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)

EMAIL_ADDR = '' # 깃허브에 공개했다가 누가 사용하려는 악성 접근이 있어서 비공개 처리
EMAIL_PASSWORD = '' # 깃허브에 공개했다가 누가 사용하려는 악성 접근이 있어서 비공개 처리

# 2. SMTP 서버에 로그인
smtp.login(EMAIL_ADDR, EMAIL_PASSWORD)

def send_email(team, sid, name, to_email, handle_id, handle_pw, competition_name):
    # 3. MIME 형태의 이메일 메세지 작성
    message = EmailMessage()
    message["Subject"] = "[ChAOS] %s 출석 확인 및 백준 핸들(계정)" %competition_name # 이메일 제목
    message["From"] = EMAIL_ADDR  #보내는 사람의 이메일 계정
    message["To"] = to_email # 받는 사람의 이메일 계정

    content = """
%s 출석 확인 메일입니다.
팀명: %s 
학번: %s 
이름: %s

대회에서 사용할 백준 핸들(계정)은 다음과 같습니다.
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
ID: %s
PW: %s
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯""" % (competition_name, team, sid, name, handle_id, handle_pw)

    message.set_content(content) # 이메일 본문

    # 4. 서버로 메일 보내기
    smtp.send_message(message)