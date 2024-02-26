import controlador
continuar_programa = True
#Menu
while continuar_programa: 
    print(
    """
    1. Realizar simulación
    2. Salir
    """)
    opcion = input("Seleccione una opcion: ")
    if opcion == "1":
        controlador.etapase()
    if opcion == "2":
        continuar_programa = False

    