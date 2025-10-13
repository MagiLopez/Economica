from fastapi import FastAPI,APIRouter,HTTPException
from app.models.models import Capitalizacion

router=APIRouter()

@router.post("/calcular_Capitalizacion_simple")
def calcular_Capitalizacion(data:Capitalizacion):
    if data.Vf is None:
        try:
            resultado = data.capitalizacion_simple()
            return {"Vf": resultado}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

@router.post("/calcular_Capitalizacion_compuesta")
def calcular_Capitalizacion(data:Capitalizacion):
    if data.Vf is None:
        try:
            resultado = data.capitalizacion_compuesta()
            return {"Vf": resultado}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))