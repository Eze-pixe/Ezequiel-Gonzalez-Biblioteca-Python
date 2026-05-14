from datetime import datetime
from typing import List, Optional

class Libro:
    def __init__(self, titulo: str, autor: str, isbn: str):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = True
        self.prestado_a = None # Guarda el ID del miembro

    def prestar(self, miembro_id: str) -> bool:
        """Marca el libro como prestado si está disponible"""
        if self.disponible:
            self.disponible = False
            self.prestado_a = miembro_id
            return True
        return False

    def devolver(self) -> bool:
        """Marca el libro como disponible"""
        if not self.disponible:
            self.disponible = False
            self.prestado_a = None
            return True
        return False

    def __str__(self):
        estado = "Disponible" if self.disponible else f"Prestado a ID: {self.prestado_a}"
        return f"[{self.isbn}] {self.titulo} - {self.autor} | {estado}"

class Miembro:
    def __init__(self, nombre: str, miembro_id: str):
        self.nombre = nombre
        self.miembro_id = miembro_id
        self.libros_prestados: List[str] = [] # Lista de ISBNs

    def agregar_libro(self, isbn: str):
        """Registra un libro prestado al miembro"""
        if isbn not in self.libros_prestados:
            self.libros_prestados.append(isbn)

    def quitar_libro(self, isbn: str):
        """Quita un libro de la lista de prestados"""
        if isbn in self.libros_prestados:
            self.libros_prestados.remove(isbn)

    def __str__(self):
        libros = ", ".join(self.libros_prestados) if self.libros_prestados else "Ninguno"
        return f"ID: {self.miembro_id} | {self.nombre} | Libros: {libros}"

class Prestamo:
    def __init__(self, libro: Libro, miembro: Miembro):
        self.libro = libro
        self.miembro = miembro
        self.fecha_prestamo = datetime.now()
        self.fecha_devolucion = None

    def registrar_devolucion(self):
        self.fecha_devolucion = datetime.now()

class Biblioteca:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.libros = {} # isbn -> Libro
        self.miembros = {} # miembro_id -> Miembro
        self.prestamos_activos = [] # Lista de Prestamo

    def registrar_libro(self, titulo: str, autor: str, isbn: str) -> bool:
        """Añade un nuevo libro al sistema"""
        if isbn in self.libros:
            print(f"Error: Ya existe un libro con ISBN {isbn}")
            return False

        self.libros[isbn] = Libro(titulo, autor, isbn)
        print(f"Libro '{titulo}' registrado correctamente")
        return True

    def registrar_miembro(self, nombre: str, miembro_id: str) -> bool:
        """Añade un nuevo miembro al sistema"""
        if miembro_id in self.miembros:
            print(f"Error: Ya existe un miembro con ID {miembro_id}")
            return False

        self.miembros[miembro_id] = Miembro(nombre, miembro_id)
        print(f"Miembro '{nombre}' registrado correctamente")
        return True

    def prestar_libro(self, isbn: str, miembro_id: str) -> bool:
        """Gestiona el préstamo de un libro a un miembro"""
        if isbn not in self.libros:
            print(f"Error: No existe libro con ISBN {isbn}")
            return False

        if miembro_id not in self.miembros:
            print(f"Error: No existe miembro con ID {miembro_id}")
            return False

        libro = self.libros[isbn]
        miembro = self.miembros[miembro_id]

        if libro.prestar(miembro_id):
            miembro.agregar_libro(isbn)
            self.prestamos_activos.append(Prestamo(libro, miembro))
            print(f"'{libro.titulo}' prestado a {miembro.nombre}")
            return True
        else:
            print(f"Error: El libro '{libro.titulo}' no está disponible")
            return False

    def devolver_libro(self, isbn: str, miembro_id: str) -> bool:
        """Gestiona la devolución de un libro"""
        if isbn not in self.libros or miembro_id not in self.miembros:
            print("Error: Libro o miembro no encontrado")
            return False

        libro = self.libros[isbn]
        miembro = self.miembros[miembro_id]

        if libro.prestado_a!= miembro_id:
            print(f"Error: El libro no está prestado a {miembro.nombre}")
            return False

        libro.devolver()
        miembro.quitar_libro(isbn)

        # Actualizar registro de préstamo
        for prestamo in self.prestamos_activos:
            if prestamo.libro.isbn == isbn and prestamo.miembro.miembro_id == miembro_id:
                prestamo.registrar_devolucion()
                self.prestamos_activos.remove(prestamo)
                break

        print(f"'{libro.titulo}' devuelto por {miembro.nombre}")
        return True

    def consultar_estado_libros(self):
        """Muestra el estado de todos los libros"""
        print(f"\n=== ESTADO DE LIBROS - {self.nombre} ===")
        if not self.libros:
            print("No hay libros registrados")
            return

        for libro in self.libros.values():
            print(libro)

    def consultar_estado_miembros(self):
        """Muestra el estado de todos los miembros"""
        print(f"\n=== ESTADO DE MIEMBROS - {self.nombre} ===")
        if not self.miembros:
            print("No hay miembros registrados")
            return

        for miembro in self.miembros.values():
            print(miembro)

    def buscar_libro(self, isbn: str) -> Optional[Libro]:
        return self.libros.get(isbn)

    def buscar_miembro(self, miembro_id: str) -> Optional[Miembro]:
        return self.miembros.get(miembro_id)

# === EJEMPLO DE USO ===
if __name__ == "__main__":
    # Crear biblioteca
    biblio = Biblioteca("Biblioteca Central Rosario")

    # Registrar libros
    biblio.registrar_libro("Cien años de soledad", "Gabriel García Márquez", "978-0307474728")
    biblio.registrar_libro("El Principito", "Antoine de Saint-Exupéry", "978-0156013987")
    biblio.registrar_libro("1984", "George Orwell", "978-0451524935")

    # Registrar miembros
    biblio.registrar_miembro("Ana García", "M001")
    biblio.registrar_miembro("Luis Pérez", "M002")

    # Prestar libros
    biblio.prestar_libro("978-0307474728", "M001")
    biblio.prestar_libro("978-0156013987", "M001")
    biblio.prestar_libro("978-0307474728", "M002") # Error: no disponible

    # Consultar estados
    biblio.consultar_estado_libros()
    biblio.consultar_estado_miembros()

    # Devolver libro
    biblio.devolver_libro("978-0307474728", "M001")

    # Consultar de nuevo
    biblio.consultar_estado_libros()