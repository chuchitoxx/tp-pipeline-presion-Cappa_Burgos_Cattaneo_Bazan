import tempfile
import unittest
from pathlib import Path

from src.fuentes import FuenteCSV, FuenteJSON
from src.modelo import MedicionPresion
from src.pipeline import PipelinePresion


class TestPipelinePresion(unittest.TestCase):

    def test_medicion_valida_e_invalida(self) -> None:
        valida = MedicionPresion(
            id_medicion=1,
            sensor_id="SENS-01",
            timestamp="2026-10-15T10:00:00",
            presion_hpa=1013.25,
            temperatura_c=20.0,
        )
        self.assertTrue(valida.es_valida())
        self.assertAlmostEqual(valida.presion_atm, 1.0, places=4)

        invalida_presion = MedicionPresion(
            id_medicion=2,
            sensor_id="SENS-01",
            timestamp="2026-10-15T10:05:00",
            presion_hpa=-10.0,
            temperatura_c=20.0,
        )
        self.assertFalse(invalida_presion.es_valida())

        invalida_sensor = MedicionPresion(
            id_medicion=3,
            sensor_id="   ",
            timestamp="2026-10-15T10:10:00",
            presion_hpa=1010.0,
            temperatura_c=20.0,
        )
        self.assertFalse(invalida_sensor.es_valida())

    def test_pipeline_integracion_csv_y_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            csv_file = tmp_path / "test.csv"
            json_file = tmp_path / "test.json"

            csv_file.write_text(
                "id_medicion,sensor_id,timestamp,presion_hpa,temperatura_c\n"
                "1,SENS-A,2026-10-15T08:00:00,1000.0,20.0\n"
                "2,SENS-A,2026-10-15T08:05:00,-500.0,20.0\n",
                encoding="utf-8",
            )

            json_file.write_text(
                '[{"id_medicion": 3, "sensor_id": "SENS-B", '
                '"timestamp": "2026-10-15T08:10:00", "presion_hpa": 1020.0, "temperatura_c": 22.0}]',
                encoding="utf-8",
            )

            pipeline = PipelinePresion([FuenteCSV(csv_file), FuenteJSON(json_file)])
            validas = pipeline.ejecutar()
            stats = pipeline.obtener_estadisticas()

            self.assertEqual(len(validas), 2)
            self.assertEqual(stats["total_validas"], 2)
            self.assertEqual(stats["total_descartadas"], 1)
            self.assertEqual(stats["presion_promedio_hpa"], 1010.0)
            self.assertIn("SENS-A", stats["por_sensor"])
            self.assertIn("SENS-B", stats["por_sensor"])


if __name__ == "__main__":
    unittest.main()
