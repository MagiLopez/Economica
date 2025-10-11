from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from servicios.ServiciosInteresSimple import router as interes_simple_router
from servicios.ServiciosIteresCompuesto import router as interes_compuesto_router
from servicios.ServiciosTasaDeInteres import router as tasa_interes_router
from servicios.ServiciosLogin import router as login_router
from servicios.ServiciosAnualidad import router as anualidad_router
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # luego puedes restringir a ["http://127.0.0.1:5000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(interes_simple_router)
app.include_router(interes_compuesto_router)
app.include_router(tasa_interes_router)
app.include_router(login_router)
app.include_router(anualidad_router)