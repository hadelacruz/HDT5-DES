import simpy
import random
import csv

env = simpy.Environment()
ram = simpy.Container(env, init=100, capacity=100)
cpu = simpy.Resource(env, capacity=1)
random.seed(42)
procesos = []
cantProcesos = 25
intervalo = 10


class Proceso:
    #Constructor de un proceso
    def __init__(self, id, cantRam, cantInstrucciones):
        self.id =id
        self.cantRam = cantRam
        self.cantInstrucciones = cantInstrucciones

def correr():
    for  i in range(cantProcesos):
        env.process(crearProceso(i))
    env.run()

def crearProceso(i):
    #----------------Creación de procesos-------------
    yield env.timeout(random.expovariate(1.0/ intervalo))
    proceso = Proceso(i, random.randint(1, 10), random.randint(1, 10))
    agregarProcesoInicio(procesos, proceso.id, env.now)
    yield from new(proceso)
    #env.process(new(proceso))


def new(proceso_actual):
    with ram.get(proceso_actual.cantRam) as req:
        yield req
        while proceso_actual.cantInstrucciones > 0:
            yield from ready(proceso_actual)
            numeroAleatorio = random.randint(1,2)
            if(numeroAleatorio == 1):
                #Cola Waiting
                yield env.timeout(2)
        ram.put(proceso_actual.cantRam)        
    
def ready(proceso_actual):
    with cpu.request() as req:
        yield req  # Esperar a que la CPU esté disponible
        #Dirigirse a la etapa Running
        yield from running(proceso_actual)

def running(proceso_actual):
    yield env.timeout(1)
    # Calcular las instrucciones a ejecutar
    numero_intrucciones = 3
    # Actualizar el contador de instrucciones del proceso
    proceso_actual.cantInstrucciones -= numero_intrucciones
    if proceso_actual.cantInstrucciones <= 0:
        print(f"Proceso {proceso_actual.id} completado. En el timepo: {env.now}")
        agregarProcesoFinal(procesos, proceso_actual.id, env.now )
    

def archivoCSV():
    # Escribir en el archivo CSV
    # Nombre del archivo CSV
    nombre_archivo = "datos.csv"
    with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as archivo_csv:
        # Crear el escritor CSV
        escritor_csv = csv.DictWriter(archivo_csv, fieldnames=["id", "tiempoCreacion", "tiempoFinalizacion"])

        # Escribir la fila de encabezado
        escritor_csv.writeheader()

        # Escribir los datos
        for item in procesos:
            escritor_csv.writerow(item)

    print(f"Los datos se han almacenado en el archivo CSV: {nombre_archivo}")


def agregarProcesoInicio(lista, id_proceso, tiempo_creacion):
    for item in lista:
        if item["id"] == id_proceso:
            # Si el ID ya existe, actualizar tiempos
            item["tiempoCreacion"] = tiempo_creacion
            return
    # Si no se encuentra, agregar nuevo diccionario
    lista.append({"id": id_proceso, "tiempoCreacion": tiempo_creacion, "tiempoFinalizacion": 0})

def agregarProcesoFinal(lista, id_proceso, tiempo_finalizacion):
    for item in lista:
        if item["id"] == id_proceso:
            # Si el ID ya existe, actualizar tiempos
            item["tiempoFinalizacion"] = tiempo_finalizacion
            return




            




    

    
            
        
        
        


        


            

            
        

    








        







