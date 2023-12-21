# import mysql
import pymysql

# mysql 연결
conn = pymysql.connect(host='localhost', user='root', password='Mdydwns97&', db='hotel_booking', charset='utf8mb4')

# cursor 생성
cursor = conn.cursor()

# 기존 테이블 삭제
cursor.execute('set foreign_key_checks = 0')
cursor.execute('drop table if exists hotel cascade')
cursor.execute('drop table if exists hotelroom cascade')
cursor.execute('drop table if exists customer cascade')
cursor.execute('drop table if exists booking cascade')
cursor.execute('set foreign_key_checks = 1')

# table 생성
cursor.execute('''CREATE TABLE hotel(
    hid         VARCHAR(30) NOT NULL,
    hname       VARCHAR(30) NOT NULL,
    haddress    VARCHAR(30) NOT NULL,
    PRIMARY KEY(hid)
)''')
cursor.execute('''CREATE TABLE hotelroom(
    hid         VARCHAR(30) NOT NULL,
    rnum        VARCHAR(30) NOT NULL,
    rprice      INT DEFAULT 0,
    PRIMARY KEY(hid, rnum),
    FOREIGN KEY(hid) REFERENCES hotel(hid)
)''')
cursor.execute('''CREATE TABLE customer(
    cid         VARCHAR(30) NOT NULL,
    cname       VARCHAR(30),
    cphone      VARCHAR(30),
    PRIMARY KEY(cid)
)''')
cursor.execute('''CREATE TABLE booking(
    cid         VARCHAR(30) NOT NULL,
    hid         VARCHAR(30) NOT NULL,
    rnum        VARCHAR(30) NOT NULL,
    checkin     DATE,
    checkout    DATE,
    PRIMARY KEY(cid, hid, rnum, checkin),
    FOREIGN KEY(cid) REFERENCES customer(cid), 
    FOREIGN KEY(hid, rnum) REFERENCES hotelroom(hid, rnum)
)''')


# 읽을 파일을 불러오기, 쓸 파일 생성하기
r_file = open('C:\\Users\\hanyj\\p_data\\PycharmProjects\\pythonProject\\assign_in.txt', 'r', encoding='utf-8')
w_file = open('C:\\Users\\hanyj\\p_data\\PycharmProjects\\pythonProject\\assign_out.txt', 'w')

# 함수이름: join_member
# 기능: 공통 메뉴에서 회원가입 기능 실행
# 반환값: 없음
# 전달인자: 없음
def join_member():
    # 데이터 전달
    line = r_file.readline().strip()
    val = line.split()
    cid, cname, cphone = val[0], val[1], val[2]

    # sql 실행
    sql = '''insert into customer values('{}', '{}', '{}')'''.format(cid, cname, cphone)
    cursor.execute(sql)

    # output.txt에 작성
    w_file.write('1.1 회원가입\n')
    w_file.write('> ' + cid + ' ' + cname + ' ' + cphone + '\n')


# 함수이름: finish
# 기능: 기능 종료
# 반환값: 없음
# 전달인자: 없음
def finish():
    w_file.write('1.2 종료\n')


# 함수이름: log_in_2
# 기능: cid로 로그인
# 반환값: id
# 전달인자: 없음
def log_in_2():
    # cid 전달
    id = r_file.readline().strip()

    w_file.write('2.1 로그인\n')
    w_file.write('> ' + id + '\n')

    # cid 반환
    return id


# 함수이름: booking_hotelroom
# 기능: 호텔방 예약
# 반환값: 없음
# 전달인자: id
def booking_hotelroom(id):
    # 데이터 전달
    line = r_file.readline().strip()
    val = line.split()
    
    hid, rnum, checkin, checkout = val[0], val[1], val[2], val[3]
    
    # sql 실행
    sql = '''insert into booking values('{}', '{}', '{}', '{}', '{}')'''.format(id, hid, rnum, checkin, checkout)
    cursor.execute(sql)

    # checkin, checkout 형식 변경
    cursor.execute('''select date_format(checkin, '%Y/%m/%d') from booking''')
    checkin = str(checkin).replace('-', '/')
    cursor.execute('''select date_format(checkout, '%Y/%m/%d') from booking''')
    checkout = str(checkout).replace('-', '/')
    
    # output.txt에 작성
    w_file.write('2.2 호텔방 예약\n')
    w_file.write('> ' + hid + ' ' + rnum + ' ' + checkin + ' ' + checkout + '\n')



# 함수이름: search_hotelroom_booking
# 기능: 예약 조회
# 반환값: 없음
# 전달인자: id
def search_hotelroom_booking(id):
    # sql 실행
    cursor.execute('select * from booking where cid = %s' %id)

    rows = cursor.fetchall()

    # output.txt에 작성
    w_file.write('2.3 호텔방 예약 조회\n')
    for cur_row in rows:
        hid = cur_row[0]
        rnum = cur_row[1]
        rprice = cur_row[2]
        checkin = cur_row[3]
        checkout = cur_row[4]
        
        # checkin, checkout 형식 변경
        cursor.execute('''select date_format(checkin, '%Y/%m/%d') from booking where cid = %s''' %id)
        checkin = str(checkin).replace('-', '/')
        cursor.execute('''select date_format(checkout, '%Y/%m/%d') from booking where cid = %s''' %id)
        checkout = str(checkout).replace('-', '/')
        
        w_file.write('> ' + id + ' ' + hid + ' ' + rnum + ' ' + str(rprice) + ' ' + checkin + ' ' + checkout + '\n')


