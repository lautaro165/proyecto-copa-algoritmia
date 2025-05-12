import re
import funciones

#FUNCIONES PRINCIPALES DEL PROGRAMA

def encontrar_pais(pregunta):
    """
    Función encargada de buscar los datos del pais que corresponda según
    el nombre de país/capital que el usuario haya ingresado en la pregunta.
    Si el pais está registrado, se devuelve su índice en la lista paises_data,
    caso contrario, se retorna el valor None
    """
    
    for i, dato in enumerate(funciones.paises_data):
        #Verificar que o la ciudad o el pais estén en la pregunta
        nombre_pais = funciones.eliminar_acentos(dato[0].lower())
        nombre_capital = funciones.eliminar_acentos(dato[1].lower())
        
        if nombre_pais in funciones.eliminar_acentos(pregunta.lower()) or nombre_capital in funciones.eliminar_acentos(pregunta.lower()):
            # Retorno el indice de los datos del pais
            return i
    return None

def encontrar_pregunta(pregunta):
    """
    Proceso similar al de la funcion encontrar_pais. Se busca que exista la pregunta
    que el usuario ingresó
    """
    for i, pregunta_patron in enumerate(funciones.preguntas_patrones):
        # Se busca la expresion creada que coincida de principio a fin con la pregunta ingresada por el usuario
        if re.fullmatch(funciones.eliminar_acentos(pregunta_patron.split(", ")[0].lower()), pregunta.lower()):
            # Retorno el indice de la pregunta y su respuesta
            return i
    return None



def agregar_pais():
    """
    Función encargada de pedir los datos necesarios para registrar un pais
    con todos los procesos de validación necesarios y de actualizar el 
    archivo en caso de que el proceso sea exitoso
    """
    archivo = funciones.leer_archivo()
    while True:
        print("--------------------------------")
        pais = funciones.pedir_dato('Ingrese el nombre de un pais para registrarlo: ', funciones.validar_pais)
        capital = funciones.pedir_dato(f'Ingrese el nombre de la capital de {pais}: ', funciones.validar_capital)
        continente = funciones.pedir_dato(f'Ingrese el continente de {pais}: ', funciones.validar_continente)
        
        for i, linea in enumerate(archivo):
            if linea.startswith("paises: "):
                archivo[i] = f"{linea.strip()}, ({pais}, {capital}, {continente})\n"
                break
            
        funciones.escribir_archivo(archivo)
        print("\nPais agregado exitosamente")
        print("--------------------------------")
        
        funciones.cargar_datos()
        break

def agregar_pregunta():
    """
    Función encargada de pedir los datos necesarios para registrar una pregunta
    con todos los procesos de validación necesarios y de actualizar el 
    archivo en caso de que el proceso sea exitoso
    """
    print("--------------------------------")
    
    print("Registre la pregunta de manera genérica usando '*pais*' o '*capital*' como marcadores de manera literal.")
    print('Ejemplo: "¿En qué continente se encuentra *pais*?".')

    preg = funciones.pedir_dato("Pregunta: ", funciones.validar_pregunta)

    print("--------------------------------")
    
    print("Registre la respuesta de manera genérica usando '*pais*' o '*capital*' como marcadores de manera literal.")
    print('Ejemplo: "*pais* está en *continente*".')
    
    resp = funciones.pedir_dato('Ahora, ingrese la respuesta: ', funciones.validar_respuesta)

    print("--------------------------------")

    archivo = funciones.leer_archivo()

    for i, linea in enumerate(archivo):
        if linea.startswith("Preguntas:"):
            archivo[i] = f'{linea.strip()}, ({preg}, {resp})'
            break
    funciones.escribir_archivo(archivo)
    print('Pregunta registrada exitosamente!')
    print("--------------------------------")
    funciones.cargar_datos()
    

def realizar_pregunta():
    """
    Función encargada de procesar las preguntas ingresadas por el usuario, obteniendo los índices tanto
    de la pregunta ingresada como del país sobre el que se hace la pregunta 
    """
    while True:
        
        pregunta = funciones.eliminar_acentos(input("Ingrese su pregunta o 'salir' si desea realizar otra accion: ")).replace("¿","").replace("?","")
        
        if not pregunta:
            print("No se ingresó ninguna pregunta")
            print("--------------------------------")
            continue
        
        if pregunta.lower().strip() == "salir" or pregunta.lower().strip() == "no":
            print("--------------------------------")
            break
        
        pregunta_indice = encontrar_pregunta(pregunta.lower())
        pais_indice = encontrar_pais(pregunta.lower())
        
        
        if pregunta_indice is not None and pais_indice is not None: # Caso donde tanto la pregunta como el pais están registrados
            pais_data = funciones.paises_data[pais_indice]
            respuesta_obtenida = funciones.preguntas[pregunta_indice].split(", ")[1].strip()
            
            respuesta_final = funciones.reemplazar_datos(respuesta_obtenida, pais_data)
            
            print("--------------------------------")
            print(respuesta_final)
            print("--------------------------------")
            
        elif pregunta_indice is None: # Caso donde la pregunta no es encontrada
            print("--------------------------------")
            print("Disculpe, no entendí su pregunta")
            while True:
                print("Digame si desea:")
                print("1 - Reformularla")
                print("2 - Registrarla")
                decision = input("").strip()
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
        elif pais_indice is None: # Caso donde no se encuentran los datos del pais/capital sobre el que se preguntó
            print("--------------------------------")
            print("Disculpe, creo que no conozco el lugar que mencionas, ¿desea registrarlo?")
            while True:
                print("1 - Sí")
                print("2 - No")
                decision = input("").lower()
                if not decision in ["1", "2", 'si', 'no']:
                    print("Opcion invalida")
                    continue
                break
            if decision == "1" or decision == "si":
                agregar_pais()
                break
            if decision == "2" or decision == "no":
                print("--------------------------------")
                continue
            print("--------------------------------")
            # continue
        
        print("¿Tiene alguna otra pregunta? En caso de que no, solamente escriba 'salir'")
            
        

#-------------------------------------------------------------------------------------------------------------

# COMIENZO DEL FLUJO DEL PROGRAMA

while True: # Bucle creado para que reitere las opciones si lo ingresado no es valido
    
    funciones.cargar_datos() #Se recargan los datos para asegurarse de refrescar los datos de los paises y preguntas registradas
    
    print("Por favor, ingrese indique cual de las siguientes opciones desea realizar: ")
    print("1 - Agregar pregunta")
    print("2 - Registrar país") 
    print("3 - Realizar una pregunta ")
    print('4 - Salir\n')
    opcion = funciones.eliminar_acentos(input("").strip())
    if opcion == '1':
        agregar_pregunta()
    elif opcion == '2':
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