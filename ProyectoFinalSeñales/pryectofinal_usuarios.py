from tkinter import *
import numpy as np
import pyaudio
import wave

#Fomrato de audio de microfono
PROFUNDIAD_BITS = pyaudio.paInt16
CANALES = 1
FRECUENCIA_MUESTREO = 44100

SEGUNDOS_GRABACION= 20

#Tamaño de CHUNK
CHUNK = 2048

window= np.blackman(CHUNK)

def analizar(stream):
    data = stream.read(CHUNK, exception_on_overflow=False)
    #"2048h"
    waveData = wave.struct.unpack("%dh"%(CHUNK),data )
    npData = np.array(waveData)

    dataEntrada = npData * window

    fftData = np.abs(np.fft.rfft(dataEntrada))

    indiceFrecuenciaDominante = fftData[1:].argmax() + 1

    #Cambio de indice a Hz
    y0, y1, y2 = np.log(fftData[indiceFrecuenciaDominante-1: indiceFrecuenciaDominante+2])
    x1 = (y2 - y0) * 0.5 / (2 * y1 - y2 -y0)
    frecuenciaDominante = (indiceFrecuenciaDominante+x1)*FRECUENCIA_MUESTREO/CHUNK

    print("Frecuencia dominante: " + str(frecuenciaDominante) + "Hz", end='\r')



if __name__ == "__main__":
    p = pyaudio.PyAudio()
    stream = p.open(format=PROFUNDIAD_BITS, channels=CANALES,
        rate=FRECUENCIA_MUESTREO, input=True, frames_per_buffer=CHUNK)


    for i in range(0, int(FRECUENCIA_MUESTREO*SEGUNDOS_GRABACION / CHUNK)):
        analizar(stream)

    stream.start_stream()
    stream.close()
    p.terminate()

ventana = Tk()
ventana.title("Proyecto Final")
ventana.geometry("800x600")


strFrecactual = StringVar()
strFrecactual.set("Frecuencia actual:")

strApretar = StringVar()
strApretar.set("Es necesario apretar la cuerda")

strAflojar = StringVar()
strAflojar.set("Es necesario aflojar la cuerda")

strPrimera = StringVar()
strPrimera.set("1era (Mi)- 329.63hz")

strSegunda = StringVar()
strSegunda.set("2da (Si)-246.94 hz")

strTercera = StringVar()
strTercera.set("3era (Sol)-196 hz")

strCuarta = StringVar()
strCuarta.set("4ta (Re)-146.83 hz")

strQuinta = StringVar()
strQuinta.set("5ta (La)-110 hz")

strSexta = StringVar()
strSexta.set("6ta (Mi)-82.40 hz")





def iniciar():

    lblfrecuencia = Label(ventana, textvariable = strFrecactual)
    lblfrecuencia.pack()

    lblApretar = Label(ventana, textvariable = strApretar)
    lblApretar.pack()

    lblAflojar = Label(ventana, textvariable = strAflojar)
    lblAflojar.pack()

    lblPrimera = Label(ventana, textvariable = strPrimera)
    lblPrimera.pack()

    lblSegunda = Label(ventana, textvariable = strSegunda)
    lblSegunda.pack()

    lblTercera = Label(ventana, textvariable = strTercera)
    lblTercera.pack()

    lblCuarta = Label(ventana, textvariable = strCuarta)
    lblCuarta.pack()

    lblQuinta = Label(ventana, textvariable = strQuinta)
    lblQuinta.pack()

    lblSexta = Label(ventana, textvariable = strSexta)
    lblSexta.pack()

    


    

etiqueta = Label(ventana, text="Afinador de cuerdas")
etiqueta.pack()

boton = Button(ventana, text="Iniciar", command=iniciar)
boton.pack()




ventana.mainloop()