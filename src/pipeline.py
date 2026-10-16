from typing import Any, Dict, List, Sequence
from src.fuentes import FuenteDatos
from src.modelo import MedicionPresion


class PipelinePresion:
    """Coordina la extracción, validación y cálculo de estadísticas de presión."""

    def __init__(self, fuentes: Sequence[FuenteDatos]) -> None:
        self.fuentes = list(fuentes)
        self.mediciones_validas: List[MedicionPresion] = []
        self.registros_descartados: int = 0

    def ejecutar(self) -> List[MedicionPresion]:
        """Ejecuta la carga desde todas las fuentes y filtra las mediciones válidas."""
        self.mediciones_validas.clear()
        self.registros_descartados = 0

        for fuente in self.fuentes:
            registros_crudos = fuente.cargar()
            for reg in registros_crudos:
                try:
                    medicion = MedicionPresion.desde_diccionario(reg)
                    if medicion.es_valida():
                        self.mediciones_validas.append(medicion)
                    else:
                        self.registros_descartados += 1
                except ValueError:
                    self.registros_descartados += 1

        return self.mediciones_validas

    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Calcula métricas agregadas globales y agrupadas por sensor."""
        if not self.mediciones_validas:
            return {
                "total_validas": 0,
                "total_descartadas": self.registros_descartados,
                "presion_promedio_hpa": 0.0,
                "presion_min_hpa": 0.0,
                "presion_max_hpa": 0.0,
                "por_sensor": {},
            }

        presiones = [m.presion_hpa for m in self.mediciones_validas]
        por_sensor: Dict[str, List[float]] = {}

        for m in self.mediciones_validas:
            por_sensor.setdefault(m.sensor_id, []).append(m.presion_hpa)

        resumen_sensores = {
            sensor: {
                "cantidad": len(vals),
                "promedio_hpa": round(sum(vals) / len(vals), 2),
                "min_hpa": round(min(vals), 2),
                "max_hpa": round(max(vals), 2),
            }
            for sensor, vals in sorted(por_sensor.items())
        }

        return {
            "total_validas": len(self.mediciones_validas),
            "total_descartadas": self.registros_descartados,
            "presion_promedio_hpa": round(sum(presiones) / len(presiones), 2),
            "presion_min_hpa": round(min(presiones), 2),
            "presion_max_hpa": round(max(presiones), 2),
            "por_sensor": resumen_sensores,
        }
