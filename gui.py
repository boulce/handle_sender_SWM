from mail import *
from tkinter import * 
from tkinter import ttk
import threading
import mysql
import csv
import os, sys

tot_cnt = 0; attendant_cnt = 0

window = Tk()

window.title("ChAOS Handle Sender")
window.geometry("1190x830+170+70")
window.resizable(False, False)

# 상단 프레임
top_frame = Frame(window)
top_frame.pack(fill="both", padx=10, pady=10)

top_frame_left = Frame(top_frame, width=200)
top_frame_left.pack(side=LEFT, expand=True,fill="both")

top_frame_center = Frame(top_frame)
top_frame_center.pack(side=LEFT, expand=True, fill="both")

top_frame_right = Frame(top_frame, width=200)
top_frame_right.pack(side=LEFT, expand = True,fill="both")

# 상단 프레임 내부 위젯
participant_label = Label(top_frame_center, text="<참가자 명단>")
participant_label.pack()

competition_name = ""
def apply_competition_name_btn():
    global competition_name
    new_name = competition_name_entry.get()
    if(new_name != competition_name):
        mysql.apply_competition_name(competition_name, new_name)
        competition_name = new_name
    
def apply_competition_name_thread():
    t = threading.Thread(target = apply_competition_name_btn)
    t.start()


competition_name_btn = Button(top_frame_right, text="적용", width=1, command=apply_competition_name_thread)
competition_name_btn.pack(side=RIGHT)

competition_name_entry = Entry(top_frame_right, width = 15, justify="center")
competition_name_entry.pack(side=RIGHT)

competition_name_label = Label(top_frame_right, text="대회명")
competition_name_label.pack(side=RIGHT)

# 참가자 명단프레임
participant_frame = Frame(window, padx = 10)
participant_frame.pack(fill="both")


#treeview
columns = ["team", "sid", "name", "email", "attendance", "handle_id", "handle_pw"]
treeview = ttk.Treeview(participant_frame, 
    column= columns,  height = 30, show='headings')

#scroll_bar
scroll_bar = Scrollbar(participant_frame, command=treeview.yview, orient=VERTICAL)
scroll_bar.pack( side = RIGHT, fill = Y )

#treeview 칼럼 설정
treeview.pack(fill = BOTH)
treeview.config( yscrollcommand = scroll_bar.set )
treeview.column("team", width=55, anchor="center")
treeview.heading("team", text="팀명", anchor="center")

treeview.column("sid", width=100, anchor="center")
treeview.heading("sid", text="학번", anchor="center")

treeview.column("name", width=100, anchor="center")
treeview.heading("name", text="이름", anchor="center")

treeview.column("email", width=150, anchor="center")
treeview.heading("email", text="이메일", anchor="center")

treeview.column("attendance", width=30, anchor="center")
treeview.heading("attendance", text="출석", anchor="center")

treeview.column("handle_id", width=120, anchor="center")
treeview.heading("handle_id", text="핸들 ID", anchor="center")

treeview.column("handle_pw", width=120, anchor="center")
treeview.heading("handle_pw", text="핸들 PW", anchor="center")

#label
participant_label = Label(window, text="<참가자 추가>")
participant_label.pack(pady=5)

# 참가자 추가 프레임 ###############
add_frame = Frame(window, padx = 10)
add_frame.pack(fill="both")

label_team = Label(add_frame, text="팀명")
label_team.pack(side=LEFT)

entry_team = Entry(add_frame, width = 15, justify="center")
entry_team.pack(side=LEFT)

label_sid = Label(add_frame, text="학번")
label_sid.pack(side=LEFT)

entry_sid = Entry(add_frame, width = 8, justify="center")
entry_sid.pack(side=LEFT)

label_name = Label(add_frame, text="이름")
label_name.pack(side=LEFT)

entry_name = Entry(add_frame, width = 7, justify="center")
entry_name.pack(side=LEFT)

label_email = Label(add_frame, text="이메일")
label_email.pack(side=LEFT)

entry_email = Entry(add_frame, width = 20, justify="center")
entry_email.pack(side=LEFT)

label_handleID = Label(add_frame, text="핸들 ID")
label_handleID.pack(side=LEFT)

