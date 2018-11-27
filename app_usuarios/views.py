import base64

from django import forms
from django.conf import settings
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, login as auth_login,
)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.forms import modelform_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, CreateView

from app_reservas.roles import ADMINISTRADOR_ROLE
from app_usuarios.utils import validateEmail
from django.contrib.auth.models import User
from .models import Usuario
from .utils import obtenerUsername
from .forms import CreateDocenteForm, CreateDocenteConfirmForm, CreateUsuarioModelForm
from .tasks import enviarMailRegistro
from app_academica.models import Docente as DocenteReserva
from app_reservas.errors import not_found_error
from rolepermissions.decorators import has_role_decorator
from rolepermissions.checkers import has_permission, has_role
from rolepermissions.mixins import HasRoleMixin


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='app_usuarios/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            user = form.get_user()
            auth_login(request, user)

            try:
                # Search Docente model user
                user_model = Usuario.objects.get(pk=user.pk)
            except Usuario.DoesNotExist:
                redirect_to = resolve_url("first_access")
            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


def CreateDocente(request):
    form = CreateDocenteForm()
    if request.method == "POST":
        form = CreateDocenteForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user_list = Usuario.objects.filter(email=email)[:1]
            if user_list:
                if not user_list[0].is_active:
                    return render(request, 'commons/warning_message.html', {
                        'title': 'Su registro requiere la aprobación de un administrador',
                        'message': 'Ya existe un usuario registrado con este email, pero requiere la aprobación de un administrador'
                    })
                else:
                    return render(request, 'commons/error_message.html', {
                        'message': 'Ya existe un usuario registrado con este email.'
                    })
            enviarMailRegistro.delay(email)

            return render(request, 'commons/success_message.html', {
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
            return render(request, 'commons/warning_message.html', {
                'title': 'Su registro requiere la aprobación de un administrador',
                'message': 'Ya existe un usuario registrado con este email, pero requiere la aprobación de un administrador'
            })
        else:
            return render(request, 'commons/error_message.html', {
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
                    return render(request, 'commons/success_message.html', {
                        'title': 'Su registro ha sido exitoso',
                        'message': 'Su registro se ha realizado con exito.'
                    })
                else:
                    return render(request, 'commons/warning_message.html', {
                        'title': 'Su registro requiere la aprobación de un administrador',
                        'message': 'Su usuario se ha creado con exito. Pero no podrá acceder al sistema hasta que un admistrador lo habilite'
                    })
        return render(request, 'app_usuarios/signup_confirm.html', {
            'form': form,
            'email': email
        })


def _getUserIsActive(email, form):
    is_active = True
    docente_obj = DocenteReserva.objects.filter(legajo=form.cleaned_data.get('legajo'))[:1]
    # Si no existe el legajo o el apellido que ingreso no se encuentra en el mail el usuario no se crea como activo
    if (form.cleaned_data.get('last_name') and not form.cleaned_data.get('last_name').lower() in email) or not docente_obj:
        is_active = False
    return is_active


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


@has_role_decorator(ADMINISTRADOR_ROLE)
def DocenteApprove(request, pk):
    docente_obj = Usuario.objects.get(id=pk)
    docente_obj.is_active = True
    docente_obj.save()
    return redirect(reverse_lazy('docente_detalle', kwargs={'pk': pk}))


@has_role_decorator(ADMINISTRADOR_ROLE)
def DocenteReject(request, pk):
    docente_obj = Usuario.objects.get(id=pk)
    if request.method == 'POST':
        docente_obj.delete()
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
    template_name = 'app_usuarios/user_profile_edit.html'
    form_class = modelform_factory(
        Usuario,
        fields=['celular', 'telefono', 'foto'],
        widgets={
            'celular': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20'}),
        }
    )

    def get_object(self):
        user_obj = Usuario.objects.filter(id=self.request.user.id)
        if user_obj:
            return user_obj[0]


class UserProfileUpdateAdminView(UpdateView):
    model = Usuario
    template_name = 'app_usuarios/user_profile_edit.html'
    form_class = modelform_factory(
        Usuario,
        fields=['legajo','celular', 'telefono', 'foto', 'areas'],
        widgets={
            'legajo': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20'}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20'}),
            'areas': forms.SelectMultiple(attrs={'class': 'form-control'})
        }
    )

    def get_success_url(self):

        return reverse_lazy('docente_detalle', kwargs={'pk': self.object.id})


class UserProfileCreateView(CreateView):
    model = Usuario
    template_name = 'app_usuarios/user_profile_edit.html'
    form_class = modelform_factory(
        Usuario,
        fields=['legajo','celular', 'telefono', 'foto'],
        widgets={
            'legajo': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20'}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20'}),
            'areas': forms.SelectMultiple(attrs={'class': 'form-control'})
        }
    )

    def get_success_url(self):
        redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

        return HttpResponseRedirect(redirect_to)


def FirstAccess(request):
    form = CreateUsuarioModelForm()
    django_user = get_object_or_404(User, pk=request.user.pk)
    if request.method == "POST":
        form = CreateUsuarioModelForm(request.POST, request.FILES)
        if form.is_valid():
            user = Usuario(user_ptr_id=django_user.pk, **form.cleaned_data)
            user.__dict__.update(django_user.__dict__)
            user.is_active = _getUserIsActive(django_user.email, form)
            user.save()

            if user.is_active:
                return render(request, 'app_usuarios/first_access.html', {
                    'title': 'Su registro ha sido exitoso',
                    'message': 'Su registro se ha realizado con exito.'
                })
            else:
                return render(request, 'commons/warning_message.html', {
                    'title': 'Su registro requiere la aprobación de un administrador',
                    'message': 'Su usuario se ha creado con exito. Pero no podrá acceder al sistema hasta que un admistrador lo habilite'
                })
    return render(request, 'app_usuarios/first_access.html', {
        'form': form,
        'email': django_user.email
    })
