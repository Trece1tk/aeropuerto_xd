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