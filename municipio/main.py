import depa
def run():
    print("============================")
    print(" Iniciando proceso de recuperación\n de datos")
    print("============================")
    print("Procesando ..")
    depa.get_departamentos()
    print("============================")
    print(" Fin del proceso")
    print("============================")

if __name__ == '__main__':
    run()