import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import letter
import mysql.connector
import tkinter.messagebox as messagebox
from reportlab.pdfgen import canvas
from datetime import date
from PyPDF2 import PdfWriter, PdfReader

import tkinter.messagebox as messagebox
from tkinter import simpledialog  # Importar el módulo simpledialog para ingresar el número de cuenta
from PyPDF2 import PdfWriter
from datetime import date


def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Adoracion1324",
        database="Test"
    )
conn = conectar_bd()

def generar_pdf_movimientos(conn):
    # Pedir al usuario que ingrese el número de cuenta
    numero_cuenta = simpledialog.askstring("Ingresar número de cuenta", "Por favor ingrese el número de cuenta:")

    # Verificar si el número de cuenta existe en la base de datos
    cursor = conn.cursor()
    select_query = "SELECT * FROM movimientos WHERE numero_de_cuenta = %s"
    cursor.execute(select_query, (numero_cuenta,))
    movimientos = cursor.fetchall()
    cursor.close()

    # Si no hay movimientos para el número de cuenta especificado, mostrar un mensaje de error
    if not movimientos:
        messagebox.showerror("Error", "No hay movimientos para el número de cuenta especificado.")
        return

    # Crear un nuevo PDF
    ruta_pdf = f"movimientos_cuenta_{numero_cuenta}_{date.today()}.pdf"
    c = canvas.Canvas(ruta_pdf, pagesize=letter)
    c.drawImage("images.png", 50, 750 - 50, width=250, height=100)
    # Agregar el mensaje
    
    # Agregar los movimientos al PDF
    y = 680 - 50  # Posición vertical inicial
    for movimiento in movimientos:
        # Formatear el texto con la fecha, número de cuenta y valor del movimiento
        texto_movimiento = f"Fecha: {movimiento[3]}, Número de Cuenta: {movimiento[2]}, Valor: {movimiento[1]}"
        # Agregar el texto al PDF
        c.drawString(100, y, texto_movimiento)
        y -= 20  # Espaciado entre movimientos
    mensaje = "Do not share with anybody. This is the data of your personal account."
    c.drawString(50, 700 - 50, mensaje)

    # Guardar el PDF
    c.save()
    pdf_writer = PdfWriter()
    pdf_reader = PdfReader(ruta_pdf)
    for page in pdf_reader.pages:
        pdf_writer.add_page(page)
    pdf_writer.encrypt("bancolombia")

    # Guardar el PDF encriptado
    with open(ruta_pdf, "wb") as encrypted_pdf:
        pdf_writer.write(encrypted_pdf)
    messagebox.showinfo("Éxito", f"Se ha generado el PDF con los movimientos en la siguiente ruta:\n{ruta_pdf}")

# Crear un botón para generar el PDF de los movimientos

def registrar_cuenta(conn):
    # Retrieve the values from entry fields
    numero_cuenta = entry_cuenta.get()
    saldo = float(entry_saldo.get())
    titular = entry_titular.get()
    tipo_de_cuenta = entry_tipo_cuenta.get()  # Retrieve the tipo_de_cuenta value

    # Insert the data into the database
    cursor = conn.cursor()
    insert_query = "INSERT INTO cuentas (numero_de_cuenta, saldo, titular, tipo_de_cuenta) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(insert_query, (numero_cuenta, saldo, titular, tipo_de_cuenta))
        conn.commit()
        messagebox.showinfo("Éxito", "Los datos fueron subidos satisfactoriamente")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al subir los datos: {str(e)}")
    finally:
        cursor.close()
def registrar_movimiento(conn):
    # Obtener la fecha actual
    fecha_actual = date.today()

    # Obtener los datos del movimiento desde los campos de entrada
    valor_movimiento = float(entry_movimiento.get())
    numero_cuenta_movimiento = entry_numcuenta.get()

    # Verificar si el número de cuenta existe en la base de datos
    cursor = conn.cursor()
    select_query = "SELECT * FROM cuentas WHERE numero_de_cuenta = %s"
    cursor.execute(select_query, (numero_cuenta_movimiento,))
    cuenta_existente = cursor.fetchone()
    cursor.close()

    # Si el número de cuenta no existe, mostrar un mensaje de error
    if not cuenta_existente:
        messagebox.showerror("Error", "El número de cuenta no existe.")
        return

    # Si el número de cuenta existe, registrar el movimiento en la base de datos
    cursor = conn.cursor()
    insert_query = "INSERT INTO movimientos (valor, numero_de_cuenta, fecha) VALUES (%s, %s, %s)"
    try:
        cursor.execute(insert_query, (valor_movimiento, numero_cuenta_movimiento, fecha_actual))
        conn.commit()
        messagebox.showinfo("Éxito", "El movimiento fue registrado satisfactoriamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al registrar el movimiento: {str(e)}")
    finally:
        cursor.close()

