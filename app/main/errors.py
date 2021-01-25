from flask import render_template, request, jsonify
from . import main


@main.app_errorhandler(403)
def forbidden(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accespt_html:
        response = jsonify({'error': 'Acesso Proibido'})
        response.status_code = 403
        return response
    return render_template('403.html')


@main.errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'Não Encontrado'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@main.errorhandler(500)
def server_error(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'Erro Interno no Servidor' })
        response.status_code = 500
        return response
    return render_template('500.html'), 500
