import simpy
import random
from collections import deque

env = simpy.Environment()
ram = simpy.Container(env, init=100, capacity=100)
cpu = simpy.Resource(env, capacity=1)
random.seed(42)
#espera_new = simpy.Store(env)
#espera_ready = simpy.Store(env)
espera_new = []
espera_ready = []
espera_waiting = []
    
def etapas():
    #----------------ETAPA NEW (Primera etapa)-------------
    cantProcesos = 10
    for i in range(cantProcesos):
        #Agregar a la cola "x" objetos
        proceso = Proceso(i, random.randint(1, 10), random.randint(1, 10), False)
        espera_new.append(proceso)

    while espera_new:
        proceso_actual = espera_new.pop()

        # Verificar si hay suficiente memoria RAM disponible
        if ram.level >= proceso_actual.cantRam:
            # Asignar memoria RAM al proceso
            yield ram.get(proceso_actual.cantRam)
            
            # Poner el proceso en la cola de ready
            espera_ready.append(proceso_actual)
            
            print(f"Proceso {proceso_actual.id} pasa a estado 'ready'. RAM disponible: {ram.level}")
        else:
            if proceso_actual not in espera_new:
                # Si no hay suficiente memoria, volver a poner el proceso en la cola de espera_new
                espera_new.append(proceso_actual)
                print(f"No hay suficiente RAM para el Proceso {proceso_actual.id}. Esperando. RAM disponible: {ram.level}")
        
        # Esperar algún tiempo antes de agregar más procesos (simulando el paso del tiempo)
        yield env.timeout(1)

    #----------ETAPA READY (Segunda etapa)--------------
    while espera_ready:
        #Elemento que esta en la cola de espera_ready
        proceso_ready = espera_ready.pop(0)

        with cpu.request() as req:
            yield req  # Esperar a que la CPU esté disponible

            # Calcular las instrucciones a ejecutar
            numero_intrucciones = 3
            instrucciones_a_ejecutar = min(numero_intrucciones, proceso_ready.cantInstrucciones)

            # Actualizar el contador de instrucciones del proceso
            proceso_ready.cantInstrucciones -= instrucciones_a_ejecutar

            print(f"Proceso {proceso_ready.id} en estado 'Running' ejecutando {instrucciones_a_ejecutar} instrucciones.")

    #----------ETAPA RUNNING (Tercera etapa)--------------

            #Verifica cuántas instrucciones le quedan al proceso
            if proceso_ready.cantInstrucciones <= 0:
                print(f"Proceso {proceso_ready.id} completado. Liberando RAM.")
                yield ram.put(proceso_ready.cantRam)  # Liberar RAM
            else:
                opcion = random.randint(1, 2)
                if opcion == 1:
                    espera_waiting.append(proceso_ready)
                    espera_waiting.remove(proceso_ready)
                    espera_ready.append(proceso_ready)
                else:
                    espera_ready.append(proceso_ready)
                    print(f"Proceso {proceso_ready.id} vuelve a estado 'Ready'. Instrucciones restantes: {proceso_ready.cantInstrucciones}")

    print("Procesos terminado " + str(len(espera_ready)) + " " + str(len(espera_waiting)))


class Proceso:
    #Constructor de un proceso
    def __init__(self, id, cantRam, cantInstrucciones, estado):
        self.id =id
        self.cantRam = cantRam
        self.cantInstrucciones = cantInstrucciones
        self.estado = estado      

env.process(etapas())
env.run(until=11)
            
        
        
        


        


            

            
        

    








        







