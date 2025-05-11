import re
import unicodedata
# print("Buenas! Soy un chat bot especializado en geografía.")

#-------------------------------------------------------------------------------------------------------------

# CARGA DE LOS DATOS DEL ARCHIVO
paises_data = []
preguntas = []
preguntas_patrones = []
def cargar_datos():
    
    global paises_data, preguntas, preguntas_patrones
    
    with open("preguntas.txt", "r", encoding="utf-8") as file:
        lineas = file.readlines()
        for linea in lineas:
            if linea.startswith("paises: "):
                paises_data = re.findall(r"\((.*?)\)", linea)
                
                # Lista de tuplas con los datos de los paises que se van a usar en el programa
                paises_data = [ tuple(pais_datos.split(", ")) for pais_datos in paises_data ]
            elif linea.startswith("Preguntas: "):
                # Se sacan las preguntas de las lineas por el contenido dentro de los paréntesis
                preguntas = re.findall(r"\((.*?)\)", linea)
                
                # Se crea una lista de expresiones regulares para buscar la pregunta más adelante
                preguntas_patrones = [ pregunta.replace("*pais*", r"(.+)").replace("*capital*",r"(.+)").replace("*continente*",r"(.+)") for pregunta in preguntas ]
                
cargar_datos()

#-------------------------------------------------------------------------------------------------------------

# FUNCIONES COMPLEMENTARIAS PARA EL FLUJO

def eliminar_acentos(texto):
    texto_sin_acento = ""
    for char in texto: 
        if char.lower() == "ñ":
            texto_sin_acento += char
        else:
            char_normalizado = unicodedata.normalize("NFD",char)
            char_sin_acento = "".join(c for c in char_normalizado if not unicodedata.combining(c))
            
            texto_sin_acento += char_sin_acento
    return texto_sin_acento

def leer_archivo():
    with open("preguntas.txt","r",encoding="utf-8") as file:
        return file.readlines()
    
def escribir_archivo(archivo_actualizado):
    with open("preguntas.txt","w", encoding="utf-8") as file:
        file.writelines(archivo_actualizado)
        
def reemplazar_datos(respuesta, datos):
    return respuesta.replace("*pais*",datos[0]).replace("*capital*",datos[1]).replace("*continente*",datos[2])

def pedir_dato(mensaje_input, validacion_de_dato):
    while True:
        dato = input(mensaje_input).strip()
        if validacion_de_dato(dato):
            return dato.capitalize()
        print("--------------------------------")
        
def validar_pais(nombre):
    paises_registrados = [eliminar_acentos(p[0].lower()) for p in paises_data]

    if not nombre:
        print("No se ingresó el nombre de ningún país")
    elif eliminar_acentos(nombre.lower()) in paises_registrados:
        print(f"{nombre.capitalize()} ya está registrado")
        return False

    return bool(nombre)

def validar_capital(nombre):
    if not nombre:
        print(f"Se debe ingresar la capital del pais para poder registrarlo")
    return bool(nombre)

def validar_continente(nombre):
    if not nombre:
        print(f"Se debe ingresar la capital de {nombre.capitalize()} para poder registrarlo")
    return bool(nombre)