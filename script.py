import re, difflib
import funciones

#FUNCIONES PRINCIPALES DEL PROGRAMA

def encontrar_pais(pregunta):
    paises_data, _, _, _ = funciones.cargar_datos()
    for i, dato in enumerate(paises_data):
        #Verificar que o la ciudad o el pais estén en la pregunta
        nombre_pais = funciones.eliminar_acentos(dato["pais"].lower())
        nombre_capital = funciones.eliminar_acentos(dato["capital"].lower())
        
        if nombre_pais in funciones.eliminar_acentos(pregunta.lower()) or nombre_capital in funciones.eliminar_acentos(pregunta.lower()):
            # Retorno el indice de los datos del pais
            return i
    return None

def encontrar_pregunta(pregunta):
    """
    Funcion que se encarga de buscar y encontrar una pregunta
    en base a un input completo o mediante keywords
    """
    paises_data, preguntas, preguntas_patrones, palabras_clave = funciones.cargar_datos()
    palabras_pregunta = funciones.eliminar_acentos(pregunta.lower()).split(" ")    

    preguntas_dinamicas = [{
        "pregunta": p["pregunta"],
        "respuesta": p["respuesta"],
        "tipo": "dinamica",
        "indice_original": i 
    } for i, p in enumerate(preguntas_patrones)]
    
    preguntas_simples = [{
        "pregunta":p["pregunta"],
        "respuesta":p["respuesta"],
        "tipo": "simple",
        "indice_original": i
    } for i, p in enumerate(preguntas)] 
    
    preguntas_unificadas = [{
        "pregunta": p["pregunta"],
        "respuesta":p["respuesta"],
        "tipo": "simple",
        "indice_original": i
    } for i, p in enumerate(preguntas)] + preguntas_dinamicas
    
    # BUSQUEDA POR PALABRAS CLAVE
    if 1 < len(palabras_pregunta) <= 3:
        pais_encontrado_indice = encontrar_pais(pregunta)
        if pais_encontrado_indice is not None:
            pais_data = paises_data[pais_encontrado_indice]
            coincidencias_dinamicas = funciones.buscar_coincidencias(preguntas_dinamicas,palabras_clave,palabras_pregunta, pais_data)
            resultado = funciones.obtener_mejor_coincidencia(coincidencias_dinamicas)
            if resultado:
                return resultado

    # Búsqueda por palabras clave en preguntas simples (1 palabra)
    elif len(palabras_pregunta) == 1:
        coincidencias_simples = funciones.buscar_coincidencias(preguntas_simples,palabras_clave,palabras_pregunta)
        resultado = funciones.obtener_mejor_coincidencia(coincidencias_simples)
        if resultado:
            return resultado
        
    # BUSQUEDA EXACTA DE LA PREGUNTA
    for p in preguntas_unificadas:
        if re.fullmatch(funciones.eliminar_acentos(p["pregunta"].lower()), pregunta.lower()):
            return p["indice_original"], p["tipo"]
    
    preguntas_registros = [p["pregunta"].lower() for p in preguntas_unificadas]
    
    # BUSQUEDA DE SIMILITUDES EN CASO DE NO ENCONTRARSE LA PREGUNTA EXACTA
    coincidencias = difflib.get_close_matches(pregunta.lower(), preguntas_registros, n=1, cutoff=0.55)

    if coincidencias:
        
        coincidencia_mayor = coincidencias[0]
        
        print(coincidencia_mayor)
        
        for p in preguntas_unificadas:
            print(p)
            if p["pregunta"].lower() == coincidencia_mayor:
                return p["indice_original"], p["tipo"]

def agregar_pais():
    paises_data, preguntas, preguntas_patrones, _ = funciones.cargar_datos()
    print("--------------------------------")
    pais = funciones.pedir_dato('Ingrese el nombre de un pais para registrarlo: ', funciones.validar_pais)
    if pais.lower().strip() == "salir":
        print("--------------------------------")
        return
        
    capital = funciones.pedir_dato(f'Ingrese el nombre de la capital de {pais}: ', funciones.validar_capital)
    if capital.lower().strip() == "salir":
        print("--------------------------------")
        return
        
    continente = funciones.pedir_dato(f'Ingrese el continente de {pais}: ', funciones.validar_continente)
    if continente.lower().strip() == "salir":
        print("--------------------------------")
        return
    
    paises_data.append({
        "pais":pais,
        "capital":capital,
        "continente":continente
    })
        
    funciones.escribir_archivo(paises_data,preguntas,preguntas_patrones)
    print("\nPais agregado exitosamente")
    print("--------------------------------")

