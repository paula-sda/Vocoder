# Documentación de Práctica: Vocoder en Python

## 1. Implementación y Resolución Técnica
Debido a problemas de compatibilidad de la librería **PyAudio** con las versiones más recientes de Python en Windows, esta práctica se ha realizado de dos formas:

- **Versión Offline (`vocoder.py`):** Ante los errores iniciales de instalación de drivers, se desarrolló un script que procesa archivos `.wav` pre-grabados para asegurar el funcionamiento del algoritmo.
- **Versión Real-Time (`vocoder_pyaudio.py`):** Tras realizar un downgrade a **Python 3.12** y configurar los alias del sistema, se logró la integración con el micrófono para procesar audio en vivo.

## 2. Requisitos Técnicos
El sistema implementa un Vocoder de 3 bandas con los siguientes parámetros:

- **Muestreo:** 16,000 Hz / Ventanas de 1024 muestras.
- **Banco de filtros (Butterworth):**
  - Graves: 300 - 600 Hz
  - Medios: 600 - 2,000 Hz
  - Altos: 2,000 - 4,000 Hz
- **Modulación:** Extracción de envolvente mediante `np.abs` para aplicar la amplitud de la voz a la portadora.

## 3. Pruebas Experimentales
Se han analizado diferentes portadoras para evaluar la claridad del sonido:

1. **Portadora 440 Hz (Sinusoidal):** Sonido agudo tipo silbido. Vocales reconocibles, pero consonantes poco claras.
2. **Portadora 110 Hz (Sinusoidal):** Voz más grave que se entiende un poco mejor.
3. **Portadora 110 Hz (Diente de Sierra):** Mejor resultado. Al tener más armónicos, la voz robótica se entiende mejor en todos los rangos.

## 4. Notas de uso
- Para la versión en tiempo real, se recomienda el uso de **auriculares** para evitar el acople entre los altavoces y el micrófono del portátil.
- Es imprescindible usar **Python 3.12** para que las librerías de audio funcionen correctamente en este entorno.
- Instalar dependencias: pip install pyaudio numpy scipy.
- Para archivo vocover.py: Asegurarse de tener un archivo entrada.wav en el directorio.
