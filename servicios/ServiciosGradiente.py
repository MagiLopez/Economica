from fastapi import FastAPI,APIRouter,HTTPException
from app.models.models import Gradiente

router=APIRouter()

@router.post("/calcular_Gradiente_aritmetico")
def calcular_Gradiente_aritmetico(data:Gradiente):
    try:
        vf=data.Valor_futuro_gradiente_aritmetico()
        va=data.Valor_actual_gradiente_aritmetico()
        return {"Valor Futuro Gradiente Aritmetico":vf,"Valor Actual Gradiente Aritmetico":va}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/calcular_Gradiente_geometrico")
def calcular_Gradiente_geometrico(data:Gradiente):
    try:    
        vf=data.Valor_futuro_gradiente_geometrico()
        va=data.Valor_presente_gradiente_geometrico()
        return {"Valor Futuro Gradiente Geometrico":vf,"Valor Actual Gradiente Geometrico":va}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/calcular_series_gradiente")
def calcular_series_gradiente(data:Gradiente):
    try:    
        series=data.series()
        return {"Series Gradiente":series}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))