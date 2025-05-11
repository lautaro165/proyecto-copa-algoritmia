import re
import unicodedata
# print("Buenas! Soy un chat bot especializado en geografía.")

#-------------------------------------------------------------------------------------------------------------

# CARGA DE LOS DATOS DEL ARCHIVO
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
#-------------------------------------------------------------------------------------------------------------

#FUNCIONES PRINCIPALES DEL PROGRAMA

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


def agregar_pais():
    
    #Verificar en cada uno que no se ingresen caracteres invalidos
    while True:
        print("--------------------------------")
        # pais = input('Ingrese el nombre de un pais para registrarlo: ').strip()
        pais = pedir_dato('Ingrese el nombre de un pais para registrarlo: ', validar_pais)
        capital = pedir_dato('Ingrese el nombre de la ciudad: ',validar_capital)
        continente = pedir_dato(f'Ingrese el continente de {pais}: ', validar_continente)
        while True:
            if re.search(r'\d', pais) or re.search(r'\d', capital) or re.search(r'\d', continente):
                break

        archivo = leer_archivo()
        
        for i, linea in enumerate(archivo):
            if linea.startswith("paises: "):
                archivo[i] = f"{linea.strip()}, ({pais}, {capital}, {continente})\n"
                break
            
        escribir_archivo(archivo)
        print("\nPais agregado exitosamente")
        print("--------------------------------")
        
        cargar_datos()
        break

#TERMINAR LAS VALIDACIONES NECESARIAS A ESTA FUNCION
def agregar_pregunta():
    print("--------------------------------")
    
    print('Ingrese la pregunta, y en el apartado donde iria el pais, la ciudad o el continente escriba *pais*, *capital* o *continente*')
    print('Ejemplo: en que continente queda *pais*, *pais* queda en *continente*') 
    #validacion pregunta 

    while True:
        preg = eliminar_acentos(input("Pregunta: ")).strip()
        if preg and ('*pais*' in preg or '*capital*' in preg or '*continente*' in preg):
            break
        print('pregunta invalida, asegurese de usar *capital*, *pais* o *continente y no dejar un espacio en blanco*')
    
    
    print("--------------------------------")
    
    while True:
        resp = eliminar_acentos(input('Ahora, ingrese la respuesta: ')).strip() 
        if resp and ('*pais*' in resp or '*capital*' in resp or '*continente*' in resp):
            break
        print('respuesta invalida, asegurese de usar *capital*, *pais* o *continente y no dejar un espacio en blanco*')
  
    
    print("--------------------------------")
    
    archivo = leer_archivo()
        
    for i, linea in enumerate(archivo):
        if linea.startswith("Preguntas:"):
            archivo[i] = f'{linea.strip()}, ({preg}, {resp})'
            break
    escribir_archivo(archivo)
    print('Pregunta registrada exitosamente!')
    print("--------------------------------")
    cargar_datos()
    

def realizar_pregunta():
    while True:
        pregunta = eliminar_acentos(input("Ingrese su pregunta: ")).replace("¿","").replace("?","")
        if not pregunta:
            print("Por favor ingrese una pregunta")
            print("--------------------------------")
            continue
        
        if pregunta.lower().strip() == "salir" or pregunta.lower().strip() == "no":
            break
        
        pregunta_indice = encontrar_pregunta(pregunta)
        pais_indice = encontrar_pais(pregunta)
        
        # Manejar bien el caso puntual donde o no se conozca el pais o se conozca la pregunta
        if pregunta_indice is not None and pais_indice is not None:
            pais_data = paises_data[pais_indice]
            respuesta_obtenida = preguntas[pregunta_indice].split(", ")[1].strip()
            
            respuesta_final = reemplazar_datos(respuesta_obtenida, pais_data)
            
            print("--------------------------------")
            print(respuesta_final)
            print("--------------------------------")
            
        elif pregunta_indice is None:
            print("--------------------------------")
            print("Disculpe, no entendí su pregunta")
            while True:
                print("Digame si desea reformularla o registrarla?")
                decision = input("")
                print("--------------------------------")
                if not any(opcion in eliminar_acentos(decision.lower()) for opcion in ["registrar","registrarla","reformular","reformularla"]): # Opciones validas que puede escribir el usuario
                    
                    print("Disculpe, no le entendí")
                    print("--------------------------------")
                    continue
                elif any(opcion in eliminar_acentos(decision.lower()) for opcion in ["registrar","registrarla"]):
                    agregar_pregunta()
                    break
                elif any(opcion in eliminar_acentos(decision.lower()) for opcion in ["reformular","reformularla"]):
                    
                    break
                else:
                    break
            continue    
        elif pais_indice is None:
            print("--------------------------------")
            print("Disculpe, creo que no conozco el lugar que mencionas, ¿desea registrarlo?")
            print("--------------------------------")
            continue
        
        print("¿Desea realizar otra pregunta?")
            
        

#-------------------------------------------------------------------------------------------------------------

# COMIENZO DEL FLUJO DEL PROGRAMA

# Se podria arrancar primero preguntando si lo que quiere el usuario es registrar algo o hacer la pregunta

while True: # Bucle creado para que reitere las opciones si lo ingresado no es valido
    
    cargar_datos()
    
    print("Por favor, ingrese una de las siguientes opciones: ")
    print("1 - Agregar pregunta")
    print("2 - Registrar país") 
    print("3 - Realizar una pregunta ")
    print('4 - Salir\n')
    opcion = eliminar_acentos(input(""))
    if opcion == '1':
        agregar_pregunta() 
    elif opcion == '2':
        print("--------------------------------")
        agregar_pais() # Mismo caso que en agregar_pregunta(), hay que agregar validaciones
    elif opcion == "3":
        print("--------------------------------")
        realizar_pregunta()
    elif opcion == '4':
        break
    else:
        print("--------------------------------")
        print("Opción invalida")
        print("--------------------------------")     

print("--------------------------------")
print("Un placer ayudarte en lo que pueda, espero volver a verte pronto")
print("--------------------------------")