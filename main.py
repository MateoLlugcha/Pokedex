import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from poke_api import obtener_pokemon, efectividad_tipo  # Importa las funciones desde poke_api.py

def buscar_pokemon():
    pokemon_name = entry.get()
    pokemon_data = obtener_pokemon(pokemon_name)
    
    if pokemon_data:
        # Mostrar la información en la pestaña correspondiente
        update_tab1(pokemon_data)
        update_tab2(pokemon_data)
    else:
        name_label_tab1.config(text="Pokémon no encontrado")
        type_label_tab1.config(text="")
        img_label_tab1.config(image='')
        effectiveness_label_tab2.config(text="")
        img_label_tab2.config(image='')

def update_tab1(pokemon_data):
    # Mostrar el nombre y tipos del Pokémon en la pestaña 1
    name_label_tab1.config(text=f"Nombre: {pokemon_data['nombre']}")
    type_label_tab1.config(text=f"Tipos: {', '.join(pokemon_data['tipo'])}")
    
    # Mostrar la imagen del Pokémon si está disponible
    if pokemon_data['imagen']:
        mostrar_imagen(pokemon_data['imagen'])
    else:
        img_label_tab1.config(image='')

def update_tab2(pokemon_data):
    # Obtener y mostrar la efectividad del primer tipo (si hay varios tipos)
    if pokemon_data['tipo']:
        type_effectiveness = efectividad_tipo(pokemon_data['tipo'][0])
        if type_effectiveness:
            strong_against = ', '.join(type_effectiveness['strong_against'])
            weak_against = ', '.join(type_effectiveness['weak_against'])
            
            effectiveness_label_tab2.config(
                text=f"Fuerte contra: {strong_against}\nDébil contra: {weak_against}"
            )
        else:
            effectiveness_label_tab2.config(text="No se pudo obtener la efectividad del tipo")
    else:
        effectiveness_label_tab2.config(text="Tipo no disponible")
    
    # Mostrar la imagen del Pokémon en la pestaña 2
    if pokemon_data['imagen']:
        mostrar_imagen(pokemon_data['imagen'], tab='tab2')
    else:
        img_label_tab2.config(image='')

def mostrar_imagen(img_url, tab='tab1'):
    try:
        # Descargar la imagen desde la URL
        response = requests.get(img_url)
        response.raise_for_status()  # Lanza un error para códigos de estado HTTP 4xx/5xx
        
        # Abrir la imagen usando Pillow
        img_data = Image.open(BytesIO(response.content))
        img = ImageTk.PhotoImage(img_data)
        
        # Mostrar la imagen en el label adecuado
        if tab == 'tab1':
            img_label_tab1.config(image=img)
            img_label_tab1.image = img  # Guardar una referencia a la imagen
        elif tab == 'tab2':
            img_label_tab2.config(image=img)
            img_label_tab2.image = img  # Guardar una referencia a la imagen
    except Exception as e:
        # Mostrar un mensaje de error en la consola
        print(f"Error al mostrar la imagen: {e}")
        if tab == 'tab1':
            img_label_tab1.config(image='')
        elif tab == 'tab2':
            img_label_tab2.config(image='')

# Crear la ventana principal
root = tk.Tk()
root.title("PokeWea")

# Crear el widget Notebook (pestañas)
notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10, expand=True, fill='both')

# Crear las pestañas
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

# Añadir pestañas al widget Notebook
notebook.add(tab1, text='Información del Pokémon')
notebook.add(tab2, text='Efectividad de Tipos')

# Contenido para la pestaña 1
label1_tab1 = tk.Label(tab1, text="Información del Pokémon")
label1_tab1.pack(padx=10, pady=10)

entry = ttk.Entry(tab1)
entry.pack(padx=10, pady=10)

button = ttk.Button(tab1, text="Buscar", command=buscar_pokemon)
button.pack(padx=10, pady=10)

img_label_tab1 = tk.Label(tab1)  # Aquí se mostrará la imagen del Pokémon en la pestaña 1
img_label_tab1.pack(padx=10, pady=10)

name_label_tab1 = tk.Label(tab1, text="Nombre:")
name_label_tab1.pack(padx=10, pady=10)

type_label_tab1 = tk.Label(tab1, text="Tipos:")
type_label_tab1.pack(padx=10, pady=10)

# Contenido para la pestaña 2

img_label_tab2 = tk.Label(tab2)  # Aquí se mostrará la imagen del Pokémon en la pestaña 2
img_label_tab2.pack(padx=10, pady=10)

info_label_tab2 = tk.Label(tab2, text="Efectividad de Tipos de Pokémon")
info_label_tab2.pack(padx=10, pady=10)

effectiveness_label_tab2 = tk.Label(tab2, text="Efectividad:")
effectiveness_label_tab2.pack(padx=10, pady=10)



# Iniciar el bucle principal de Tkinter
root.mainloop()
