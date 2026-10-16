from pathlib import Path
from src.fuentes import FuenteCSV, FuenteJSON
from src.pipeline import PipelinePresion


def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent
    ruta_csv = base_dir / "data" / "mediciones.csv"
    ruta_json = base_dir / "data" / "mediciones.json"

    fuentes = [
        FuenteCSV(ruta_csv),
        FuenteJSON(ruta_json),
    ]

    pipeline = PipelinePresion(fuentes)
    mediciones = pipeline.ejecutar()
    stats = pipeline.obtener_estadisticas()

    print("=" * 55)
    print("  REPORTE DEL PIPELINE DE MEDICIONES DE PRESIÓN")
    print("=" * 55)
    print(f"Mediciones válidas procesadas : {stats['total_validas']}")
    print(f"Registros inválidos/descartados: {stats['total_descartadas']}")
    print(f"Presión promedio (hPa)        : {stats['presion_promedio_hpa']} hPa")
    print(f"Presión mínima (hPa)          : {stats['presion_min_hpa']} hPa")
    print(f"Presión máxima (hPa)          : {stats['presion_max_hpa']} hPa")
    print("-" * 55)
    print("Detalle por Sensor:")
    for sensor, info in stats["por_sensor"].items():
        print(
            f"  • {sensor}: {info['cantidad']} lecturas | "
            f"Prom: {info['promedio_hpa']} hPa "
            f"(Mín: {info['min_hpa']} / Máx: {info['max_hpa']})"
        )
    print("=" * 55)


if __name__ == "__main__":
    main()
