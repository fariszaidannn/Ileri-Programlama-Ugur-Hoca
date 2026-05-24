'''
Seyahatify is an application where you would need to sign up and log in to an account that will then precede you to type in a city's name screen. 
Your login info will then be stored in SQLite, and then you can proceed to log in based on the login info. 
Once you type the city's name, the app will then call the news and weather API to the main screen. 
Then, on the sidebar, you will have a to-do list that you can input your own personal mission before planning the trip. 
'''

# Importing app necessities
import sqlite3
import tkinter as tk
from tkinter import messagebox as msg
import sys
import requests # For API calls

#  Manual Dark Theme Settings (Adapted to Seyahatify Style) 
BG_COLOR = "#1f1f1f"       
FG_COLOR = "#ffffff"       
BTN_ACTIVE = "#4a90e2"     
BTN_INACTIVE = "#2a2a2b"   
BTN_HOVER = "#0c589b"      
BTN_FG_HOVER = "#0d2b46"   
ENTRY_BG = "#333333"       

FONT_TITLE = ("Poppins", 24, "bold")
FONT_NORMAL = ("Poppins", 12)
FONT_BTN = ("Poppins", 12, "bold")

# Initialize app
root = tk.Tk()
root.title("Seyahatify - Trip Planner")
root.config(bg=BG_COLOR)
root.geometry("400x500")

# Database setup with SQLite locally
conn = sqlite3.connect("seyahatify_users.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")
conn.commit()

#  Main Centered Wrapper 
main_wrapper = tk.Frame(root, bg=BG_COLOR)
main_wrapper.place(relx=0.5, rely=0.5, anchor="center") 
# Relative X and Y set to 0.5 to center

#  Logo 
title_label = tk.Label(main_wrapper, 
                       text="Seyahatify", 
                       bg=BG_COLOR, 
                       fg=FG_COLOR, 
                       font=FONT_TITLE)
title_label.pack(pady=(0, 20))

    #  Tabs Frame 
tab_frame = tk.Frame(main_wrapper, 
                     bg=BG_COLOR)
tab_frame.pack(fill="x", pady=(0, 20))

def show_login():
    register_frame.pack_forget() # Forget = remove current 
    login_frame.pack(fill="both", expand=True)
    btn_login.config(bg=BTN_ACTIVE)
    btn_register.config(bg=BTN_INACTIVE)

def show_register():
    login_frame.pack_forget()
    register_frame.pack(fill="both", expand=True)
    btn_register.config(bg=BTN_ACTIVE)
    btn_login.config(bg=BTN_INACTIVE)

    # Tab Buttons
btn_login = tk.Button(tab_frame,
                      text="Log In", 
                      command=show_login, 
                      bg=BTN_ACTIVE, fg=FG_COLOR, 
                      relief="flat", font=FONT_BTN, activebackground=BTN_HOVER, activeforeground=BTN_FG_HOVER)
btn_login.pack(side="left", expand=True, fill="x", padx=(0, 5), ipady=5)

btn_register = tk.Button(tab_frame, 
                         text="Sign Up", 
                         command=show_register, 
                         bg=BTN_INACTIVE, fg=FG_COLOR, 
                         relief="flat", font=FONT_BTN, activebackground=BTN_HOVER, activeforeground=BTN_FG_HOVER)
btn_register.pack(side="right", expand=True, fill="x", padx=(5, 0), ipady=5)

#  Content Frame 
content_frame = tk.Frame(main_wrapper, bg=BG_COLOR)
content_frame.pack(fill="both", expand=True)

    #  Content Frame > Login Form 
login_frame = tk.Frame(content_frame, bg=BG_COLOR)

tk.Label(login_frame, 
         text="Username:", 
         bg=BG_COLOR, fg=FG_COLOR, font=FONT_NORMAL).pack()
login_user = tk.Entry(login_frame, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR, relief="flat", font=FONT_NORMAL)
login_user.pack(pady=5, ipady=5, ipadx=10)

tk.Label(login_frame, 
         text="Password:", 
         bg=BG_COLOR, fg=FG_COLOR, font=FONT_NORMAL).pack()
login_pass = tk.Entry(login_frame, show="*", bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR, relief="flat", font=FONT_NORMAL)
login_pass.pack(pady=5, ipady=5, ipadx=10)

def login():
    u = login_user.get() 
    p = login_pass.get() 
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p)) # From SQLite, select all from users where username and password match the input
    if cursor.fetchone():
        msg.showinfo("Login Success", f"Welcome back, {u}!")
        # TODO: Destroy main_wrapper and call your weather API / Main App Screen here
    else:
        msg.showerror("Failed", "Incorrect username or password!")

tk.Button(login_frame, text="Login", command=login, bg=BTN_ACTIVE, fg=FG_COLOR, 
          activebackground=BTN_HOVER, activeforeground=BTN_FG_HOVER, relief="flat", font=FONT_BTN).pack(pady=20, ipadx=30, ipady=5)


    #  Content Frame > Register Form 
register_frame = tk.Frame(content_frame, bg=BG_COLOR)

tk.Label(register_frame,
         text="Create a Username:", 
         bg=BG_COLOR, fg=FG_COLOR, font=FONT_NORMAL).pack()
reg_user = tk.Entry(register_frame, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR, relief="flat", font=FONT_NORMAL)
reg_user.pack(pady=5, ipady=5, ipadx=10)

tk.Label(register_frame, 
         text="Create a Password:", 
         bg=BG_COLOR, fg=FG_COLOR, 
         font=FONT_NORMAL).pack()
reg_pass = tk.Entry(register_frame, show="*", bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR, relief="flat", font=FONT_NORMAL)
reg_pass.pack(pady=5, ipady=5, ipadx=10)

def register():
    u = reg_user.get()
    p = reg_pass.get()
    if not u or not p:
        msg.showwarning("Failed", "Fields cannot be empty!")
        return
        
    try:
        cursor.execute("INSERT INTO users(username, password) VALUES (?, ?)", (u, p))
        conn.commit()
        msg.showinfo("Success", "Account created! You can now log in.")
        reg_user.delete(0, 'end')
        reg_pass.delete(0, 'end')
        show_login() # Automatically switch back to login tab
    except sqlite3.IntegrityError:
        msg.showerror("Failed", "Username already exists!")

tk.Button(register_frame, text="Register", command=register, bg=BTN_ACTIVE, fg=FG_COLOR, 
          activebackground=BTN_HOVER, activeforeground=BTN_FG_HOVER, relief="flat", font=FONT_BTN).pack(pady=20, ipadx=30, ipady=5)

# Initialize by showing the Login tab
show_login()

def main_screen():
    frame = tk.Frame(root, bg=BG_COLOR)
    

root.mainloop()