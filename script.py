import re
import funciones

#FUNCIONES PRINCIPALES DEL PROGRAMA

def encontrar_pais(pregunta):
    for i, dato in enumerate(funciones.paises_data):
        #Verificar que o la ciudad o el pais estén en la pregunta
        nombre_pais = funciones.eliminar_acentos(dato[0].lower())
        nombre_capital = funciones.eliminar_acentos(dato[1].lower())
        
        if nombre_pais in funciones.eliminar_acentos(pregunta.lower()) or nombre_capital in funciones.eliminar_acentos(pregunta.lower()):
            # Retorno el indice de los datos del pais
            return i
    return None

def encontrar_pregunta(pregunta):
    for i, pregunta_patron in enumerate(funciones.preguntas_patrones):
        # Se busca la expresion creada que coincida de principio a fin con la pregunta ingresada por el usuario
        if re.fullmatch(funciones.eliminar_acentos(pregunta_patron.split(", ")[0].lower()), pregunta.lower()):
            # Retorno el indice de la pregunta y su respuesta
            return i
    return None



def agregar_pais():
    paises_data, preguntas, preguntas_patrones = funciones.cargar_datos()
    while True:
        print("--------------------------------")
        pais = funciones.pedir_dato('Ingrese el nombre de un pais para registrarlo: ', funciones.validar_pais)
        capital = funciones.pedir_dato(f'Ingrese el nombre de la capital de {pais}: ', funciones.validar_capital)
        continente = funciones.pedir_dato(f'Ingrese el continente de {pais}: ', funciones.validar_continente)
        
        paises_data.append({
            "pais":pais,
            "capital":capital,
            "continente":continente
        })
            
        funciones.escribir_archivo(paises_data,preguntas,preguntas_patrones)
        print("\nPais agregado exitosamente")
        print("--------------------------------")
        break

def agregar_pregunta():
    paises_data, preguntas, preguntas_patrones = funciones.cargar_datos()
    print("--------------------------------")
    print("💡 INSTRUCCIONES PARA REGISTRAR UNA PREGUNTA 💡\n")
    print("Puede registrar una pregunta de dos maneras:")
    print("1. **Pregunta dinámica:** Utiliza marcadores para insertar datos de países registrados. Los marcadores disponibles son:")
    print("   - (pais) → Reemplazado por el nombre del país.")
    print("   - (capital) → Reemplazado por la capital del país.")
    print("   - (continente) → Reemplazado por el continente del país.")
    print("   Ejemplo: ¿Cuál es la capital de (pais)?")
    print()
    print("2. **Pregunta simple:** No contiene marcadores y tiene una única respuesta fija.")
    print("   Ejemplo: ¿Cuál es el continente más grande del mundo?")
    print("--------------------------------")

    preg, tipo_pregunta = funciones.pedir_dato("Ingrese su pregunta: ", funciones.validar_pregunta)

    print("--------------------------------")
    print("Ahora, ingrese la respuesta correspondiente.")
    print("💡 Si la pregunta es dinámica, asegúrese de usar los mismos marcadores utilizados en la pregunta.")
    print("   Ejemplos:")
    print("   - Respuesta dinámica: (pais) está en (continente).")
    print("   - Respuesta simple: El continente más grande es Asia.")
    print("--------------------------------")

    resp = funciones.pedir_dato('Ingrese la respuesta: ', lambda r: funciones.validar_respuesta(r, tipo_pregunta))


    print("--------------------------------")

    pregunta_agregada = {
        "pregunta":preg,
        "respuesta":resp
    }
    
    preguntas.append(pregunta_agregada) if tipo_pregunta == "simple" else preguntas_patrones.append(pregunta_agregada)
    
    funciones.escribir_archivo(paises_data, preguntas, preguntas_patrones)
    print(f'Pregunta {tipo_pregunta} registrada exitosamente!')
    print("--------------------------------")

def realizar_pregunta():
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