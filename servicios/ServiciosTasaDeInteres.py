from fastapi import FastAPI,APIRouter,HTTPException
from app.models.models import Tasa_interes

router=APIRouter()
tasa_interes=Tasa_interes()

@router.post("/calcular_Tasa_de_Interes")

def calcular_Tasa_de_Interes(data:Tasa_interes):
    resultado = [0,0,0]   
    resultado[0]= data.calcular_tasa_de_interes_por_periodos() 
    resultado[1] = data.calcular_valor_futuro_mensual()
    resultado[2] = data.calcular_valor_futuro()
    
    return {"i_mensual": resultado[0],"Vf_mensual": resultado[1],"Vf": resultado[2]}    