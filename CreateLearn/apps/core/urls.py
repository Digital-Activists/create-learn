from django.urls import include, path
from django.http import HttpResponse


# Тестовая view-функция
def test_view(request):
    return HttpResponse("Работает! Проект успешно запущен!")


urlpatterns = [
    path("test/", test_view, name="test-page"),
]
