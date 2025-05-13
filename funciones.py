import re
import unicodedata
print("¡Hola! Soy tu chatbot de confianza para responder preguntas de geografía sobre la ubicación de países y sus capitales. Estoy aquí para ayudarte y espero poder complacerte con mis respuestas. ¡Estoy a la espera de tus preguntas!")
print("--------------------------------")
#-------------------------------------------------------------------------------------------------------------

paises_data = [] 
preguntas = [] 
preguntas_patrones = []
# -------------------------------------------------------------
def cargar_datos():
    """
    Función encargada de abrir el archivo y de asignar a las variables globales sus datos correspondientes
    Se usa al arranque del programa y en cada proceso donde se modifique el archivo 'preguntas.txt'
    """
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
    
    """
    Función encargada de eliminar los acentos y caracteres especiales del texto excepto la letra 'ñ'.
    Convierte caracteres acentuados a su versión base (e.g., 'é' se convierte a 'e').
    """
    
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
    """
    Función encargada de leer el archivo 'preguntas.txt' y devolver una lista de líneas
    para poder usar los datos de interes
    """
    with open("preguntas.txt","r",encoding="utf-8") as file:
        return file.readlines()
    
def escribir_archivo(archivo_actualizado):
    """
    Función encargada de escribir el archivo de preguntas con las lineas del archivo 
    que recibe como parametro
    """
    with open("preguntas.txt","w", encoding="utf-8") as file:
        file.writelines(archivo_actualizado)
        
def reemplazar_datos(respuesta, datos):
    """
    Función encargada de reemplazar los marcadores en la respuesta por los datos correspondientes
    del pais, capital o continente de la respuesta final a una pregunta del usuario
    """
    return respuesta.replace("*pais*",datos[0]).replace("*capital*",datos[1]).replace("*continente*",datos[2])

def pedir_dato(mensaje_input, validacion_de_dato):
    """
    Función encargada de predir y procesar un dato y validarlo con la funcion 
    que se le pase como segundo parametro. En caso de no ser valido, se pide el
    dato nuevamente, en caso de ser valido, se retorna el dato 
    """
    while True:
        dato = input(mensaje_input).strip()
        if validacion_de_dato(dato):
            return dato.capitalize()
        print("--------------------------------")

# FUNCIONES DE VALIDACION

def validar_pais(nombre):
    """
    La función busca que el pais que se haya ingresado no esté ya registrado
    """
    paises_registrados = [eliminar_acentos(p[0].lower()) for p in paises_data]

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
    """
    Solamente se valida no se envíe un string vacio como dato
    """
    if not nombre:
        print(f"Se debe ingresar la capital del pais para poder registrarlo")
        return False
    elif any(char.isdigit() for char in nombre):
        print('ingrese el nombre sin ningun numero por favor')
        return False
    
    return True
    
    

def validar_continente(nombre):
    """
    Se verifica que el continente ingresado exista
    """
    nombre_sin_acentos = eliminar_acentos(nombre.lower())
    if not nombre:
        print(f"Se debe ingresar el continente de {nombre.capitalize()} para poder registrarlo")
        return False
    elif not nombre_sin_acentos in ["america", "africa", "asia", "oceania", "sudamerica", "norteamerica"]:
        print("Continente invalido")
        return False
    
    return nombre.capitalize()

def validar_pregunta(pregunta):
    """
    Se verifica que el formato de la pregunta a registrar contenga
    marcadores para poder crear una pregunta dinámica
    """
    marcadores = ["*capital*","*pais*"]
    
    if not pregunta:
        print("No se ingresó ninguna pregunta")
        return False
    elif not any(marcador in pregunta for marcador in marcadores):
        print("Para poder registrar la pregunta, ésta debe contener uno de los siguientes marcadores: *capital* o *pais* o *continente*")
        return False
    elif eliminar_acentos(pregunta) in preguntas:
        print("Disculpe, esa pregunta ya está registrada")
        return False
    
    return True

def validar_respuesta(respuesta):
    """
    Se verifica que el formato de la respuesta a registrar contenga 
    marcadores para poder crear una respuesta dinámica
    """
    marcadores = ["*capital*","*pais*","*continente*"]
    
    if not respuesta:
        print("No se ingresó ninguna pregunta")
        return False
    elif not any(marcador in respuesta for marcador in marcadores):
        print("Para poder registrar la respuesta, ésta debe contener uno o más de los siguientes marcadores: *capital*, *pais* o *continente*")
        return False
    return True