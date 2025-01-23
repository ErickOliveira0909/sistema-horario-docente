from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'professor_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def exibir_mensagem(mensagem, tipo):
    """
    Adiciona uma mensagem para exibição na próxima página carregada.

    :param tipo: Tipo da mensagem ('sucesso', 'erro', 'info', etc.)
    :param mensagem: Texto da mensagem a ser exibida.
    """
    flash(tipo,mensagem)
