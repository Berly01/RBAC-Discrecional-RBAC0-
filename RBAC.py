import cmd
import os

class RBAC:
    def __init__(self):
        self.roles = {}
        self.usuarios = {}

    def agregar_rol(self, nombre_rol, permisos):
        self.roles[nombre_rol] = permisos
        print(f"Rol '{nombre_rol}' agregado con permisos: {permisos}")

    def asignar_rol_a_usuario(self, nombre_usuario, nombre_rol):
        if nombre_rol in self.roles:
            if nombre_usuario not in self.usuarios:
                self.usuarios[nombre_usuario] = []
            self.usuarios[nombre_usuario].append(nombre_rol)
            print(f"Usuario '{nombre_usuario}' asignado al rol '{nombre_rol}'")
        else:
            print(f"El rol '{nombre_rol}' no existe.")

    def obtener_permisos_usuario(self, nombre_usuario):
        if nombre_usuario not in self.usuarios:
            print(f"El usuario '{nombre_usuario}' no existe.")
            return []

        permisos = set()
        for rol in self.usuarios[nombre_usuario]:
            permisos.update(self.roles[rol])
        return list(permisos)

    def verificar_permiso(self, nombre_usuario, permiso):
        permisos_usuario = self.obtener_permisos_usuario(nombre_usuario)
        return permiso in permisos_usuario

class SistemaArchivosRBAC(RBAC):
    def crear_archivo(self, nombre_usuario, nombre_archivo, contenido=""):
        if self.verificar_permiso(nombre_usuario, 'crear'):
            with open(nombre_archivo, 'w') as archivo:
                archivo.write(contenido)
            print(f"Archivo '{nombre_archivo}' creado por '{nombre_usuario}'")
        else:
            print(f"Acceso denegado: El usuario '{nombre_usuario}' no tiene permiso para crear archivos.")

    def leer_archivo(self, nombre_usuario, nombre_archivo):
        if self.verificar_permiso(nombre_usuario, 'leer'):
            if os.path.exists(nombre_archivo):
                with open(nombre_archivo, 'r') as archivo:
                    contenido = archivo.read()
                print(f"Contenido de '{nombre_archivo}':\n{contenido}")
            else:
                print(f"El archivo '{nombre_archivo}' no existe.")
        else:
            print(f"Acceso denegado: El usuario '{nombre_usuario}' no tiene permiso para leer archivos.")

    def escribir_archivo(self, nombre_usuario, nombre_archivo, contenido):
        if self.verificar_permiso(nombre_usuario, 'escribir'):
            if os.path.exists(nombre_archivo):
                with open(nombre_archivo, 'w') as archivo:
                    archivo.write(contenido)
                print(f"Archivo '{nombre_archivo}' actualizado por '{nombre_usuario}'")
            else:
                print(f"El archivo '{nombre_archivo}' no existe.")
        else:
            print(f"Acceso denegado: El usuario '{nombre_usuario}' no tiene permiso para escribir archivos.")

    def eliminar_archivo(self, nombre_usuario, nombre_archivo):
        if self.verificar_permiso(nombre_usuario, 'eliminar'):
            if os.path.exists(nombre_archivo):
                os.remove(nombre_archivo)
                print(f"Archivo '{nombre_archivo}' eliminado por '{nombre_usuario}'")
            else:
                print(f"El archivo '{nombre_archivo}' no existe.")
        else:
            print(f"Acceso denegado: El usuario '{nombre_usuario}' no tiene permiso para eliminar archivos.")

class InterfazRBAC(cmd.Cmd):
    intro = "Bienvenido al sistema de archivos RBAC. Escribe 'help' o '?' para listar los comandos."
    prompt = "(RBAC) "

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rbac = SistemaArchivosRBAC()

    def do_agregar_rol(self, arg):
        "Agregar un nuevo rol: agregar_rol <nombre_rol> <permiso1, permiso2, ...>"
        try:
            partes = arg.split()
            nombre_rol = partes[0]
            permisos = partes[1].split(',')
            self.rbac.agregar_rol(nombre_rol, permisos)
        except IndexError:
            print("Error: Proporcione un nombre de rol y una lista de permisos.")

    def do_asignar_rol(self, arg):
        "Asignar un rol a un usuario: asignar_rol <nombre_usuario> <nombre_rol>"
        try:
            nombre_usuario, nombre_rol = arg.split()
            self.rbac.asignar_rol_a_usuario(nombre_usuario, nombre_rol)
        except ValueError:
            print("Error: Proporcione tanto el nombre del usuario como el nombre del rol.")

    def do_crear_archivo(self, arg):
        "Crear un nuevo archivo: crear_archivo <nombre_usuario> <nombre_archivo> <contenido>"
        try:
            partes = arg.split(maxsplit=2)
            nombre_usuario, nombre_archivo = partes[0], partes[1]
            contenido = partes[2] if len(partes) > 2 else ""
            self.rbac.crear_archivo(nombre_usuario, nombre_archivo, contenido)
        except IndexError:
            print("Error: Proporcione un nombre de usuario, nombre de archivo y contenido opcional.")

    def do_leer_archivo(self, arg):
        "Leer un archivo: leer_archivo <nombre_usuario> <nombre_archivo>"
        try:
            nombre_usuario, nombre_archivo = arg.split()
            self.rbac.leer_archivo(nombre_usuario, nombre_archivo)
        except ValueError:
            print("Error: Proporcione tanto el nombre del usuario como el nombre del archivo.")

    def do_escribir_archivo(self, arg):
        "Escribir en un archivo existente: escribir_archivo <nombre_usuario> <nombre_archivo> <contenido>"
        try:
            partes = arg.split(maxsplit=2)
            nombre_usuario, nombre_archivo, contenido = partes[0], partes[1], partes[2]
            self.rbac.escribir_archivo(nombre_usuario, nombre_archivo, contenido)
        except ValueError:
            print("Error: Proporcione un nombre de usuario, nombre de archivo y contenido.")

    def do_eliminar_archivo(self, arg):
        "Eliminar un archivo: eliminar_archivo <nombre_usuario> <nombre_archivo>"
        try:
            nombre_usuario, nombre_archivo = arg.split()
            self.rbac.eliminar_archivo(nombre_usuario, nombre_archivo)
        except ValueError:
            print("Error: Proporcione tanto el nombre del usuario como el nombre del archivo.")

    def do_obtener_permisos(self, nombre_usuario):
        "Obtener los permisos de un usuario: obtener_permisos <nombre_usuario>"
        permisos = self.rbac.obtener_permisos_usuario(nombre_usuario)
        if permisos:
            print(f"Permisos del usuario '{nombre_usuario}': {', '.join(permisos)}")
        else:
            print(f"El usuario '{nombre_usuario}' no tiene permisos o no existe.")

    def do_verificar_permiso(self, arg):
        "Verificar si un usuario tiene un permiso especifico: verificar_permiso <nombre_usuario> <permiso>"
        try:
            nombre_usuario, permiso = arg.split()
            if self.rbac.verificar_permiso(nombre_usuario, permiso):
                print(f"El usuario '{nombre_usuario}' tiene permiso de '{permiso}'.")
            else:
                print(f"El usuario '{nombre_usuario}' no tiene permiso de '{permiso}'.")
        except ValueError:
            print("Error: Proporcione tanto el nombre del usuario como el permiso.")

    def do_salir(self, arg):
        "Salir del sistema RBAC"
        print("Saliendo del sistema RBAC...")
        return True

if __name__ == '__main__':
    InterfazRBAC().cmdloop()
