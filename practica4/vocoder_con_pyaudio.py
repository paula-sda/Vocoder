# BIBLIOTECAS:
import numpy as np
import pyaudio
import time
from scipy.signal import butter, lfilter

# Parámetros del audio (Completados según enunciado)
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000     # Frecuencia de muestreo exigida
VENTANA = 1024   # Tamaño de bloque exigido

# Función para crear la señal portadora
def portadora(freq=440, length=VENTANA, rate=RATE):
    t = np.arange(length) / rate  
    # Ecuación de la portadora sinusoidal
    senalPortadora = np.sin(2 * np.pi * freq * t)
    return senalPortadora

# Función para crear filtro pasa-banda:
def filtroPasaBanda(data, lowcut, highcut, rate, order=5):
    nyquist = 0.5 * rate
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, data)

# Función para aplicar el vocoder en modulación AM:
def vocoder(voz, senal_portadora):
    # 1. Separa la señal de la voz en tres bandas (según los rangos de la práctica)
    bandaGraves = filtroPasaBanda(voz, 300, 600, RATE)
    bandaMedios = filtroPasaBanda(voz, 600, 2000, RATE)
    bandaAltos  = filtroPasaBanda(voz, 2000, 4000, RATE)
   
    # 2. Modula cada banda por la portadora (AM)
    # IMPORTANTE: Usamos np.abs para extraer la envolvente y que se entienda la voz
    gravesModulados = np.abs(bandaGraves) * senal_portadora
    mediosModulados = np.abs(bandaMedios) * senal_portadora
    altosModulados  = np.abs(bandaAltos) * senal_portadora
   
    # 3. Recombinar las bandas en una única señal, sumándolas:
    SenalRecombinada = gravesModulados + mediosModulados + altosModulados

    return SenalRecombinada
   
# Inicialitzar PyAudio
p = pyaudio.PyAudio()

# Función de callback para el procesamiento en tiempo real:
def callback(in_data, frame_count, time_info, status):
    # Normalizar la voz (convertir de int16 a float entre -1 y 1)
    voz = np.frombuffer(in_data, dtype=np.int16) / 32768.0  
   
    # Aplicar el proceso del vocoder
    senalModulada = vocoder(voz, portadora(frec_portadora))  
   
    # Limitar para evitar distorsión y volver a formato int16
    senalModulada = np.clip(senalModulada, -1.0, 1.0)
    senalModulada = (senalModulada * 32767).astype(np.int16)  
   
    return (senalModulada.tobytes(), pyaudio.paContinue)

# Crea la señal portadora inicial (440Hz según el enunciado)
frec_portadora = 440

# Abrir el flujo de audio (Stream)
flujoVoz = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=VENTANA,
                stream_callback=callback)

# Iniciar el flujo de audio
flujoVoz.start_stream()
print(f"Vocoder activo a {frec_portadora}Hz.")
print("Puedes empezar a hablar para escuchar el efecto de vocoder en tiempo real.")
print("Presiona Ctrl+C para detener.")

# El bucle principal mantiene el programa vivo mientras el callback procesa el audio
try:
    while flujoVoz.is_active():
        time.sleep(0.1)  # Pausa para evitar el uso alto de CPU
except KeyboardInterrupt:
    print("\nDeteniendo el vocoder...")

# Cerrar PyAudio al salir
flujoVoz.stop_stream()
flujoVoz.close()
p.terminate()