import re
# print("Buenas! Soy un chat bot especializado en geografía.")
# print("¿En qué puedo ayudarte hoy?")

with open("preguntas.txt", "r", encoding="utf-8") as file:
    lineas = file.readlines()
    for linea in lineas:
        if linea.startswith("paises: "):
            paises_data = re.findall(r"\((.*?)\)", linea)
            
            paises_data = [ tuple(pais_datos.split(", ")) for pais_datos in paises_data ]
        elif linea.startswith("Preguntas: "):
            # Se sacan las preguntas de las lineas por el contenido dentro de los parentesis
            preguntas = re.findall(r"\((.*?)\)", linea)
            
            # Se crea una lista de expresiones regulares para buscar la pregunta mas adelante
            preguntas_patrones = [ pregunta.replace("*pais*", r"(.+)").replace("*ciudad*",r"(.+)").replace("*capital*",r"(.+)").replace("*continente*",r"(.+)") for pregunta in preguntas ]
        

def encontrar_pais(pregunta):
    for i, dato in enumerate(paises_data):
        #Verificar que o la ciudad o el pais estén en la pregunta
        if dato[0].lower() in pregunta.lower() or dato[1].lower() in pregunta.lower():
            # Retorno el indice de los datos del pais
            return i
    return None

def encontrar_pregunta(pregunta):
    for i, pregunta_patron in enumerate(preguntas_patrones):
        # Se busca la expresion creada que coincida de principio a fin con la pregunta ingresada por el usuario
        if re.fullmatch(pregunta_patron.split(", ")[0].lower(), pregunta.lower()):
            # Retorno el indice de la pregunta y su respuesta
            return i
    return None

def reemplazar_datos(respuesta, datos):
    return respuesta.replace("*pais*",datos[0]).replace("*ciudad*",datos[1]).replace("*continente*",datos[2])

while True:
    pregunta = input("Ingrese su pregunta: ")
    
    if pregunta.lower().strip() == "salir":
        break
    
    pregunta_indice = encontrar_pregunta(pregunta)
    pais_indice = encontrar_pais(pregunta)
        
    if pregunta_indice is not None and pais_indice is not None:
        
        pais_data = paises_data[pais_indice]
        respuesta_obtenida = preguntas[pregunta_indice].split(", ")[1].strip()
        
        respuesta_final = reemplazar_datos(respuesta_obtenida, pais_data)
        
        print(respuesta_final)
    else:
        print("Disculpe, no entendí su pregunta")
        
print("Un placer ayudarte en lo que pueda, espero volver a verte pronto :)")