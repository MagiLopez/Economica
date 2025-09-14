from pydantic import BaseModel
from typing import Optional as opcional 


class Usuario (BaseModel):
    cedula: str=""
    nombre: str=""
    apellido:opcional[str]=None
    password: str=""
    correo: opcional[str]=None