entry_handleID = Entry(add_frame, width = 20, justify="center")
entry_handleID.pack(side=LEFT)

label_handlePW = Label(add_frame, text="핸들 PW")
label_handlePW.pack(side=LEFT)

entry_handlePW = Entry(add_frame, width = 20, justify="center")
entry_handlePW.pack(side=LEFT)

def add_participant():
    global tot_cnt, attendant_cnt_label
    tot_cnt += 1
    attendant_cnt_label["text"] = "출석 인원수: " + str(attendant_cnt) + " / " + str(tot_cnt)
    tmp_dic = {'team':entry_team.get(), 'sid':entry_sid.get(), 'name':entry_name.get(), 'email':entry_email.get()
    , 'attendance':'X', 'handle_id': entry_handleID.get(), 'handle_pw':entry_handlePW.get()}
    
    mysql.add_sql(tmp_dic)
    treeview.insert("", "end", text="", values=list(tmp_dic.values()))
    entry_team.delete(0, END)
    entry_sid.delete(0, END)
    entry_name.delete(0, END)
    entry_email.delete(0, END)
    entry_handleID.delete(0 ,END)
    entry_handlePW.delete(0, END)

def add_participant_thread():
    t = threading.Thread(target = add_participant)
    t.start()

btn_add = Button(add_frame, text="추가", command=add_participant_thread, width=1)
btn_add.pack()

##################################

# 기타 전체추가, 긴급 전송, 삭제,출석 프레임 ###############
etc_frame = Frame(window, padx = 10, pady = 10)
etc_frame.pack(fill="both")

def all_add():
    global tot_cnt, attendant_cnt_label

    # pyinstaller를 통한 executable file에서 csv 파일 열기 위해 사용
    # https://stackoverflow.com/questions/64428122/using-pyinstaller-to-make-an-executable-file-from-python-py-file-utilizing-pand
    # pyinstaller -F -w -n=handler_sender --icon=chaos_logo_white.icns gui.py --add-data "participant.csv:."
    try: # running using executable
        path = sys._MEIPASS

    except: # running using .py sript
        path = os.path.abspath('.')

    csv_path = os.path.join(path, 'participant.csv') # valid path of the csv file
    f = open(csv_path, 'r', encoding='utf-8')

    rdr = csv.reader(f)
    next(rdr)
    for line in rdr:
        team = line[0]
        handle_id = line[10]
        handle_pw = line[11]
        for i in range(1, 9, 3):
            name = line[i]
            sid = line[i+1]
            email_addr = line[i+2]

            if(name == ""):
                continue

            tot_cnt += 1
            attendant_cnt_label["text"] = "출석 인원수: " + str(attendant_cnt) + " / " + str(tot_cnt)
            tmp_dic = {'team':team, 'sid':sid, 'name':name, 'email':email_addr
            , 'attendance':'X', 'handle_id':handle_id, 'handle_pw':handle_pw}
            
            mysql.add_sql(tmp_dic)
            treeview.insert("", "end", text="", values=list(tmp_dic.values()))
        print(line)
    f.close()

def all_add_thread():
    t = threading.Thread(target = all_add)
    t.start()

btn_all_add = Button(etc_frame, text="전체 추가", command=all_add_thread)
btn_all_add.pack(fill=BOTH)

def emergency_send():

    # pyinstaller를 통한 executable file에서 csv 파일 열기 위해 사용
    # https://stackoverflow.com/questions/64428122/using-pyinstaller-to-make-an-executable-file-from-python-py-file-utilizing-pand
    # pyinstaller -F -w -n=handler_sender --icon=chaos_logo_white.icns gui.py --add-data "participant.csv:."
    try: # running using executable
        path = sys._MEIPASS

    except: # running using .py sript
        path = os.path.abspath('.')

    csv_path = os.path.join(path, 'participant.csv') # valid path of the csv file

    f = open(csv_path, 'r', encoding='utf-8')
    rdr = csv.reader(f)
    next(rdr)
    for line in rdr:
        team = line[0]
        handle_id = line[10]
        handle_pw = line[11]
        for i in range(1, 9, 3):
            name = line[i]
            sid = line[i+1]
            email_addr = line[i+2]

            if(name == ""):
                continue

            tmp_dic = {'team':team, 'sid':sid, 'name':name, 'email':email_addr
            , 'attendance':'X', 'handle_id':handle_id, 'handle_pw':handle_pw}

            send_email(tmp_dic["team"], tmp_dic["sid"], tmp_dic["name"]
            , tmp_dic["email"], tmp_dic["handle_id"], tmp_dic["handle_pw"], competition_name)

        print(line)
    f.close()

