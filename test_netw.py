import subprocess
import platform
import os

ip_dns='8.8.8.8' #IP del DNS
ip_host1='192.168.1.1' #IP de DMP
ip_host2='192.168.100.1' #IP de ISP1
ip_host3='192.168.101.1' #IP de ISP2

def limpiar_pantalla():
    if platform.system().lower() == 'windows':
        os.system('cls')
    else:
        os.system('clear')

def realizar_ping(ip, nombre='host'):
    try:
        if platform.system().lower() == 'windows':
            comando = ['ping', '-n', '2', ip]
        else:
            comando = ['ping', '-c', '2', ip]

        resultado = subprocess.run(
            comando,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if resultado.returncode == 0:
            print(f'    Hay conexión con {nombre}\n')
            #print(resultado.stdout)
        else:
            print(f'    No hay conexión {nombre}\n')
            #print(resultado.stderr)

    except Exception as e:
        print(f'Ocurrió un error: {e}')

def ejecutar_comando(comando):
    print(f'Ejecutando prueba, por favor espere...')
    try:
        result = subprocess.run(comando, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f'    Error al ejecutar el comando: {result.stderr}')
    except Exception as e:
        print(f'Ocurrió un error: {e}')

def ping_dns():
    realizar_ping(ip_dns,'la Internet')

def ping_host_1():
    realizar_ping(ip_host1, 'el Router')

def pign_host_2():
    realizar_ping(ip_host2,'el ISP 1')

def ping_host_3():
    realizar_ping(ip_host3,'el ISP 2')

def tracert_dns():
    comando=['tracert',ip_dns] if platform.system().lower() == 'windows' else ['traceroute', ip_dns]
    ejecutar_comando(comando)

def speedtest():
    comando = ['speedtest.exe']
    ejecutar_comando(comando)

def diagnostico_automatico():
    hosts = [
        (ip_host1,'el Router'),
        (ip_host2,'el ISP 1'),
        (ip_host3,'el ISP 2'),
        (ip_dns,'la Internet')
    ]
    for ip, nombre in hosts:
        print(f'Verificando conexión con {nombre}')
        realizar_ping(ip, nombre)

def menu():
    opciones={
        1:lambda:diagnostico_automatico(),
        2:lambda:ping_dns(),
        3:lambda:tracert_dns(),
        4:lambda:speedtest(),
        0:lambda:exit()
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