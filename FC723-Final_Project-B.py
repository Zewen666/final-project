#
# FC723 Final Project
# 2024.07
#
import random
import sqlite3
import string

db_conn: sqlite3.Connection


def main_menu():
    print('✈  Main menu  ✈\n')
    print('\033[1;31m' + '1. C' + '\033[0m' + 'heck availability of seat')
    print('\033[1;31m' + '2. B' + '\033[0m' + 'ook a seat')
    print('\033[1;31m' + '3. F' + '\033[0m' + 'ree a seat')
    print('\033[1;31m' + '4. S' + '\033[0m' + 'how booking state')
    print('\033[1;31m' + '5. E' + '\033[0m' + 'xit program')
    user_key = input('please enter key: ')
    user_key = user_key.lower()
    if user_key in ['1', 'c']:
        check_seat()
    elif user_key in ['2', 'b']:
        book_seat()
    elif user_key in ['3', 'f']:
        free_seat()
    elif user_key in ['4', 's']:
        show_book()
    elif user_key in ['5', 'e']:
        print('✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈')
        print('✈   Good bye Apache Airlines   ✈')
        print('✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈')
        exit(0)
    else:
        print('invalid key')


def check_seat():
    conn_database()
    cursor = db_conn.cursor()
    cursor.execute("SELECT count(*) FROM seat where state='F'")
    num_empty_seats = cursor.fetchone()[0]
    cursor.execute("SELECT count(*) FROM seat where state!='S'")
    num_total_seats = cursor.fetchone()[0]
    cursor.close()
    close_database()

    print('✈')
    print('✈', 'Total number of seats:', num_total_seats)
    print('✈', 'Number of empty seats:', num_empty_seats)
    print()


def choose_seat() -> tuple:
    conn_database()
    cursor = db_conn.cursor()
    cursor.execute("SELECT count(*) FROM seat where state='F' and seat_r<=25")
    num_empty_seats_f = cursor.fetchone()[0]
    cursor.execute("SELECT count(*) FROM seat where state='F' and seat_r>25 and seat_r<55")
    num_empty_seats_m = cursor.fetchone()[0]
    cursor.execute("SELECT count(*) FROM seat where state='F' and seat_r>=55")
    num_empty_seats_r = cursor.fetchone()[0]

    cursor.execute("SELECT count(*) FROM seat where state!='S' and seat_r<=25")
    num_seats_f = cursor.fetchone()[0]
    cursor.execute("SELECT count(*) FROM seat where state!='S' and seat_r>25 and seat_r<55")
    num_seats_m = cursor.fetchone()[0]
    cursor.execute("SELECT count(*) FROM seat where state!='S' and seat_r>=55")
    num_seats_r = cursor.fetchone()[0]
    cursor.close()
    close_database()
    while True:
        print('✈  Choose seat  ✈\n')
        print('\033[1;31m' + '1. F' + '\033[0m' + 'ront part,', num_empty_seats_f, 'remaining, total', num_seats_f)
        print('\033[1;31m' + '2. M' + '\033[0m' + 'iddle part,', num_empty_seats_m, 'remaining, total', num_seats_m)
        print('\033[1;31m' + '3. R' + '\033[0m' + 'ear part,', num_empty_seats_r, 'remaining, total', num_seats_r)
        print('\033[1;31m' + '4. ' + '\033[0m' + 'r' + '\033[1;31m' + 'E' + '\033[0m' + 'turn')

        user_key = input('please choose cabin part: ')
        user_key = user_key.lower()
        sql_str = ''
        if user_key in ['1', 'f']:
            sql_str = "SELECT * FROM seat where seat_r<=25"
        elif user_key in ['2', 'm']:
            sql_str = "SELECT * FROM seat where seat_r>25 and seat_r<55"
        elif user_key in ['3', 'r']:
            sql_str = "SELECT * FROM seat where seat_r>=55"
        elif user_key in ['4', 'e']:
            return 'Q', 'Q'
        else:
            print('invalid key')
            continue
        break
    if sql_str == '':
        return 'Q', 'Q'

    cursor = db_conn.cursor()
    cursor.execute(sql_str)
    seats = cursor.fetchall()
    cursor.close()
    close_database()
    col_a = ''
    col_b = ''
    col_c = ''
    col_d = ''
    col_e = ''
    col_f = ''

    for seat in seats:

        if seat[2] != 'F':
            if len(seat[2]) > 1:
                seat_s = '\033[1;37m' + str(seat[0]) + seat[1] + '-R|\033[0m'
            else:
                seat_s = '\033[1;37m' + str(seat[0]) + seat[1] + '-' + seat[2] + '|\033[0m'
        else:
            seat_s = str(seat[0]) + seat[1] + '  |'

        if seat[1] == 'A':
            col_a = col_a + ' ' + seat_s
        elif seat[1] == 'B':
            col_b = col_b + ' ' + seat_s
        elif seat[1] == 'C':
            col_c = col_c + ' ' + seat_s
        elif seat[1] == 'D':
            col_d = col_d + ' ' + seat_s
        elif seat[1] == 'E':
            col_e = col_e + ' ' + seat_s
        elif seat[1] == 'F':
            col_f = col_f + ' ' + seat_s

    print(col_a)
    print(col_b)
    print(col_c)
    print('               Walk way                        ' * 3)
    print(col_d)
    print(col_e)
    print(col_f)

    print('✈  Choose seat  ✈\n')
    while True:
        user_key = input(
            'Please enter seat number, Grey seats are not available，\nEnter Q to return to the main menu: ')
        user_key = user_key.upper()

        if user_key == 'Q':
            return 'Q', 'Q'

        if len(user_key) < 2 or len(user_key) > 3:
            print('Please enter a 2 or 3-digit seat number')
            continue

        try:
            seat_r = int(user_key[:-1])
        except:
            print('Please enter row in 1 to 80')
            continue
        if seat_r < 1 or seat_r > 80:
            print('Please enter row in 1 to 80')
            continue
        seat_c = user_key[-1]
        if seat_c not in ['A', 'B', 'C', 'D', 'E', 'F']:
            print('Please enter col in A-F')
            continue
        return seat_r, seat_c


