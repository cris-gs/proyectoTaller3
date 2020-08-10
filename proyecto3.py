from tkinter import *
from datetime import datetime
import cv2
import json
import jsonpickle
from visionAPI import reconocer_caras
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk
from PIL import Image
from tkinter import messagebox

#Crea la ventan principal de la interfaz grafica
ventana = tk.Tk()
ventana.geometry("250x200")
ventana.title("Asistencia")
menu = Menu(ventana)
new_item = Menu(menu)

#lista en la cual se cargan los datos recaudados por medio de las diferentes funciones 
lista=[]
respaldo=[]

def Asistencia():
    """[Esta función crea una ventana secundaria en la cual se carga los botones y 
    entrys los cuales vana permitir realizar las distintas funciones mencionasdas más adelante]
    """
    
    #ventana secundaria
    ventana1= Tk()
    ventana1.title("Datos")
    ventana1.geometry("350x190")
    #se crea un entry que cuenta con un label a su izquierda para especificar que se mostrara el numerod e cedula
    label = Label(ventana1, text="Cedula")
    label.grid(column=0,row=0,padx=(10,10), pady=(10,10))
    entry = Entry(ventana1)
    entry.grid(column=1,row=0,padx=(10,10), pady=(10,10))
     #se crea un entry que cuenta con un label a su izquierda para especificar que se mostrara el codigo del gurso
    label2 = Label(ventana1, text="#Curso")
    label2.grid(column=0,row=1,padx=(10,10), pady=(10,10))
    entry2 = Entry(ventana1)
    entry2.grid(column=1,row=1,padx=(10,10), pady=(10,10))

    class registro():
        """[clase por la cual se van a administrar los datos para luego enviarlos al arbol]
        """
        fecha=None
        codigo_curso=None
        Cedula=None
        emocion=None
        def __init__(self, fecha, codigo_curso, cedula, emocion):
            self.fecha=fecha
            self.codigo_curso=codigo_curso
            self.Cedula=cedula
            self.emocion=emocion
           
        def __str__(self):
            string = u"[<asistencia> fecha:%s codigo del curso:%s Cedula:%s emocion:%s]" %(self.fecha, self.codigo_curso, self.Cedula, self.emocion)
            return string
        
    def insert():
        """[Esta funcion sera llamda por medio del boton Leer Codigo y esta llama a la funcion codigo
        para que esta active la camara y tome una fotogracia del codigo Qr del carnet del estudiante
        y por medio de la lectura asigna a los dos entry anteriormente creados para asi permitirle
        al usuario editar la informacion que se encuestra en este.]
        """
        codigo()
        entry.insert(0,a)
        entry2.insert(0,b)
    
    def subir_asistencia():
        """[Esta funcion es llamada por medio del boton guardar, lo que hace esta es definir la fecha,
        datos que se encuentrar en los entry ya se que se hayan modificado o no, y las emociones de 
        de la foto del estudiantes ya haya sido cargada o tomada.]
        """
        Fecha=datetime.now()
        dato1=entry.get()
        dato2=entry2.get()
        lista.append(registro(Fecha,dato2,dato1,total))
        
    def guardar():
        a_file = open("registros.bin", "w")
        json.dump(lista, a_file)
        a_file.close()

    def abrir():    
        a_file = open("registros.bin", "r")
        salida = a_file.read()
        print(salida)

    def salir():
        """[Funcion que permite cerrar la ventana secundaria de la interfaz grafica]
        """
        ventana1.destroy()

    #Boton que permite tomar una fotografia del codigo Qr
    btn = Button(ventana1, text="Leer Codigo",command=insert)
    btn.grid(column=0, row=2,padx=(10,10), pady=(10,10))

    #Boton que permite tomar una forografia al estudiante para reconocer la emosiones con las 
    btn = Button(ventana1, text="Tomar Foto",command=tomar_foto)
    btn.grid(column=1, row=2,padx=(10,10), pady=(10,10))

    #Boton que permite al estudiante seleccionar una foto desde su explorador de archivos
    btn = Button(ventana1, text="Cargar Foto",command=cargar_foto)
    btn.grid(column=2, row=2,padx=(10,10), pady=(10,10))

    #Boton para cargarla fecha, cedula, codigo del curso y emosiones en el arbol.
    btn = Button(ventana1, text="Subir asistencia",command=subir_asistencia)
    btn.grid(column=2, row=0,padx=(10,10), pady=(10,10))

    #Boton para ver la asistencia anteriormente guardada en archivos.
    btn = Button(ventana1, text="ver registros",command=abrir)
    btn.grid(column=0, row=3,padx=(10,10), pady=(10,10))

    #Boton para guardar la fecha, cedula, codigo del curso y emosiones en archivos.
    btn = Button(ventana1, text="Guardar", command=guardar)
    btn.grid(column=1, row=3,padx=(10,10), pady=(10,10))

    #Boton para salir de la ventana 
    btn = Button(ventana1, text="Salir",command=salir)
    btn.grid(column=2, row=3,padx=(10,10), pady=(10,10))
   


    ventana1.mainloop()
    
