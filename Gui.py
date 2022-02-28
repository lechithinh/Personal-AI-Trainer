from tkinter import *
from tkinter import messagebox
import sqlite3
import ExerciseModule as ex
import sys


f = ('Times', 14)

con = sqlite3.connect('Database/userdata.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS record(
                    name text, 
                    email text, 
                    contact number, 
                    gender text, 
                    country text,
                    password text
                )
            ''')
con.commit()

ws = Tk()
ws.title('Personal Fitness AI Trainer')
ws.geometry('940x500')
ws.config(bg='#0B5A81')
#Algorithms and functions
exercise = ex.simulate_exercise(difficulty_level= 1)
result = {"calories": 0, "time_elapsed": 0}
def skip():
    skip_performance = exercise.skip()
    result["calories"] += skip_performance["calories"]
    result["time_elapsed"] += skip_performance["time_elapsed"]
    print(result)
def push_up():
    pushup_performance = exercise.push_ups()
    result["calories"] += pushup_performance["calories"]
    result["time_elapsed"] += pushup_performance["time_elapsed"]
    print(result)
def bicep_curls():
    bicep_curls_performance = exercise.bicep_curls()
    result["calories"] += bicep_curls_performance["calories"]
    result["time_elapsed"] += bicep_curls_performance["time_elapsed"]
    print(result)

def mountain_climbers():
    mountain_performance = exercise.mountain_climbers()
    result["calories"] += mountain_performance["calories"]
    result["time_elapsed"] += mountain_performance["time_elapsed"]
    print(result)
def squats():
    squats_performance = exercise.squats()
    result["calories"] += squats_performance["calories"]
    result["time_elapsed"] += squats_performance["time_elapsed"]
    print(result)
def stop():
    print(result)
    sys.exit()

def insert_record():
    check_counter = 0
    warn = ""
    if register_name.get() == "":
        warn = "Name can't be empty"
    else:
        check_counter += 1

    if register_email.get() == "":
        warn = "Email can't be empty"
    else:
        check_counter += 1

    if register_mobile.get() == "":
        warn = "Contact can't be empty"
    else:
        check_counter += 1

    if var.get() == "":
        warn = "Select Gender"
    else:
        check_counter += 1

    if variable.get() == "":
        warn = "Select Country"
    else:
        check_counter += 1

    if register_pwd.get() == "":
        warn = "Password can't be empty"
    else:
        check_counter += 1

    if pwd_again.get() == "":
        warn = "Re-enter password can't be empty"
    else:
        check_counter += 1

    if register_pwd.get() != pwd_again.get():
        warn = "Passwords didn't match!"
    else:
        check_counter += 1

    if check_counter == 8:
        try:
            con = sqlite3.connect('userdata.db')
            cur = con.cursor()
            cur.execute("INSERT INTO record VALUES (:name, :email, :contact, :gender, :country, :password)", {
                'name': register_name.get(),
                'email': register_email.get(),
                'contact': register_mobile.get(),
                'gender': var.get(),
                'country': variable.get(),
                'password': register_pwd.get()

            })
            con.commit()
            messagebox.showinfo('confirmation', 'Record Saved')

        except Exception as ep:
            messagebox.showerror('', ep)
    else:
        messagebox.showerror('Error', warn)


def login_response():
    try:
        con = sqlite3.connect('Database/userdata.db')
        c = con.cursor()
        for row in c.execute("Select * from record"):
            username = row[1]
            pwd = row[5]

    except Exception as ep:
        messagebox.showerror('', ep)

    uname = email_tf.get()
    upwd = pwd_tf.get()
    check_counter = 0
    if uname == "":
        warn = "Username can't be empty"
    else:
        check_counter += 1
    if upwd == "":
        warn = "Password can't be empty"
    else:
        check_counter += 1
    if check_counter == 2:
        if (uname == username and upwd == pwd):
            messagebox.showinfo('Login Status', 'Logged in Successfully!')

        else:
            messagebox.showerror('Login Status', 'invalid username or password')
    else:
        messagebox.showerror('', warn)


var = StringVar()
var.set('male')

countries = []
variable = StringVar()
world = open('Gui/countries.txt', 'r')
for country in world:
    country = country.rstrip('\n')
    countries.append(country)
variable.set(countries[22])

# widgets
left_frame = Frame(
    ws,
    bd=2,
    bg='#CCCCCC',
    relief=SOLID,
    padx=10,
    pady=10
)

Label(
    left_frame,
    text="Enter Email",
    bg='#CCCCCC',
    font=f).grid(row=0, column=0, sticky=W, pady=10)

Label(
    left_frame,
    text="Enter Password",
    bg='#CCCCCC',
    font=f
).grid(row=1, column=0, pady=10)

#SET difficulty level
Label(
    left_frame,
    text="Difficulty Level",
    bg='#CCCCCC',
    font=f
).grid(row=3, column=0, pady=10)

gender_frame = LabelFrame(
    left_frame,
    bg='#CCCCCC',
    padx=10,
    pady=10,
)


email_tf = Entry(
    left_frame,
    font=f
)
pwd_tf = Entry(
    left_frame,
    font=f,
    show='*'
)
login_btn = Button(
    left_frame,
    width=15,
    text='Login',
    font=f,
    relief=SOLID,
    cursor='hand2',
    command=login_response
)

var_diff = StringVar()
var_diff.set('Easy')

difficulty_frame = LabelFrame(
    left_frame,
    bg='#CCCCCC',
    padx=10,
    pady=10,
)
easy_lb = Radiobutton(
    difficulty_frame,
    text='Easy',
    bg='#CCCCCC',
    variable=var_diff,
    value='male',
    font=('Times', 10),
)

medium_lb = Radiobutton(
    difficulty_frame,
    text='Medium',
    bg='#CCCCCC',
    variable=var_diff,
    value='female',
    font=('Times', 10),

)

hard_lb = Radiobutton(
    difficulty_frame,
    text='Intensive',
    bg='#CCCCCC',
    variable=var_diff,
    value='others',
    font=('Times', 10)
)

difficulty_frame.grid(row=3, column=1, pady=10, padx=20)
easy_lb.pack(expand=True, side=LEFT)
medium_lb.pack(expand=True, side=LEFT)
hard_lb.pack(expand=True, side=LEFT)

#========= AI part ========= #
exercise_frame = LabelFrame(
    left_frame,
    bg='#CCCCCC',
    padx=100,
    pady=100,
).grid(row=4, column=0, pady=10, padx=10)

skip_btn = Button(
    left_frame,
    width=10,
    text='Skip',
    font=f,
    relief=SOLID,
    command = skip
).grid(row=4, column=0, pady=0, padx=0)

push_btn = Button(
    left_frame,
    width=10,
    text='Push up',
    font=f,
    relief=SOLID,
    command = push_up
).grid(row=4, column=1, pady=0, padx=0)

bicep_btn = Button(
    left_frame,
    width=10,
    text='Bicep Curl',
    font=f,
    relief=SOLID,
    command = bicep_curls
).grid(row=5, column=0, pady=20, padx=0)

squat_btn = Button(
    left_frame,
    width=10,
    text='Squats',
    font=f,
    relief=SOLID,
    command = squats
).grid(row=6, column=0, pady=0, padx=0)

mountain_btn = Button(
    left_frame,
    width=10,
    text='Climber',
    font=f,
    relief=SOLID,
    command = mountain_climbers
).grid(row=5, column=1,pady=0, padx= 0)

stop_btn = Button(
    left_frame,
    width=10,
    text='Stop',
    font=f,
    relief=SOLID,
    command = stop
).grid(row=6, column=1, pady=0, padx=0)


#==============================#
right_frame = Frame(
    ws,
    bd=2,
    bg='#CCCCCC',
    relief=SOLID,
    padx=10,
    pady=10
)

Label(
    right_frame,
    text="Enter Name",
    bg='#CCCCCC',
    font=f
).grid(row=0, column=0, sticky=W, pady=10)

Label(
    right_frame,
    text="Enter Email",
    bg='#CCCCCC',
    font=f
).grid(row=1, column=0, sticky=W, pady=10)

Label(
    right_frame,
    text="Contact Number",
    bg='#CCCCCC',
    font=f
).grid(row=2, column=0, sticky=W, pady=10)

Label(
    right_frame,
    text="Select Gender",
    bg='#CCCCCC',
    font=f
).grid(row=3, column=0, sticky=W, pady=10)

Label(
    right_frame,
    text="Select Country",
    bg='#CCCCCC',
    font=f
).grid(row=4, column=0, sticky=W, pady=10)

Label(
    right_frame,
    text="Enter Password",
    bg='#CCCCCC',
    font=f
).grid(row=5, column=0, sticky=W, pady=10)

Label(
    right_frame,
    text="Re-Enter Password",
    bg='#CCCCCC',
    font=f
).grid(row=6, column=0, sticky=W, pady=10)

gender_frame = LabelFrame(
    right_frame,
    bg='#CCCCCC',
    padx=10,
    pady=10,
)

register_name = Entry(
    right_frame,
    font=f
)

register_email = Entry(
    right_frame,
    font=f
)

register_mobile = Entry(
    right_frame,
    font=f
)

male_rb = Radiobutton(
    gender_frame,
    text='Male',
    bg='#CCCCCC',
    variable=var,
    value='male',
    font=('Times', 10),
)

female_rb = Radiobutton(
    gender_frame,
    text='Female',
    bg='#CCCCCC',
    variable=var,
    value='female',
    font=('Times', 10),

)

others_rb = Radiobutton(
    gender_frame,
    text='Others',
    bg='#CCCCCC',
    variable=var,
    value='others',
    font=('Times', 10)
)

register_country = OptionMenu(
    right_frame,
    variable,
    *countries)

register_country.config(
    width=15,
    font=('Times', 12)
)
register_pwd = Entry(
    right_frame,
    font=f,
    show='*'
)
pwd_again = Entry(
    right_frame,
    font=f,
    show='*'
)

register_btn = Button(
    right_frame,
    width=15,
    text='Register',
    font=f,
    relief=SOLID,
    cursor='hand2',
    command=insert_record
)

# widgets placement
email_tf.grid(row=0, column=1, pady=10, padx=20)
pwd_tf.grid(row=1, column=1, pady=10, padx=20)
login_btn.grid(row=2, column=1, pady=10, padx=20)
left_frame.place(x=50, y=50)

register_name.grid(row=0, column=1, pady=10, padx=20)
register_email.grid(row=1, column=1, pady=10, padx=20)
register_mobile.grid(row=2, column=1, pady=10, padx=20)
register_country.grid(row=4, column=1, pady=10, padx=20)
register_pwd.grid(row=5, column=1, pady=10, padx=20)
pwd_again.grid(row=6, column=1, pady=10, padx=20)
register_btn.grid(row=7, column=1, pady=10, padx=20)
right_frame.place(x=500, y=50)

gender_frame.grid(row=3, column=1, pady=10, padx=20)
male_rb.pack(expand=True, side=LEFT)
female_rb.pack(expand=True, side=LEFT)
others_rb.pack(expand=True, side=LEFT)

# infinite loop
ws.mainloop()