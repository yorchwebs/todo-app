from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib import messages
from .models import List, Task


@login_required
def index_view(request):
    user = request.user


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
        if "title" in request.POST:
            title = request.POST["title"]
            if List.objects.filter(user=user, title=title).exists():
                messages.error(request, "La lista ya existe.")
            else:
                List.objects.create(title=title, user=user)
                messages.success(request, "La lista se ha creado correctamente.")
        elif "create_task" in request.POST:
            # Crear una nueva tarea
            title = request.POST["title"]
            description = request.POST["description"]
            due_date = request.POST["due_date"]
            list_id = request.POST["list_id"]
            try:
                list_obj = List.objects.get(
                    id=list_id, user=user
                )
                Task.objects.create(
                    title=title,
                    description=description,
                    due_date=due_date,
                    list=list_obj,
                )
                return redirect("index")
            except List.DoesNotExist:
                raise ValueError("La lista no pertenece al usuario autenticado")

    return render(request, "index.html", data)
