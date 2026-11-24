from django.http import HttpResponse
from django.shortcuts import render, reverse
import datetime
import os

EXCHANGE_RATES = {
    'USD_RUB': 90.5,
    'EUR_RUB': 98.0,
    'USD_EUR': 0.92,
    'EUR_USD': 1.09,
    'RUB_USD': 0.011,
    'RUB_EUR': 0.010,
}


def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir'),
        'Конвертировать валюту': reverse('convert'),
        'О проекте': reverse('about')
    }
    
    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет, 
    # возвращается просто текст
    current_time = datetime.datetime.now().time()
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    # по аналогии с `time_view`, напишите код,
    # который возвращает список файлов в рабочей
    # директории
    workdir = '<br>'.join(os.listdir('.'))
    msg = f'Список файлов в рабочей директории:<br> {workdir}'
    return HttpResponse(msg)


def convert_view(request):
    # конвертация валют

    from_currency = request.GET.get('from')
    to_currency = request.GET.get('to')
    amount = request.GET.get('amount')

    try:
        if amount:
            amount = float(amount)
    except ValueError:
        return HttpResponse('Вы ввели нечисловое значение amount')

    if not (from_currency and to_currency and amount):
        return HttpResponse(f'Пожалуйста, укажите параметры: from, to, amount')
    elif f'{from_currency}_{to_currency}' in EXCHANGE_RATES:
        result = EXCHANGE_RATES[f'{from_currency}_{to_currency}'] * amount
        return HttpResponse(f'{amount} {from_currency} = {result:.2f} {to_currency}')
    else:
        return HttpResponse(f'Курс для пары {from_currency} → {to_currency} не найден')


def about_view(request):
    template_name = 'app/about.html'
    return render(request, template_name)
