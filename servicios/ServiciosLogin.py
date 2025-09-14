from fastapi import FastAPI, Request, APIRouter,HTTPException
from fastapi.responses import JSONResponse
import firebase_admin
from firebase_admin import credentials, auth
from app.models.login import Usuario

router = APIRouter()
usuario = Usuario()
registros=[]

# Inicializar Firebase Admin
cred = credentials.Certificate("serviceAccountKey.json")  # tu clave privada de Firebase
firebase_admin.initialize_app(cred)

@router.post("/login/verificacionGoogle")
async def verificacionGoogle(request: Request):
    try:
        data = await request.json()
        token = data.get("token")

        decoded_token = auth.verify_id_token(token)
        uid = decoded_token["uid"]
        email = decoded_token.get("email")
        name = decoded_token.get("name")

        return JSONResponse({
            "success": True,
            "uid": uid,
            "email": email,
            "name": name
        })

    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=401)
    

@router.post("/validar_login")
def validar_login_usuario(req:Usuario):
    for usuario in registros:
        if usuario["cedula"] == req.cedula and usuario["password"] == req.password:
            return {"success":True,"mensage":"login exitoso"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.post("/login/registro")
def registrar_usuario(request: dict):  # Cambiado para recibir dict directamente
    # Extraer los datos del request
    cedula = request.get("cedula")
    nombres = request.get("nombres")  # Campo que viene del frontend
    apellidos = request.get("apellidos")  # Campo que viene del frontend
    correo = request.get("correo")
    password = request.get("password")
    
    # Validar que todos los campos estén presentes
    if not all([cedula, nombres, apellidos, correo, password]):
        raise HTTPException(status_code=400, detail="Todos los campos son obligatorios")
    
    # Verificar si el usuario ya existe
    for reg in registros:
        if reg["cedula"] == cedula:
            raise HTTPException(status_code=400, detail="Usuario ya registrado")
    
    # Crear el usuario con los campos correctos
    nuevo_usuario = {
        "cedula": cedula,
        "nombre": nombres,  # Mapear 'nombres' a 'nombre'
        "apellido": apellidos,  # Mapear 'apellidos' a 'apellido'
        "correo": correo,
        "password": password
    }
    
    registros.append(nuevo_usuario)
    return {"message": "Usuario registrado exitosamente", "usuario": nuevo_usuario}

@router.get("/usuarios")
def ver_usuarios():
    return {"usuarios": registros}

