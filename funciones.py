import unicodedata, json

print("------------------------------------------------------------------------------------------------")
print("¡Hola! Soy tu chatbot de confianza para responder preguntas de geografía sobre la ubicación de países y sus capitales. Estoy aquí para ayudarte y espero poder complacerte con mis respuestas. ¡Estoy a la espera de tus preguntas!")
print("------------------------------------------------------------------------------------------------")

# -------------------------------------------------------------    
def cargar_datos():
    try:
        with open("preguntas.json", "r", encoding="utf-8") as file:
            archivo_json = json.load(file)

            paises_data = archivo_json.get("paises")
            preguntas = archivo_json.get("preguntasSimples")
            preguntas_patrones = archivo_json.get("preguntasPatrones")

            # Se establecen principales palabras clave
            palabras_clave = ["pais", "continente","everest", "capital", "rio", "grande", "mundo", "geografia", "poblado", "obelisco", "oceano", "oceanos","pequeño","desierto"]

            #Se agregan a palabras_clave los paises y capitales registrados
            for p in paises_data:
                palabras_clave.append(p["pais"].lower())
                palabras_clave.append(p["capital"].lower())
            
            
            return paises_data, preguntas, preguntas_patrones, palabras_clave
    except FileNotFoundError:
        print("Disculpe, no se ha encontrado el archivo 'preguntas.json', se creará uno nuevo")
        escribir_archivo([],[],[])
        return [],[],[]
    except json.decoder.JSONDecodeError:
        print("El archivo json tiene errores en su formato")
        return [],[],[]
    except Exception as e:
        print(f"Ocurrió un error en la lectura del archivo: {e}")
        return [],[],[]
    
#-------------------------------------------------------------------------------------------------------------

# FUNCIONES COMPLEMENTARIAS PARA EL FLUJO

def buscar_coincidencias(preguntas, palabras_clave, palabras_pregunta, pais_data=None):
    coincidencias = []
    for p in preguntas:
            
        pregunta_texto = p["pregunta"].lower()
        palabras_formateadas = pregunta_texto.split(" ")
        
        # Coincidencias exactas
        if pregunta_texto == " ".join(palabras_pregunta):
            return [(p, len(palabras_formateadas))]

        # Coincidencias con datos del país (solo si existe pais_data)
        datos_de_pais_encontrados = 0
        if pais_data:
            datos_de_pais = " ".join(pais_data.values()).lower().split(" ")
            datos_de_pais_encontrados = sum(
                1 for palabra in datos_de_pais 
                if palabra in palabras_formateadas and palabra in palabras_pregunta
            )

        # Coincidencias con palabras clave
        palabras_encontradas = sum(
            1 for palabra in palabras_clave 
            if palabra in palabras_formateadas and palabra in palabras_pregunta
        )

        coincidencias_totales = palabras_encontradas + datos_de_pais_encontrados
        if coincidencias_totales > 0:
            coincidencias.append((p, coincidencias_totales))

    return coincidencias


def obtener_mejor_coincidencia(coincidencias):
    """
    Funcion que se usa para buscar la pregunta que mejor coincida con respecto
    a una busqueda realizada por el usuario
    """
    if len(coincidencias) > 0:
        coincidencias.sort(key=lambda x: x[1], reverse=True)
        pregunta_seleccionada, _ = coincidencias[0]
        return pregunta_seleccionada["indice_original"], pregunta_seleccionada["tipo"]
    return None

def reemplazar_marcadores(texto, pais_data=None):
    if pais_data:
        return texto.replace("*pais*", eliminar_acentos(pais_data["pais"])).replace("*capital*", eliminar_acentos(pais_data["capital"])).replace("*continente*", eliminar_acentos(pais_data["continente"]))
    return texto.replace("*pais*", r"(.+)").replace("*capital*", r"(.+)").replace("*continente*", r"(.+)")

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
    
    try:
        with open("preguntas.json","w", encoding="utf-8") as file:
            json.dump(archivo_actualizado, file, indent=4, ensure_ascii=False, separators=(",", ": "))
    except Exception as e:
        print(f"Ha ocurrido un error al escribir el archivo: {e}")
        
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
    """
    Funcion para pedir un dato al usuario hasta que pase la validacion indicada
    """
    resultado_validacion = None
    while not resultado_validacion: # El bucle se ejecuta hasta que el resultado de la validacion de el dato sea valido (True)
        dato = input(mensaje_input).strip()
        resultado_validacion = validacion_de_dato(dato, *args)

        if isinstance(resultado_validacion, tuple):
            return dato.capitalize(), resultado_validacion[1]  # Caso especial para la validacion de preguntas, donde se retorna una tupla con la pregunta como tal y su tipo (dinamica o simple)
        
        # En los demás casos, devolvemos solo el dato
        elif resultado_validacion:
            return dato.capitalize()
        print("--------------------------------")

# FUNCIONES DE VALIDACION DE DATOS

def validar_pais(nombre):
    paises_data, _, _, _ = cargar_datos()
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
        print('Ingrese el nombre sin ningun numero por favor')
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
    _, preguntas, preguntas_patrones, _ = cargar_datos()
    marcadores = ["*capital*","*pais*","(capital)","(pais)"]
    if pregunta.lower().strip() == 'salir':
        print("--------------------------------")
        # break #Acá el break no va porque no es un bucle, en todo caso la validacion de que "salir" va dentro del bucle donde se está ejecutando esto
    if not pregunta:
        print("No se ingresó ninguna pregunta")
        return False
    
    pregunta_sin_acentos = normalizar_marcadores(eliminar_acentos(pregunta))
    
    todas_preguntas = [p["pregunta"] for p in preguntas + preguntas_patrones]
    if pregunta_sin_acentos in todas_preguntas:
        print("Disculpe, esa pregunta ya está registrada")
        return False

    if any(marcador in pregunta for marcador in marcadores):
        return pregunta, "dinamica"
    return pregunta, "simple"

def validar_respuesta(respuesta, tipo_pregunta):
    marcadores = ["*capital*","*pais*","*continente*","(capital)","(pais)","(continente)"]
    
    if not respuesta:
        print("No se ingresó ninguna pregunta")
        return False
    
    if tipo_pregunta == "dinamica" and not any(marcador in respuesta for marcador in marcadores):
        print("Para una pregunta dinámica, la respuesta debe contener al menos un marcador: (capital), (pais), (continente)")
        return False
    elif tipo_pregunta == "simple" and any(marcador in respuesta for marcador in marcadores):
        print("Para una pregunta simple, la respuesta no debe contener marcadores")
        return False
    return True