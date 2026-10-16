# Diccionario de Datos (`data/`)

Esta carpeta contiene los lotes de mediciones de presión capturados por los sensores en distintos formatos.

## Esquema de Datos

Cada registro representa una lectura de presión y contiene los siguientes campos:

| Campo | Tipo | Descripción | Criterio de Validez |
|---|---|---|---|
| `id_medicion` | `int` | Identificador único de la lectura | Entero positivo |
| `sensor_id` | `str` | Código identificador del sensor (ej. `SENS-01`) | Cadena no vacía |
| `timestamp` | `str` | Fecha y hora en formato ISO 8601 (`YYYY-MM-DDTHH:MM:SS`) | Formato válido |
| `presion_hpa` | `float` | Presión registrada en hectopascales (hPa) | Entre `300.0` y `1500.0` hPa |
| `temperatura_c` | `float` | Temperatura del sensor en grados Celsius (°C) | Entre `-50.0` y `85.0` °C |

## Archivos incluidos
* `mediciones.csv`: Lote de lecturas exportadas en formato tabular separado por comas. Incluye registros válidos y casos de borde/inválidos para probar el filtrado del pipeline.
* `mediciones.json`: Lote de lecturas exportadas en formato JSON (lista de objetos).