# Función para cargar una imagen y mostrarla en un widget Label
def cargar_imagen(ruta, width, height):
    imagen = Image.open(ruta)
    imagen = imagen.resize((width, height))
    imagen = ImageTk.PhotoImage(imagen)
    return imagen

# Crear la ventana principal
root = tk.Tk()
root.title("Registro de Cuentas y Movimientos")

# Establecer el fondo de color blanco en toda la ventana
root.configure(bg="white")

# Crear un estilo para los widgets
style = ttk.Style()

# Cargar las imágenes
imagen_cuenta = cargar_imagen("bancolombia.png", 100, 100)
imagen_movimiento = cargar_imagen("movimientos.png", 100, 100)

# Crear y posicionar los elementos de la interfaz
frame_cuenta = ttk.Frame(root, padding="20")
frame_cuenta.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

label_imagen_cuenta = ttk.Label(frame_cuenta, image=imagen_cuenta)
label_imagen_cuenta.grid(row=0, column=0, columnspan=2)

label_crearcuenta = ttk.Label(frame_cuenta, text="Crea una cuenta", font=("Helvetica", 14, "bold"))
label_crearcuenta.grid(row=1, column=0, columnspan=2, pady=10)

label_cuenta = ttk.Label(frame_cuenta, text="Número de Cuenta:")
label_cuenta.grid(row=2, column=0, sticky="w")
entry_cuenta = ttk.Entry(frame_cuenta)
entry_cuenta.grid(row=2, column=1, padx=10, pady=5)

label_saldo = ttk.Label(frame_cuenta, text="Saldo:")
label_saldo.grid(row=3, column=0, sticky="w")
entry_saldo = ttk.Entry(frame_cuenta)
entry_saldo.grid(row=3, column=1, padx=10, pady=5)

label_titular = ttk.Label(frame_cuenta, text="Titular:")
label_titular.grid(row=4, column=0, sticky="w")
entry_titular = ttk.Entry(frame_cuenta)
entry_titular.grid(row=4, column=1, padx=10, pady=5)

label_tipo_cuenta = ttk.Label(frame_cuenta, text="Tipo de Cuenta:")
label_tipo_cuenta.grid(row=5, column=0, sticky="w")
entry_tipo_cuenta = ttk.Entry(frame_cuenta)
entry_tipo_cuenta.grid(row=5, column=1, padx=10, pady=5)

button_registrar_cuenta = ttk.Button(frame_cuenta, text="Registrar Cuenta", command=lambda: registrar_cuenta(conn), cursor="hand2")
button_registrar_cuenta.grid(row=6, column=0, columnspan=2, pady=10)

frame_movimiento = ttk.Frame(root, padding="20")
frame_movimiento.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

label_imagen_movimiento = ttk.Label(frame_movimiento, image=imagen_movimiento)
label_imagen_movimiento.grid(row=0, column=0, columnspan=2)

label_ingresarmovimiento = ttk.Label(frame_movimiento, text="Ingresa un movimiento", font=("Helvetica", 14, "bold"))
label_ingresarmovimiento.grid(row=1, column=0, columnspan=2, pady=10)

label_numcuenta = ttk.Label(frame_movimiento, text="Número de Cuenta:")
label_numcuenta.grid(row=2, column=0, sticky="w")
entry_numcuenta = ttk.Entry(frame_movimiento)
entry_numcuenta.grid(row=2, column=1, padx=10, pady=5)

label_movimiento = ttk.Label(frame_movimiento, text="Valor del Movimiento:")
label_movimiento.grid(row=3, column=0, sticky="w")
entry_movimiento = ttk.Entry(frame_movimiento)
entry_movimiento.grid(row=3, column=1, padx=10, pady=5)

button_registrar_movimiento = ttk.Button(frame_movimiento, text="Registrar Movimiento", command=lambda: registrar_movimiento(conn), cursor="hand2")
button_registrar_movimiento.grid(row=4, column=0, columnspan=2, pady=10)

button_generar_pdf = ttk.Button(frame_movimiento, text="Generar PDF de Movimientos", command=lambda: generar_pdf_movimientos(conn), cursor="hand2")
button_generar_pdf.grid(row=5, column=0, columnspan=2, pady=10)
# Establecer el tamaño mínimo de las columnas y filas para que no cambie el tamaño de los widgets
root.grid_columnconfigure(0, weight=1, minsize=250)
root.grid_columnconfigure(1, weight=1, minsize=250)
root.grid_rowconfigure(0, weight=1)

# Ejecutar la interfaz
root.mainloop()
