import radio
from microbit import *

def main():
    # String con un identificador del emisor, cámbialo para no coincidir con el
    # de otros microbits que puedan estar transmitiendo cerca de ti
    COMMAND= "FORWARD,RIGHT,FORWARD,STOP"

    # Periodo de emisión del mensaje, en milisegundos
    PERIOD = 10000

    # Enciende la radio
    radio.on()

    # Establece la potencia de la emisión, de 0 a 7 siendo 7 la potencia máxima
    # Mira la documentación para ver otros parámetros que pueden fijarse en radio.config()
    radio.config(power=7)

    check = True
    while check:
        # Muestra dos recuadros en pantalla para indicar que va a enviar un mensaje
        if button_a.was_pressed() or button_b.was_pressed():
            display.show(Image.SQUARE_SMALL)
            sleep(500)
            # Envía el mensaje
            radio.send(COMMAND)
            print("Sent")
            display.show(Image.SQUARE)
            sleep(500)
            display.clear()
            sleep(PERIOD-1000)  # ya se han esperado 1000ms al mostrar las imágenes

if __name__ == "__main__":
    main()