def agregar_pregunta():
    paises_data, preguntas, preguntas_patrones, _ = funciones.cargar_datos()
    print("--------------------------------")
    print(" INSTRUCCIONES PARA REGISTRAR UNA PREGUNTA \n")
    print("Puede registrar una pregunta de dos maneras:")
    print("1. **Pregunta dinámica:** Utiliza marcadores para insertar datos de países registrados. Los marcadores disponibles son:")
    print("   - (pais) → Reemplazado por el nombre del país.")
    print("   - (capital) → Reemplazado por la capital del país.")
    print("   - (continente) → Reemplazado por el continente del país.")
    print("   Ejemplo: ¿Cuál es la capital de (pais)?")
    print()
    print("2. **Pregunta simple:** No contiene marcadores y tiene una única respuesta fija.")
    print("   Ejemplo: ¿Cuál es el continente más grande del mundo?")
    print("escribi solo 'salir' en cualquier momento para volver para atras")
    print("--------------------------------")

    preg, tipo_pregunta = funciones.pedir_dato("Ingrese su pregunta (para salir ingrese 'salir'): ", funciones.validar_pregunta)
    if preg.lower().strip() == "salir" or tipo_pregunta.lower().strip() == 'salir':
        print("--------------------------------")
        return
        
   

    print("--------------------------------")
    print("Ahora, ingrese la respuesta correspondiente.")
    print("Si la pregunta es dinámica, asegúrese de usar los mismos marcadores utilizados en la pregunta.")
    print("   Ejemplos:")
    print("   - Respuesta dinámica: (pais) está en (continente).")
    print("   - Respuesta simple: El continente más grande es Asia.")
    print("--------------------------------")

    resp = funciones.pedir_dato('Ingrese la respuesta: ', lambda r: funciones.validar_respuesta(r, tipo_pregunta))
    if resp.lower().strip() == "salir":
        
        print("ANULANDO")
        print("--------------------------------")
        return


    print("--------------------------------")

    pregunta_agregada = {
        "pregunta":funciones.normalizar_marcadores(preg),
        "respuesta":funciones.normalizar_marcadores(resp)
    }
    
    preguntas.append(pregunta_agregada) if tipo_pregunta == "simple" else preguntas_patrones.append(pregunta_agregada)
    
    funciones.escribir_archivo(paises_data, preguntas, preguntas_patrones)
    print(f'Pregunta {tipo_pregunta} registrada exitosamente!')
    print("--------------------------------")

def realizar_pregunta():
    repreguntar = True
    while repreguntar:
        paises_data, preguntas, preguntas_patrones, _ = funciones.cargar_datos()
        
        pregunta = funciones.eliminar_acentos(input("Ingrese su pregunta o 'salir' si desea realizar otra accion: ")).replace("¿","").replace("?","")
        
        if not pregunta:
            print("No se ingresó ninguna pregunta")
            print("--------------------------------")
            continue
        
        if pregunta.lower().strip() == "salir" or pregunta.lower().strip() == "no":
            print("--------------------------------")
            return
        
        pregunta_datos = encontrar_pregunta(pregunta)
        
        if pregunta_datos is None:
            print("--------------------------------")
            print("Disculpe, no entendí su pregunta")
            
            salir = False # Variable que indica si se debe salir del bucle o no
            while not salir:
                print("Digame si desea:")
                print("1 - Reformularla")
                print("2 - Registrarla")
                print("3 - Salir al menú principal")
                opcion = input("").lower().strip()
                print("--------------------------------")
                
                if not opcion in ["1","2","3","salir"]: # Opciones validas que puede escribir el usuario
                    print("Disculpe, no se ingresó una opción valida")
                    print("--------------------------------")
                
                elif opcion == "1":
                    salir = True
                    
                elif opcion == "2":
                    agregar_pregunta()
                    salir = True
                else:
                    return #Se corta la funcion completa si el usuario elige salir
                
            
            continue
        
        pregunta_indice, tipo_pregunta = pregunta_datos
        pais_indice = encontrar_pais(pregunta.lower()) if tipo_pregunta == "dinamica" else None
        
        pregunta = preguntas[pregunta_indice].get("pregunta") if tipo_pregunta == "simple" else preguntas_patrones[pregunta_indice].get("pregunta")
        respuesta = preguntas[pregunta_indice].get("respuesta") if tipo_pregunta == "simple" else preguntas_patrones[pregunta_indice].get("respuesta")
        
        # En caso de que la pregunta sea dinamica y no simple
        if tipo_pregunta == "dinamica": 
            if pais_indice is not None: # Se hace el proceso de conversion de los datos si la pregunta es dinamica
                pais_data = paises_data[pais_indice]
                respuesta = funciones.reemplazar_datos(respuesta, pais_data)
                print("\n")
                print(respuesta)
                print("----------------------------------------------------------------")
            else: #Si el pais no esta registrado se pregunta si desea registrar o no
                print("--------------------------------")
                print("Disculpe, creo que no conozco el lugar que mencionas, ¿desea registrarlo?")
                opcion = ""
                while opcion.lower() not in ["1", "2", "si", "no"]: #Bucle para asegurarse de operar con valores validos
                    print("1 - Sí")
                    print("2 - No")
                    opcion = input("").lower()
                    if not opcion in ["1", "2", 'si', 'no']:
                        print("Opcion invalida")
                        print("----------------------------------------------------------------")

                if opcion.lower() in ["1","si"] :
                    agregar_pais()
                if opcion.lower() in ["2", "no"]:
                    print("--------------------------------")
                    repreguntar = False
                    continue
                print("--------------------------------")
            continue
        
        #Si la pregunta es simple solamente se imprime la respuesta
        print("--------------------------------")
        print(respuesta)
        print("--------------------------------")

#-------------------------------------------------------------------------------------------------------------

# COMIENZO DEL FLUJO DEL PROGRAMA

def menu_principal():
    opcion = ""
    while opcion != "4": # Bucle creado para que reitere las opciones si lo ingresado no es valido
    
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
            print("--------------------------------")
            print("Un placer ayudarte en lo que pueda, espero volver a verte pronto")
            print("--------------------------------")
        else:
            print("--------------------------------")
            print("Opción invalida")
            print("--------------------------------")

if __name__ == "__main__":
    menu_principal()