from tkinter import *
from tkinter import messagebox
import heapq as hp
import graphviz as gv
from PIL import ImageTk, Image
import networkx as nx
import matplotlib.pyplot as plt
import math
import csv


graph = gv.Digraph("grafo1")
path_file = "Short.csv"
diccionario = {}
diccionario2 = [None]*20

deleteAirportFilter=False
deleteAristaFilter=False

ladj = [[] for _ in range(21)]

ruta = []

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

def Dijkstra(graph, start, final):
    n = len(graph)
    visited = [False]*n
    path = [None]*n
    cost = [float('inf')]*n
    cost[start] = 0

    # Cola de Prioridad
    pq = []
    pq.append((0,start))

    while pq:
        c , v = hp.heappop(pq)
        if not visited[v]:
            visited[v] = True
            for u, w in graph[v]:
                if not visited[u]:
                    if c + w < cost[u]:
                        cost[u] = c + w
                        path[u] = v
                        hp.heappush(pq,(cost[u],u))

    for i in range(len(path) - 1):
      if i == final:
        return cost[i]

def drawG_al(G, path=[]):
  n = len(G)
  added = set()
  for v, u in enumerate(path):
    if u != -1:
      graph.edge(diccionario2[u], diccionario2[v], dir="forward", penwidth="2", color="orange")
      added.add(f"{u},{v}")
      added.add(f"{v},{u}")
  for u in range(n):
    for i in G[u]:
      v = i[0]
      if not f"{u},{v}" in added:
        added.add(f"{u},{v}")
        added.add(f"{v},{u}")
        graph.edge(diccionario2[u], diccionario2[v], str(i[1]))
  return graph

def bfs_al(G, s):
  n = len(G)
  visited = [False]*n
  path = [-1]*n # parent
  queue = [s]
  visited[s] = True

  while queue:
    u = queue.pop(0)
    for i in G[u]:
      v = i[0]
      if not visited[v]:
        visited[v] = True
        path[v] = u
        queue.append(v)
  return path

def borrar_aeropuerto(lista, a):
    print("AEROPUERTO:",a)
    print(lista)
    ind = diccionario[a]
    lista[ind] = []
    print(lista)
    return print("Se borro el aeropuerto")

def borrar_arista(balde, origen, destino):
  ori = diccionario[origen]
  dest = diccionario[destino]
  print("ori",ori)
  print("dest",dest)


  lista = balde[ori]
  print("list",lista)

  if len(lista) == 1:
    balde[ori].pop(0)
  else:
    for i in range(len(lista) - 1):
      tupla = lista[i]
      if dest == tupla[0]:
        balde[ori].pop(i)
        #print("Se borro la arista con origen en {} y destino en {}".format(diccionario2[ori], diccionario2[dest]))

def horasMin(h):
  h = int(h)
  return 60*h

def escala(pos, path,firstIATA,secondIATA):
  valor_ini = diccionario[str(firstIATA)]
  valor_fin = diccionario[str(secondIATA)]
  if path[valor_fin] == -1:
    return []

  if pos == valor_ini:
    print("Y la ruta ES")
    print(path)
    return ruta

  ruta.append(diccionario2[path[pos]])
  return escala(path[pos], path,firstIATA,secondIATA)

def read_file(archivo):
  cont = 0
  cont2 = 0
  with open(archivo, "r") as archivo:
    for linea in archivo:
      linea = linea.rstrip()
      separador = ","
      lista = linea.split(",")

      #Recojo de datos
      salida = lista[0]
      destino = lista[1]
      fhora = lista[2]
      fmin = lista[3]

      #Validacion de Datos
      fhora = fhora.split("h")
      fhora.pop(1)
      hora = fhora[0]

      horaMin = horasMin(hora)

      fmin = fmin.split("m")
      fmin.pop(1)
      min = fmin[0]

      #Peso de la arista
      #val = str(hora) + "h " + str(min) + "m"
      val = int(horaMin) + int(min)

      #Validacion de diccionario (salida)
      if salida not in diccionario:
        diccionario[salida] = cont
        diccionario2[cont] = salida
        cont+=1

      #Validacion de diccionario (destino)
      if destino not in diccionario:
        diccionario[destino] = cont
        diccionario2[cont] = destino
        cont+=1

      #Creamos una lista de adyacencia
      ladj[diccionario[salida]].append((diccionario[destino], val))

  return ladj

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
    return 0

window = Tk()
window = window
window.geometry('1366x718')
window.resizable(0, 0)
window.title('Ruta mas rapida entre aeropuertos')

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

nodeInput = Entry(window, highlightthickness=0,relief=FLAT, bg="#ffffff", fg="#4f4e4d",
                       font=("yu gothic ui ", 12, "bold"))
