from django.shortcuts import render, render_to_response
from django.template import RequestContext


def not_found_error(request, *args, **argv):
    response = render_to_response('app_usuarios/error_message.html', {
        'message': 'El link desde el intentas ingresar no es un link válido.'
    },
                                 context_instance=RequestContext(request))
    response.status_code = 404
    return response


def custom_error(request, message):
    return render(request, 'app_usuarios/error_message.html', {
        'message': message
    })
