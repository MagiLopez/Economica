from fastapi import FastAPI,APIRouter,HTTPException
from app.models.models import Interes_Simple

router=APIRouter()
interes_simple=Interes_Simple()

@router.post("/calcular_Interes_Simple")
def calcular_Interes_Simple(data:Interes_Simple):
    if data.Vf is None:
        try:
            resultado = data.calcular_valor_futuro()
            return {"Vf": resultado}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif data.Vi is None:
        try:
            resultado = data.calcular_valor_inicial()
            return {"Vi": resultado}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif data.t_a is None and data.t_m is None and data.t_d is None:
        try:
            resultado = data.calcular_tiempo()
            return {"t": resultado}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))