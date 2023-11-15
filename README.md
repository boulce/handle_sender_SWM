# Handler Sender 프로젝트


- 중앙대학교 알고리즘 동아리 ChAOS에서 대회를 운영하며 겪은 문제점에서 진행한 프로젝트
- 대회 현장에 출석한 참가자들에게 대회용 계정(핸들)을 이메일로 전송합니다.

# 변수 설정


1. main.py 내에 STMP 서버 및 이메일 정보를 입력합니다.

```python
# STMP 서버의 url과 port 번호
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465

```python
EMAIL_ADDR = '' # 이메일 주소
EMAIL_PASSWORD = '' # 이메일 비밀번호
```

2. mysql.py 내에 DB 정보를 입력합니다.

```python
con = pymysql.connect(host='', # 호스트 입력
                    user='', # 유저네임 입력
                    password='', # 암호 입력
                    db='', # 접속할 DB 입력
                    charset='utf8', # 한글처리 (charset = 'utf8')
                    cursorclass=pymysql.cursors.DictCursor)
```

# 실행 방법

1. 다음과 같은 모듈을 설치합니다.

```
pip install tkinter
pip install mysql
pip install pymysql
```

1. 실행 파일을 만들기 위한 모듈을 설치합니다.

```
pip install pyinstaller
```

2. 다음 명령어를 통해 실행파일을 만듭니다.

```jsx
pyinstaller --noconsole --onefile gui.py
```

3. dist 디렉토리 안에 생성된 실행파일을 실행합니다.