def emergency_send_thread():
    t = threading.Thread(target = emergency_send)
    t.start()

btn_emergency_send = Button(etc_frame, text="긴급 전송", command = emergency_send_thread)
btn_emergency_send.pack(fill=BOTH)


def delete():
   # Get selected item to Delete

   selected = treeview.focus()
   if(selected):
        global tot_cnt, attendant_cnt,attendant_cnt_label
        tot_cnt -= 1
        
        selected_item = treeview.item(selected).get('values')
        selected_item = {'team':selected_item[0], 'sid':selected_item[1], 'name':selected_item[2]
        , 'email':selected_item[3], 'attendance':selected_item[4], 'handle_id':selected_item[5]
        , 'handle_pw':selected_item[6]}
        if(selected_item['attendance'] == "O"): # 출석 한 사람 지우면 출석 인원 수도 감소
            attendant_cnt -= 1
        
        mysql.delete_sql(selected_item)

        attendant_cnt_label["text"] = "출석 인원수: " + str(attendant_cnt) + " / " + str(tot_cnt)
        treeview.delete(selected)

def delete_thread():
    t = threading.Thread(target = delete)
    t.start()

def send_btn():
    selected = treeview.focus()
    if(selected):
        selected_item = treeview.item(selected).get('values')
        selected_item = {'team':selected_item[0], 'sid':selected_item[1], 'name':selected_item[2]
        , 'email':selected_item[3], 'attendance':selected_item[4], 'handle_id':selected_item[5]
        , 'handle_pw':selected_item[6]}

        if(selected_item["attendance"] == "X"): # 출석 안했을 때만 이메일 보냄
            global tot_cnt, attendant_cnt,attendant_cnt_label
            send_email(selected_item["team"], selected_item["sid"], selected_item["name"]
            , selected_item["email"], selected_item["handle_id"], selected_item["handle_pw"], competition_name)

            mysql.attend_sql(selected_item)
            attendant_cnt += 1
            attendant_cnt_label["text"] = "출석 인원수: " + str(attendant_cnt) + " / " + str(tot_cnt)
            selected_item["attendance"] = "O" # 이메일 보내면 출석 상태를 X에서 O로 변경
            treeview.item(selected, values=list(selected_item.values()))
    

def send_thread():
    t = threading.Thread(target = send_btn)
    t.start()

btn_del = Button(etc_frame, text="삭제", command=delete_thread)
btn_del.pack(fill=BOTH)

btn_att = Button(etc_frame, text="출석", command=send_thread)
btn_att.pack(fill=BOTH)

attendant_cnt_label = Label(etc_frame, text="출석 인원수: " + str(attendant_cnt) + " / " + str(tot_cnt))
attendant_cnt_label.pack(side=RIGHT, padx=5)

##################################

# DB에서 초기 정보 가져오기
def init_competion_name():
    global competition_name_entry, competition_name
    competition_name = mysql.init_competition_name_fetch()
    competition_name_entry.insert(0, competition_name)

def init_treeview():
    global tot_cnt, attendant_cnt, attendant_cnt_label, treeview
    init_participant = mysql.init_fetch()
    for p in init_participant:
        tot_cnt += 1
        if p["attendance"] == "O":
            attendant_cnt += 1
        attendant_cnt_label["text"] = "출석 인원수: " + str(attendant_cnt) + " / " + str(tot_cnt)
        treeview.insert("", "end", text="", values=list(p.values()))

init_competion_name()
init_treeview()

window.mainloop()

mysql.con.close() # DB 연결 종료

smtp.quit() # 5. 메일 서버와의 연결 끊기