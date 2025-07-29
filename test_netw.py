import subprocess
import platform
import os

#guardo las direcciones que necesito consultar
ip_host1 = '192.168.1.1' #IP de DMP
ip_host2 = '192.168.199.1' #IP del hEX
ip_dns = '94.140.14.14' #IP del DNS

#con este codigo obtengo el nombre del DNS a partir de su direccion IP
if ip_dns == '1.1.1.1' : nombre_dns = 'CloudFlare'
elif ip_dns == '8.8.8.8' : nombre_dns = 'Google'
elif ip_dns == '94.140.14.14' : nombre_dns = 'AdGuard'

#la siguiente funcion me permite limpiar la pantalla de la terminal
def limpiar_pantalla():
    if platform.system().lower() == 'windows':
        os.system('cls')
    else:
        os.system('clear')

#la siguiente funcion me permite hacer ping a la direccion IP del host 1
def ping_host_1():
    try:
        if platform.system().lower() == 'windows':
            comando = ['ping','-n','4',ip_host1]
        else:
            comando = ['ping','-c','4',ip_host1]

        resultado = subprocess.run(
            comando,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if resultado.returncode == 0:
            print(f'    Ping exitoso, hay conexión con el host\n')
            #print(resultado.stdout)
        else:
            print(f'    No se pudo hacer ping al host\n')
            #print(resultado.stderr)

    except Exception as e:
        print(f'Ocurrió un error: {e}')

#la siguiente funcion me permite hacer ping a la direccion IP del host 2
def ping_host_2():
    try:
        if platform.system().lower() == 'windows':
            comando = ['ping','-n','4',ip_host2]
        else:
            comando = ['ping','-c','4',ip_host2]

        resultado = subprocess.run(
            comando,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if resultado.returncode == 0:
            print(f'    Ping exitoso, hay conexión con el host\n')
            #print(resultado.stdout)
        else:
            print(f'    No se pudo hacer ping al host\n')
            #print(resultado.stderr)
    except Exception as e:
        print(f'Ocurrió un error: {e}')

#la siguiente funcion me permite hacer ping a la direccion IP del DNS
def ping_dns():
    try:
        if platform.system().lower() == "windows":
            comando = ['ping','-n','4',ip_dns]
        else:
            comando = ['ping','-c','4',ip_dns]

        resultado = subprocess.run(
            comando,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if resultado.returncode == 0:
            print(f'    Ping exitoso, hay conexión con {nombre_dns}\n')
            #print(resultado.stdout)
        else:
            print(f'    No se pudo hacer ping a {nombre_dns}\n')
            #print(resultado.stderr)
    except Exception as e:
        print(f'Ocurrió un error: {e}')

#la siguiente funcion me permite trazar la ruta hacia la direccion IP del DNS
def tracert_dns():
    try:
        comando = ['tracert', ip_dns] if subprocess.os.name == 'nt' else ['traceroute', ip_dns]
        result = subprocess.run(comando, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f'    Error al ejecutar el comando: {result.stderr}')
    except Exception as e:
        print(f'Ocurrió un error: {e}')

#la siguiente funcion me permite ejecutar un diagnostico automatico
def diag_auto():
    print(f'Verificando conexión con el host {ip_host1}')
    ping_host_1()
    print(f'Verificando conexión con el host {ip_host2}')
    ping_host_2()
    print(f'Verificando conexión con {nombre_dns}')
    ping_dns()

#la siguiente funcion me permite mostrar un menu con las opciones disponibles
def menu():
    while True:
        print(f'1: Verificar conexión a internet')
        print(f'2: Trazar ruta hacia {nombre_dns}')
        print(f'3: Diagnóstico automático')
        print(f'4: Verificar conexion con el host {ip_host1}')
        print(f'5: Verificar conexión con el host {ip_host2}')
        print(f'0: Salir\n')
        opcion = int(input(f'Ingrese el número de la acción correspondiente: '))
        limpiar_pantalla()


        if opcion == 1:
            print(f'Verificando conexión a internet...\n')
            ping_dns()
            input('Presione Enter para volver al menú ')
            limpiar_pantalla()

        elif opcion == 2:
            print(f'Trazando ruta hacia {nombre_dns}\n')
            tracert_dns()
            input('Presione Enter para volver al menú ')
            limpiar_pantalla()

        elif opcion == 3:
            print(f'Ejecutando diagnóstico automático...\n')
            diag_auto()
            input('Presione Enter para volver al menú ')
            limpiar_pantalla()

        elif  opcion == 4:
            print(f'Verificando conexión con el host {ip_host1}\n')
            ping_host_1()
            input('Presione Enter para volver al menú ')
            limpiar_pantalla()

        elif opcion == 5:
            print(f'Verificando conexión con el host {ip_host2}\n')
            ping_host_2()
            input('Presione Enter para volver al menú ')
            limpiar_pantalla()

        elif opcion == 0:
            break

        else:
            print(f'La opción no es válida')

#inicio el programa
menu()