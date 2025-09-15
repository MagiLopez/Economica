from fastapi import FastAPI,APIRouter,HTTPException
from app.models.models import Anualidad


router=APIRouter()


@router.post("/calcular_Anualidad")
def calcular_Anualidad(data:Anualidad):
    if data.vf ==0:
        try:
            resultado = data.calcular_valor_futuro_anualidad()
            return {"vf": resultado}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif data.va ==0:
        try:
            resultado = data.calcular_valor_anualidad()
            return {"va": resultado}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    