import re
from funciones import paises_data, preguntas, preguntas_patrones, leer_archivo, pedir_dato, eliminar_acentos, cargar_datos, validar_capital, validar_continente, validar_pais,escribir_archivo, reemplazar_datos

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
    archivo = leer_archivo()
    #Verificar en cada uno que no se ingresen caracteres invalidos
    while True:
        print("--------------------------------")
        # pais = input('Ingrese el nombre de un pais para registrarlo: ').strip()
        pais = pedir_dato('Ingrese el nombre de un pais para registrarlo: ', validar_pais)
        ciudad = pedir_dato('Ingrese el nombre de la ciudad: ',validar_capital)
        continente = pedir_dato(f'Ingrese el continente de {pais}: ', validar_continente)
        
        for i, linea in enumerate(archivo):
            if linea.startswith("paises: "):
                archivo[i] = f"{linea.strip()}, ({pais}, {ciudad}, {continente})\n"
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
    print("--------------------------------")
    cargar_datos()
    

def realizar_pregunta():
    while True:
        pregunta = eliminar_acentos(input("Ingrese su pregunta: ")).replace("¿","").replace("?","")
        
        if not pregunta:
            print("Por favor ingrese una pregunta")
            print("--------------------------------")
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
            
            print("--------------------------------")
            print(respuesta_final)
            print("--------------------------------")
            
        elif pregunta_indice is None:
            print("--------------------------------")
            print("Disculpe, no entendí su pregunta")
            while True:
                print("Digame si desea:")
                print("1 - Reformularla")
                print("2 - Registrarla")
                decision = input("")
                print("--------------------------------")
                if not decision in ["1", "2"]: # Opciones validas que puede escribir el usuario
                    print("Disculpe, no se ingresó una opción valida")
                    print("--------------------------------")
                    continue
                elif decision == "1":
                    break
                elif decision == "2":
                    agregar_pregunta()
                    break
                else:
                    break
            continue    
        elif pais_indice is None:
            print("--------------------------------")
            print("Disculpe, creo que no conozco el lugar que mencionas, ¿desea registrarlo?")
            print("--------------------------------")
            continue
        
        print("¿Tiene alguna otra pregunta? En caso de que no, solamente escriba 'salir'")
            
        

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
        agregar_pais()
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