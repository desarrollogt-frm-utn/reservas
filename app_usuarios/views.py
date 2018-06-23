import base64
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from app_usuarios.utils import validateEmail
from django.contrib.auth.models import User
from .models import Usuario
from .utils import obtenerUsername
from .forms import CreateDocenteForm, CreateDocenteConfirmForm
from .tasks import enviarMailRegistro
from app_reservas.models import Docente as DocenteReserva
from app_reservas.errors import not_found_error
from rolepermissions.decorators import has_role_decorator
from rolepermissions.checkers import has_permission, has_role
from rolepermissions.mixins import HasRoleMixin


def CreateDocente(request):
    form = CreateDocenteForm()
    if request.method == "POST":
        form = CreateDocenteForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user_list = Usuario.objects.filter(email=email)[:1]
            if user_list:
                if not user_list[0].is_active:
                    return render(request, 'app_usuarios/warning_message.html', {
                        'title': 'Su registro requiere la aprobación de un administrador',
                        'message': 'Ya existe un usuario registrado con este email, pero requiere la aprobación de un administrador'
                    })
                else:
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
        return not_found_error(request)
    docente_list = Usuario.objects.filter(email=email)[:1]
    if docente_list:
        if not docente_list[0].is_active:
            return render(request, 'app_usuarios/warning_message.html', {
                'title': 'Su registro requiere la aprobación de un administrador',
                'message': 'Ya existe un usuario registrado con este email, pero requiere la aprobación de un administrador'
            })
        else:
            return render(request, 'app_usuarios/error_message.html', {
                'message': 'Ya existe un usuario registrado con este email.'
            })
    else:
        form = CreateDocenteConfirmForm()
        if request.method == "POST":
            form = CreateDocenteConfirmForm(request.POST, request.FILES)
            if form.is_valid():
                password = form.cleaned_data.pop('password')
                user = Usuario(**form.cleaned_data)
                user.is_active = _getUserIsActive(email, form)
                user.email = email
                user.username = obtenerUsername(email)
                user.set_password(password)
                user.save()

                if user.is_active:
                    return render(request, 'app_usuarios/success_message.html', {
                        'title': 'Su registro ha sido exitoso',
                        'message': 'Su registro se ha realizado con exito.'
                    })
                else:
                    return render(request, 'app_usuarios/warning_message.html', {
                        'title': 'Su registro requiere la aprobación de un administrador',
                        'message': 'Su usuario se ha creado con exito. Pero no podrá acceder al sistema hasta que un admistrador lo habilite'
                    })
        return render(request, 'app_usuarios/signup_confirm.html', {
            'form': form,
            'email': email
        })

def _getUserIsActive(email, form):
    isActive = True
    docenteObj = DocenteReserva.objects.filter(legajo = form.cleaned_data.get('legajo'))[:1]
    # Si no existe el legajo o el apellido que ingreso no se encuentra en el mail el usuario no se crea como activo
    if not form.cleaned_data.get('last_name').lower() in email or not docenteObj:
        isActive = False
    return isActive


class DocenteDetail(HasRoleMixin, DetailView):
    allowed_roles = 'administrador'
    template_name = 'app_usuarios/docente_detail.html'
    model = Usuario

    def get_context_data(self, **kwargs):
        context = super(DocenteDetail, self).get_context_data(**kwargs)
        context['edit_docente_estado'] = has_permission(self.request.user, 'edit_docente_estado')
        model_user_obj = context['object']
        context['tecnico'] = has_role(model_user_obj, 'tecnico')
        context['soporte'] = has_role(model_user_obj, 'soporte')
        context['administrador'] = has_role(model_user_obj, 'administrador')
        context['bedel'] = has_role(model_user_obj, 'bedel')
        context['aliano'] = has_role(model_user_obj, 'aliano')
        return context


@has_role_decorator('administrador')
def DocenteApprove(request, pk):
    docente_obj = Usuario.objects.get(id=pk)
    docente_obj.is_active = True
    docente_obj.save()
    return redirect(reverse_lazy('docente_detalle', kwargs={'pk': pk}))


@has_role_decorator('administrador')
def DocenteReject(request, pk):
    docente_obj = Usuario.objects.get(id=pk)
    if request.method == 'POST':
        docente_obj.email = 'None'
        docente_obj.is_active = False
        docente_obj.save()
        return redirect(reverse_lazy('user_roles'))
    return render(request, 'app_usuarios/docente_reject_confirm.html', {'docente': docente_obj, })


class UserProfileDetail(DetailView):
    template_name = 'app_usuarios/user_profile.html'
    model = User

    def get_object(self):
        user_obj = Usuario.objects.filter(id=self.request.user.id)
        if user_obj:
            return user_obj[0]
        return User.objects.get(id=self.request.user.id)


class UserProfileUpdate(UpdateView):
    model = Usuario
    fields = ['celular', 'telefono', 'foto']
    template_name = 'app_usuarios/user_profile_edit.html'

    def get_object(self):
        user_obj = Usuario.objects.filter(id=self.request.user.id)
        if user_obj:
            return user_obj[0]
