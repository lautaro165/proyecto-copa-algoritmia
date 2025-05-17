import json
import unicodedata

print("------------------------------------------------------------------------------------------------")
print("¡Hola! Soy tu chatbot de confianza para responder preguntas de geografía sobre la ubicación de países y sus capitales. Estoy aquí para ayudarte y espero poder complacerte con mis respuestas. ¡Estoy a la espera de tus preguntas!")
print("------------------------------------------------------------------------------------------------")

# -------------------------------------------------------------
def cargar_datos():
    with open("preguntas.json", "r", encoding="utf-8") as file:
        archivo_json = json.load(file)
        
        paises_data = archivo_json.get("paises")
        preguntas = archivo_json.get("preguntasSimples")
        preguntas_patrones = archivo_json.get("preguntasPatrones")
        
        return paises_data, preguntas, preguntas_patrones

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
    
def escribir_archivo(paises_data, preguntas, preguntas_patrones):
    archivo_actualizado = {
        "paises":paises_data,
        "preguntasSimples":preguntas,
        "preguntasPatrones":preguntas_patrones
    }
    
    with open("preguntas.json","w", encoding="utf-8") as file:
        json.dump(archivo_actualizado, file, indent=4, ensure_ascii=False)
        
def normalizar_marcadores(texto):
    reemplazos = {
        "(pais)": "*pais*",
        "(capital)": "*capital*",
        "(continente)": "*continente*"
    }
    
    for key, value in reemplazos.items():
        texto = texto.replace(key, value)
    
    return texto
        
def reemplazar_datos(respuesta, datos):
    return respuesta.replace("*pais*",datos["pais"]).replace("*capital*",datos["capital"]).replace("*continente*",datos["continente"])

def pedir_dato(mensaje_input, validacion_de_dato, *args):
    while True:
        dato = input(mensaje_input).strip()
        resultado_validacion = validacion_de_dato(dato, *args)
        if isinstance(resultado_validacion, tuple):
            return dato.capitalize(), resultado_validacion[1]  # Devolvemos el dato y el tipo de pregunta
        
        # En los demás casos, devolvemos solo el dato
        elif resultado_validacion:
            return dato.capitalize()
        print("--------------------------------")

# FUNCIONES DE VALIDACION

def validar_pais(nombre):
    paises_data, _, _ = cargar_datos()
    paises_registrados = [eliminar_acentos(p["pais"].lower()) for p in paises_data]

    if not nombre:
        print("No se ingresó el nombre de ningún país")
        return False
    
    elif any(char.isdigit() for char in nombre):
        print('ingrese el nombre sin ningun numero por favor')
        return False
    elif eliminar_acentos(nombre.lower()) in paises_registrados:
        print(f"{nombre.capitalize()} ya está registrado")
        return False

    return True

def validar_capital(nombre):
    if not nombre:
        print(f"Se debe ingresar la capital del pais para poder registrarlo")
        return False
    elif any(char.isdigit() for char in nombre):
        print('ingrese el nombre sin ningun numero por favor')
        return False
    
    return True

def validar_continente(nombre):
    nombre_sin_acentos = eliminar_acentos(nombre.lower())
    if not nombre:
        print(f"Se debe ingresar el continente de {nombre.capitalize()} para poder registrarlo")
        return False
    elif not nombre_sin_acentos in ["america", "africa", "asia", "oceania", "sudamerica", "norteamerica","centroamerica"]:
        print("Continente invalido")
        return False
    
    return nombre.capitalize()

def validar_pregunta(pregunta):
    _, preguntas, preguntas_patrones = cargar_datos()
    marcadores = ["*capital*","*pais*"]
    if pregunta.lower().strip() == 'salir':
        print("--------------------------------")
        break
    if not pregunta:
        print("No se ingresó ninguna pregunta")
        return False
    
    pregunta_sin_acentos = eliminar_acentos(pregunta)
    
    todas_preguntas = [p["pregunta"] for p in preguntas + preguntas_patrones]
    if pregunta_sin_acentos in todas_preguntas:
        print("Disculpe, esa pregunta ya está registrada")
        return False

    if any(marcador in pregunta for marcador in marcadores):
        return pregunta, "dinamica"
    return pregunta, "simple"

def validar_respuesta(respuesta, tipo_pregunta):
    marcadores = ["*capital*","*pais*","*continente*"]
    
    if not respuesta:
        print("No se ingresó ninguna pregunta")
        return False
    
    if tipo_pregunta == "dinamica":
        if not any(marcador in respuesta for marcador in respuesta):
            print("Para una pregunta dinámica, la respuesta debe contener al menos un marcador: *capital*, *pais*, *continente*")
            return False
    elif tipo_pregunta == "simple":
        if any(marcador in respuesta for marcador in marcadores):
            print("Para una pregunta simple, la respuesta no debe contener marcadores")
            return False
    return True