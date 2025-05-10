import re
import unicodedata
# print("Buenas! Soy un chat bot especializado en geografía.")
# print("¿En qué puedo ayudarte hoy?")

#FALTA OPTIMIZAR BIEN EL TEMA DE APERTURAS INNECESARIAS DEL ARCHIVO (Lo hago yo)

def eliminar_acentos(texto):
    texto_normalizado = unicodedata.normalize("NFD",texto)
    texto_sin_acento = "".join(char for char in texto_normalizado if not unicodedata.combining(char))
    return texto_sin_acento

def leer_archivo():
    with open("preguntas.txt","r",encoding="utf-8") as file:
        return file.readlines()
    
def escribir_archivo(archivo_actualizado):
    with open("preguntas.txt","w", encoding="utf-8") as file:
        file.writelines(archivo_actualizado)

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

def agregar_pais():
    archivo = leer_archivo()
    
    print("--------------------------------")
    pais = eliminar_acentos(input('Ingrese el nombre del pais ').strip())
    ciudad = eliminar_acentos(input('Ingrese el nombre de la ciudad ').strip())
    continente = eliminar_acentos(input('Ingrese el continente ').strip())
    print("--------------------------------")
    if (pais, ciudad, continente) not in paises_data: # Sensible a mayusculas y minusculas (CORREGIR), tambien hay que iterar para en cada dato para ver que no exista ya
        for i, linea in enumerate(archivo):
            if linea.startswith("paises:"):
                archivo[i] = f"{linea.strip()}, ({pais}, {ciudad}, {continente})\n" 
                break
        escribir_archivo(archivo)
        print("Pais registrado exitosamente")
    else:
        print('Ese pais ya esta en el programa') #Podriamos poner el nombre del pais que ya existe en este mensaje

def agregar_pregunta():
    print("--------------------------------")
    
    print('Ingrese la pregunta, y en el apartado donde iria el pais, la ciudad o el continente escriba *pais*, *ciudad* o *continente*')
    print('Ejemplo: en que continente queda *pais*, *pais* queda en *continente*') 
    
    
    preg = eliminar_acentos(input("Pregunta: "))
    
    print("--------------------------------")
    
    resp = eliminar_acentos(input('Ahora, ingrese la respuesta: ')) 
    
    print("--------------------------------")
    
    archivo = leer_archivo()
        
    for i, linea in enumerate(archivo):
        if linea.startswith("Preguntas:"):
            archivo[i] = f'{linea.strip()}, ({preg}, {resp})'
            break
    escribir_archivo(archivo)
    print('Pregunta registrada exitosamente!')


# Se podria arrancar primero preguntando si lo que quiere el usuario es registrar algo o hacer la pregunta
while True:
    pregunta = eliminar_acentos(input("Ingrese su pregunta: "))
    
    if not pregunta:
        print("Por favor ingrese una pregunta")
        continue
    
    if pregunta.lower().strip() == "salir":
        break
    
    pregunta_indice = encontrar_pregunta(pregunta)
    pais_indice = encontrar_pais(pregunta)
    
    # Manejar bien el caso puntual donde o no se conozca el pais o se conozca la pregunta
    if pregunta_indice is not None and pais_indice is not None:
        pais_data = paises_data[pais_indice]
        respuesta_obtenida = preguntas[pregunta_indice].split(", ")[1].strip()
        
        respuesta_final = reemplazar_datos(respuesta_obtenida, pais_data)
        
        print(respuesta_final)
    elif pregunta_indice is None:
        pass
    elif pais_indice is None:
        pass
    else:
        print("--------------------------------") # Estas lineas divisorias son para mejor claridad en la consola
        print("Disculpe, no entendí su pregunta")
        print("--------------------------------")
        while True: # Bucle creado para que reitere las opciones si lo ingresado no es valido
            
            print("Por favor, ingrese una de las siguientes opciones: ")
            print("1 - Agregar pregunta")
            print("2 - Registrar país") 
            print("3 - Realizar una pregunta \n")
            opcion = eliminar_acentos(input(""))
            if opcion == '1':
                agregar_pregunta() # No toma como error si se ingresan tanto pregunta como respuesta vacia (Hay que verificar que el usuario haya agregado algo valido y no un espacio vacio o que lo ingresado tenga caracteres invalidos como numeros)
            elif opcion == '2':
                agregar_pais() # Mismo caso que en agregar_pregunta(), hay que agregar validaciones
            elif opcion == "3":
                break
            else:
                print("--------------------------------")
                print('Opción invalida')
                print("--------------------------------")
        
print("Un placer ayudarte en lo que pueda, espero volver a verte pronto")