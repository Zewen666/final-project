import random
import string
import sqlite3

# Define the database connection variable
db_conn: sqlite3.Connection


# Main menu function
def main_menu():
    print('✈  Main menu  ✈\n')
    print('\033[1;31m' + '1. C' + '\033[0m' + 'heck availability of seat')
    print('\033[1;31m' + '2. B' + '\033[0m' + 'ook a seat')
    print('\033[1;31m' + '3. F' + '\033[0m' + 'ree a seat')
    print('\033[1;31m' + '4. S' + '\033[0m' + 'how booking state')
    print('\033[1;31m' + '5. E' + '\033[0m' + 'xit program')
    user_key = input('please enter key: ')
    user_key = user_key.lower()

    # Call the appropriate function based on user input
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


# Function to check seat availability
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


# Function to choose a seat
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

    # Provide the cabin section selection menu
    while True:
        print('✈  Choose seat  ✈\n')
        print('\033[1;31m' + '1. F' + '\033[0m' + 'ront part,', num_empty_seats_f, 'remaining, total', num_seats_f)
        print('\033[1;31m' + '2. M' + '\033[0m' + 'iddle part,', num_empty_seats_m, 'remaining, total', num_seats_m)
        print('\033[1;31m' + '3. R' + '\033[0m' + 'ear part,', num_empty_seats_r, 'remaining, total', num_seats_r)
        print('\033[1;31m' + '4. ' + '\033[0m' + 'r' + '\033[1;31m' + 'E' + '\033[0m' + 'turn')

        user_key = input('please choose cabin part: ')
        user_key = user_key.lower()
        sql_str = ''

        # Generate corresponding SQL query based on user selection
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

    # Display seat map
    col_a = ''
    col_b = ''
    col_c = ''
    col_d = ''
    col_e = ''
    col_f = ''

    for seat in seats:
        if seat[2] != 'F':
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

    # Get user input for the seat number
    while True:
        user_key = input('please enter seat number, Enter Q to return to the main menu: ')
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


# Function to generate a random 8-character booking reference
def generate_booking_reference(length=8):
    possible_characters = string.ascii_letters + string.digits
    return ''.join(random.choice(possible_characters) for _ in range(length))


# Function to book a seat
def book_seat() -> str:
    seat_r, seat_c = choose_seat()
    if seat_c == 'Q':
        return 'Q'

    sql_str = "select * from seat where seat_r=? and seat_c=? and state<>'S'"
    conn_database()
    cursor = db_conn.cursor()
    cursor.execute(sql_str, [seat_r, seat_c])
    seat = cursor.fetchone()
    if seat:
        booking_reference = generate_booking_reference()
        sql_str = "update seat set state=? where seat_r=? and seat_c=?"
        cursor.execute(sql_str, [booking_reference, seat_r, seat_c])
        db_conn.commit()
        print('✈')
        print('✈', str(seat_r) + seat_c, 'booking was successful. Your booking reference is:', booking_reference)
    else:
        print(str(seat_r) + seat_c, 'Reservations are not available, so please select again.')
    cursor.close()
    close_database()


# Function to free a seat
def free_seat():
    seat_r, seat_c = choose_seat()
    if seat_c == 'Q':
        return 'Q'

    sql_str = "select * from seat where seat_r=? and seat_c=? and state='R'"
    conn_database()
    cursor = db_conn.cursor()
    cursor.execute(sql_str, [seat_r, seat_c])
    seat = cursor.fetchone()
    if seat:
        sql_str = "update seat set state='F', booking_reference=NULL where seat_r=? and seat_c=?"
        cursor.execute(sql_str, [seat_r, seat_c])
        db_conn.commit()
        print('✈', str(seat_r) + seat_c, 'seat release completed.')
    else:
        print(str(seat_r) + seat_c, 'The seat has not been booked and cannot be released.')
    cursor.close()
    close_database()


# Function to show booking state
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

    cursor.execute("SELECT seat_r, seat_c, booking_reference FROM seat where state='R'")
    bookings = cursor.fetchall()

    cursor.close()
    close_database()

    print('✈  Show booking  ✈')
    print('✈', '1. Front part,', num_empty_seats_f, 'remaining, total', num_seats_f)
    print('✈', '2. Middle part,', num_empty_seats_m, 'remaining, total', num_seats_m)
    print('✈', '3. Rear part,', num_empty_seats_r, 'remaining, total', num_seats_r)
    print()

    print('✈  Booking References  ✈')
    for booking in bookings:
        print(f'Seat {booking[0]}{booking[1]} - Booking Reference: {booking[2]}')
    print()


# Function to connect to the database
def conn_database():
    global db_conn
    try:
        if 'db_conn' not in dir():
            db_conn = sqlite3.connect("seatDB")
    except sqlite3.Error as e:
        print('database connect error！', e)
    except NameError as e:
        print('db_conn name error！', e)


# Function to close the database connection
def close_database():
    try:
        if 'db_conn' in dir():
            db_conn.close()
    except sqlite3.Error as e:
        print('database close error！', e)
    except NameError as e:
        print('db_conn name error！', e)


# Main program entry point
if __name__ == "__main__":
    print()
    print('✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈')
    print('✈  Welcome to Apache Airlines  ✈')
    print('✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈ ✈')
    print()
    while True:
        main_menu()
