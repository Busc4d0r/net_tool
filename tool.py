import subprocess
import platform
import os
import json
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# Constante para verificar el sistema operativo
IS_WINDOWS = platform.system().lower() == 'windows'

# Variable global para los hosts
hosts = {}

def cargar_hosts():
    """Carga la lista de hosts desde el archivo hosts.json."""
    global hosts
    try:
        with open('hosts.json', 'r') as f:
            hosts = json.load(f)
        return True
    except FileNotFoundError:
        print(Fore.RED + "Error: No se encontró el archivo 'hosts.json'.")
        print("Por favor, cree el archivo con el formato {'ip': 'nombre', ...}")
        return False
    except json.JSONDecodeError:
        print(Fore.RED + "Error: El archivo 'hosts.json' tiene un formato inválido.")
        return False

def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if IS_WINDOWS else 'clear')

def ejecutar_comando(comando):
    """Ejecuta un comando en la terminal y muestra su salida en tiempo real."""
    print(f'Ejecutando: {" ".join(comando)}' + '\nPor favor espere...')
    try:
        proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        for linea in proceso.stdout:
            print(linea, end='')
        ret_code = proceso.wait()
        if ret_code:
            print(Fore.RED + f'El comando "{" ".join(comando)}" terminó con código de error: {ret_code}')
    except Exception as e:
        print(Fore.RED + f'Ocurrió un error al ejecutar "{" ".join(comando)}": {e}')

def realizar_ping(ip):
    """
    Realiza un ping a una dirección IP para verificar la conectividad.

    Args:
        ip (str): La dirección IP a la que hacer ping.

    Returns:
        bool: True si el ping es exitoso, False en caso contrario.
    """
    try:
        param = '-n' if IS_WINDOWS else '-c'
        comando = ['ping', param, '2', ip]
        subprocess.run(comando, capture_output=True, text=True, check=True, timeout=10)
        return True
    except subprocess.CalledProcessError:
        # El comando ping falló (no hubo respuesta)
        return False
    except subprocess.TimeoutExpired:
        print(Fore.YELLOW + f'    El ping a {ip} tardó demasiado en responder.')
        return False
    except Exception as e:
        # Otros errores, como que el comando no exista
        print(Fore.RED + f'    Error inesperado al hacer ping a {ip}: {e}')
        return False

def trazar_ruta(direccion):
    """Ejecuta un traceroute (o tracert) a una dirección."""
    print(f"Trazando la ruta hacia {direccion}...")
    comando = ['tracert', direccion] if IS_WINDOWS else ['traceroute', direccion]
    ejecutar_comando(comando)

def diagnostico_automatico():
    """Realiza un ping a todos los hosts definidos en hosts.json."""
    if not hosts:
        print(Fore.YELLOW + "No hay hosts definidos para el diagnóstico.")
        return

    print("Iniciando diagnóstico automático...")
    for ip, nombre in hosts.items():
        print(f'Verificando conexión con {nombre} ({ip})...')
        if realizar_ping(ip):
            print(Fore.GREEN + f'    ✓ Hay conexión con {nombre}\n')
        else:
            print(Fore.RED + f'    ✗ No hay conexión con {nombre}\n')

def menu():
    """Muestra el menú principal y maneja la selección del usuario."""
    while True:
        print("===== MENÚ DE DIAGNÓSTICO DE RED =====")
        print("1: Diagnóstico automático")
        print("2: Trazar ruta hacia Internet (8.8.8.8)")
        print("0: Salir\n")

        opcion = input('Ingrese el número de la acción correspondiente: ')
        limpiar_pantalla()

        if opcion == '1':
            diagnostico_automatico()
        elif opcion == '2':
            trazar_ruta('8.8.8.8')
        elif opcion == '0':
            print("Saliendo del programa.")
            break  # Sale del bucle while y termina el script
        else:
            print(Fore.RED + 'La opción no es válida. Intente de nuevo.')

        if opcion != '0':
            print("\n" + "="*40)
            input(Fore.YELLOW + 'Presione Enter para volver al menú...')
            limpiar_pantalla()

if __name__ == "__main__":
    if cargar_hosts():
        menu()
