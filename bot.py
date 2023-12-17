import radio
from microbit import *
import gigglebot

def main():
    radio.on()

    turnA = {"RIGHT" : 1, "LEFT" : 0}
    turnK = turnA.keys()

    driveA = {"FORWARD" : 1, "BACKWARD" : -1}
    driveK = driveA.keys()

    ind = 0
    check = True
    received = None
    while received == None:
        sleep(1000)
        # Intenta recoger un mensaje que haya llegado al microbit
        # Si no ha llegado ningún mensaje receive_full() devuelve None
        # Si ha llegado un mensaje, receive_full() devuelve una tupla de 3 valores:
        #   - una lista de bytes con el mensaje recibido
        #   - la potencia de señal recibida, en dBm, entre 0 (potencia máxima) y -255 (potencia mínima)
        #   - una marca de tiempo con el instante en que se recibió el mensaje
        received = radio.receive_full()
        if received != None:
            # Separamos los 3 valores de la tupla. La marca de tiempo no la usaremos
            msg = received[0]
            dBm = received[1]
            ts = received[2]

            # En msg los primeros 3 bytes de la lista son una cabecera que descartamos
            # Convertimos el resto de bytes a un string con codificación UTF8
            identifier = str(msg[3:], 'utf8')
            identifier = identifier.split(",")
            print(identifier)
            display.show(str(dBm))
            length = len(identifier) - 1


    while check:

        print(ind)
        if button_a.get_presses():
            if identifier[ind] == "STOP":
                gigglebot.stop()
                check = False

            elif identifier[ind] not in driveK:
                gigglebot.turn(turnA[identifier[ind]],500)
            else:
                gigglebot.drive(driveA[identifier[ind]],1000)

            if ind == length:
                ind = 0
            else:
                ind+=1

        elif button_b.get_presses():

            if ind == 0:
                ind = length
            else:
                ind-=1

            reverse = 0
            if identifier[ind] == "STOP":
                gigglebot.stop()
                check = False
            elif identifier[ind] not in driveK:
                for x in turnK:
                    if identifier[ind] != x:
                        reverse = x
                gigglebot.turn(turnA[reverse],500)
            else:

                for x in driveK:
                    if identifier[ind] != x:
                        reverse = x
                gigglebot.drive(driveA[reverse],1000)

if __name__ == "__main__":
    main()