# 함수이름: cancel_booking
# 기능: 예약 취소
# 반환값: 없음
# 전달인자: id
def cancel_booking(id):
    # sql 실행
    cursor.execute('delete from booking where cid = %s' %id)

    # output.txt에 작성
    w_file.write('2.4 호텔방 예약 취소\n')


# 함수이름: log_out_2
# 기능: 로그아웃
# 반환값: 없음
# 전달인자: id
def log_out_2(id):
    w_file.write('2.5 로그아웃\n')
    w_file.write('> ' + id + '\n')

    # cid 초기화
    id = None


# 함수이름: log_in_3
# 기능: 로그인
# 반환값: id
# 전달인자: 없음
def log_in_3():
    # 데이터 전달
    line = r_file.readline()
    id = line.strip()

    # output.txt에 작성
    w_file.write('3.1 로그인\n')
    w_file.write('> ' + id + '\n')

    # cid 반환
    return id


# 함수이름: insert_hotel_info
# 기능: 호텔 정보 등록
# 반환값: 없음
# 전달인자: 없음
def insert_hotel_info():
    # 데이터 전달
    line = r_file.readline()
    val = line.split()
    hid, hname, haddress = val[0], val[1], val[2]

    # sql 실행
    sql = '''insert into hotel values('{}', '{}', '{}')'''.format(hid, hname, haddress)
    cursor.execute(sql)

    # output.txt에 작성
    w_file.write('3.2 호텔 정보 등록\n')
    w_file.write('> ' + hid + ' ' + hname + ' ' + haddress + '\n')


# 함수이름: insert_hotelroom_info
# 기능: 호텔방 정보 등록
# 반환값: 없음
# 전달인자: 없음
def insert_hotelroom_info():
    # 데이터 전달
    line = r_file.readline()
    val = line.split()
    hid, rnum, rprice = val[0], val[1], val[2]

    # sql 실행
    sql = '''insert into hotelroom values('{}', '{}', '{}')'''.format(hid, rnum, rprice)
    cursor.execute(sql)

    # output.txt에 작성
    w_file.write('3.3 호텔방 정보 등록\n')
    w_file.write('> ' + hid + ' ' + rnum + ' ' + rprice + '\n')


# 함수이름: search_booking
# 기능: 예약 내역 조회
# 반환값: 없음
# 전달인자: 없음
def search_booking():
    # sql 실행
    cursor.execute('''
                select c.cid, c.cname, h.hid, h.hname, h.haddress, r.rnum, r.rprice, b.checkin, b.checkout
                from booking b
                join customer c on b.cid = c.cid
                join hotel h on b.hid = h.hid
                join hotelroom r on b.hid = r.hid and b.rnum = r.rnum
                ''')

    rows = cursor.fetchall()

    # output.txt에 작성
    w_file.write('3.4 예약 내역 조회\n')
    for cur_row in rows:
        cid = cur_row[0]
        cname = cur_row[1]
        hid = cur_row[2]
        hname = cur_row[3]
        haddress = cur_row[4]
        rnum = cur_row[5]
        rprice = cur_row[6]
        checkin = cur_row[7]
        checkout = cur_row[8]
        
        # checkin, checkout 형식 변경
        cursor.execute('''select date_format(checkin, '%Y/%m/%d')
                        from booking b
                        join customer c on b.cid = c.cid
                        join hotel h on b.hid = h.hid
                        join hotelroom r on b.hid = r.hid and b.rnum = r.rnum''')
        checkin = str(checkin).replace('-', '/')
        cursor.execute('''select date_format(checkout, '%Y/%m/%d')
                       from booking b
                        join customer c on b.cid = c.cid
                        join hotel h on b.hid = h.hid
                        join hotelroom r on b.hid = r.hid and b.rnum = r.rnum''')
        checkout = str(checkout).replace('-', '/')
        
        w_file.write('> ' + cid + ' ' + cname + ' ' + hid + ' ' + hname + ' ' + haddress + ' ' + rnum + ' ' + str(rprice) + ' ' + str(checkin) + ' ' + str(checkout) + '\n')


# 함수이름: log_out_3
# 기능: 로그아웃
# 반환값: 없음
# 전달인자: id
def log_out_3(id):
    w_file.write('3.5 로그아웃\n')
    w_file.write('> ' + id + '\n')

    # cid 초기화
    id = None


# 함수이름: do_task
# 기능: 메모장 파일을 읽어와 기능 실행
# 반환값: 없음
# 전달인자: 없음
def do_task():
    # 매개변수로 사용할 cid 선언
    cid = None

    # 1 2가 입력되기 전까지 반복
    while True:
        line = r_file.readline()
        line.strip()

        # 메뉴 구분 위한 숫자 구분
        menu_1, menu_2 = line.split()

        if menu_1 == '1':
            if menu_2 == '1': join_member()
            # while 종료 조건
            elif menu_2 == '2':
                finish()
                break

        elif menu_1 == '2':
            if menu_2 == '1':
                # cid 할당
                cid = log_in_2()
            elif menu_2 == '2':
                booking_hotelroom(cid)
            elif menu_2 == '3':
                search_hotelroom_booking(cid)
            elif menu_2 == '4':
                cancel_booking(cid)
            elif menu_2 == '5':
                log_out_2(cid)

        elif menu_1 == '3':
            if menu_2 == '1':
                # cid 할당
                cid = log_in_3()
            elif menu_2 == '2': insert_hotel_info()
            elif menu_2 == '3': insert_hotelroom_info()
            elif menu_2 == '4': search_booking()
            elif menu_2 == '5': log_out_3(cid)


# input.txt에 적힌 내용을 불러와 함수 실행
do_task()

# mysql 연결 종료
conn.close()

# file 연결 종료
r_file.close()
w_file.close()