"""
Sustentabilidade Agrónoma — Módulo de Base de Dados (SQLite)
Gestão de agricultores, actividades e preferências com persistência local.
"""

import sqlite3
import os
import hashlib
import uuid
from datetime import datetime

# Caminho da base de dados no mesmo directório do projecto
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'sustentabilidade.db')


def _get_connection():
    """Cria conexão com a base de dados SQLite e garante que o directório existe."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def inicializar_bd():
    """Cria as tabelas do sistema caso ainda não existam."""
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS agricultores (
            id TEXT PRIMARY KEY,
            nome_completo TEXT NOT NULL,
            nome_machamba TEXT NOT NULL,
            provincia TEXT NOT NULL,
            distrito TEXT,
            telefone TEXT UNIQUE NOT NULL,
            email TEXT,
            senha_hash TEXT NOT NULL,
            cultura_principal TEXT,
            area_hectares REAL DEFAULT 0,
            latitude REAL,
            longitude REAL,
            data_registo TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS actividades (
            id TEXT PRIMARY KEY,
            agricultor_id TEXT NOT NULL,
            tipo TEXT NOT NULL,
            data TEXT NOT NULL,
            hora_inicio TEXT,
            hora_fim TEXT,
            parcela TEXT,
            quantidade_agua_litros REAL DEFAULT 0,
            observacoes TEXT,
            estado TEXT DEFAULT 'Pendente',
            data_criacao TEXT NOT NULL,
            FOREIGN KEY (agricultor_id) REFERENCES agricultores(id)
        );
    """)

    conn.commit()
    conn.close()


# ─── Funções de Autenticação ───

def hash_senha(senha: str) -> str:
    """Gera hash SHA-256 da senha com salt fixo do sistema."""
    salt = "sustentabilidade_agronoma_mz_2026"
    return hashlib.sha256(f"{salt}:{senha}".encode('utf-8')).hexdigest()


