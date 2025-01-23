from app import db

# Tabela de junção para relação muitos-para-muitos entre Turma e Disciplina
turma_disciplina = db.Table(
    'turma_disciplina',
    db.Column('turma_id', db.Integer, db.ForeignKey('turma.id'), primary_key=True),
    db.Column('disciplina_id', db.Integer, db.ForeignKey('disciplina.id'), primary_key=True)
)

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    disciplinas = db.relationship('Disciplina', backref='professor', lazy=True)  # Um professor pode lecionar várias disciplinas

    def __repr__(self):
        return f"<Professor {self.nome}>"

class Disciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(100), nullable=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)  # Relacionamento com professor

    # Relacionamento muitos-para-muitos com a Turma
    turmas = db.relationship(
        'Turma',
        secondary=turma_disciplina,
        back_populates='disciplinas'
    )

    def __repr__(self):
        return f"<Disciplina {self.nome}>"

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    # Relacionamento muitos-para-muitos com a Disciplina
    disciplinas = db.relationship(
        'Disciplina',
        secondary=turma_disciplina,
        back_populates='turmas'
    )

    def __repr__(self):
        return f"<Turma {self.nome}>"

class Horario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dia_semana = db.Column(db.String(20), nullable=False)  # Ex: 'Segunda-feira', 'Terça-feira', etc.
    hora_inicio = db.Column(db.Time, nullable=False)  # Hora de início da aula
    hora_fim = db.Column(db.Time, nullable=False)  # Hora de término da aula
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)  # Relacionamento com a Turma
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'), nullable=False)  # Relacionamento com a Disciplina
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)  # Relacionamento com o Professor

    turma = db.relationship('Turma', backref=db.backref('horarios', lazy=True))
    disciplina = db.relationship('Disciplina', backref=db.backref('horarios', lazy=True))
    professor = db.relationship('Professor', backref=db.backref('horarios', lazy=True))

    def __repr__(self):
        return f"<Horario {self.dia_semana} - {self.hora_inicio} - {self.hora_fim}>"