nodeInput.place(x=1030, y=264, width=230)

arista1Input = Entry(window, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#4f4e4d",
                       font=("yu gothic ui ", 12, "bold"))
arista1Input.place(x=1030, y=434, width=230)

arista2Input = Entry(window, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#4f4e4d",
                       font=("yu gothic ui ", 12, "bold"))
arista2Input.place(x=1030, y=485, width=230)

# ========================================================================
txt = "Ruta mas rapida entre aeropuertos"
heading = Label(lgn_frame, text=txt, font=('yu gothic ui', 25, "bold"), bg="#ffffff", fg='black', bd=10, relief=FLAT)
heading.place(x=25, y=30, width=900, height=30)

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



# ============================Calculate button================================
contador=0
lista=[]

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
        global contador
        global lista
        if contador==0:
           lista = read_file(path_file)
           contador=contador+1

        showStatusIcons(True, True)
        valor_ini = diccionario[str(firstIATA)]
        valor_fin = diccionario[str(secondIATA)]

        print("SEND",deleteAirportFilter)
        if deleteAirportFilter:
            deleteAirport(ladj)
        if deleteAristaFilter:
            deleteAristas(ladj)

        path = bfs_al(lista, valor_ini)

        ruta_final = escala(valor_fin, path,firstIATA,secondIATA)
        showDisplayableRute(ruta_final,secondIATA)
        showDisplayableRuteTime(Dijkstra(ladj,valor_ini,valor_fin))
        ruta_final.append(secondIATA)

        #instanciaryañadir(ruta_final)
        ruta.clear()

def showDisplayableRute(ruta_final_p,destination_airport):
    rutespath=[]
    for i in ruta_final_p:
        rutespath.append(i)
    rutespath.reverse()
    routesresut="Ruta: "
    for i in rutespath:
        routesresut=routesresut+" "+i+" - "
    routesresut=routesresut+" "+ destination_airport
    print(routesresut)
    showAirplane(routesresut)
def showAirplane(routesresut_p):
    escala_frame = Image.open('images\\airplane.png')
    photo = ImageTk.PhotoImage(escala_frame)
    airplane_icon_label = Label(lgn_frame, image=photo, bg='#ffffff')
    airplane_icon_label.image = photo
    airplane_icon_label.place(x=600, y=450)
    label = Label(lgn_frame, text=routesresut_p, font=('yu gothic ui', 19,"bold"), bg="#ffffff", fg='black', bd=0, relief=FLAT)
    label.place(x=300, y=380)


def showDisplayableRuteTime(totalTime):
    timeInHours=math.floor(totalTime/60)
    timeInMinutes=totalTime-(timeInHours*60)
    timeFormat="Tiempo total: "+str(timeInHours)+" horas con "+str(timeInMinutes)+" minutos"
    showTimeFormat(timeFormat)

def showTimeFormat(timeFormat):
    label = Label(lgn_frame, text=timeFormat, font=('yu gothic ui', 19,"bold"), bg="#ffffff", fg='black', bd=0, relief=FLAT)
    label.place(x=260, y=430)

def deleteAirport(ladj_P):
    airport=nodeInput.get().upper()
    borrar_aeropuerto(ladj_P,str(airport) )
    return 0

def deleteAristas(ladj_P):
    firstArista=arista1Input.get().upper()
    secondArista=arista2Input.get().upper()
    borrar_arista(ladj_P,str(firstArista),str(secondArista))
    return 0

def EnableAirportFilter():
    global deleteAirportFilter
    deleteAirportFilter=True

def EnableAristasFilter():
    global deleteAristaFilter
    deleteAristaFilter=True

_button = Image.open('images\\btn1.png')
photo = ImageTk.PhotoImage(_button)
_button_label = Label(lgn_frame, image=photo, bg='#ffffff')
_button_label.image = photo
_button_label.place(x=330, y=270)
calc_Button = Button(_button_label, text='CALCULAR', command=sendCalculateButton, font=("yu gothic ui", 13, "bold"), width=27, bd=0,
               bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white')
calc_Button.place(x=10, y=10)

#======================FILTERS BUTTONS ================
deleteNode_Button = Button(window, text='ELIMINAR', command=EnableAirportFilter,  font=("yu gothic ui", 13, "bold"), width=21, bd=0,
               bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white')
deleteNode_Button.place(x=1030, y=311)

deleteArista_Button = Button(window, text='ELIMINAR', command=EnableAristasFilter,  font=("yu gothic ui", 13, "bold"), width=21, bd=0,
               bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white')
deleteArista_Button.place(x=1030, y=541)

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
