from fastapi import APIRouter, Response, status
from config.db import conn
from models.user import users
from schemas.user import User
from starlette.status import HTTP_204_NO_CONTENT #Para poder enviar un estado 


from cryptography.fernet import Fernet  # para cifrar contraseñas

key = Fernet.generate_key()  # Genera los caracteres aleatorios para el cifrado
cifrado = Fernet(key)  # La funcion para cifrar

user = APIRouter()


@user.get("/users", response_model=list[User], tags=["users"])
def get_users():
    return conn.execute(users.select()).fetchall()


@user.post("/users", response_model=User, tags=["users"])
def create_user(user: User):
    # Creamos nuestro usuario como un diccionario para guardar los datos obtenidos
    new_user = {"name": user.name, "email": user.email}

    # Se tiene que encriptar las contrasenas pero antes tenemos que cofificarlas en formatos como el utf-8
    new_user["pasword"] = cifrado.encrypt(user.password.encode("utf-8"))

    # Guardando los datos en la base de datos
    # Si lo guardamos en una variable podria aceptar distintos metodos como el .lastrowid para que nos debuelva el id del usuario creado
    result = conn.execute(users.insert().values(new_user))

    '''retornamos el usuario creado
    Ejecutamos una consulta SELECT de la tabla "users" con el metodo execute de la coneccion y lo condicionamos con where
    En users.c.id -> La "c" hace referencia a la columana "id" en este caso'''
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()


@user.get("/users/{id}", response_model=User, tags=["users"])
def get_user(id: str):
    return conn.execute(users.select().where(users.c.id == id)).first()


@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: str):

    # Una pequena validacion de que si el usuario existe creo que no es el mas optimo --- INVESTIGAR
    if get_user(id) == None:
        return "Usuario no encontrado"
    # En este caso usamos el metodo delete para borrar y el first() hace referencia al primero que encuentre
    conn.execute(users.delete().where(users.c.id == id))

    return Response(status_code=HTTP_204_NO_CONTENT)


@user.put("/users/{id}", response_model=User, tags=["users"])
def update_user(id: str, user: User):
    conn.execute(users.update().values(name=user.name, email=user.email,
                 pasword=cifrado.encrypt(user.password.encode("utf-8"))).where(users.c.id == id))
    return conn.execute(users.select().where(users.c.id == id)).first()
