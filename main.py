from tkinter import *
from tkinter import messagebox
import graphviz as gv
from PIL import ImageTk, Image

graph = gv.Digraph("grafo1")
path_file = "Short.csv"
diccionario = {}
diccionario2 = [None] * 21
valor_ini = 0
valor_fin = 0
ruta = []
path = []

ladj = [[] for _ in range(21)]


def bfs_al(G, s):
    n = len(G)
    visited = [False] * n
    path = [-1] * n  # parent
    queue = [s]
    visited[s] = True

    while queue:
        u = queue.pop(0)
        for v in G[u]:
            if not visited[v]:
                visited[v] = True
                path[v] = u
                queue.append(v)
    return path


def read_file(archivo):
    cont = 0
    with open(archivo, "r") as archivo:
        for linea in archivo:
            linea = linea.rstrip()
            separador = ","
            lista = linea.split(",")

            salida = lista[0]
            destino = lista[1]

            # Validacion de diccionario (salida)
            if salida not in diccionario:
                diccionario[salida] = cont
                diccionario2[cont] = salida
                cont += 1

            # Validacion de diccionario (destino)
            if destino not in diccionario:
                diccionario[destino] = cont
                diccionario2[cont] = destino
                cont += 1

            # Creamos una lista de adyacencia
            ladj[diccionario[salida]].append(diccionario[destino])

            # hora = lista[2]
            # min = lista[3]
    return ladj


def escala(valor_ini, pos, path):
    if pos == valor_ini:
        return ruta

    ruta.append(diccionario2[path[pos]])
    return escala(valor_ini, path[pos], path)


"""root = Tk()
root.title("Fastest route by plane")

myFrame = Frame(root, width=100, height=200)
root.geometry("800x450")
myFrame.pack()

title = Label(myFrame, text="Calcule la ruta mas rapida entre aeropuertos", bd=1, font=("Helvetica 12"), justify=CENTER,
              pady=14)
title.grid(row=0, column=3)

initialIATA = Entry(myFrame)
initialIATA.grid(row=3, column=1)

finalIATA = Entry(myFrame)
finalIATA.grid(row=3, column=6)

initialIATALabel = Label(myFrame, text="Origen (IATA) :", pady=20)
initialIATALabel.grid(row=3, sticky="e", column=0)

finalIATALabel = Label(myFrame, text="Destino (IATA) :")
finalIATALabel.grid(row=3, sticky="e", column=5)


def sendCalculateButton():
    firstIATA = initialIATA.get()
    secondIATA = finalIATA.get()

    if len(firstIATA) == 0 or len(secondIATA) == 0:
        return messagebox.showinfo('Error', 'Campos Incompletos')
    else:
        lista = read_file(path_file)

        valor_ini = diccionario[str(firstIATA)]
        valor_fin = diccionario[str(secondIATA)]

        path = bfs_al(lista, valor_ini)

        ruta_final = escala(valor_ini, valor_fin, path)

        result.set("Ruta: " + str(ruta_final))

sendButton = Button(root, text="Calcular", command=sendCalculateButton)
sendButton.pack()

result = StringVar()

label = Label(root, textvariable=result)
label.pack()

root.mainloop()"""

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

initialIATA = Entry(lgn_frame, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#4f4e4d",
                       font=("yu gothic ui ", 12, "bold"))
initialIATA.place(x=130, y=198, width=230)

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

# ============================FINAL====================================
password_label = Label(lgn_frame, text="IATA FINAL", bg="#ffffff", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
password_label.place(x=550, y=160)

finalIATA = Entry(lgn_frame, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#4f4e4d",
                       font=("yu gothic ui", 12, "bold"))
finalIATA.place(x=580, y=198, width=230)

password_line = Canvas(lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
password_line.place(x=550, y=223)

# ======== airport icon FINAL ================
password_icon = Image.open('images\\end_icon.png')
photo = ImageTk.PhotoImage(password_icon)
password_icon_label = Label(lgn_frame, image=photo, bg='#ffffff')
password_icon_label.image = photo
password_icon_label.place(x=550, y=196)


# ============================Calculate button================================

def sendCalculateButton():
    firstIATA = initialIATA.get().upper()
    secondIATA = finalIATA.get().upper()


    if len(firstIATA) == 0 or len(secondIATA) == 0:
        temporaryRight=True
        temporaryLeft=True
        if len(firstIATA)== 0:
            temporaryLeft= False
        if len(secondIATA)== 0:
            temporaryRight= False

        showStatusIcons(temporaryLeft,temporaryRight)
    else:
        showStatusIcons(True, True)
        lista = read_file(path_file)

        valor_ini = diccionario[str(firstIATA)]
        valor_fin = diccionario[str(secondIATA)]

        path = bfs_al(lista, valor_ini)

        ruta_final = escala(valor_ini, valor_fin, path)

        result.set("Ruta: " + str(ruta_final))



lgn_button = Image.open('images\\btn1.png')
photo = ImageTk.PhotoImage(lgn_button)
lgn_button_label = Label(lgn_frame, image=photo, bg='#ffffff')
lgn_button_label.image = photo
lgn_button_label.place(x=330, y=270)
login = Button(lgn_button_label, text='CALCULAR', command=sendCalculateButton, font=("yu gothic ui", 13, "bold"), width=27, bd=0,
               bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white')
login.place(x=10, y=10)

result = StringVar()

label = Label(lgn_frame, textvariable=result, font=('yu gothic ui', 20, "bold"), bg="#ffffff", fg='black', bd=0, relief=FLAT)
label.place(x=30, y=380, width=900, height=30)


# ========= Validate IATA ==================================================================

def showStatusIcons(first, end):
    invalidText="Campo incompleto"
    print(first, end)
    if first:
        firstButton = Button(lgn_frame, image=valid, relief=FLAT, activebackground="white",borderwidth=0, background="white", cursor="hand2")
        firstButton.place(x=370, y=196)
        InvalidlabelFirst = Label(lgn_frame, text=invalidText, font=('yu gothic ui', 9), bg="#ffffff", fg='white', bd=0, relief=FLAT)
        InvalidlabelFirst.place(x=100, y=231)
    if not first:
        firstButton = Button(lgn_frame, image=invalid, relief=FLAT, activebackground="white",borderwidth=0, background="white", cursor="hand2")
        firstButton.place(x=370, y=196)
        InvalidlabelFirst = Label(lgn_frame, text=invalidText, font=('yu gothic ui', 9), bg="#ffffff", fg='red', bd=0, relief=FLAT)
        InvalidlabelFirst.place(x=100, y=231)
    if end:
        endButton = Button(lgn_frame, image=valid, relief=FLAT, activebackground="white",borderwidth=0, background="white", cursor="hand2")
        endButton.place(x=820, y=196)
        InvalidlabelEnd = Label(lgn_frame, text=invalidText, font=('yu gothic ui', 9), bg="#ffffff", fg='white', bd=0, relief=FLAT)
        InvalidlabelEnd.place(x=550, y=231)
    if not end:
        endButton = Button(lgn_frame, image=invalid, relief=FLAT, activebackground="white",borderwidth=0, background="white", cursor="hand2")
        endButton.place(x=820, y=196)
        InvalidlabelEnd = Label(lgn_frame, text=invalidText, font=('yu gothic ui', 9), bg="#ffffff", fg='red', bd=0, relief=FLAT)
        InvalidlabelEnd.place(x=550, y=231)


valid = ImageTk.PhotoImage \
    (file='images\\valid.png')

invalid = ImageTk.PhotoImage \
    (file='images\\invalid.png')


window.mainloop()
