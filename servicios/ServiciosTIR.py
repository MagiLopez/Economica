from fastapi import FastAPI,APIRouter,HTTPException
from app.models.models import Tasa_Interna_De_Retorno
from typing import List

router=APIRouter()

@router.post("/calcular_TIR")
def calcular_TIR(data:Tasa_Interna_De_Retorno):
        try:
            tasa=data.calcular_tasa_interna_de_retorno()
            return {"TIR":tasa}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))