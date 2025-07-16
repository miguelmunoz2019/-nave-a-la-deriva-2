from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Dict
import time

app = FastAPI()

# Diccionario simulado de datos de saturación (presión en MPa)
saturation_data = {
    0: {"specific_volume_liquid": 0.001000, "specific_volume_vapor": 10.000},
    1: {"specific_volume_liquid": 0.001043, "specific_volume_vapor": 1.6941},
    2: {"specific_volume_liquid": 0.001061, "specific_volume_vapor": 0.8857},
    3: {"specific_volume_liquid": 0.001072, "specific_volume_vapor": 0.5950},
    4: {"specific_volume_liquid": 0.001081, "specific_volume_vapor": 0.4543},
    5: {"specific_volume_liquid": 0.001088, "specific_volume_vapor": 0.3688},
    6: {"specific_volume_liquid": 0.001095, "specific_volume_vapor": 0.3126},
    7: {"specific_volume_liquid": 0.001101, "specific_volume_vapor": 0.2732},
    8: {"specific_volume_liquid": 0.001106, "specific_volume_vapor": 0.2439},
    9: {"specific_volume_liquid": 0.001110, "specific_volume_vapor": 0.2214},
    10: {"specific_volume_liquid": 0.0035, "specific_volume_vapor": 0.0035},
}

# Registro en memoria de consultas realizadas
request_log: Dict[str, int] = {}

@app.get("/phase-change-diagram")
def get_phase_data(pressure: float = Query(..., gt=0)):
    pressure_int = int(pressure)

    # Registrar la petición
    key = f"pressure={pressure_int}"
    request_log[key] = request_log.get(key, 0) + 1

    # Mostrar en consola para observación en tiempo real
    print(f"[{time.strftime('%H:%M:%S')}] Consulta: {key} | Total: {request_log[key]}")

    if pressure_int in saturation_data:
        return JSONResponse(content=saturation_data[pressure_int])
    else:
        raise HTTPException(status_code=404, detail="Presión no encontrada en la tabla de saturación")

@app.get("/requests-log")
def get_log():
    return request_log
