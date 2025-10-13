from fastapi import FastAPI,APIRouter,HTTPException
from app.models.models import Amortizacion

router=APIRouter()

@router.post("/calcular_Amortizacion")
def calcular_Amortizacion(data:Amortizacion):
    if data.A is None:
        try:
            A=data.Amortizacion_Sistema_Frances()
            return {"Cuota de Amortizacion":A}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    elif data.n is None:
        try:
            i=data.Amortizacion_Sistema_Americano()
            return {"interes":i}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        try:
            A[0,0,0,]=data.Amortizacion_Sistema_Aleman()
            return {"Cuota":A[0],"Amortizacion":A[1],"Interes":A[2]}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

