from pydantic import BaseModel
from typing import Optional as opcional 
import math


def convertir_tiempo(t_a: opcional[float] = 0, 
                     t_m: opcional[float] = 0, 
                     t_d: opcional[float] = 0) -> float:
   
    tiempo = 0.0
    if t_a:
        tiempo += t_a
    if t_m:
        tiempo += t_m / 12
    if t_d:
        tiempo += t_d / 365
    
    if tiempo == 0:
        raise ValueError("Se debe proporcionar al menos uno de los valores de tiempo: t_a, t_m o t_d")
    
    return tiempo

def calcular_tasa_de_interes(i_anual: float, n) -> float:  
        i_mensual=math.pow((1+i_anual),(1/n))-1
        return i_mensual 

class Interes_Simple(BaseModel):
    Vf:opcional[float]=None
    Vi:opcional[float]=None
    i:opcional[float]=None
    t_a:opcional[float]=None
    t_m:opcional[float]=None
    t_d:opcional[float]=None
    t: opcional[float] = None 
   
    def calcular_valor_futuro(self):
        tiempo = convertir_tiempo(self.t_a, self.t_m, self.t_d)
        self.Vf = self.Vi * (1 + (self.i/100) * tiempo)
        interes = self.Vf - self.Vi
        return { round(self.Vf, 2), round(interes, 2)}


    def calcular_valor_inicial(self):
        self.Vi = self.Vf / (1 + (self.i/100) * convertir_tiempo(self.t_a, self.t_m, self.t_d))
        return self.Vi
     
    def calcular_tiempo(self):
            if not self.Vi or not self.Vf or not self.i:
                raise ValueError("Faltan Vf, Vi o i para calcular el tiempo")
            self.t = ((self.Vf / self.Vi) - 1) /(self.i/100)
            return self.t
    
class Interes_compuesto(BaseModel):
    Vf:opcional[float]=None
    Vp:opcional[float]=None
    i:opcional[float]=None
    n:opcional[float]=None

    def calcular_valor_futuro(self):
        self.Vf=self.Vp*math.pow((1+(self.i/100)),self.n)
        return self.Vf
    
    def calcular_tasa_de_interes(self):
        self.i=math.pow((self.Vf/self.Vp),(1/self.n))-1
        return self.i*100
    
    def calcular_tiempo_necesario(self):
        self.n=(math.log(self.Vf)-math.log(self.Vp))/math.log(1+(self.i/100))
        return self.n

class Tasa_interes(BaseModel):
    Vp:opcional[float]=None
    n:opcional[float]=None
    i:opcional[float]=None
    
    
    def calcular_tasa_de_interes_por_periodos(self):
        i_mensual=math.pow((1+(self.i/100)),(1/self.n))-1
        return i_mensual*100
    
    def calcular_valor_futuro_mensual(self):
        Vf_mensual=self.Vp*(calcular_tasa_de_interes((self.i/100),self.n)/(1 - math.pow((1+ calcular_tasa_de_interes(self.i,self.n)),-self.n)))
        return Vf_mensual

    def calcular_valor_futuro(self):
        Vf=self.Vp*math.pow((1+calcular_tasa_de_interes((self.i/100),self.n)),self.n)
        return Vf

class Anualidad(BaseModel):
    vf:opcional[float]=None
    va:opcional[float]=None
    i:float
    n:float
    A:float

    def calcular_valor_futuro_anualidad(self):
        self.vf=self.A*(((math.pow((1+(self.i/100)),self.n)-1)/(self.i/100)))
        return self.vf

    def calcular_valor_anualidad(self):
        self.va=self.A*(((1-(math.pow((1+(self.i/100)),-self.n)))/(self.i/100)))
        return self.va
    
