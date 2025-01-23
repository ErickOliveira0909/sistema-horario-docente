from flask import Blueprint, render_template,request, jsonify, session, url_for, redirect,abort
import generate_hash
import verif_bdd 
from .models import Professor, Disciplina, Turma, turma_disciplina, Horario
from app import  db
from app.utils import login_required, exibir_mensagem
from datetime import datetime

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/cadastro_professores")
def cadastro_professores():
    return render_template("cadastro_professores.html")

@main.route("/cadastrar_professor", methods=["POST"])
def cadastrar():
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    senha_hash = generate_hash.generate_password_hash(senha)
    verificar_professor = verif_bdd.verificar_professor(email)
    if verificar_professor:
        exibir_mensagem("erro", "Professor já cadastrado")
        return redirect("/cadastro_professores")
    else:
        novo_professor = Professor(nome=nome, email=email, senha=senha_hash)
        db.session.add(novo_professor)
        db.session.commit()
        session.clear()
        session['professor_id'] = novo_professor.id
        session["professor_nome"] = novo_professor.nome
    print(f"{nome} {email} {senha}")
    exibir_mensagem("sucesso", "Professor cadastrado com sucesso!")
    return redirect("/dashboard")

@main.route("/dashboard")
@login_required
def dashboard():
    numero_disciplinas = Disciplina.query.filter_by(professor_id=session["professor_id"]).count()
    return render_template("dashboard.html", numero_disciplinas=numero_disciplinas)

@main.route("/disciplinas")
@login_required
def disciplinas():
    disciplinas = Disciplina.query.filter_by(professor_id=session["professor_id"]).all()
    numero_disciplinas = Disciplina.query.filter_by(professor_id=session["professor_id"]).count()
    return render_template("disciplinas.html", disciplinas=disciplinas, numero_disciplinas=numero_disciplinas)

@main.route("/cadastrando_disciplina", methods=["POST"])
def cadastrando_disciplina():
    if request.method == "POST":
        nome = request.form['nome']
        descricao = request.form["descricao"]
        verificar_disciplina = verif_bdd.verificar_disciplina(nome)
        
        if verificar_disciplina:
            exibir_mensagem("erro","Disciplina já cadastrada")
            return redirect("/disciplinas")
        else:
            nova_disciplina = Disciplina(nome=nome,professor_id=session["professor_id"], descricao=descricao)
            db.session.add(nova_disciplina)
            db.session.commit()
            exibir_mensagem("sucesso", "Disciplina criada com Sucesso!")
        return redirect("/disciplinas")

@main.route("/login")
def login():
    return render_template("login.html")

@main.route("/verificar_login", methods=["POST"])
def verificar_login():
    email = request.form.get("email")
    senha = request.form.get("senha")

    professor = Professor.query.filter_by(email=email).first()

    if professor and generate_hash.check_password_hash(professor.senha, senha):
        session["professor_id"] = professor.id
        session["professor_nome"] = professor.nome
        return redirect("dashboard")
    else:
        exibir_mensagem("erro", "E-mail ou senha incorretos. Tente novamente.")
        return redirect("/login")

@main.route("/logout")
def logout():
    session.pop("professor_id", None)
    session.pop("professor_nome", None)
    return redirect("/")

@main.route("/turmas")
@login_required
def turmas():
    """disciplinas_ids = db.session.query(Disciplina.id).filter_by(professor_id=session["professor_id"]).all()
    disciplinas_ids = [d.id for d in disciplinas_ids]  # Acessa o atributo 'id' diretamente

    turmas = db.session.query(Turma).join(turma_disciplina).filter(
        turma_disciplina.c.disciplina_id.in_(disciplinas_ids)
    ).all()
    numero_turmas = db.session.query(Turma).join(turma_disciplina).filter(
        turma_disciplina.c.disciplina_id.in_(disciplinas_ids)
    ).count()"""
    turmas = Turma.query.all()
    disciplinas = Disciplina.query.filter_by(professor_id=session["professor_id"]).all()
    numero_disciplinas = Disciplina.query.filter_by(professor_id=session["professor_id"]).count()

    return render_template("turmas.html", numero_disciplinas=numero_disciplinas, disciplinas=disciplinas, turmas=turmas)

