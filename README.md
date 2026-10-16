# TP Pipeline de Presión - Grupo Cappa Burgos Cattaneo Bazan

Pipeline de procesamiento, validación y análisis de mediciones de presión a partir de múltiples fuentes de datos (CSV y JSON).

## Estructura del Proyecto

```text
tp-pipeline-presion-Cappa_Burgos_Cattaneo_Bazan
├── README.md
├── .gitignore
├── data/
│   ├── README.md
│   ├── mediciones.csv
│   └── mediciones.json
├── src/
│   ├── fuentes.py
│   ├── modelo.py
│   ├── pipeline.py
│   └── main.py
└── tests/
    └── test_pipeline.py
```

## Requisitos e Instalación

El proyecto utiliza únicamente la librería estándar de Python (Python 3.9+). No requiere instalar paquetes externos para su ejecución principal.

## Ejecución

Para correr el pipeline principal desde la raíz del proyecto:

```bash
python -m src.main
```

## Ejecución de Tests

Para correr las pruebas unitarias con `unittest`:

```bash
python -m unittest discover -s tests
```
