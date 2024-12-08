import tkinter as tk
from tkinter import messagebox
import math

## Funciones ##

def calcular_xp_base(nivel_mob):
    return (nivel_mob * 5) + 45

def zd(nivel_jugador):
    if 1 <= nivel_jugador <= 9:
        return 5
    elif 10 <= nivel_jugador <= 19:
        return 6
    elif 20 <= nivel_jugador <= 29:
        return 7
    elif 30 <= nivel_jugador <= 39:
        return 8
    elif 40 <= nivel_jugador <= 44:
        return 9
    elif 45 <= nivel_jugador <= 49:
        return 11
    elif 50 <= nivel_jugador <= 54:
        return 12
    elif 55 <= nivel_jugador <= 59:
        return 13
    else:
        return None

def calcular_xp_mob(nivel_jugador, nivel_mob):
    valor_zd = zd(nivel_jugador)
    if valor_zd is None:
        raise ValueError("El nivel del jugador debe estar entre 1 y 59!")
    if nivel_mob >= nivel_jugador:  
        diferencia = nivel_mob - nivel_jugador
        xp_base = calcular_xp_base(nivel_mob)
        return xp_base * (1 + 0.05 * min(diferencia, 4))  
    else:  
        diferencia = nivel_jugador - nivel_mob
        xp_base = calcular_xp_base(nivel_mob) 
        if diferencia <= valor_zd:  
            return xp_base * (1 - (diferencia / valor_zd))
        else:  
            return 0

def calcular_mobs_necesarios(nivel_jugador, nivel_mob, xp_para_subir):
    xp_por_mob = calcular_xp_mob(nivel_jugador, nivel_mob)
    if xp_por_mob > 0:
        return math.ceil(xp_para_subir / xp_por_mob)
    return float('inf')

def calcular_mobs():
    try:
        nivel_jugador = int(nivel_jugador_entry.get())
        nivel_mob = int(nivel_mob_entry.get())
        
        if nivel_jugador < 1 or nivel_jugador >= 60:
            messagebox.showerror("Error...", "El nivel del jugador debe estar entre 1 y 59.")
            return

        if nivel_mob < 1 or nivel_mob > 60:
            messagebox.showerror("Error...", "El nivel del mob debe estar entre 1 y 60.")
            return

        xp_para_subir = xp_para_subir_de_nivel[nivel_jugador]
        mobs_necesarios = calcular_mobs_necesarios(nivel_jugador, nivel_mob, xp_para_subir)

        if mobs_necesarios == float('inf'):
            result_label.config(text="El mob no te otorgará experiencia a ese nivel (Zona Gris)...")
        else:
            result_label.config(text=f"Necesitarás derrotar {mobs_necesarios} mobs.")
    except ValueError:
        messagebox.showerror("Error!!", "Por favor, ingresa valores numéricos positivos para los niveles.")

def cambio_razas(*args): ## No sabemos como ni porque funciona esto de *args, nos ayudo un foro de internet ##
    faccion = faccion_var.get()
    menu_razas = raza_menu["menu"]
    menu_razas.delete(0, "end")
    for raza in facciones[faccion]:
        menu_razas.add_command(label=raza, command=tk._setit(raza_var, raza))
    raza_var.set(list(facciones[faccion])[0])

## Datos para las funciones ##
xp_para_subir_de_nivel = {
    nivel: xp for nivel, xp in enumerate(
        [400, 900, 1400, 2100, 2800, 3600, 4500, 5400, 6500, 7600,
         8800, 10100, 11400, 12900, 14400, 16000, 17700, 19400, 21300, 23200,
         25200, 27300, 29400, 31700, 34000, 36400, 38900, 41400, 44300, 47400,
         50800, 54500, 58600, 62800, 67100, 71600, 76100, 80800, 85700, 90700,
         95800, 101000, 106300, 111800, 117500, 123200, 129100, 135100, 141200,
         147500, 153900, 160400, 167100, 173900, 180800, 187900, 195000, 202300,
         209800], start=1
    )
}

facciones = {
    "Horda": {"Nomuerto", "Tauren", "Trol", "Orco"},
    "Alianza": {"Humano", "Enano", "Elfo", "Gnomo"}
}

## Interfaz ##

root = tk.Tk()
root.title("Simulador de Experiencia WoW Classic")
root.geometry("854x480")
root.configure(bg="#1e1e1e")

frame_inicio = tk.Frame(root, bg="#1e1e1e")
frame_simulador = tk.Frame(root, bg="#1e1e1e")