class Amortizacion(BaseModel):
    p:float
    i:float
    n:opcional[int]=None
    

    def Amortizacion_Sistema_Frances(self):
        datos=[]
        
        for periodo in range(0,self.n+1):
            if periodo==0:
                saldo=self.p
                intereses=0
                pago=0
                amortizacion=0
            else:
                pago= self.p*(self.i/100)/(1-math.pow((1+(self.i/100)),-self.n))
                intereses=saldo*(self.i/100)
                amortizacion=pago-intereses
                saldo-=amortizacion
            # Añadimos una fila completa
            datos.append([periodo, round(pago, 2), round(intereses, 2), round(amortizacion, 2), round(saldo, 2)])
        return datos
    
    def Amortizacion_Sistema_Aleman(self):
        datos=[]
        for periodo in range(0, self.n + 1):
            if periodo==0:
                saldo = self.p
                intereses = 0
                pago = 0
                amortizacion = 0
            else:
                intereses = saldo * (self.i / 100)
                amortizacion = self.p/self.n
                pago = intereses + amortizacion
                saldo -= amortizacion
            # Añadimos una fila completa
            datos.append([periodo, round(pago, 2), round(intereses, 2), round(amortizacion, 2), round(saldo, 2)])
        return datos

    def Amortizacion_Sistema_Americano(self):

        datos = []
        intereses = self.p * (self.i / 100)

        for periodo in range(1, self.n + 1):
            if periodo == self.n:
                amortizacion = self.p
                pago = intereses + amortizacion
                saldo = 0
            else:
                amortizacion = 0
                pago = intereses
                saldo = self.p

            # Añadimos una fila completa
            datos.append([
                periodo,
                round(pago, 2),
                round(intereses, 2),
                round(amortizacion, 2),
                round(saldo, 2)
            ])

        return datos

            
       

class Gradiente (BaseModel):
    ct:list
    t:float
    A:float
    g:float #para el gradiente aritmetico es una cantidad fija
    G:float #para el gradiente geometrico es %
    i:float
    n:float #numero de cuotas
    vf:opcional[float]=None
    va:opcional[float]=None

    def Valor_futuro_gradiente_aritmetico(self):
        self.vf=self.A*(((math.pow((1+(self.i/100)),self.n+1)-1)/(self.i/100)))+(self.g/self.i)*(((math.pow((1+(self.i/100)),self.n+1)-1)/(self.i/100))- (self.n*(1+self.i/100)))
        return round(self.vf,2)
    def Valor_actual_gradiente_aritmetico(self):
        self.va=self.A*((((math.pow((1+(self.i/100)),self.n)-1))/(self.i/100)*math.pow((1+(self.i/100)),self.n))+(self.g/self.i/100)*(((math.pow((1+(self.i/100)),-self.n)-1))/(self.i/100)*math.pow((1+(self.i/100)),self.n)- (self.n/(math.pow((1+(self.i/100)),self.n)))))
        return round(self.va,2)
    
    def Valor_presente_gradiente_geometrico(self):
        if self.G == self.i:
            self.va=self.A*(self.n/1+(self.i/100))
            return round(self.vf,2)
        else:
            self.va=self.A*(((math.pow((1+(self.G/100)),self.n)- math.pow((1+(self.i/100)),self.n))/((self.i/100)-(self.g/100)*math.pow((1+(self.i/100)),self.n))))
            return round(self.vf,2)
    
    def Valor_futuro_gradiente_geometrico(self):
        if self.G == self.i:
            self.vf=self.A*(self.n*(math.pow((1+(self.i/100)),self.n-1)))
            return round(self.vf,2)
        else:
            self.vf=self.A*(((math.pow((1+(self.G/100)),self.n)- math.pow((1+(self.i/100)),self.n))/((self.i/100)-(self.g/100))))
            return round(self.vf,2)

    def series(self):
        self.va=[ct/math.pow((1+(self.i/100)),t) for t,ct in enumerate(self.ct, start=1)]
        
        self.vf=[ct*math.pow((1+(self.i/100)),self.n-t) for t,ct in enumerate(self.ct, start=1)]

        return {round(sum(self.va),2), round(sum(self.vf),2)}

class Capitalizacion(BaseModel):
    c:float
    i:float
    n:float
    Vf:opcional[float]=None
#es practicamente como lo del semetre pasado
    def capitalizacion_compuesta(self):
        self.vf=self.c*math.pow((1+(self.i/100)),self.n)
        return round(self.Vf,2)
    def capitalizacion_simple(self):
        self.vf=self.c*(1+(self.i/100)*self.n)
        return round(self.Vf,2)

class Tasa_Interna_De_Retorno(BaseModel):
    flujo_de_caja:list
    tasa:opcional[float]=None

    def calcular_tasa_interna_de_retorno(self):
        tir=0.0
        for i in range(0,100000):
            npv=0.0
            for t, flujo in enumerate(self.flujo_de_caja):
                npv += flujo / ((1 + tir) ** t)
            if npv > 0:
                tir += 0.001
            else:
                break
        self.tasa=tir*100
        return round(self.tasa,2)