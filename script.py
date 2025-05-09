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

def agregar_pais():
    pais = input('Ingrese el nombre del pais ').strip()
    ciudad = input('ingrese el nombre de la ciudad ').strip()
    continente = input('ingrese el continente ').strip()
    if (pais, ciudad, continente) not in paises_data:
        paises_data.append((pais, ciudad, continente))
        with open('preguntas.txt', 'a', encoding='utf-8') as file:
            file.write(f', ({pais}, {ciudad}, {continente})')
        print(f'datos de {pais} ingresados')
    else:
        print('ese pais ya esta en el programa')

def agregar_pregunta():
    tipo_pregunta = input('ingrese el tipo de pregunta (ciudad,pais,continente)')
    if tipo_pregunta not in ['ciudad', 'pais', 'continente' ]:
        print('respuesta invalida')
        return
    else:
        preg = input('ingrese la pregunta, y en el apartado donde iria el pais, la ciudad o el continente escriba *pais* , *ciudad* , o *continente* ')
        resp = input('ahora, ingrese la respuesta ')  
        print('ejemplo: en que continente queda *pais*, *pais* queda en *continente* ') 
        with open('preguntas.txt', 'a', encoding='utf-8') as file:
            file.write(f'. ({preg}, {resp})') 
        print('pregunta agregada')
    
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
        modificar = input('quiere agregar una pregunta? (si/no)')
        if modificar == 'si':
            tipopreg = input('desea agregar una pregunta o un pais ')
            if tipopreg == 'pregunta':
                agregar_pregunta()
            elif tipopreg == 'pais':
              agregar_pais()  
            else:
                print('respuesta invalida')
       
        
print("Un placer ayudarte en lo que pueda, espero volver a verte pronto")