
import sqlite3

from pathlib import Path


# Caminho do banco de dados.
CAMINHO_BANCO = (
    Path(__file__).resolve().parent.parent
    / "banco_de_dados"
    / "score.db"
)



def inicializar_banco():

    CAMINHO_BANCO.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    conexao = sqlite3.connect(CAMINHO_BANCO)

    cursor = conexao.cursor()

    # Histórico de partidas vencidas.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_jogador TEXT NOT NULL,
            score INTEGER NOT NULL,
            data_vitoria TEXT NOT NULL
        )
    """)

    # Histórico de sessões.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_jogador TEXT NOT NULL,
            score_total INTEGER NOT NULL,
            quantidade_vitorias INTEGER NOT NULL,
            media_score REAL NOT NULL,
            data_inicio TEXT NOT NULL,
            data_fim TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()



def registrar_vitoria(nome_jogador, score):

    from datetime import datetime

    conexao = sqlite3.connect(CAMINHO_BANCO)

    cursor = conexao.cursor()

    data_vitoria = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )

    cursor.execute("""
        INSERT INTO partidas (
            nome_jogador,
            score,
            data_vitoria
        )
        VALUES (?, ?, ?)
    """, (
        nome_jogador,
        score,
        data_vitoria
    ))

    conexao.commit()
    conexao.close()


def registrar_sessao(
    nome_jogador,
    score_total,
    quantidade_vitorias,
    data_inicio
):

    from datetime import datetime

    # Não registra sessões sem nenhuma vitória.
    if quantidade_vitorias <= 0:
        return

    media_score = score_total / quantidade_vitorias

    data_fim = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )

    conexao = sqlite3.connect(CAMINHO_BANCO)

    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO sessoes (
            nome_jogador,
            score_total,
            quantidade_vitorias,
            media_score,
            data_inicio,
            data_fim
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        nome_jogador,
        score_total,
        quantidade_vitorias,
        media_score,
        data_inicio,
        data_fim
    ))

    conexao.commit()
    conexao.close()


def buscar_melhores_partidas():

    conexao = sqlite3.connect(CAMINHO_BANCO)

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT nome_jogador, score, data_vitoria
        FROM partidas
        ORDER BY score DESC, id ASC
        LIMIT 10
    """)

    resultados = cursor.fetchall()

    conexao.close()

    return resultados


def buscar_melhores_sessoes():

    conexao = sqlite3.connect(CAMINHO_BANCO)

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            nome_jogador,
            score_total,
            quantidade_vitorias,
            media_score,
            data_inicio,
            data_fim
        FROM sessoes
        ORDER BY score_total DESC, id ASC
        LIMIT 10
    """)

    resultados = cursor.fetchall()

    conexao.close()

    return resultados