def generate_booking_reference(length=8):
    possible_characters = string.ascii_letters + string.digits
    r_s = ''.join(random.choice(possible_characters) for _ in range(length))
    print(r_s)
    return r_s


def book_seat() -> str:
    seat_r, seat_c = choose_seat()
    if seat_c == 'Q':
        return 'Q'
    t_seat = SeatClass()
    t_seat.row = seat_r
    t_seat.col = seat_c

    sql_str = "select * from seat where seat_r=? and seat_c=? and state='F'"
    conn_database()
    cursor = db_conn.cursor()
    cursor.execute(sql_str, [seat_r, seat_c])
    seat = cursor.fetchone()
    random_code = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    t_seat.code = random_code
    if seat:
        sql_str = "update seat set state=? where seat_r=? and seat_c=?"
        cursor.execute(sql_str, [t_seat.code, t_seat.row, t_seat.col])
        db_conn.commit()
        print('✈')
        print('✈', str(seat_r) + seat_c, 'booking was successful.booking code:', '\033[1;31m' + t_seat.code + '\033[0m')
    else:
        print(str(seat_r) + seat_c, 'Reservations are not available, so please choose again.')
    cursor.close()
    close_database()


def free_seat():
    """
    free seat
    """
    seat_r, seat_c = choose_seat()
    if seat_c == 'Q':
        return 'Q'
    sql_str = "update seat set state='F' where seat_r=? and seat_c=? and state<>'S'"
    conn_database()
    cursor = db_conn.cursor()
    cursor.execute(sql_str, [seat_r, seat_c])
    db_conn.commit()
    print('✈')
    print('✈', str(seat_r) + seat_c, 'free was successful.')
    cursor.close()
    close_database()


def show_book():
    conn_database()
    cursor = db_conn.cursor()
    cursor.execute("SELECT count(*) FROM seat where state='F' and seat_r<=25")
    num_empty_seats_f = cursor.fetchone()[0]
    cursor.execute("SELECT count(*) FROM seat where state='F' and seat_r>25 and seat_r<55")
    num_empty_seats_m = cursor.fetchone()[0]
    cursor.execute("SELECT count(*) FROM seat where state='F' and seat_r>=55")
    num_empty_seats_r = cursor.fetchone()[0]

    cursor.execute("SELECT count(*) FROM seat where state!='S' and seat_r<=25")
    num_seats_f = cursor.fetchone()[0]
    cursor.execute("SELECT count(*) FROM seat where state!='S' and seat_r>25 and seat_r<55")
    num_seats_m = cursor.fetchone()[0]
    cursor.execute("SELECT count(*) FROM seat where state!='S' and seat_r>=55")
    num_seats_r = cursor.fetchone()[0]
    cursor.close()
    close_database()

    print('✈  Show booking  ✈')
    print('✈', '1. Front part,', num_empty_seats_f, 'remaining, total', num_seats_f)
    print('✈', '2. Middle part,', num_empty_seats_m, 'remaining, total', num_seats_m)
    print('✈', '3. Rear part,', num_empty_seats_r, 'remaining, total', num_seats_r)
    print()


class SeatClass:
    """
    class seat
    """

    def __init__(self):
        self.row: int = 0
        self.col: str = 'A'
        self.code: str = ''


def conn_database():
    global db_conn
    try:
        if 'db_conn' not in dir():
            db_conn = sqlite3.connect("seatDB")
    except sqlite3.Error as e:
        print('database connect error！', e)
    except NameError as e:
        print('db_conn name error！', e)


def close_database():
    try:
        if 'db_conn' in dir():
            db_conn.close()
    except sqlite3.Error as e:
        print('database close error！', e)
    except NameError as e:
        print('db_conn name error！', e)


if __name__ == "__main__":
    print()
    print('✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈')
    print('✈  Welcome to Apache Airlines  ✈')
    print('✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈')
    print()
    while True:
        main_menu()
