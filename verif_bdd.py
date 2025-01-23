from app import db
from app.models import Professor, Turma,Disciplina,Horario
def verificar_professor(email):
    professor = Professor.query.filter_by(email=email).first()
    if professor:
        return True
    else:
        return False
    
def verificar_turma(nome):
    turma = Turma.query.filter_by(nome=nome).first()
    if turma:
        return True
    
    else:
        return False
    
def verificar_disciplina(nome):
    disciplina = Disciplina.query.filter_by(nome=nome).first()
    if disciplina:
        return True
    else:
        return False

from datetime import time

def verificar_conflito_horario(dia_semana, hora_inicio, hora_fim, turma_id):
    # Verificar horários conflitantes
    conflitos = Horario.query.filter(
        Horario.dia_semana == dia_semana,
        Horario.turma_id == turma_id,
        (
            # Novo horário começa dentro de um horário existente
            (Horario.hora_inicio <= hora_inicio) & (Horario.hora_fim > hora_inicio)
        ) |
        (
            # Novo horário termina dentro de um horário existente
            (Horario.hora_inicio < hora_fim) & (Horario.hora_fim >= hora_fim)
        ) |
        (
            # Novo horário engloba completamente um horário existente
            (Horario.hora_inicio >= hora_inicio) & (Horario.hora_fim <= hora_fim)
        )
    ).all()

    if conflitos:
        return True, conflitos  # Há conflitos
    return False, None  # Sem conflitos