@main.route("/criando_turmas", methods=["POST"])
def criando_turmas():
    if request.method == "POST":
        nome_turma = request.form.get("nome")
        disciplinas_ids = request.form.getlist("disciplinas")
        
        if verif_bdd.Turma(nome_turma):
            exibir_mensagem("erro","Essa turma já existe!")
            return redirect("/turmas")

        turma = Turma(nome=nome_turma)
        db.session.add(turma)
        for disciplina_id in disciplinas_ids:
            disciplina = Disciplina.query.get(disciplina_id)
            print(disciplina.nome)
            turma.disciplinas.append(disciplina)
        
        db.session.commit()
        exibir_mensagem("Turma criada com sucesso!","sucesso")
        return redirect("/turmas")

@main.route("/horarios")
def horarios():
    return render_template("horarios.html")

@main.route('/get_horarios')
def get_horarios():
    horarios = Horario.query.all()
    eventos_json = [
        {
            "id": horario.id,
            "title": f"""{horario.professor.nome} - {horario.disciplina.nome}""",
            "start":f"{horario.dia_semana}T{horario.hora_inicio.strftime('%H:%M:%S')}",
            "end":f"{horario.dia_semana}T{horario.hora_fim.strftime('%H:%M:%S')}"

        }
        for horario in horarios
    ]
    return jsonify(eventos_json)

@main.route("/editar_disciplina", methods=["POST"])
def editar_disciplina():
    data = request.get_json()
    if not data:
        return redirect("/disciplinas")
    disciplina_id = data.get("id")
    nome = data.get("nome")
    descricao = data.get("descricao")
    

    if not disciplina_id or not nome or not descricao:
        
        exibir_mensagem("erro","Informe todos os dados")
        return redirect("/disciplinas")
        
    disciplina = Disciplina.query.get(disciplina_id)
    if not disciplina:
        return redirect("/disciplinas")

    if nome != disciplina.nome and verif_bdd.verificar_disciplina(nome):
        exibir_mensagem("erro","Já existe disciplina com essas caracteristicas!")
        return redirect("/disciplinas")

    disciplina.nome = nome
    disciplina.descricao = descricao
    
    

    try:
        db.session.commit()
        exibir_mensagem("sucesso","Disciplina editada com sucesso!")
    except Exception as e:
        db.session.rollback()
        exibir_mensagem("erro","Erro ao editar turma")
    return redirect("/disciplinas")

@main.route("/apagar_disciplina", methods=["POST"])
def apagar_disciplina():
    data = request.get_json()
    disciplina_id = data.get("id")
    disciplina = Disciplina.query.get(disciplina_id)

    if not disciplina:
        return redirect("/disciplinas")
    try:
         # Verificar e remover registros na tabela turma_disciplina
        turma_disciplina.delete().where(turma_disciplina.c.disciplina_id==disciplina_id)

        # Verificar e remover registros na tabela horario
        Horario.query.filter_by(disciplina_id=disciplina_id).delete()

        # Remover a disciplina
        db.session.delete(disciplina)
        db.session.commit()
        exibir_mensagem("sucesso", "Disciplina apagada com sucesso!")
        return redirect("/disciplinas")
    except Exception as e:
        db.session.rollback()
        exibir_mensagem("erro", "Erro ao apagar disciplina!")
        return redirect("/disciplinas")


@main.route("/editar_turma", methods=["POST"])
def editar_turma():
    turma_id = request.form.get("turma_id")
    nome = request.form.get("nome")
    disciplinas = request.form.getlist("disciplinas")  # Para múltiplos valores

    if not turma_id or not nome:
        exibir_mensagem("DADOS INCOMPLETOS!", "erro")
        return redirect("/turmas")

    if not isinstance(disciplinas, list):
        exibir_mensagem("Disciplina deve ser uma lista!", "erro")
        return redirect("/turmas")

    turma = Turma.query.get(turma_id)

    if nome != turma.nome and verif_bdd.verificar_turma(nome):
        exibir_mensagem("Já existe turma com esse nome!", "erro")
        return redirect("/turmas")

    turma.nome = nome
    turma.disciplinas.clear()

    for disciplina_id in disciplinas:
        disciplina = Disciplina.query.get(disciplina_id)
        turma.disciplinas.append(disciplina)

    try:
        db.session.commit()
        exibir_mensagem("Alterações salvas com sucesso", "sucesso")
        
    except Exception as e:
        db.session.rollback()
        exibir_mensagem("Erro ao salvar alterações", "erro")
        print(f"Erro ao salvar alterações: {e}")
        
    return redirect("/turmas")
