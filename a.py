from datetime import datetime, timedelta

class Avion:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.pasajeros = []

    def __str__(self):
        return f"Avión con capacidad para {self.capacidad} pasajeros."


class Pasajero:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

    def __str__(self):
        return f"• {self.nombre} {self.apellido}"


class Vuelo:
    def __init__(self, codigo, origen, destino, avion, duracion_horas):
        self.codigo = codigo
        self.origen = origen
        self.destino = destino
        self.avion = avion
        self.duracion_horas = duracion_horas
        self.hora_salida = None
        self.hora_llegada = None
        self.puerta_asignada = None
        self.estado = "En espera"
        self.personal_asignado = []
        self.pasajeros_asignados = []

    def asignar_horarios(self, hora_salida):
        self.hora_salida = hora_salida
        self.hora_llegada = hora_salida + timedelta(hours=self.duracion_horas)

    def __str__(self):
        puerta = f"Puerta {self.puerta_asignada.numero}" if self.puerta_asignada else "No asignada"
        salida = self.hora_salida.strftime("%H:%M") if self.hora_salida else "Por asignar"
        llegada = self.hora_llegada.strftime("%H:%M") if self.hora_llegada else "Por asignar"
        return (f"Vuelo {self.codigo}: {self.origen} → {self.destino} - {puerta}\n"
                f"   Avión: {self.avion} - Estado: {self.estado}\n"
                f"   Salida: {salida}, Llegada: {llegada}")


class PuertaEmbarque:
    def __init__(self, numero):
        self.numero = numero
        self.vuelo_asignado = None


class Personal:
    def __init__(self, nombre, apellido, rol):
        self.nombre = nombre
        self.apellido = apellido
        self.rol = rol

    def __str__(self):
        return f"• {self.nombre} {self.apellido} ({self.rol})"
    
class SimuladorAeropuerto:
    def __init__(self):
        self.vuelos = []
        self.aviones = [Avion(10)] 
        self.puertas = [PuertaEmbarque(i) for i in range(1, 6)]
        self.personal = []
        self.pasajeros = []

    def programar_vuelo(self, codigo, origen, destino, duracion_horas):
        avion = self.aviones[0]
        vuelo = Vuelo(codigo, origen, destino, avion, duracion_horas)
        self.vuelos.append(vuelo)
        return vuelo

    def asignar_puerta_a_vuelo(self, vuelo, hora_base):
        
        if vuelo.puerta_asignada:
            return f"La puerta ya está asignada al vuelo {vuelo.codigo}."

        for puerta in self.puertas:
            if puerta.vuelo_asignado is None: 
                puerta.vuelo_asignado = vuelo
                vuelo.puerta_asignada = puerta
                hora_salida = hora_base + timedelta(minutes=30)
                vuelo.asignar_horarios(hora_salida)
                return f"Puerta {puerta.numero} asignada al vuelo {vuelo.codigo}."
        return "No hay puertas disponibles."

    def agregar_pasajero(self, vuelo, nombre, apellido):
        if len(vuelo.pasajeros_asignados) >= 10:
            return "No se pueden agregar más pasajeros a este vuelo. Límite alcanzado."
        pasajero = Pasajero(nombre, apellido)
        vuelo.pasajeros_asignados.append(pasajero)
        return f"Pasajero {pasajero} agregado al vuelo {vuelo.codigo}."

    def agregar_personal(self, vuelo, nombre, apellido, rol):
        if rol == "Piloto" and len([p for p in vuelo.personal_asignado if p.rol == "Piloto"]) >= 2:
            return "No se pueden agregar más pilotos a este vuelo. Límite alcanzado."
        elif rol == "Sobrecargo" and len([p for p in vuelo.personal_asignado if p.rol == "Sobrecargo"]) >= 3:
            return "No se pueden agregar más sobrecargos a este vuelo. Límite alcanzado."
        persona = Personal(nombre, apellido, rol)
        vuelo.personal_asignado.append(persona)
        return f"Personal {persona} agregado al vuelo {vuelo.codigo}."

    def simular_trafico(self, hora_base):
        for vuelo in self.vuelos:
            if vuelo.estado == "En espera" and vuelo.hora_salida and vuelo.hora_salida <= hora_base:
                vuelo.estado = "En vuelo"
            elif vuelo.estado == "En vuelo" and vuelo.hora_llegada and vuelo.hora_llegada <= hora_base:
                vuelo.estado = "Aterrizado"

    def ver_lista_vuelos(self):
        if not self.vuelos:
            return "No hay vuelos registrados."
        return "\n".join(str(vuelo) for vuelo in self.vuelos)

    def ver_lista_personal(self, vuelo):
        if not vuelo.personal_asignado:
            return f"No hay personal registrado en el vuelo {vuelo.codigo}."
        return "\n".join(str(persona) for persona in vuelo.personal_asignado)

    def ver_lista_pasajeros(self, vuelo):
        if not vuelo.pasajeros_asignados:
            return f"No hay pasajeros registrados en el vuelo {vuelo.codigo}."
        return "\n".join(str(pasajero) for pasajero in vuelo.pasajeros_asignados)
    