for frame in (frame_inicio, frame_simulador):
    frame.place(relwidth=1, relheight=1)

def mostrar_frame(frame):
    frame.tkraise()

def salir():
    root.destroy()

def mostrar_informacion():
    messagebox.showinfo(
        "Ayuda",
        "¡Bienvenid@ al Simulador de Experiencia de WoW Classic!\n\n"
        "En este programa, pordrás calcular cuántos mobs necesitas derrotar para subir de nivel en WoW Classic.\n\n"
        "¿Cómo funciona?\n\n"
        "El usuario escoge su facción y raza (las cuales no influyen realmente en el cálculo) y escoge el nivel de su personaje y el nivel del mob que quiere derrotar.\n"
        "El programa entonces tomará el nivel del jugador y del mob y a partir de estos calculará la cantindad necesaria de mobs de dicho nivel necesarios para subir de nivel.\n"
        "Naturalmente hay factores que afectan el resultado, como la diferencia entre el nivel del mob y del jugador, y el rango en que se encuentran.\n\n"
        "¿Bueno... y qué es un MOB?\n\n"
        "En WoW, un MOB, o Mobile Object, es un enemigo o criatura que te da experiencia cuando lo derrotas.\n"
        "En relación a lo anterior, si un mob se encuentra en la Zona Gris, este no te dará experiencia.\n\n"
        "¿Qué es la Zona Gris?\n\n"
        "La Zona gris en WoW se refiere al rango de nivel en el que un mob deja de darte experiencia.\n"
        "Este rango está definido de forma distinta para cada intervalo de niveles. Por ejemplo, entre nivel 10-19, los mobs que tengan una diferencia de 6 niveles con respecto al del jugador, no otorgarán experiencia.\n\n"
        "¡Muchas gracias por preferir nuestro programa!"
    )

## Pantalla de Inicio ## ## Todo lo de TK fue realizado con ayuda de foros tambien ##

tk.Label(frame_inicio, text="Simulador de Experiencia de WoW Classic", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="#E5D8B0").pack(pady=50)
tk.Button(frame_inicio, text="Comenzar", command=lambda: mostrar_frame(frame_simulador), bg="#3F3026", fg="#E5D8B0", activebackground="#3F3026").pack(pady=10)
tk.Button(frame_inicio, text="Ayuda", command=mostrar_informacion, bg="#3F3026", fg="#E5D8B0", activebackground="#3F3026").pack(pady=10)
tk.Button(frame_inicio, text="Salir", command=salir, bg="#805A3B", fg="#E5D8B0", activebackground="#805A3B").pack(pady=10)

## Pantalla con la calculadora ##

tk.Label(frame_simulador, text="Simulador de Experiencia de WoW Classic", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="#E5D8B0").pack(pady=10)

tk.Label(frame_simulador, text="Selecciona tu facción:", bg="#1e1e1e", fg="#E5D8B0").pack(pady=5)
faccion_var = tk.StringVar(value="Horda")
faccion_var.trace("w", cambio_razas)
tk.OptionMenu(frame_simulador, faccion_var, *facciones.keys()).pack(pady=5)

tk.Label(frame_simulador, text="Selecciona tu raza:", bg="#1e1e1e", fg="#E5D8B0").pack(pady=5)
raza_var = tk.StringVar()
raza_menu = tk.OptionMenu(frame_simulador, raza_var, "")
raza_menu.pack(pady=5)
cambio_razas()

tk.Label(frame_simulador, text="Nivel del jugador (1-59):", bg="#1e1e1e", fg="#E5D8B0").pack(pady=5)
nivel_jugador_entry = tk.Entry(frame_simulador)
nivel_jugador_entry.pack(pady=5)

tk.Label(frame_simulador, text="Nivel del mob (1-60):", bg="#1e1e1e", fg="#E5D8B0").pack(pady=5)
nivel_mob_entry = tk.Entry(frame_simulador)
nivel_mob_entry.pack(pady=5)

tk.Button(frame_simulador, text="Calcular mobs necesarios", command=calcular_mobs, bg="#3F3026", fg="#E5D8B0", activebackground="#3F3026").pack(pady=10)
result_label = tk.Label(frame_simulador, text="", font=("Arial", 12), bg="#1e1e1e", fg="#E5D8B0")
result_label.pack(pady=10)

tk.Button(frame_simulador, text="Volver", command=lambda: mostrar_frame(frame_inicio), bg="#805A3B", fg="#E5D8B0", activebackground="#805A3B").pack(pady=10)

mostrar_frame(frame_inicio)

root.mainloop()