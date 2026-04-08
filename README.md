# Documentación de Práctica: Vocoder en Python

## 1. Descripción del Proyecto
Este proyecto implementa un sistema Vocoder de 3 bandas diseñado para procesar una señal moduladora (voz) y aplicarla sobre una señal portadora sinusoidal. El objetivo es conseguir el efecto de "voz robótica" mediante la manipulación de la amplitud de diferentes bandas de frecuencia.

## 2. Requisitos Técnicos Implementados
- Frecuencia de muestreo: 16,000 Hz.
- Procesamiento: Análisis por ventanas de 1024 muestras.
- Banco de filtros: 3 filtros pasa-banda Butterworth  
  - Graves: 300-600 Hz  
  - Medios: 600-2 KHz  
  - Altos: 2-4 KHz
- Modulación: Extracción de envolvente mediante rectificación de señal (np.abs) para evitar cancelaciones de fase.

## 3. Pruebas y Resultados Experimentales
Durante el desarrollo, se han realizado diferentes pruebas cambiando parámetros de la portadora para analizar la inteligibilidad y calidad del sonido.

### Prueba 1: Portadora Estándar (440 Hz Sinusoidal)
**Configuración:** Onda senoidal pura a 440 Hz (Nota La).  
**Resultado:** Se obtiene un sonido de silbido electrónico. Las vocales son reconocibles, pero las consonantes fricativas (como la "S" o la "J") se pierden debido a la pureza de la onda, que no contiene armónicos para rellenar las bandas agudas.  
**Observación:** La vocal "U" suena más débil debido a que su energía principal cae por debajo del punto de corte del primer filtro (300 Hz).

### Prueba 2: Portadora Grave (110 Hz Sinusoidal)
**Configuración:** Cambio de frecuencia a 110 Hz.  
**Resultado:** La voz se percibe más "masculina" y robusta. Se entiende mejor el contenido hablado porque la frecuencia fundamental está más cerca del rango natural de la voz humana.

### Prueba 3: Portadora Musical (110 Hz Diente de Sierra)
**Configuración:** Cambio del tipo de onda a sawtooth.  
**Resultado:** Es el resultado con mayor claridad. Al ser una onda rica en armónicos, todos los filtros (agudos, medios y graves) reciben señal constante. Las palabras se entienden un poco mejor.

## Nota técnica
Debido a limitaciones de hardware en entorno Windows y ausencia de micrófono, la entrada de datos se realiza mediante lectura de archivos .wav pre-grabados, garantizando la estabilidad del algoritmo y la repetibilidad de las pruebas.
