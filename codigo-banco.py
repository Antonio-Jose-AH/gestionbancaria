import json
import os
from datetime import datetime, timedelta

BD = "usuarios.json"

def cargar_bd():
    if not os.path.exists(BD):
        with open(BD, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
    with open(BD, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_bd(data):
    with open(BD, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def crear_usuario():
    data = cargar_bd()
    nombre = input("Nombre: ")
    dni = input("DNI: ")
    contraseña = input("Contraseña: ")

    for u in data:
        if u["dni"] == dni:
            print("Ese DNI ya está registrado.")
            return

    hoy = datetime.now().strftime("%Y-%m-%d")

    nuevo = {
        "nombre": nombre,
        "dni": dni,
        "password": contraseña,
        "saldo": 0,
        "historial": [],
        "pendientes": [],
        "cobradores": [],
        "bloqueado_hasta": "",
        "creado": hoy
    }

    data.append(nuevo)
    guardar_bd(data)
    print("Cuenta creada correctamente.")

def verificar_bloqueo(usuario):
    if usuario["bloqueado_hasta"] == "":
        return False
    hoy = datetime.now().strftime("%Y-%m-%d")
    return hoy < usuario["bloqueado_hasta"]

def iniciar_sesion():
    data = cargar_bd()
    dni = input("DNI: ")
    usuario = None
    for u in data:
        if u["dni"] == dni:
            usuario = u
            break
    if usuario is None:
        print("No existe un usuario con ese DNI.")
        return None, data

    if verificar_bloqueo(usuario):
        print("Agotaste tus intentos, vuelva otro día.")
        return None, data

    intentos = 3
    while intentos > 0:
        pw = input("Contraseña: ")
        if pw == usuario["password"]:
            procesar_pendientes(usuario, data)
            procesar_cobros_automaticos(usuario, data)
            procesar_cobro_semanal(usuario, data)
            guardar_bd(data)
            return usuario, data
        intentos -= 1

    mañana = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    usuario["bloqueado_hasta"] = mañana
    guardar_bd(data)
    print("Agotaste tus intentos, vuelva otro día.")
    return None, data
