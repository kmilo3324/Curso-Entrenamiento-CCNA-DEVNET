

def solicitar_datos():
    nombre = input("Introduce tu nombre: ")
    apellido = input("Introduce tu apellido: ")
    edad = input("Introduce tu edad: ")
    sede = input("Introduce tu sede: ")

    print("\nDatos introducidos:")
    print(f"Nombre: {nombre}")
    print(f"Apellido: {apellido}")
    print(f"Edad: {edad}")
    print(f"Sede: {sede}")

if __name__ == "__main__":
    solicitar_datos()
