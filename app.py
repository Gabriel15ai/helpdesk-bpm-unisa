import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "helpdesk-bpm-demo")
DB_PATH = os.environ.get("DATABASE_PATH", "chamados.db")

CATEGORIAS = {
    "Hardware": "Suporte de TI",
    "Software": "Suporte de TI",
    "Acesso e senha": "Suporte de TI",
    "Administrativo": "Setor Administrativo",
    "Financeiro": "Setor Financeiro",
    "Outros": "Central de Atendimento",
}

def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def inicializar_banco():
    with conectar() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chamados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                solicitante TEXT NOT NULL,
                setor TEXT NOT NULL,
                categoria TEXT NOT NULL,
                prioridade TEXT NOT NULL,
                descricao TEXT NOT NULL,
                responsavel TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Aberto',
                solucao TEXT DEFAULT '',
                criado_em TEXT NOT NULL,
                atualizado_em TEXT NOT NULL
            )
        """)

@app.route("/")
def index():
    filtro = request.args.get("status", "")
    busca = request.args.get("q", "").strip()
    sql = "SELECT * FROM chamados WHERE 1=1"
    params = []
    if filtro in ("Aberto", "Em andamento", "Concluído"):
        sql += " AND status = ?"
        params.append(filtro)
    if busca:
        sql += " AND (CAST(id AS TEXT) LIKE ? OR solicitante LIKE ? OR descricao LIKE ? OR categoria LIKE ?)"
        params.extend([f"%{busca}%"] * 4)
    sql += " ORDER BY id DESC"
    with conectar() as conn:
        chamados = conn.execute(sql, params).fetchall()
        totais = {
            "total": conn.execute("SELECT COUNT(*) FROM chamados").fetchone()[0],
            "abertos": conn.execute("SELECT COUNT(*) FROM chamados WHERE status='Aberto'").fetchone()[0],
            "andamento": conn.execute("SELECT COUNT(*) FROM chamados WHERE status='Em andamento'").fetchone()[0],
            "concluidos": conn.execute("SELECT COUNT(*) FROM chamados WHERE status='Concluído'").fetchone()[0],
        }
    return render_template("index.html", chamados=chamados, totais=totais,
                           filtro=filtro, busca=busca)

@app.route("/novo", methods=["POST"])
def novo():
    solicitante = request.form.get("solicitante", "").strip()
    setor = request.form.get("setor", "").strip()
    categoria = request.form.get("categoria", "")
    prioridade = request.form.get("prioridade", "Média")
    descricao = request.form.get("descricao", "").strip()
    if not all([solicitante, setor, categoria, descricao]):
        flash("Preencha todos os campos obrigatórios.", "erro")
        return redirect(url_for("index"))
    responsavel = CATEGORIAS.get(categoria, "Central de Atendimento")
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    with conectar() as conn:
        cur = conn.execute("""
            INSERT INTO chamados
            (solicitante, setor, categoria, prioridade, descricao, responsavel,
             status, criado_em, atualizado_em)
            VALUES (?, ?, ?, ?, ?, ?, 'Aberto', ?, ?)
        """, (solicitante, setor, categoria, prioridade, descricao,
              responsavel, agora, agora))
        numero = cur.lastrowid
    flash(f"Chamado #{numero} registrado e encaminhado para {responsavel}.", "sucesso")
    return redirect(url_for("index"))

@app.route("/atualizar/<int:chamado_id>", methods=["POST"])
def atualizar(chamado_id):
    status = request.form.get("status", "Aberto")
    solucao = request.form.get("solucao", "").strip()
    if status not in ("Aberto", "Em andamento", "Concluído"):
        flash("Status inválido.", "erro")
        return redirect(url_for("index"))
    if status == "Concluído" and not solucao:
        flash("Informe a solução antes de concluir o chamado.", "erro")
        return redirect(url_for("index"))
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    with conectar() as conn:
        conn.execute("""
            UPDATE chamados SET status=?, solucao=?, atualizado_em=? WHERE id=?
        """, (status, solucao, agora, chamado_id))
    flash(f"Chamado #{chamado_id} atualizado.", "sucesso")
    return redirect(url_for("index"))

@app.route("/excluir/<int:chamado_id>", methods=["POST"])
def excluir(chamado_id):
    with conectar() as conn:
        conn.execute("DELETE FROM chamados WHERE id=?", (chamado_id,))
    flash(f"Chamado #{chamado_id} excluído.", "sucesso")
    return redirect(url_for("index"))

inicializar_banco()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
