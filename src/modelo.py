from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass
class MedicionPresion:
    """Representa una lectura individual de presión y temperatura de un sensor."""
    id_medicion: int
    sensor_id: str
    timestamp: str
    presion_hpa: float
    temperatura_c: float

    MIN_PRESION_HPA: float = 300.0
    MAX_PRESION_HPA: float = 1500.0
    MIN_TEMP_C: float = -50.0
    MAX_TEMP_C: float = 85.0

    def es_valida(self) -> bool:
        """Valida que los campos tengan valores físicamente coherentes y formato correcto."""
        if not isinstance(self.id_medicion, int) or self.id_medicion <= 0:
            return False
        if not isinstance(self.sensor_id, str) or not self.sensor_id.strip():
            return False
        if not (self.MIN_PRESION_HPA <= self.presion_hpa <= self.MAX_PRESION_HPA):
            return False
        if not (self.MIN_TEMP_C <= self.temperatura_c <= self.MAX_TEMP_C):
            return False
        try:
            datetime.fromisoformat(self.timestamp)
        except (ValueError, TypeError):
            return False
        return True

    @property
    def presion_psi(self) -> float:
        """Convierte la presión de hectopascales (hPa) a libras por pulgada cuadrada (PSI)."""
        return round(self.presion_hpa * 0.01450377, 4)

    @property
    def presion_atm(self) -> float:
        """Convierte la presión de hectopascales (hPa) a atmósferas estándar (atm)."""
        return round(self.presion_hpa / 1013.25, 4)

    @classmethod
    def desde_diccionario(cls, data: Dict[str, Any]) -> "MedicionPresion":
        """Instancia una MedicionPresion convirtiendo los tipos crudos desde un diccionario."""
        try:
            return cls(
                id_medicion=int(data["id_medicion"]),
                sensor_id=str(data["sensor_id"]).strip(),
                timestamp=str(data["timestamp"]).strip(),
                presion_hpa=float(data["presion_hpa"]),
                temperatura_c=float(data["temperatura_c"]),
            )
        except (KeyError, ValueError, TypeError) as exc:
            raise ValueError(f"Error al parsear el registro {data}: {exc}") from exc
