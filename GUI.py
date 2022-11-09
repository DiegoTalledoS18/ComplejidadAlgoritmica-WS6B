from tkinter import *
from PIL import ImageTk, Image

window = Tk()
window = window
window.geometry('1366x718')
window.resizable(0, 0)
window.title('Fastest route by plane V2')

# ============================background image============================
bg_frame = Image.open('images\\background1.png')
photo = ImageTk.PhotoImage(bg_frame)
bg_panel = Label(window, image=photo)
bg_panel.image = photo
bg_panel.pack(fill='both', expand='yes')
# ====== Frame =========================
lgn_frame = Frame(window, bg='#ffffff', width=950, height=600)
lgn_frame.place(x=200, y=70)

# ========================================================================
txt = "CALCULADOR DE RUTA MAS RAPIDA"
heading = Label(lgn_frame, text=txt, font=('yu gothic ui', 25, "bold"), bg="#ffffff", fg='black', bd=10, relief=FLAT)
heading.place(x=10, y=30, width=900, height=30)

# ============ Eliga su destino =============================================
sign_in_label = Label(lgn_frame, text="Eliga su destino", bg="#ffffff", fg="#4f4e4d", font=("yu gothic ui", 17, "bold"))
sign_in_label.place(x=380, y=93)

# ============================INICIO====================================
username_label = Label(lgn_frame, text="IATA INICIO", bg="#ffffff", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
username_label.place(x=100, y=160)

username_entry = Entry(lgn_frame, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#4f4e4d",
                       font=("yu gothic ui ", 12, "bold"))
username_entry.place(x=130, y=198, width=230)

password_line = Canvas(lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
password_line.place(x=100, y=223)

username_line = Canvas(lgn_frame, width=300, height=2.0, bg="#ffffff", highlightthickness=0)
username_line.place(x=100, y=355)
# ===== airport icon inicial =========
username_icon = Image.open('images\\initial_icon.png')
photo = ImageTk.PhotoImage(username_icon)
username_icon_label = Label(lgn_frame, image=photo, bg='#ffffff')
username_icon_label.image = photo
username_icon_label.place(x=100, y=196)

# ============================Calculate button================================
lgn_button = Image.open('images\\btn1.png')
photo = ImageTk.PhotoImage(lgn_button)
lgn_button_label = Label(lgn_frame, image=photo, bg='#ffffff')
lgn_button_label.image = photo
lgn_button_label.place(x=330, y=270)
login = Button(lgn_button_label, text='CALCULAR', font=("yu gothic ui", 13, "bold"), width=27, bd=0,
               bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white')
login.place(x=10, y=10)

# ============================FINAL====================================
password_label = Label(lgn_frame, text="IATA FINAL", bg="#ffffff", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
password_label.place(x=550, y=160)

password_entry = Entry(lgn_frame, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#4f4e4d",
                       font=("yu gothic ui", 12, "bold"))
password_entry.place(x=580, y=198, width=230)

password_line = Canvas(lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
password_line.place(x=550, y=223)

# ======== airport icon FINAL ================
password_icon = Image.open('images\\end_icon.png')
photo = ImageTk.PhotoImage(password_icon)
password_icon_label = Label(lgn_frame, image=photo, bg='#ffffff')
password_icon_label.image = photo
password_icon_label.place(x=550, y=196)


# ========= Validate IATA ==================================================================

def Correct():
    hide_button = Button(lgn_frame, image=hide_image, command=Incorrect, relief=FLAT, activebackground="white",
                         borderwidth=0, background="white", cursor="hand2")
    hide_button.place(x=820, y=196)
    password_entry.config(show='')


def Incorrect():
    show_button = Button(lgn_frame, image=show_image, command=Correct, relief=FLAT, activebackground="white",
                         borderwidth=0, background="white", cursor="hand2")
    show_button.place(x=820, y=196)
    password_entry.config(show='')


show_image = ImageTk.PhotoImage \
    (file='images\\valid.png')

hide_image = ImageTk.PhotoImage \
    (file='images\\invalid.png')

show_button = Button(lgn_frame, image=show_image, command=Correct, relief=FLAT, activebackground="white", borderwidth=0,
                     background="white", cursor="hand2")
show_button.place(x=820, y=196)

show_button = Button(lgn_frame, image=show_image, command=Correct, relief=FLAT, activebackground="white", borderwidth=0,
                     background="white", cursor="hand2")
show_button.place(x=370, y=196)

window.mainloop()