@main.route("/horarios_turma")
def horarios_turma():
    id = request.args.get("id")
    session["turma_id"] = id
    print(id)
    disciplinas = Disciplina.query.filter_by(professor_id=session["professor_id"]).all()
    return render_template("horarios_turma.html",id=id, disciplinas=disciplinas)

@main.route("/get_horarioturma")
def get_horarioturma():
    session.pop("turma_id", None)
    id = request.args.get("id")
    session["turma_id"] = id
    
    horarios = Horario.query.filter_by(turma_id=id).all()
    eventos_json = [
        {
            "id": horario.id,
            "title": f"""{horario.professor.nome} - {horario.disciplina.nome}""",
            "start":f"{horario.dia_semana}T{horario.hora_inicio.strftime('%H:%M:%S')}",
            "end":f"{horario.dia_semana}T{horario.hora_fim.strftime('%H:%M:%S')}"

        }
        for horario in horarios
    ]
    if eventos_json:
        return jsonify(eventos_json)
    else:
        
        return redirect(f"/horarios_turma?id={id}")

@main.route("/add_horarioturma", methods=["POST"])
def add_horarioturma():
    data_inicio = request.form['dataInicio']
    hora_inicio = request.form['horaInicio']
    hora_fim = request.form['horaFim']
    disciplina_id = request.form['disciplina']
    
    

    # Lógica para salvar o horário associado à disciplina
    print(f"Data: {data_inicio}, Início: {hora_inicio}, Fim: {hora_fim}, Disciplina: {disciplina_id}")
    


        # Validação simples
    if not data_inicio or not hora_inicio or not hora_fim:
        exibir_mensagem("erro", "Todos os campos são obrigatorios!")
        return redirect(f"/horarios_turma?id={session['turma_id']}")

    # Conversão para os formatos adequados
    hora_inicio = datetime.strptime(hora_inicio, "%H:%M").time()
    hora_fim = datetime.strptime(hora_fim, "%H:%M").time()

    horarios_turma = Horario.query.filter_by(turma_id=session["turma_id"]).all()
    for horario in horarios_turma:
        if hora_inicio >= horario.hora_inicio and hora_fim <= horario.hora_fim:
            exibir_mensagem("erro", "Conflitos com Horarios já existentes!")
            return redirect(f"/horarios_turma?id={session['turma_id']}")
    horarios_prof = Horario.query.filter_by(professor_id=session["professor_id"]).all()

    for horario in horarios_prof:
        if hora_inicio >= horario.hora_inicio and hora_fim <= horario.hora_fim:
            exibir_mensagem("erro", "Conflito com Horarios do professor!")
            return redirect(f"/horarios_turma?id={session['turma_id']}")

    # Criar novo horário
    novo_horario = Horario(
        dia_semana=data_inicio,  # Data do evento
        hora_inicio=hora_inicio,
        hora_fim=hora_fim,
        turma_id=session["turma_id"],
        disciplina_id=disciplina_id,
        professor_id=session["professor_id"]
    )
    exibir_mensagem("sucesso", "Horario adicionado com sucesso!")
    db.session.add(novo_horario)
    db.session.commit()
    return redirect(f"/horarios_turma?id={session['turma_id']}")

@main.route("/remover_horario", methods=["POST"])
def remover_horario():
    data = request.get_json()
    horario_id = data.get("id")

    db.session.query(Horario).filter_by(id=horario_id).delete()
    db.session.commit()
    return redirect(f"/horarios?id={session['turma_id']}")
