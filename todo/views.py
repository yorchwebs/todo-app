from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import List, Task


@login_required  # Asegúrate de que solo los usuarios autenticados puedan acceder a esta vista
def index_view(request):
    user = request.user  # Obtén el usuario autenticado

    # Obtén las listas y tareas del usuario autenticado
    lists = List.objects.filter(user=user)
    tasks = Task.objects.filter(list__in=lists)

    data = {
        "lists": [{"id": list.id, "title": list.title} for list in lists],
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "due_date": task.due_date,
                "completed": task.completed,
            }
            for task in tasks
        ],
    }

    if request.method == "POST":
        if "create_list" in request.POST:
            # Crear una nueva lista
            title = request.POST["title"]
            List.objects.create(title=title, user=user)  # Usa el usuario autenticado
            return redirect("index")
        elif "create_task" in request.POST:
            # Crear una nueva tarea
            title = request.POST["title"]
            description = request.POST["description"]
            due_date = request.POST["due_date"]
            list_id = request.POST["list_id"]
            try:
                list_obj = List.objects.get(
                    id=list_id, user=user
                )  # Verifica que la lista pertenezca al usuario
                Task.objects.create(
                    title=title,
                    description=description,
                    due_date=due_date,
                    list=list_obj,
                )
                return redirect("index")
            except List.DoesNotExist:
                raise ValueError("La lista no pertenece al usuario autenticado")

    return render(request, "todo/index.html", data)
