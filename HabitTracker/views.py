from django.shortcuts import render, redirect
from .models import ToDoList
from django.contrib.auth.models import User

def work_list(response):
    if response.user.is_authenticated:
        user = response.user
        ls = ToDoList.objects.filter(user=user)
        if response.method == 'POST':
            if response.POST.get('Add'):
                name = response.POST.get('name')
                detail = response.POST.get('detail')
                category = response.POST.get('category')
                newItem = ToDoList(user=user,name=name,detail=detail,category=category)
                newItem.save()
            elif response.POST.get('Delete'):
                item_id = response.POST.get('Delete')
                select_Item = ToDoList.objects.get(id=item_id).delete()

    else:
        return redirect('/login')
    return render(response, 'ht/ht.html', {'ls':ls})