def menu_principal():
    simulador = SimuladorAeropuerto()

    # Configuración inicial con hora actual
    print("\n=== Configuración inicial ===")
    hora_base = datetime.now()

    def agregar_personal():
        print("\n=== Agregar Personal ===")
        nombre = input("Nombre del personal: ")
        apellido = input("Apellido del personal: ")
        print("Seleccione el rol:")
        print("1. Piloto")
        print("2. Sobrecargo")
        opcion_rol = input("Seleccione una opción (1 o 2): ")
        rol = "Piloto" if opcion_rol == "1" else "Sobrecargo" if opcion_rol == "2" else None
        if not rol:
            print("Rol inválido.")
            return
        vuelo_codigo = input("Ingrese el código del vuelo al que se asignará el personal: ")
        vuelo = next((v for v in simulador.vuelos if v.codigo == vuelo_codigo), None)
        if vuelo:
            mensaje = simulador.agregar_personal(vuelo, nombre, apellido, rol)
            print(mensaje)
        else:
            print("Vuelo no encontrado.")

    def agregar_pasajero():
        print("\n=== Agregar Pasajero ===")
        nombre = input("Nombre del pasajero: ")
        apellido = input("Apellido del pasajero: ")
        vuelo_codigo = input("Ingrese el código del vuelo al que se asignará el pasajero: ")
        vuelo = next((v for v in simulador.vuelos if v.codigo == vuelo_codigo), None)
        if vuelo:
            mensaje = simulador.agregar_pasajero(vuelo, nombre, apellido)
            print(mensaje)
        else:
            print("Vuelo no encontrado.")

    def programar_vuelo():
        print("\n=== Programar Vuelo ===")
        codigo = input("Código del vuelo: ")
        origen = input("Ciudad de origen: ")
        destino = input("Ciudad de destino: ")
        duracion_horas = int(input("Duración del vuelo (en horas): "))
        vuelo = simulador.programar_vuelo(codigo, origen, destino, duracion_horas)
        print(f"Vuelo {vuelo} programado con éxito.")

    def asignar_puerta():
        print("\n=== Asignar Puerta a Vuelo ===")
        if not simulador.vuelos:
            print("No hay vuelos disponibles.")
            return
        vuelo_codigo = input("Ingrese el código del vuelo al que se asignará la puerta: ")
        vuelo = next((v for v in simulador.vuelos if v.codigo == vuelo_codigo), None)
        if vuelo:
            mensaje = simulador.asignar_puerta_a_vuelo(vuelo, hora_base)
            print(mensaje)
        else:
            print("Vuelo no encontrado.")

    def ver_listas():
        print("\n=== Ver Listas ===")
        vuelo_codigo = input("Ingrese el código del vuelo para ver las listas de pasajeros y personal: ")
        vuelo = next((v for v in simulador.vuelos if v.codigo == vuelo_codigo), None)
        if vuelo:
            print("\nLista de Personal:")
            print(simulador.ver_lista_personal(vuelo))
            print("\nLista de Pasajeros:")
            print(simulador.ver_lista_pasajeros(vuelo))
        else:
            print("Vuelo no encontrado.")

    def trafico_aereo():
        simulador.simular_trafico(hora_base)
        print("\nTráfico Aéreo simulado.")
        print("\n=== Lista de Vuelos ===")
        print(simulador.ver_lista_vuelos())

    while True:
        print("\n=== Menú Principal ===")
        print("1. Programar Vuelo")
        print("2. Asignar Puerta")
        print("3. Agregar Personal")
        print("4. Agregar Pasajero")
        print("5. Tráfico Aéreo")
        print("6. Ver Listas")
        print("7. Salir")
        opcion = input("Seleccione una opción (1-7): ")

        if opcion == "1":
            programar_vuelo()
        elif opcion == "2":
            asignar_puerta()
        elif opcion == "3":
            agregar_personal()
        elif opcion == "4":
            agregar_pasajero()
        elif opcion == "5":
            trafico_aereo()
        elif opcion == "6":
            ver_listas()
        elif opcion == "7":
            print("Saliendo del simulador...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


menu_principal()    