def cargar_foto ():
    """[permite seleccionar una imagen para cargarla y ser reconocida, extraela ubicaion de 
    la imagen seleccionada y la almacena en un archivo temporal txt para separar la ubicacion
    de los demas datos que tiene la variable ventana.filename]
    """
    ventana.filename =  filedialog.askopenfile(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    
    a=str(ventana.filename)
    print(a)
    b=a.find("mode")
    textfile=open("ubicacion_tmp.txt","tw")
    textfile.write(a)
    textfile.seek(23)
    textfile.write("\n")
    textfile.seek(b-2)
    textfile.write("\n")
    textfile.close()

    
    "____________________________________________________________________________________________________________"
    def lee_Lineas(n,archivo):
        """[funcion que permite recorrel el archivo txt temporal que se creo para separar la ubicacion de los demas
        datos asi extrayendo solamete la ubicacion de la imagen selecciona y asignadola a una variable]

        Args:
            n ([type:str]): [Esta es una varaible que se asigna al llamar la funcion, que es el numero de lineas que
            tiene el archivo txt que se lea y asi saber cauntas veces ralizar el ciclo de lectura]
            archivo ([type:str]): [este es el nombre del archivo que se debe abrir e igual mente es  una variable que
            obtiene el valor a la hora de llamar a la funcion]
        """
        file=open(archivo,"tr")
        respuesta=list()
        while n>1:
            linea=""
            caracter=file.read(1)
            if caracter!="":
                while True:
                    if caracter=="\n":
                        break
                    else:                        linea+=caracter
                    caracter=file.read(1)
            if caracter!="":
                respuesta.append(linea)
            else:
                respuesta.append(None)
            n-=1
        file.close()   
        return(respuesta)
    l=str(lee_Lineas(3,"ubicacion_tmp.txt")[1])#llama a la funcion lee lineas
    r=reconocer_caras(l)#obtine los resultados del metodo reconocer caras llamado desde visionAPI.py}
    if len(r)>1: #detecta existe mas de un rostro en la imagen cargada
        messagebox.showinfo('Error!', 'Más de un rostro')
    else:
        conteo=(r[0]["face_expressions"]["joy_likelihood"])
        valor=0
        if conteo=="VERY_LIKELY":
            valor=valor+5
        elif conteo=="LIKELY":
            valor=valor+4
        elif conteo=="POSSIBLE":
            valor=valor+3
        elif conteo=="UNLIKELY":
            valor=valor+2
        elif conteo=="VERY_UNLIKELY":
            valor=valor+0
        valor=((valor/1)*20)
        conteo=(r[0]["face_expressions"]["sorrow_likelihood"])
        valor1=0
        if conteo=="VERY_LIKELY":
            valor1=valor1+5
        elif conteo=="LIKELY":
            valor1=valor1+4
        elif conteo=="POSSIBLE":
            valor1=valor1+3  
        elif conteo=="UNLIKELY":
            valor1=valor1+2
        elif conteo=="VERY_UNLIKELY":
            valor1=valor1+0
        valor1=((valor1/1)*20)
        conteo=(r[0]["face_expressions"]["anger_likelihood"])
        valor2=0
        if conteo=="VERY_LIKELY":
            valor2=valor2+5
        elif conteo=="LIKELY":
            valor2=valor2+4
        elif conteo=="POSSIBLE":
            valor2=valor2+3
        elif conteo=="UNLIKELY":
            valor2=valor2+2
        elif conteo=="VERY_UNLIKELY":
            valor2=valor2+0
        valor2=((valor2/1)*20)
        conteo=(r[0]["face_expressions"]["surprise_likelihood"])
        valor3=0
        if conteo=="VERY_LIKELY":
            valor3=valor3+5
        elif conteo=="LIKELY":
            valor3=valor3+4
        elif conteo=="POSSIBLE":
            valor3=valor3+3
        elif conteo=="UNLIKELY":
            valor3=valor3+2
        elif conteo=="VERY_UNLIKELY":
            valor3=valor3+0
        valor3=((valor3/1)*20)
        conteo=(r[0]["face_expressions"]["under_exposed_likelihood"])
        valor4=0
        if conteo=="VERY_LIKELY":
            valor4=valor4+5
        elif conteo=="LIKELY":
            valor4=valor+4
        elif conteo=="POSSIBLE":
            valor4=valor4+3
        elif conteo=="UNLIKELY":
            valor4=valor4+2
        elif conteo=="VERY_UNLIKELY":
            valor4=valor4+0
        valor4=((valor4/1)*20)
        conteo=(r[0]["face_expressions"]["blurred_likelihood"])
        valor5=0
        if conteo=="VERY_LIKELY":
            valor5=valor5+5
        elif conteo=="LIKELY":
            valor5=valor5+4
        elif conteo=="POSSIBLE":
            valor5=valor5+3
        elif conteo=="UNLIKELY":
            valor5=valor5+2
        elif conteo=="VERY_UNLIKELY":
            valor5=valor5+0
        valor5=((valor5/1)*20)
        conteo=(r[0]["face_expressions"]["headwear_likelihood"])
        valor6=0
        if conteo=="VERY_LIKELY":
            valor6=valor6+5
        elif conteo=="LIKELY":
            valor6=valor6+4
        elif conteo=="POSSIBLE":
            valor6=valor6+3
        elif conteo=="UNLIKELY":
            valor6=valor6+2
        elif conteo=="VERY_UNLIKELY":
            valor6=valor6+0
        valor6=((valor6/1)*20)

        """[convierten el valor de reconocimiento de cada expresion facial a un str para luego concatenarce con el
        el nombre de cada una de estas expresiones al mostrarse en la ventana de la interfaz grafica]
        """
        #crea las variables de forma global para ser utilizadas por la clase registro
        lmayor=[]
        e=["Felicidad:","tristeza:","ira:","sorpresa:","subexpuesta:","borrosa:","sombrero:"]
        global total
        v1=(str(valor))
        v2=(str(valor1))
        v3=(str(valor2))
        v4=(str(valor3))
        v5=(str(valor4))
        v6=(str(valor5))
        v7=(str(valor6))
        lmayor.append(v1)
        lmayor.append(v2)
        lmayor.append(v3)
        lmayor.append(v4)
        lmayor.append(v5)
        lmayor.append(v6)
        lmayor.append(v7)
        numero=max(lmayor)
        dato=(lmayor.index(numero))
        palabra=e[dato]
        total=palabra+str(numero)
        
def codigo():
    """[toma una fotografia del codigo Qr]
    """
    
    #Captura de fotografía basado en la cámara
    cap = cv2.VideoCapture(0)
    leido, frame = cap.read()
    if leido == True:
        cv2.imwrite("codigo.png", frame)
        print("Foto tomada correctamente")
    else:
        print("Error al acceder a la cámara")
    cap.release()
    img=cv2.imread(r'codigo.png')
    detector=cv2.QRCodeDetector()
    data, points, stight_code = detector.detectAndDecode(img)
    #separa el numero de cedual del codigo del surso y se asigna a dos variables distintas
    global a
    global b                       
    a=data[0:8]
    b=data[9:]
   
def tomar_foto():
    """[permite tomar una forografia al estudiantes y cargarla al visionAPI de google para reconocer las
    emociones]
    """
    #Captura de fotografía basado en la cámara
    cap = cv2.VideoCapture(0)
    leido, frame = cap.read()
    if leido == True:
        cv2.imwrite("estudiante.png", frame)
        print("Foto tomada correctamente")
    cap.release() 
    global r
    r=reconocer_caras("estudiante.png")
    if len(r)>1: 
        messagebox.showinfo('Error!', 'Más de un rostro')
    else:
        conteo=(r[0]["face_expressions"]["joy_likelihood"])
        valor=0
        if conteo=="VERY_LIKELY":
            valor=valor+5
        elif conteo=="LIKELY":
            valor=valor+4
        elif conteo=="POSSIBLE":
            valor=valor+3
        elif conteo=="UNLIKELY":
            valor=valor+2
        elif conteo=="VERY_UNLIKELY":
            valor=valor+0
        valor=((valor/1)*20)
        conteo=(r[0]["face_expressions"]["sorrow_likelihood"])
        valor1=0
        if conteo=="VERY_LIKELY":
            valor1=valor1+5
        elif conteo=="LIKELY":
            valor1=valor1+4
        elif conteo=="POSSIBLE":
            valor1=valor1+3  
        elif conteo=="UNLIKELY":
            valor1=valor1+2
        elif conteo=="VERY_UNLIKELY":
            valor1=valor1+0
        valor1=((valor1/1)*20)
        conteo=(r[0]["face_expressions"]["anger_likelihood"])
        valor2=0
        if conteo=="VERY_LIKELY":
            valor2=valor2+5
        elif conteo=="LIKELY":
            valor2=valor2+4
        elif conteo=="POSSIBLE":
            valor2=valor2+3
        elif conteo=="UNLIKELY":
            valor2=valor2+2
        elif conteo=="VERY_UNLIKELY":
            valor2=valor2+0
        valor2=((valor2/1)*20)
        conteo=(r[0]["face_expressions"]["surprise_likelihood"])
        valor3=0
        if conteo=="VERY_LIKELY":
            valor3=valor3+5
        elif conteo=="LIKELY":
            valor3=valor3+4
        elif conteo=="POSSIBLE":
            valor3=valor3+3
        elif conteo=="UNLIKELY":
            valor3=valor3+2
        elif conteo=="VERY_UNLIKELY":
            valor3=valor3+0
        valor3=((valor3/1)*20)
        conteo=(r[0]["face_expressions"]["under_exposed_likelihood"])
        valor4=0
        if conteo=="VERY_LIKELY":
            valor4=valor4+5
        elif conteo=="LIKELY":
            valor4=valor+4
        elif conteo=="POSSIBLE":
            valor4=valor4+3
        elif conteo=="UNLIKELY":
            valor4=valor4+2
        elif conteo=="VERY_UNLIKELY":
            valor4=valor4+0
        valor4=((valor4/1)*20)
        conteo=(r[0]["face_expressions"]["blurred_likelihood"])
        valor5=0
        if conteo=="VERY_LIKELY":
            valor5=valor5+5
        elif conteo=="LIKELY":
            valor5=valor5+4
        elif conteo=="POSSIBLE":
            valor5=valor5+3
        elif conteo=="UNLIKELY":
            valor5=valor5+2
        elif conteo=="VERY_UNLIKELY":
            valor5=valor5+0
        valor5=((valor5/1)*20)
        conteo=(r[0]["face_expressions"]["headwear_likelihood"])
        valor6=0
        if conteo=="VERY_LIKELY":
            valor6=valor6+5
        elif conteo=="LIKELY":
            valor6=valor6+4
        elif conteo=="POSSIBLE":
            valor6=valor6+3
        elif conteo=="UNLIKELY":
            valor6=valor6+2
        elif conteo=="VERY_UNLIKELY":
            valor6=valor6+0
        valor6=((valor6/1)*20)

        """[convierten el valor de reconocimiento de cada expresion facial a un str para luego concatenarce con el
        el nombre de cada una de estas expresiones al mostrarse en la ventana de la interfaz grafica]
        """
        #crea las variables de forma global para ser utilizadas por la clase registro
        lmayor=[]
        e=["Felicidad:","tristeza:","ira:","sorpresa:","subexpuesta:","borrosa:","sombrero:"]
        global total
        v1=(str(valor))
        v2=(str(valor1))
        v3=(str(valor2))
        v4=(str(valor3))
        v5=(str(valor4))
        v6=(str(valor5))
        v7=(str(valor6))
        lmayor.append(v1)
        lmayor.append(v2)
        lmayor.append(v3)
        lmayor.append(v4)
        lmayor.append(v5)
        lmayor.append(v6)
        lmayor.append(v7)
        numero=max(lmayor)
        dato=(lmayor.index(numero))
        palabra=e[dato]
        total=palabra+str(numero)



  




#menu principal para entrar a la segunda ventana

#abre la ventana para el registro de asistencia
new_item.add_command(label='Asistencia', command=Asistencia)

#permite cerrar la ventana
new_item.add_command(label='Salir', command=ventana.destroy)

menu.add_cascade(label='Opciones', menu=new_item)

ventana.config(menu=menu)

ventana.mainloop()

