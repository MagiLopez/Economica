from fastapi import FastAPI,APIRouter,HTTPException
from app.models.models import Gradiente

router=APIRouter()
@router.post("/calcular_Gradiente")
def calcular_Gradiente_aritmetico(data:Gradiente):
    try:
        if data.g != 0 and data.G == 0:
            vf=data.Valor_futuro_gradiente_aritmetico()
            va=data.Valor_actual_gradiente_aritmetico()
            return {"Valor Futuro Gradiente Aritmetico":vf,"Valor Actual Gradiente Aritmetico":va}
        elif data.G != 0 and data.g == 0:
            vf=data.Valor_futuro_gradiente_geometrico()
            va=data.Valor_presente_gradiente_geometrico()
            return {"Valor Futuro Gradiente Geometrico":vf,"Valor Actual Gradiente Geometrico":va}
        else:
            raise HTTPException(status_code=400, detail="Por favor ingrese solo uno de los dos tipos de gradiente (g o G)")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))