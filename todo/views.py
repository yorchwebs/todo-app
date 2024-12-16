from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.contrib import messages
from .models import List, Task


@login_required
def index_view(request):
    user = request.user


    lists = List.objects.filter(user=user)
    tasks = Task.objects.filter(list=lists.first())

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


def update_list(request, list_id):
    if request.method == "POST":
        # Acceder al campo correcto
        new_title = request.POST.get("new_title", None)  # Usar get para evitar errores
        list_obj = get_object_or_404(List, id=list_id)  # Manejar caso donde la lista no existe
        
        if new_title:  # Verificar que new_title no sea None o vacío
            list_obj.title = new_title
            list_obj.save()
        
        return redirect("todo:index")  # Redirigir a la vista deseada

    return redirect("todo:index")  # Manejar caso donde no sea POST (opcional)


def create_task(request, list_id):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        due_date = request.POST["due_date"]
        list_obj = List.objects.get(id=list_id)
        Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            list=list_obj,
        )
        return redirect("todo:index")
    
    
def update_task(request, list_id, task_id):
    
    list_obj = List.objects.get(id=list_id)
    
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        completed = request.POST.get('completed')
        
        if completed == '1':
            task.completed = 1
        else:
            task.completed = 0
        
        task.save()
    
    return redirect('todo:index') 


def delete_task(request, list_id, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect("todo:index")


def delete_list(request, list_id):
    list_obj = List.objects.get(id=list_id)
    list_obj.delete()
    return redirect("todo:index")

