from django.shortcuts import render


def not_found_error(request):
    return render(request, 'app_usuarios/error_message.html', {
        'message': 'El link desde el intentas ingresar no es un link valido.'
    })


def custom_error(request, message):
    return render(request, 'app_usuarios/error_message.html', {
        'message': message
    })
