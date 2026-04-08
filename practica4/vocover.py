import numpy as np
from scipy.signal import butter, lfilter
from scipy.io import wavfile

# --- PARÁMETROS SEGÚN EL ENUNCIADO ---
RATE = 16000         # Frecuencia de muestreo exigida: 16KHz
VENTANA = 1024       # Tamaño de ventana exigido
frec_portadora = 440 # Frecuencia fundamental exigida

# 1. Función para crear la señal portadora (Ecuación: sin(2*pi*f*t))
def portadora(freq, length, rate):
    t = np.arange(length) / rate
    return np.sin(2 * np.pi * freq * t)

# 2. Función para crear filtros pasa-banda (Butterworth)
def filtroPasaBanda(data, lowcut, highcut, rate, order=5):
    nyquist = 0.5 * rate
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, data)

# 3. Función Vocoder (Ecuaciones de modulación)
def vocoder(voz, senal_portadora):
    # Separación en 3 bandas según requisitos de la práctica
    bandaGraves = filtroPasaBanda(voz, 300, 600, RATE)
    bandaMedios = filtroPasaBanda(voz, 600, 2000, RATE)
    bandaAltos  = filtroPasaBanda(voz, 2000, 4000, RATE)
    
    # Modulación AM usando envolvente (np.abs) 
    # Esto permite que la portadora siga la amplitud de la voz
    gravesModulados = np.abs(bandaGraves) * senal_portadora
    mediosModulados = np.abs(bandaMedios) * senal_portadora
    altosModulados  = np.abs(bandaAltos) * senal_portadora
    
    # Recombinación final (Suma de bandas)
    return gravesModulados + mediosModulados + altosModulados

# --- PROCESAMIENTO ---
try:
    # Se lee el archivo de audio
    fs, data = wavfile.read('entrada.wav')
    
    # Pre-procesado: Mono y Normalización
    if len(data.shape) > 1: data = data[:,0]
    voz_norm = data.astype(np.float32) / np.max(np.abs(data))

    # Generamos la portadora total
    t_total = np.arange(len(voz_norm)) / RATE
    portadora_total = np.sin(2 * np.pi * frec_portadora * t_total)
    
    # Aplicamos el algoritmo
    print("Aplicando filtros y modulación...")
    resultado = vocoder(voz_norm, portadora_total)
    
    # Normalización final y guardado
    resultado_final = (resultado / np.max(np.abs(resultado)) * 32767).astype(np.int16)
    wavfile.write('resultado_vocoder.wav', RATE, resultado_final)
    
    print("Proceso finalizado. Archivo generado: resultado_vocoder.wav")

except FileNotFoundError:
    print("Error: No se encuentra el archivo 'entrada.wav' en la carpeta.")
except Exception as e:
    print(f"Ha ocurrido un error: {e}")