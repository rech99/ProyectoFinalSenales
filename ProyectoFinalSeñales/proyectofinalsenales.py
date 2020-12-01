from tkinter import *
import numpy as np
import pyaudio
import wave

ventana = Tk()
ventana.geometry("800x600")
ventana.title("Afinador")

strAfinado= StringVar()
strNota = StringVar()
strFrecAct= StringVar()

PROFUNDIDAD_BITS = pyaudio.paInt16
CANALES = 1
FRECUENCIA_MUESTREO = 44100
SEGUNDOS_GRABACION= 6
CHUNK = 2048

window= np.blackman(CHUNK)

def afinador():

    def analisis(stream):
        data = stream.read(CHUNK, exception_on_overflow=False)
        waveData = wave.struct.unpack("%dh"%(CHUNK),data )
        npData = np.array(waveData)
        dataEntrada = npData * window
        fftData = np.abs(np.fft.rfft(dataEntrada))

        indiceFrecuenciaDominante = fftData[1:].argmax() + 1

        
        y0, y1, y2 = np.log(fftData[indiceFrecuenciaDominante-1: indiceFrecuenciaDominante+2])
        x1 = (y2 - y0) * 0.5 / (2 * y1 - y2 -y0)
        frecuenciaDominante = (indiceFrecuenciaDominante+x1)*FRECUENCIA_MUESTREO/CHUNK
        freq = str(frecuenciaDominante)
        

        strFrecAct.set(freq)

        margen= 20
        margen_afin= 2.0

        if frecuenciaDominante > 329.63 - margen and frecuenciaDominante < 329.63  + margen:
            Nota= "1ra Mi con una frecuencia de  329.63 Hz"
            if frecuenciaDominante >329.63  - margen_afin and frecuenciaDominante < 329.63  + margen_afin:
                Afinado = "Tiene la afinacion indicada"
            elif frecuenciaDominante < 329.63  + margen_afin:
                Afinado = "Aprieta la cuerda"
            else:
                Afinado = "Afloja la cuerda"

        elif frecuenciaDominante > 246.94- margen and frecuenciaDominante < 246.94 + margen:
            Nota= "2da Si con una frecuencia de 246.94 Hz"
            if frecuenciaDominante >246.94 - margen_afin and frecuenciaDominante < 246.94 + margen_afin:
                Afinado = "Tiene la afinacion indicada"
            elif frecuenciaDominante < 246.94 + margen_afin:
                Afinado = "Aprieta la cuerda"
            else:
                Afinado = "Afloja la cuerda"

        elif frecuenciaDominante > 196.0 - margen and frecuenciaDominante < 196.0 + margen:
            Nota= "3ra Sol con una frecuencia de 196.0 Hz"
            if frecuenciaDominante >196.0 - margen_afin and frecuenciaDominante < 196.0 + margen_afin:
                Afinado = "Tiene la afinacion indicada"
            elif frecuenciaDominante < 196.0 + margen_afin:
                Afinado = "Aprieta la cuerda"
            else:
                Afinado = "Afloja la cuerda"

        elif frecuenciaDominante > 146.83 - margen and frecuenciaDominante < 146.83 + margen:
            Nota= "4ta Re con una frecuencia de 146.83 Hz"
            if frecuenciaDominante >146.83 - margen_afin and frecuenciaDominante < 146.83 + margen_afin:
                Afinado = "Tiene la afinacion indicada"
            elif frecuenciaDominante < 146.83 + margen_afin:
                Afinado = "Aprieta la cuerda "
            else:
                Afinado = "Afloja la cuerda"
        
        elif frecuenciaDominante > 110.0 - margen and frecuenciaDominante < 110.0 + margen:
            Nota= "5ta La con una frecuencia de 110.0 Hz"
            if frecuenciaDominante >110.0 - margen_afin and frecuenciaDominante < 110.0 + margen_afin:
                Afinado = "Tiene la afinacion indicada"
            elif frecuenciaDominante < 110.0 + margen_afin:
                Afinado = "Aprieta la cuerda"
            else:
                Afinado = "Afloja la cuerda"

        elif frecuenciaDominante > 82.4 - margen and frecuenciaDominante < 82.4 + margen:
            Nota= "6ta Mi con una frecuencia de 82.4 Hz"
            if frecuenciaDominante >82.4 - margen_afin and frecuenciaDominante < 82.4 + margen_afin:
                Afinado = "Tiene la afinacion indicada"
            elif frecuenciaDominante < 82.4 + margen_afin:
                Afinado = "Aprieta la cuerda"
            else:
                Afinado = "Afloja la cuerda"

        else:
            Nota = "Intentelo de nuevo"
            Afinado = "No se reconoce la cuerda"

        strNota.set(Nota)
        strAfinado.set(Afinado)


    

    if __name__=="__main__":
   
        p = pyaudio.PyAudio()
        stream = p.open(format=PROFUNDIDAD_BITS, channels=CANALES, rate=FRECUENCIA_MUESTREO, input=True, frames_per_buffer=CHUNK)
        
        for i in range(0, int(FRECUENCIA_MUESTREO * SEGUNDOS_GRABACION / CHUNK)):
            analisis(stream)


        
        stream.stop_stream()
        stream.close()
        p.terminate()    

        

    

etiqueta1 = Label(ventana, text="Afinador de cuerdas")
etiqueta1.pack()

etiqueta2 = Label(ventana, textvariable=strNota)
etiqueta2.pack()

etiqueta3 = Label(ventana, textvariable=strFrecAct)
etiqueta3.pack()

etiqueta4 = Label(ventana,textvariable=strAfinado)
etiqueta4.pack()

boton = Button(ventana, text="Iniciar", command=afinador)
boton.pack()




ventana.mainloop()