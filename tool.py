import subprocess
import platform
import os
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# Constante para verificar el sistema operativo
IS_WINDOWS = platform.system().lower() == 'windows'

# Diccionario de hosts
hosts = {
    '192.168.1.1': 'el Router',
    '192.168.100.1': 'Servitel',
    '192.168.101.1': 'Inter',
    '8.8.8.8': 'la Internet'
}

# Función para limpiar la pantalla
def limpiar_pantalla():
    os.system('cls' if IS_WINDOWS else 'clear')

# Función para ejecutar un comando en la terminal
def ejecutar_comando(comando):
    print(f'Ejecutando prueba, por favor espere...\n')
    try:
        # Usamos Popen para mostrar la salida en tiempo real
        proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        if proceso.stdout:
            for linea in proceso.stdout:
                print(linea, end='')
        proceso.wait()
    except Exception as e:
        print(Fore.RED + f'Ocurrió un error: {e}')

# Función para realizar un ping a una IP
def realizar_ping(ip, nombre='host'):
    """Realiza un ping a una IP y devuelve True si hay éxito, False si no."""
    try:
        # Ocultar la salida del comando ping en la consola
        param = '-n' if IS_WINDOWS else '-c'
        comando = ['ping', param, '2', ip]
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        return True
    except Exception as e:
        # Si hay un error (ej. check=True falla), asumimos que no hay conexión
        return False

# Función para trazar una ruta hacia Internet
def tracert_dns(direccion):
    comando = ['tracert', direccion] if IS_WINDOWS else ['traceroute', direccion]
    ejecutar_comando(comando)

# Función para el diagnóstico automático
def diagnostico_automatico():
    for ip, nombre in hosts.items():
        print(f'Verificando conexión con {nombre}')
        if realizar_ping(ip, nombre):
            print(Fore.GREEN + f'    ✓ Hay conexión con {nombre}\n')
        else:
            print(Fore.RED + f'    ✗ No hay conexión con {nombre}\n')

# Menú principal
def menu():
    opciones = {
        '1': diagnostico_automatico,
        '2': lambda: tracert_dns('8.8.8.8'),
        '0': exit
    }
    
    while True:
        print(f'1: Diagnóstico automático')
        print(f'2: Trazar ruta hacia Internet')
        print(f'0: Salir\n')

        try:
            opcion = input(f'Ingrese el número de la acción correspondiente: ')
            limpiar_pantalla()
            if opcion in opciones:
                opciones[opcion]()
                print("\n" + "="*40)
                input(Fore.YELLOW + 'Presione Enter para volver al menú...')
                limpiar_pantalla()
            else:
                print(Fore.RED + f'La opción no es válida. Intente de nuevo.')
                input(Fore.YELLOW + 'Presione Enter para continuar...')
                limpiar_pantalla()
        except KeyboardInterrupt:
            print(Fore.YELLOW + '\nSaliendo del programa...')
            break

# Punto de entrada del programa
if __name__ == "__main__":
    menu()