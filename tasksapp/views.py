from django.shortcuts import render


def index(request):
    context = {
        'page_title': 'решение задач'
    }
    return render(request, 'tasksapp/index.html', context=context)


