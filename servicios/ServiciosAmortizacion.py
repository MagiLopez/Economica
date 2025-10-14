from fastapi import FastAPI,APIRouter,HTTPException
from app.models.models import Amortizacion

router=APIRouter()

@router.post("/calcular_Amortizacion")
def calcular_Amortizacion_sistema_frances(data:Amortizacion):
        try:
            A=data.Amortizacion_Sistema_Frances()
            return {"Cuota de Amortizacion":A}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.post("/calcular_Amortizacion_Sistema_Americano")
def calcular_Amortizacion_sistema_aleman(data:Amortizacion):
        datos=[]
        try:
            datos = data.Amortizacion_Sistema_Americano()
            return {"tabla":datos}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.post("/calcular_Amortizacion_Sistema_Aleman")
def calcular_Amortizacion_sistema_aleman(data:Amortizacion):
        datos=[]
        try:
            datos = data.Amortizacion_Sistema_Aleman()
            return datos
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