def registar_agricultor(dados: dict) -> tuple[bool, str]:
    """
    Regista um novo agricultor na base de dados.
    Retorna (sucesso: bool, mensagem: str).
    """
    conn = _get_connection()
    cursor = conn.cursor()

    try:
        # Verificar se o telefone já existe
        cursor.execute("SELECT id FROM agricultores WHERE telefone = ?", (dados['telefone'],))
        if cursor.fetchone():
            return False, "Este número de telefone já está registado no sistema."

        agricultor_id = f"AGR-{uuid.uuid4().hex[:8].upper()}"
        agora = datetime.now().isoformat()

        cursor.execute("""
            INSERT INTO agricultores (id, nome_completo, nome_machamba, provincia, distrito,
                                      telefone, email, senha_hash, cultura_principal,
                                      area_hectares, latitude, longitude, data_registo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            agricultor_id,
            dados['nome_completo'],
            dados['nome_machamba'],
            dados['provincia'],
            dados.get('distrito', ''),
            dados['telefone'],
            dados.get('email', ''),
            hash_senha(dados['senha']),
            dados.get('cultura_principal', ''),
            dados.get('area_hectares', 0),
            dados.get('latitude'),
            dados.get('longitude'),
            agora
        ))

        conn.commit()
        return True, f"Agricultor registado com sucesso! ID: {agricultor_id}"

    except Exception as e:
        return False, f"Erro ao registar: {str(e)}"
    finally:
        conn.close()


def autenticar(telefone: str, senha: str) -> dict | None:
    """
    Autentica um agricultor pelo telefone e senha.
    Retorna os dados do agricultor ou None se falhar.
    """
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM agricultores WHERE telefone = ? AND senha_hash = ?",
        (telefone, hash_senha(senha))
    )

    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None


def obter_agricultor(agricultor_id: str) -> dict | None:
    """Obtém dados de um agricultor pelo ID."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agricultores WHERE id = ?", (agricultor_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def actualizar_agricultor(agricultor_id: str, dados: dict) -> bool:
    """Actualiza os dados de um agricultor."""
    conn = _get_connection()
    cursor = conn.cursor()

    campos = []
    valores = []
    for chave, valor in dados.items():
        if chave not in ('id', 'data_registo'):
            campos.append(f"{chave} = ?")
            valores.append(valor)

    valores.append(agricultor_id)

    try:
        cursor.execute(f"UPDATE agricultores SET {', '.join(campos)} WHERE id = ?", valores)
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def redefinir_senha(telefone: str, nome_machamba: str, nova_senha: str) -> tuple[bool, str]:
    """
    Recupera e redefine a senha do agricultor validando o telefone e o nome da machamba.
    Retorna (sucesso: bool, mensagem: str).
    """
    conn = _get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, nome_machamba FROM agricultores WHERE telefone = ?",
            (telefone.strip(),)
        )
        row = cursor.fetchone()
        if not row:
            return False, "Não foi encontrada nenhuma conta associada a este número de telefone."

        if row['nome_machamba'].strip().lower() != nome_machamba.strip().lower():
            return False, "O nome da machamba informado não corresponde ao registo deste telefone."

        cursor.execute(
            "UPDATE agricultores SET senha_hash = ? WHERE id = ?",
            (hash_senha(nova_senha), row['id'])
        )
        conn.commit()
        return True, "Senha redefinida com sucesso! Já pode entrar na sua conta com a nova senha."
    except Exception as e:
        return False, f"Erro ao redefinir senha: {str(e)}"
    finally:
        conn.close()


# ─── Funções de Actividades ───

def registar_actividade(dados: dict) -> tuple[bool, str]:
    """Regista uma nova actividade agrícola."""
    conn = _get_connection()
    cursor = conn.cursor()

    try:
        act_id = f"ACT-{uuid.uuid4().hex[:8].upper()}"
        agora = datetime.now().isoformat()

        cursor.execute("""
            INSERT INTO actividades (id, agricultor_id, tipo, data, hora_inicio, hora_fim,
                                     parcela, quantidade_agua_litros, observacoes, estado, data_criacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            act_id,
            dados['agricultor_id'],
            dados['tipo'],
            dados['data'],
            dados.get('hora_inicio', ''),
            dados.get('hora_fim', ''),
            dados.get('parcela', ''),
            dados.get('quantidade_agua_litros', 0),
            dados.get('observacoes', ''),
            dados.get('estado', 'Concluída'),
            agora
        ))

        conn.commit()
        return True, f"Actividade registada! ID: {act_id}"
    except Exception as e:
        return False, f"Erro: {str(e)}"
    finally:
        conn.close()


def obter_actividades(agricultor_id: str, filtros: dict = None) -> list[dict]:
    """
    Obtém actividades de um agricultor com filtros opcionais.
    filtros pode conter: tipo, estado, data_inicio, data_fim
    """
    conn = _get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM actividades WHERE agricultor_id = ?"
    params = [agricultor_id]

    if filtros:
        if filtros.get('tipo') and filtros['tipo'] != 'Todos':
            query += " AND tipo = ?"
            params.append(filtros['tipo'])
        if filtros.get('estado') and filtros['estado'] != 'Todos':
            query += " AND estado = ?"
            params.append(filtros['estado'])
        if filtros.get('data_inicio'):
            query += " AND data >= ?"
            params.append(filtros['data_inicio'])
        if filtros.get('data_fim'):
            query += " AND data <= ?"
            params.append(filtros['data_fim'])

    query += " ORDER BY data DESC, hora_inicio DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(r) for r in rows]


def actualizar_actividade(act_id: str, dados: dict) -> bool:
    """Actualiza uma actividade existente."""
    conn = _get_connection()
    cursor = conn.cursor()

    campos = []
    valores = []
    for chave, valor in dados.items():
        if chave not in ('id', 'agricultor_id', 'data_criacao'):
            campos.append(f"{chave} = ?")
            valores.append(valor)

    valores.append(act_id)

    try:
        cursor.execute(f"UPDATE actividades SET {', '.join(campos)} WHERE id = ?", valores)
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def apagar_actividade(act_id: str) -> bool:
    """Remove uma actividade pelo ID."""
    conn = _get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM actividades WHERE id = ?", (act_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()


def contar_irrigacoes_hoje(agricultor_id: str) -> int:
    """Conta irrigações concluídas hoje."""
    hoje = datetime.now().strftime('%Y-%m-%d')
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM actividades WHERE agricultor_id = ? AND tipo = 'Irrigação' AND data = ? AND estado = 'Concluída'",
        (agricultor_id, hoje)
    )
    count = cursor.fetchone()[0]
    conn.close()
    return count


def calcular_agua_total(agricultor_id: str) -> float:
    """Calcula o total de água utilizada (litros) por um agricultor."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COALESCE(SUM(quantidade_agua_litros), 0) FROM actividades WHERE agricultor_id = ? AND estado = 'Concluída'",
        (agricultor_id,)
    )
    total = cursor.fetchone()[0]
    conn.close()
    return total


def calcular_streak_irrigacao(agricultor_id: str) -> int:
    """Calcula dias consecutivos com pelo menos uma irrigação concluída."""
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT data FROM actividades
        WHERE agricultor_id = ? AND tipo = 'Irrigação' AND estado = 'Concluída'
        ORDER BY data DESC
    """, (agricultor_id,))

    datas = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not datas:
        return 0

    streak = 0
    from datetime import timedelta
    dia_esperado = datetime.now().date()

    for data_str in datas:
        data = datetime.strptime(data_str, '%Y-%m-%d').date()
        if data == dia_esperado:
            streak += 1
            dia_esperado -= timedelta(days=1)
        elif data == dia_esperado - timedelta(days=1):
            # Permite que o dia actual ainda não tenha irrigação
            dia_esperado = data
            streak += 1
            dia_esperado -= timedelta(days=1)
        else:
            break

    return streak
