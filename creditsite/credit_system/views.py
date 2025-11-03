from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

def index(request):
    # return render(request, 'index.html')
    return HttpResponse("<h1>Це головна сторінка сайту</h2>")

def credits_list(request, credid):
    # if (request.GET):
    #     print(request.GET)  # Друк параметрів GET-запиту
    return HttpResponse(f"<h2>Список кредитів</h2><p>{credid}</p>")

# Повідомлення для помилки 404 якщо ми генеруємо помилку через команду raise Http404()
def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Сторінка не найдена</h1>")