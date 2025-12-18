from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# "Base de datos"
DB = {
    "users": {},
    # {dni, nia, nombre, apellidos, email, password, rol (professor, student, coordinator, admin), lista permisos (), LIST (NOMBRE ASIG, GRUPO), lista de notificaciones (título, mensaje, fecha, leída)}
    "subjects": {},
    # {code, name, año} 
    # {code, name, año, lista de usuarios global (nombre, apellidos, grupo, rol), lista de grupos (code), lista de exámenes (codes)}
    "groups": {},
    "exams": {},
    "instances": {},
    "annotations": {},
}

def getPK(entidad, data):
    if entidad == "users":
        return data.get("dni")
    elif entidad == "notifications":
        return data.get("id")
    elif entidad == "subjects":
        return data.get("code")
    elif entidad == "groups":
        return data.get("id")
    elif entidad == "exams":
        return data.get("id")
    elif entidad == "instances":
        return data.get("id")
    elif entidad == "annotations":
        return data.get("id")

# --- View genérica CRUD por entidad (ASIGNATURAS, GRUPOS, USUARIOS, EXÁMENES, INSTANCIAS, ANOTACIONES, NOTIFICACIONES) ---
class EntityView(APIView):
    """
    Endpoint genérico para CRUD.

    /api/<entidad>/ -> get, post
    /api/<entidad>/<pk>/ -> get, put, delete
    """
    permission_classes = []

    def get(self, request, entidad, pk=None):
        if pk:
            objeto = DB.get(entidad, {}).get(pk)
            return Response({
                "entity": entidad,
                "pk": pk,
                "result": objeto
            })

        return Response({
            "entity": entidad,
            "results": DB.get(entidad, {})
        })

    def post(self, request, entidad):
        DB.get(entidad, {})[getPK(entidad, request.data)] = request.data
        return Response({
            "message": "Object created",
            "entity": entidad,
            "object": request.data
        }, status=status.HTTP_201_CREATED)

    def put(self, request, entidad, pk):
        DB.get(entidad, {})[pk] = request.data
        return Response({
            "message": "Object updated",
            "entity": entidad,
            "pk": pk,
            "object": request.data
        })

    def delete(self, request, entidad, pk=None):
        if pk:
            DB.get(entidad, {}).pop(pk, None)
            return Response({
                "message": "Object deleted",
                "entity": entidad,
                "pk": pk
            })

        DB[entidad] = {}
        return Response({
            "message": "All objects deleted",
            "entity": entidad
        })
