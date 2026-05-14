from typing import List, Optional, Dict

class Estudiante:
    def __init__(self, nombre: str, apellido: str, matricula: str, carrera: str):
        self.nombre = nombre
        self.apellido = apellido
        self.matricula = matricula # Identificador único
        self.carrera = carrera
        self.cursos_inscriptos: List[str] = [] # Lista de códigos de curso

    def inscribirse(self, codigo_curso: str) -> bool:
        """Agrega un curso a la lista del estudiante"""
        if codigo_curso not in self.cursos_inscriptos:
            self.cursos_inscriptos.append(codigo_curso)
            return True
        return False

    def darse_de_baja(self, codigo_curso: str) -> bool:
        """Quita un curso de la lista del estudiante"""
        if codigo_curso in self.cursos_inscriptos:
            self.cursos_inscriptos.remove(codigo_curso)
            return True
        return False

    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"

    def __str__(self):
        cursos = ", ".join(self.cursos_inscriptos) if self.cursos_inscriptos else "Ninguno"
        return f"[{self.matricula}] {self.nombre_completo()} | {self.carrera} | Cursos: {cursos}"

class Curso:
    def __init__(self, nombre: str, codigo: str, profesor: str, capacidad_max: int):
        self.nombre = nombre
        self.codigo = codigo
        self.profesor = profesor
        self.capacidad_max = capacidad_max
        self.estudiantes_inscriptos: List[str] = [] # Lista de matrículas

    def tiene_cupo(self) -> bool:
        """Verifica si hay cupos disponibles"""
        return len(self.estudiantes_inscriptos) < self.capacidad_max

    def inscribir_estudiante(self, matricula: str) -> bool:
        """Inscribe un estudiante si hay cupo"""
        if self.tiene_cupo() and matricula not in self.estudiantes_inscriptos:
            self.estudiantes_inscriptos.append(matricula)
            return True
        return False

    def dar_de_baja_estudiante(self, matricula: str) -> bool:
        """Da de baja un estudiante del curso"""
        if matricula in self.estudiantes_inscriptos:
            self.estudiantes_inscriptos.remove(matricula)
            return True
        return False

    def cupos_disponibles(self) -> int:
        return self.capacidad_max - len(self.estudiantes_inscriptos)

    def __str__(self):
        inscriptos = len(self.estudiantes_inscriptos)
        return (f"[{self.codigo}] {self.nombre} - Prof. {self.profesor} | "
                f"Inscriptos: {inscriptos}/{self.capacidad_max} | "
                f"Disponibles: {self.cupos_disponibles()}")

