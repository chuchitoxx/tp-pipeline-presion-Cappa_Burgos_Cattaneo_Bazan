import csv
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List


class FuenteDatos(ABC):
    """Clase base abstracta para las fuentes de datos de mediciones."""

    def __init__(self, ruta_archivo: str | Path) -> None:
        self.ruta_archivo = Path(ruta_archivo)

    @abstractmethod
    def cargar(self) -> List[Dict[str, Any]]:
        """Lee la fuente de datos y devuelve una lista de diccionarios crudos."""
        pass

    def _verificar_existencia(self) -> None:
        if not self.ruta_archivo.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {self.ruta_archivo}")


class FuenteCSV(FuenteDatos):
    """Implementación de lectura de datos desde archivos CSV."""

    def cargar(self) -> List[Dict[str, Any]]:
        self._verificar_existencia()
        registros: List[Dict[str, Any]] = []
        with open(self.ruta_archivo, mode="r", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            for fila in lector:
                registros.append(dict(fila))
        return registros


class FuenteJSON(FuenteDatos):
    """Implementación de lectura de datos desde archivos JSON."""

    def cargar(self) -> List[Dict[str, Any]]:
        self._verificar_existencia()
        with open(self.ruta_archivo, mode="r", encoding="utf-8") as f:
            datos = json.load(f)
            if not isinstance(datos, list):
                raise ValueError("El archivo JSON debe contener una lista de objetos.")
            return datos
