import base64
from django.shortcuts import render
from app_usuarios.utils import validateEmail
from .models import Docente
from .utils import obtenerUsername
from .forms import CreateDocenteForm, CreateDocenteConfirmForm
from .tasks import enviarMailRegistro


def CreateDocente(request):
    form = CreateDocenteForm()
    if request.method == "POST":
        form = CreateDocenteForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            docente_list = Docente.objects.filter(email=email)[:1]
            if docente_list:
                return render(request, 'app_usuarios/error_message.html', {
                    'message': 'Ya existe un usuario registrado con este email.'
                })
            enviarMailRegistro.delay(email)

            return render(request, 'app_usuarios/success_message.html', {
                'title': 'Su solicitud de registro se ha procesado',
                'message': 'Pronto recibirá en su correo un mail informando como continuar con el registro dentro del sistema. '
            })
    return render(request, 'app_usuarios/signup.html', {
        'form': form,
    })


def CreateDocenteConfirm(request, code):
    try:
        email = base64.b64decode(code).decode('utf-8')
    except Exception:
        email = "Byte no válido"
    if not validateEmail(email):
        return render(request, 'app_usuarios/error_message.html', {
            'message': 'El link desde el intentas ingresar no es un link valido.'
        })
    docente_list = Docente.objects.filter(email=email)[:1]
    if docente_list:
        return render(request, 'app_usuarios/error_message.html', {
            'message': 'Ya existe un usuario registrado con este email.'
        })
    else:
        form = CreateDocenteConfirmForm()
        if request.method == "POST":
            form = CreateDocenteConfirmForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data.pop('password')
                user = Docente(**form.cleaned_data)
                user.email = email
                user.username = obtenerUsername(email)
                user.set_password(password)
                user.save()

                return render(request, 'app_usuarios/success_message.html', {
                    'title': 'Su registro ha sido exitoso',
                    'message': 'Su registro se ha realizado con exito.'
                })
        return render(request, 'app_usuarios/signup_confirm.html', {
            'form': form,
            'email': email
        })