class Facultad:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.estudiantes: Dict[str, Estudiante] = {} # matricula -> Estudiante
        self.cursos: Dict[str, Curso] = {} # codigo -> Curso

    def registrar_estudiante(self, nombre: str, apellido: str, matricula: str, carrera: str) -> bool:
        """Registra un nuevo estudiante"""
        if matricula in self.estudiantes:
            print(f"Error: Ya existe un estudiante con matrícula {matricula}")
            return False

        self.estudiantes[matricula] = Estudiante(nombre, apellido, matricula, carrera)
        print(f"Estudiante {nombre} {apellido} registrado correctamente")
        return True

    def registrar_curso(self, nombre: str, codigo: str, profesor: str, capacidad_max: int) -> bool:
        """Registra un nuevo curso"""
        if codigo in self.cursos:
            print(f"Error: Ya existe un curso con código {codigo}")
            return False

        if capacidad_max <= 0:
            print("Error: La capacidad máxima debe ser mayor a 0")
            return False

        self.cursos[codigo] = Curso(nombre, codigo, profesor, capacidad_max)
        print(f"Curso '{nombre}' registrado correctamente")
        return True

    def inscribir_a_curso(self, matricula: str, codigo_curso: str) -> bool:
        """Inscribe un estudiante a un curso"""
        if matricula not in self.estudiantes:
            print(f"Error: No existe estudiante con matrícula {matricula}")
            return False

        if codigo_curso not in self.cursos:
            print(f"Error: No existe curso con código {codigo_curso}")
            return False

        estudiante = self.estudiantes[matricula]
        curso = self.cursos[codigo_curso]

        if not curso.tiene_cupo():
            print(f"Error: El curso '{curso.nombre}' no tiene cupos disponibles")
            return False

        if codigo_curso in estudiante.cursos_inscriptos:
            print(f"Error: El estudiante ya está inscripto en '{curso.nombre}'")
            return False

        curso.inscribir_estudiante(matricula)
        estudiante.inscribirse(codigo_curso)
        print(f"{estudiante.nombre_completo()} inscripto en '{curso.nombre}'")
        return True

    def dar_de_baja_de_curso(self, matricula: str, codigo_curso: str) -> bool:
        """Da de baja un estudiante de un curso"""
        if matricula not in self.estudiantes or codigo_curso not in self.cursos:
            print("Error: Estudiante o curso no encontrado")
            return False

        estudiante = self.estudiantes[matricula]
        curso = self.cursos[codigo_curso]

        if codigo_curso not in estudiante.cursos_inscriptos:
            print(f"Error: El estudiante no está inscripto en '{curso.nombre}'")
            return False

        curso.dar_de_baja_estudiante(matricula)
        estudiante.darse_de_baja(codigo_curso)
        print(f"{estudiante.nombre_completo()} dado de baja de '{curso.nombre}'")
        return True

    def consultar_estado_cursos(self):
        """Muestra el estado de todos los cursos"""
        print(f"\n=== ESTADO DE CURSOS - {self.nombre} ===")
        if not self.cursos:
            print("No hay cursos registrados")
            return

        for curso in self.cursos.values():
            print(curso)
            if curso.estudiantes_inscriptos:
                nombres = [self.estudiantes[m].nombre_completo() for m in curso.estudiantes_inscriptos]
                print(f" Estudiantes: {', '.join(nombres)}")

    def consultar_estado_estudiantes(self):
        """Muestra el estado de todos los estudiantes"""
        print(f"\n=== ESTADO DE ESTUDIANTES - {self.nombre} ===")
        if not self.estudiantes:
            print("No hay estudiantes registrados")
            return

        for estudiante in self.estudiantes.values():
            print(estudiante)

    def buscar_estudiante(self, matricula: str) -> Optional[Estudiante]:
        return self.estudiantes.get(matricula)

    def buscar_curso(self, codigo: str) -> Optional[Curso]:
        return self.cursos.get(codigo)

# === EJEMPLO DE USO ===
if __name__ == "__main__":
    # Crear facultad
    facu = Facultad("Facultad de Ingeniería - UNR")

    # Registrar estudiantes
    facu.registrar_estudiante("Juan", "González", "E001", "Ingeniería en Sistemas")
    facu.registrar_estudiante("María", "López", "E002", "Ingeniería Civil")
    facu.registrar_estudiante("Carlos", "Rodríguez", "E003", "Ingeniería en Sistemas")

    # Registrar cursos
    facu.registrar_curso("Programación I", "PROG1", "Dr. Fernández", 2)
    facu.registrar_curso("Álgebra Lineal", "ALG101", "Dra. Martínez", 30)
    facu.registrar_curso("Física I", "FIS1", "Dr. Gómez", 25)

    # Inscripciones
    facu.inscribir_a_curso("E001", "PROG1")
    facu.inscribir_a_curso("E002", "PROG1")
    facu.inscribir_a_curso("E003", "PROG1") # Error: sin cupo
    facu.inscribir_a_curso("E001", "ALG101")

    # Consultar estados
    facu.consultar_estado_cursos()
    facu.consultar_estado_estudiantes()

    # Dar de baja
    facu.dar_de_baja_de_curso("E001", "PROG1")
    facu.inscribir_a_curso("E003", "PROG1") # Ahora sí hay cupo

    print("\n--- DESPUÉS DE LOS CAMBIOS ---")
    facu.consultar_estado_cursos()