from fastapi import FastAPI,APIRouter,HTTPException
from app.models.models import Interes_compuesto

router=APIRouter()
interes_compuesto=Interes_compuesto()

@router.post("/calcular_Interes_Compuesto")
def calcular_Interes_Compuesto(data:Interes_compuesto):
    if data.Vf ==0:
        try:
            resultado = data.calcular_valor_futuro()
            return {"Vf": resultado}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif data.i ==0:
        try:
            resultado = data.calcular_tasa_de_interes()
            return {"i": resultado}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif data.n ==0:
        try:
            resultado = data.calcular_tiempo_necesario()
            return {"n": resultado}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))