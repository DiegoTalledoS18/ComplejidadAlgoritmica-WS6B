from tkinter import *
from tkinter import messagebox
import graphviz as gv
from PIL import ImageTk, Image
import networkx as nx
import matplotlib.pyplot as plt
import csv

graph = gv.Digraph("grafo1")
path_file = "Short.csv"
diccionario = {}
diccionario2 = [None] * 21
valor_ini = 0
valor_fin = 0
ruta = []
path = []

ladj = [[] for _ in range(21)]
lista_general = []
nombre_archivo = "Short.csv"
with open(nombre_archivo, "r") as archivo:
    lector = csv.reader(archivo, delimiter=",")
    for fila in lector:
        partida_iata = fila[0]
        destino_iata = fila[1]
        t_hora = fila[2][0:1]
        t_min = fila[3][0:1]
        t_total = int(t_hora) * 60 + int(t_min)
        lista_general.append([partida_iata, destino_iata, t_total])

def agregar_arista(G, u, v, w=1, di=True):
    G.add_edge(u, v, weight=w)

    # Si el grafo no es dirigido
    if not di:
        # Agrego otra arista en sentido contrario
        G.add_edge(v, u, weight=w)

def instanciaryañadir(list):
    G = nx.Graph()
    for i in range(len(lista_general)):
        for j in range(len(list)):
            if (list[j]==lista_general[i][0]) and (lista_general[i][1] in list):
                agregar_arista(G, lista_general[i][0], lista_general[i][1], lista_general[i][2])

    # Draw the networks
    pos = nx.layout.spring_layout(G)
    nx.draw_networkx(G, pos, with_labels=True, node_size=400, node_color="green", font_size=8, font_color="white",width=2, edge_color="black", alpha=0.9)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=6)
    plt.title("Grafo de los AITA")
    plt.show()



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


window = Tk()
window = window
window.geometry('1366x718')
window.resizable(0, 0)
window.title('Calculadora de Ruta')

# ============================background image============================
bg_frame = Image.open('images\\background1.png')
photo = ImageTk.PhotoImage(bg_frame)
bg_panel = Label(window, image=photo)
bg_panel.image = photo
bg_panel.pack(fill='both', expand='yes')

# ====== Frame =========================
lgn_frame = Frame(window, bg='#ffffff', width=1200, height=600)
lgn_frame.place(x=85, y=70)


# ==========FILTERS================
filter_frame = Image.open('images\\filters.png')
photo = ImageTk.PhotoImage(filter_frame)
filter_panel = Label(window, image=photo,bg='#ffffff')
filter_panel.image = photo
filter_panel.place(x=970, y=100)

nodeInput = Entry(window, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#4f4e4d",
                       font=("yu gothic ui ", 12, "bold"))
nodeInput.place(x=1030, y=264, width=230)

arista1Input = Entry(window, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#4f4e4d",
                       font=("yu gothic ui ", 12, "bold"))
arista1Input.place(x=1030, y=434, width=230)
arista2Input = Entry(window, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#4f4e4d",
                       font=("yu gothic ui ", 12, "bold"))
arista2Input.place(x=1030, y=485, width=230)

deleteNode_Button = Button(window, text='ELIMINAR',  font=("yu gothic ui", 13, "bold"), width=21, bd=0,
               bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white')
deleteNode_Button.place(x=1030, y=311)

deleteArista_Button = Button(window, text='ELIMINAR',  font=("yu gothic ui", 13, "bold"), width=21, bd=0,
               bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white')
deleteArista_Button.place(x=1030, y=541)

# ========================================================================
txt = "CALCULADOR DE RUTA MAS RAPIDA"
heading = Label(lgn_frame, text=txt, font=('yu gothic ui', 25, "bold"), bg="#ffffff", fg='black', bd=10, relief=FLAT)
heading.place(x=10, y=30, width=900, height=30)

# ============ Eliga su destino =============================================
label = Label(lgn_frame, text="Eliga su destino", bg="#ffffff", fg="#4f4e4d", font=("yu gothic ui", 17, "bold"))
label.place(x=380, y=93)

# ============================INICIO====================================
F_IATA_label = Label(lgn_frame, text="IATA INICIO", bg="#ffffff", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
F_IATA_label.place(x=100, y=160)

initialIATA = Entry(lgn_frame, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#4f4e4d",
                       font=("yu gothic ui ", 12, "bold"))
initialIATA.place(x=130, y=198, width=230)

F_line = Canvas(lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
F_line.place(x=100, y=223)

I_line = Canvas(lgn_frame, width=300, height=2.0, bg="#ffffff", highlightthickness=0)
I_line.place(x=100, y=355)

# ===== airport icon inicial =========
L_icon = Image.open('images\\initial_icon.png')
photo = ImageTk.PhotoImage(L_icon)
I_icon_label = Label(lgn_frame, image=photo, bg='#ffffff')
label.image = photo
I_icon_label.place(x=100, y=196)

# ============================FINAL====================================
E_IATA_label = Label(lgn_frame, text="IATA FINAL", bg="#ffffff", fg="#4f4e4d", font=("yu gothic ui", 13, "bold"))
E_IATA_label.place(x=550, y=160)

finalIATA = Entry(lgn_frame, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#4f4e4d",
                       font=("yu gothic ui", 12, "bold"))
finalIATA.place(x=580, y=198, width=230)

F_line = Canvas(lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
F_line.place(x=550, y=223)

# ======== airport icon FINAL ================
R_icon = Image.open('images\\end_icon.png')
photo = ImageTk.PhotoImage(R_icon)
F_icon_label = Label(lgn_frame, image=photo, bg='#ffffff')
F_icon_label.image = photo
F_icon_label.place(x=550, y=196)


var1 = IntVar()
Checkbutton(lgn_frame, text="Filtros", variable=var1,background="#ffffff",font=("yu gothic ui", 12, "bold"),bd="10").place(x=450, y=356)


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

        showDisplayableRute(ruta_final,secondIATA)

        ruta_final.append(secondIATA)
        instanciaryañadir(ruta_final)
        ruta.clear()

def showDisplayableRute(ruta_final_p,destination_airport):
    rutespath=[]
    for i in ruta_final_p:
        rutespath.append(i)
    rutespath.reverse()
    routesresut="Ruta: "
    for i in rutespath:
        routesresut=routesresut+" "+i+" "
    routesresut=routesresut+" "+ destination_airport
    showAirplane(routesresut)
    return routesresut
def showAirplane(routesresut_p):

    escala_frame = Image.open('images\\airplane.png')
    photo = ImageTk.PhotoImage(escala_frame)
    airplane_icon_label = Label(lgn_frame, image=photo, bg='#ffffff')
    airplane_icon_label.image = photo
    airplane_icon_label.place(x=550, y=380)
    label = Label(lgn_frame, text=routesresut_p, font=('yu gothic ui', 20, "bold"), bg="#ffffff", fg='black', bd=0, relief=FLAT)
    label.place(x=300, y=380)


_button = Image.open('images\\btn1.png')
photo = ImageTk.PhotoImage(_button)
_button_label = Label(lgn_frame, image=photo, bg='#ffffff')
_button_label.image = photo
_button_label.place(x=330, y=270)
calc_Button = Button(_button_label, text='CALCULAR', command=sendCalculateButton, font=("yu gothic ui", 13, "bold"), width=27, bd=0,
               bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white')
calc_Button.place(x=10, y=10)



# ========= Validate IATA ==================================================================

def showStatusIcons(first, end):
    invalidText="Campo incompleto"
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
