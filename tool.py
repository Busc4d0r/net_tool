import subprocess
import platform
import os

# Diccionario de hosts
hosts = {
    '192.168.1.1': 'el Router',
    '192.168.100.1': 'el ISP 1',
    '192.168.101.1': 'el ISP 2',
    '8.8.8.8': 'la Internet'
}

def limpiar_pantalla():
    os.system('cls' if platform.system().lower() == 'windows' else 'clear')

def realizar_ping(ip, nombre='host'):
    try:
        comando = ['ping', '-n', '2', ip] if platform.system().lower() == 'windows' else ['ping', '-c', '2', ip]
        resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if resultado.returncode == 0:
            print(f'    Hay conexión con {nombre}\n')
        else:
            print(f'    No hay conexión con {nombre}\n')
    except Exception as e:
        print(f'Ocurrió un error al intentar hacer ping a {nombre} ({ip}): {e}')

def ejecutar_comando(comando):
    print(f'Ejecutando prueba, por favor espere...\n')
    try:
        result = subprocess.run(comando, capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f'    Error al ejecutar el comando: {result.stderr}')
    except Exception as e:
        print(f'Ocurrió un error: {e}')

def tracert_dns():
    comando = ['tracert', hosts['8.8.8.8']] if platform.system().lower() == 'windows' else ['traceroute', hosts['8.8.8.8']]
    ejecutar_comando(comando)

def speedtest():
    comando = ['speedtest.exe']
    ejecutar_comando(comando)

def diagnostico_automatico():
    for ip, nombre in hosts.items():
        print(f'Verificando conexión con {nombre}')
        realizar_ping(ip, nombre)
    speedtest()

def menu():
    opciones = {
        1: diagnostico_automatico,
        2: lambda: realizar_ping('8.8.8.8', 'la Internet'),
        3: tracert_dns,
        4: speedtest,
        0: exit
    }

    while True:
        print(f'1: Diagnóstico automático')
        print(f'2: Verificar conexión a Internet')
        print(f'3: Trazar ruta hacia Internet')
        print(f'4: Prueba de velocidad')
        print(f'0: Salir\n')

        try:
            opcion = int(input(f'Ingrese el número de la acción correspondiente: '))
            limpiar_pantalla()
            if opcion in opciones:
                opciones[opcion]()
                input('Presione Enter para volver al menú ')
                limpiar_pantalla()
            else:
                print(f'La opción no es válida')
        except ValueError:
            print(f'Por favor, ingrese un número válido.')

menu()