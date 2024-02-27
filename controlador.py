import simpy
import random
env = simpy.Environment()
ram = simpy.Container(env, init=100, capacity=100)
cpu = simpy.Resource(env, capacity=1)
random.seed(42)
cantProcesos = 25

class Proceso:
    #Constructor de un proceso
    def __init__(self, id, cantRam, cantInstrucciones):
        self.id =id
        self.cantRam = cantRam
        self.cantInstrucciones = cantInstrucciones

def crearProceso():
    #----------------Creación de procesos-------------
    for i in range(cantProcesos):
        intervalo = 10
        yield env.timeout(random.expovariate(1.0/ intervalo))
        proceso = Proceso(i, random.randint(1, 10), random.randint(1, 10))
        #print(f'Proceso {proceso.id} creado, solicita {proceso.cantRam} de ram y con {proceso.cantInstrucciones} intrucciones en {env.now}')
        #yield from new(proceso)
        env.process(new(proceso))


def new(proceso_actual):
    with ram.get(proceso_actual.cantRam) as req:
        yield req
        yield ram.get(proceso_actual.cantRam)
        while proceso_actual.cantInstrucciones >0:
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
    
def correr():
    env.process(crearProceso())
    env.run()


            




    

    
            
        
        
        


        


            

            
        

    








        







