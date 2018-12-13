from flask import Flask, render_template, request, url_for, redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

class Pessoa(db.Model):

    __tablename__ = 'pessoa'

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)

    def __init__(self, nome):
        self.nome = nome

db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")

        if nome:
            p = Pessoa(nome)
            db.session.add(p)
            db.session.commit()

    return redirect(url_for("index"))

@app.route("/lista")
def lista():
    pessoas = Pessoa.query.all()
    return render_template("lista.html", pessoas=pessoas)

@app.route("/excluir/<int:id>")
def excluir(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()

    db.session.delete(pessoa)
    db.session.commit()

    pessoas = Pessoa.query.all()

    return render_template("lista.html", pessoas=pessoas)

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()

    if request.method == "POST":
        nome = request.form.get("nome")

        if nome:
            pessoa.nome = nome

            db.session.commit()

            return redirect(url_for("lista"))

    return render_template("editar.html", pessoa=pessoa)


if __name__ == '__main__':
    app.run(debug=True)