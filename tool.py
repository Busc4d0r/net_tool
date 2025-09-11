import subprocess
import platform
import os
import speedtest
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
        for linea in proceso.stdout:
            print(linea, end='')
        proceso.wait()
    except Exception as e:
        print(Fore.RED + f'Ocurrió un error: {e}')

# Función para realizar un ping a una IP
def realizar_ping(ip, nombre='host'):
        # """Realiza un ping a una IP y devuelve True si hay éxito, False si no."""
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

# Función para realizar una prueba de velocidad
def realizar_speedtest():
    # """Realiza una prueba de velocidad usando la biblioteca speedtest-cli."""
    try:
        print('Iniciando prueba de velocidad (esto puede tardar un momento)...')
        st = speedtest.Speedtest()
        print('Buscando el mejor servidor...')
        st.get_best_server()
        print('Realizando prueba de descarga...')
        velocidad_descarga = st.download() / 1_000_000  # Convertir a Mbps
        print('Realizando prueba de subida...')
        velocidad_subida = st.upload() / 1_000_000  # Convertir a Mbps
        
        print("\n---Resultados de la Prueba de Velocidad---")
        print(f"    Descarga: {Fore.CYAN}{velocidad_descarga:.2f} Mbps")
        print(f"    Subida:   {Fore.CYAN}{velocidad_subida:.2f} Mbps")
        print(f"    Ping:     {Fore.CYAN}{st.results.ping} ms")
        print("------------------------------------------\n")

    except Exception as e:
        print(Fore.RED + f'Ocurrió un error durante la prueba de velocidad: {e}')

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
        '3': realizar_speedtest,
        '0': exit
    }
    
    while True:
        print(f'1: Diagnóstico automático')
        print(f'2: Trazar ruta hacia Internet')
        print(f'3: Prueba de velocidad')
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
        except ValueError:
            print(Fore.RED + f'Por favor, ingrese un número válido.')

# Punto de entrada del programa
if __name__ == "__main__":
    menu()