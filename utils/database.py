"""
Sustentabilidade Agrónoma — Módulo de Base de Dados (MongoDB Atlas + Migração SQLite)
Gestão de agricultores, actividades, cidades e configurações no MongoDB Atlas (sustentabilidadedb).
"""

import sqlite3
import os
import hashlib
import uuid
import tempfile
from datetime import datetime, timedelta
from pymongo import MongoClient, ASCENDING, DESCENDING

# URI de ligação ao MongoDB Atlas (sustentabilidadedb)
MONGODB_URI = os.environ.get(
    "MONGODB_URI",
    "mongodb+srv://rofinacumbe01_db_user:Z9NKPFKwtpAiln2N@cluster0.kjp90za.mongodb.net/sustentabilidadedb?appName=Cluster0"
)
DB_NAME = "sustentabilidadedb"

# Caminho da base de dados SQLite local (usada para migração inicial e espelho local)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'sustentabilidade.db')

_mongo_client = None
_mongo_db = None
_bd_inicializada = False
_ultimo_erro_ts = 0.0


def get_mongo_db():
    """
    Retorna a instância da base de dados MongoDB Atlas (singleton).
    Se a ligação falhar (ex: IP ainda não autorizado no Atlas Network Access),
    faz fallback imediato para SQLite local e volta a tentar após 30 segundos.
    """
    global _mongo_client, _mongo_db, _ultimo_erro_ts
    if _mongo_db is not None:
        return _mongo_db

    agora_ts = datetime.now().timestamp()
    if agora_ts - _ultimo_erro_ts < 30:
        return None

    try:
        client = MongoClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=2500,
            connectTimeoutMS=2500,
            socketTimeoutMS=3000,
            maxPoolSize=15,
            minPoolSize=1,
            maxIdleTimeMS=45000,
            tlsAllowInvalidCertificates=True,
        )
        client.admin.command("ping")
        _mongo_client = client
        _mongo_db = client[DB_NAME]
        return _mongo_db
    except Exception:
        _ultimo_erro_ts = agora_ts
        return None


def _get_sqlite_connection():
    """Cria conexão com a base de dados SQLite local, garantindo escrita em ambientes Serverless/Vercel (usando /tmp)."""
    global DB_PATH
    try:
        data_dir = os.path.dirname(DB_PATH)
        os.makedirs(data_dir, exist_ok=True)
        # Testar escrita
        test_file = os.path.join(data_dir, '.write_check')
        with open(test_file, 'w') as f:
            f.write('1')
        if os.path.exists(test_file):
            os.remove(test_file)
        conn = sqlite3.connect(DB_PATH)
    except Exception:
        # Se o filesystem for read-only (ex: /var/task no Vercel), usar diretório temporário do sistema
        tmp_db = os.path.join(tempfile.gettempdir(), 'sustentabilidade.db')
        DB_PATH = tmp_db
        conn = sqlite3.connect(tmp_db)

    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode=WAL")
    except Exception:
        pass
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def inicializar_bd():
    """
    Inicializa as colecções e índices no MongoDB Atlas (sustentabilidadedb)
    e migra automaticamente todos os dados locais (SQLite + dados de referência do sistema).
    """
    global _bd_inicializada
    if _bd_inicializada:
        return

    # 1. Garantir tabelas SQLite locais de forma segura
    agricultores_sqlite = []
    actividades_sqlite = []
    try:
        conn = _get_sqlite_connection()
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
                idioma TEXT DEFAULT 'pt',
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
        try:
            cursor.execute("ALTER TABLE agricultores ADD COLUMN idioma TEXT DEFAULT 'pt'")
        except sqlite3.OperationalError:
            pass
        conn.commit()

        # Ler registos existentes no SQLite se existirem
        cursor.execute("SELECT * FROM agricultores")
        agricultores_sqlite = [dict(r) for r in cursor.fetchall()]

        cursor.execute("SELECT * FROM actividades")
        actividades_sqlite = [dict(r) for r in cursor.fetchall()]
        conn.close()
    except Exception as e:
        pass

    # 2. Inicializar e popular MongoDB Atlas
    db = get_mongo_db()
    if db is not None:
        try:
            # Criar índices únicos e de pesquisa
            db.agricultores.create_index([("id", ASCENDING)], unique=True)
            db.agricultores.create_index([("telefone", ASCENDING)], unique=True)
            db.actividades.create_index([("id", ASCENDING)], unique=True)
            db.actividades.create_index([("agricultor_id", ASCENDING), ("data", DESCENDING)])
            db.cidades_mocambique.create_index([("nome", ASCENDING)], unique=True)
            db.configuracoes_sistema.create_index([("chave", ASCENDING)], unique=True)

            # Migrar agricultores do SQLite para o MongoDB
            for agr in agricultores_sqlite:
                db.agricultores.update_one(
                    {"id": agr["id"]},
                    {"$set": agr},
                    upsert=True
                )

            # Migrar actividades do SQLite para o MongoDB
            for act in actividades_sqlite:
                db.actividades.update_one(
                    {"id": act["id"]},
                    {"$set": act},
                    upsert=True
                )

            # Guardar cidades de Moçambique na colecção cidades_mocambique
            from utils.weather import CIDADES_MOCAMBIQUE
            for nome_cidade, info in CIDADES_MOCAMBIQUE.items():
                doc_cidade = {
                    "nome": nome_cidade,
                    "provincia": info["provincia"],
                    "lat": info["lat"],
                    "lon": info["lon"],
                }
                db.cidades_mocambique.update_one(
                    {"nome": nome_cidade},
                    {"$set": doc_cidade},
                    upsert=True
                )

            # Guardar configurações e catálogos do sistema na colecção configuracoes_sistema
            from utils.i18n import IDIOMAS, CULTURAS_TRADUCAO, TIPOS_ACTIVIDADE_TRADUCAO
            from utils.irrigation import NIVEIS_IRRIGACAO

            db.configuracoes_sistema.update_one(
                {"chave": "idiomas_suportados"},
                {"$set": {"chave": "idiomas_suportados", "dados": IDIOMAS, "actualizado_em": datetime.now().isoformat()}},
                upsert=True
            )
            db.configuracoes_sistema.update_one(
                {"chave": "catalogo_culturas"},
                {"$set": {"chave": "catalogo_culturas", "dados": CULTURAS_TRADUCAO, "actualizado_em": datetime.now().isoformat()}},
                upsert=True
            )
            db.configuracoes_sistema.update_one(
                {"chave": "tipos_actividade"},
                {"$set": {"chave": "tipos_actividade", "dados": TIPOS_ACTIVIDADE_TRADUCAO, "actualizado_em": datetime.now().isoformat()}},
                upsert=True
            )
            db.configuracoes_sistema.update_one(
                {"chave": "niveis_irrigacao"},
                {"$set": {"chave": "niveis_irrigacao", "dados": NIVEIS_IRRIGACAO, "actualizado_em": datetime.now().isoformat()}},
                upsert=True
            )
        except Exception:
            pass

    _bd_inicializada = True


# ─── Funções de Autenticação ───

def hash_senha(senha: str) -> str:
    """Gera hash SHA-256 da senha com salt fixo do sistema."""
    salt = "sustentabilidade_agronoma_mz_2026"
    return hashlib.sha256(f"{salt}:{senha}".encode('utf-8')).hexdigest()


def registar_agricultor(dados: dict) -> tuple[bool, str]:
    """
    Regista um novo agricultor no MongoDB Atlas (e no espelho SQLite local).
    Retorna (sucesso: bool, mensagem: str).
    """
    telefone = dados['telefone'].strip()
    agricultor_id = f"AGR-{uuid.uuid4().hex[:8].upper()}"
    agora = datetime.now().isoformat()

    doc_agricultor = {
        'id': agricultor_id,
        'nome_completo': dados['nome_completo'],
        'nome_machamba': dados['nome_machamba'],
        'provincia': dados['provincia'],
        'distrito': dados.get('distrito', ''),
        'telefone': telefone,
        'email': dados.get('email', ''),
        'senha_hash': hash_senha(dados['senha']),
        'cultura_principal': dados.get('cultura_principal', ''),
        'area_hectares': float(dados.get('area_hectares', 0)),
        'latitude': dados.get('latitude'),
        'longitude': dados.get('longitude'),
        'idioma': dados.get('idioma', 'pt'),
        'data_registo': agora,
    }

    db = get_mongo_db()
    if db is not None:
        try:
            if db.agricultores.find_one({"telefone": telefone}):
                return False, "Este número de telefone já está registado no sistema."
            db.agricultores.insert_one(doc_agricultor.copy())
        except Exception as e:
            return False, f"Erro ao registar no MongoDB: {str(e)}"

    # Espelhar também no SQLite local
    try:
        conn = _get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO agricultores (id, nome_completo, nome_machamba, provincia, distrito,
                                      telefone, email, senha_hash, cultura_principal,
                                      area_hectares, latitude, longitude, idioma, data_registo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            doc_agricultor['id'],
            doc_agricultor['nome_completo'],
            doc_agricultor['nome_machamba'],
            doc_agricultor['provincia'],
            doc_agricultor['distrito'],
            doc_agricultor['telefone'],
            doc_agricultor['email'],
            doc_agricultor['senha_hash'],
            doc_agricultor['cultura_principal'],
            doc_agricultor['area_hectares'],
            doc_agricultor['latitude'],
            doc_agricultor['longitude'],
            doc_agricultor['idioma'],
            doc_agricultor['data_registo']
        ))
        conn.commit()
        conn.close()
    except Exception:
        pass

    return True, f"Agricultor registado com sucesso! ID: {agricultor_id}"


def autenticar(telefone: str, senha: str) -> dict | None:
    """
    Autentica um agricultor pelo telefone e senha no MongoDB Atlas.
    Retorna os dados do agricultor ou None se falhar.
    """
    senha_h = hash_senha(senha)
    db = get_mongo_db()
    if db is not None:
        try:
            doc = db.agricultores.find_one(
                {"telefone": telefone.strip(), "senha_hash": senha_h},
                {"_id": 0}
            )
            if doc:
                return doc
        except Exception:
            pass

    conn = _get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM agricultores WHERE telefone = ? AND senha_hash = ?",
        (telefone.strip(), senha_h)
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def obter_agricultor(agricultor_id: str) -> dict | None:
    """Obtém dados de um agricultor pelo ID a partir do MongoDB Atlas."""
    db = get_mongo_db()
    if db is not None:
        try:
            doc = db.agricultores.find_one({"id": agricultor_id}, {"_id": 0})
            if doc:
                return doc
        except Exception:
            pass

    conn = _get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agricultores WHERE id = ?", (agricultor_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def actualizar_agricultor(agricultor_id: str, dados: dict) -> bool:
    """Actualiza os dados de um agricultor no MongoDB Atlas e no espelho local."""
    campos_update = {k: v for k, v in dados.items() if k not in ('id', 'data_registo', '_id')}
    if not campos_update:
        return True

    sucesso_mongo = False
    db = get_mongo_db()
    if db is not None:
        try:
            res = db.agricultores.update_one(
                {"id": agricultor_id},
                {"$set": campos_update}
            )
            sucesso_mongo = res.matched_count > 0
        except Exception:
            pass

    try:
        conn = _get_sqlite_connection()
        cursor = conn.cursor()
        campos = [f"{k} = ?" for k in campos_update.keys()]
        valores = list(campos_update.values()) + [agricultor_id]
        cursor.execute(f"UPDATE agricultores SET {', '.join(campos)} WHERE id = ?", valores)
        conn.commit()
        conn.close()
        return True
    except Exception:
        return sucesso_mongo


def redefinir_senha(telefone: str, nome_machamba: str, nova_senha: str) -> tuple[bool, str]:
    """
    Recupera e redefine a senha do agricultor validando o telefone e o nome da machamba.
    """
    tel_limpo = telefone.strip()
    nova_hash = hash_senha(nova_senha)

    db = get_mongo_db()
    if db is not None:
        try:
            doc = db.agricultores.find_one({"telefone": tel_limpo}, {"_id": 0})
            if not doc:
                return False, "Não foi encontrada nenhuma conta associada a este número de telefone."
            if doc['nome_machamba'].strip().lower() != nome_machamba.strip().lower():
                return False, "O nome da machamba informado não corresponde ao registo deste telefone."

            db.agricultores.update_one(
                {"id": doc["id"]},
                {"$set": {"senha_hash": nova_hash}}
            )

            # Actualizar também SQLite local
            try:
                conn = _get_sqlite_connection()
                conn.execute("UPDATE agricultores SET senha_hash = ? WHERE id = ?", (nova_hash, doc["id"]))
                conn.commit()
                conn.close()
            except Exception:
                pass

            return True, "Senha redefinida com sucesso! Já pode entrar na sua conta com a nova senha."
        except Exception as e:
            return False, f"Erro ao redefinir senha: {str(e)}"

    conn = _get_sqlite_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, nome_machamba FROM agricultores WHERE telefone = ?", (tel_limpo,))
        row = cursor.fetchone()
        if not row:
            return False, "Não foi encontrada nenhuma conta associada a este número de telefone."
        if row['nome_machamba'].strip().lower() != nome_machamba.strip().lower():
            return False, "O nome da machamba informado não corresponde ao registo deste telefone."
        cursor.execute("UPDATE agricultores SET senha_hash = ? WHERE id = ?", (nova_hash, row['id']))
        conn.commit()
        return True, "Senha redefinida com sucesso! Já pode entrar na sua conta com a nova senha."
    except Exception as e:
        return False, f"Erro ao redefinir senha: {str(e)}"
    finally:
        conn.close()


# ─── Funções de Actividades ───

def registar_actividade(dados: dict) -> tuple[bool, str]:
    """Regista uma nova actividade agrícola no MongoDB Atlas (e no espelho SQLite)."""
    act_id = f"ACT-{uuid.uuid4().hex[:8].upper()}"
    agora = datetime.now().isoformat()

    doc_act = {
        'id': act_id,
        'agricultor_id': dados['agricultor_id'],
        'tipo': dados['tipo'],
        'data': dados['data'],
        'hora_inicio': dados.get('hora_inicio', ''),
        'hora_fim': dados.get('hora_fim', ''),
        'parcela': dados.get('parcela', ''),
        'quantidade_agua_litros': float(dados.get('quantidade_agua_litros', 0)),
        'observacoes': dados.get('observacoes', ''),
        'estado': dados.get('estado', 'Concluída'),
        'data_criacao': agora,
    }

    db = get_mongo_db()
    if db is not None:
        try:
            db.actividades.insert_one(doc_act.copy())
        except Exception as e:
            return False, f"Erro no MongoDB: {str(e)}"

    try:
        conn = _get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO actividades (id, agricultor_id, tipo, data, hora_inicio, hora_fim,
                                     parcela, quantidade_agua_litros, observacoes, estado, data_criacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            doc_act['id'],
            doc_act['agricultor_id'],
            doc_act['tipo'],
            doc_act['data'],
            doc_act['hora_inicio'],
            doc_act['hora_fim'],
            doc_act['parcela'],
            doc_act['quantidade_agua_litros'],
            doc_act['observacoes'],
            doc_act['estado'],
            doc_act['data_criacao']
        ))
        conn.commit()
        conn.close()
    except Exception:
        pass

    return True, f"Actividade registada! ID: {act_id}"


def obter_actividades(agricultor_id: str, filtros: dict = None) -> list[dict]:
    """
    Obtém actividades de um agricultor com filtros opcionais a partir do MongoDB Atlas.
    """
    db = get_mongo_db()
    if db is not None:
        try:
            query_mongo = {"agricultor_id": agricultor_id}
            if filtros:
                if filtros.get('tipo') and filtros['tipo'] != 'Todos':
                    query_mongo['tipo'] = filtros['tipo']
                if filtros.get('estado') and filtros['estado'] != 'Todos':
                    query_mongo['estado'] = filtros['estado']
                if filtros.get('data_inicio') or filtros.get('data_fim'):
                    cond_data = {}
                    if filtros.get('data_inicio'):
                        cond_data['$gte'] = filtros['data_inicio']
                    if filtros.get('data_fim'):
                        cond_data['$lte'] = filtros['data_fim']
                    query_mongo['data'] = cond_data

            cursor_mongo = db.actividades.find(query_mongo, {"_id": 0}).sort(
                [("data", DESCENDING), ("hora_inicio", DESCENDING)]
            )
            return list(cursor_mongo)
        except Exception:
            pass

    conn = _get_sqlite_connection()
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
    """Actualiza uma actividade existente no MongoDB Atlas e no espelho local."""
    campos_update = {k: v for k, v in dados.items() if k not in ('id', 'agricultor_id', 'data_criacao', '_id')}
    if not campos_update:
        return True

    sucesso_mongo = False
    db = get_mongo_db()
    if db is not None:
        try:
            res = db.actividades.update_one({"id": act_id}, {"$set": campos_update})
            sucesso_mongo = res.matched_count > 0
        except Exception:
            pass

    try:
        conn = _get_sqlite_connection()
        cursor = conn.cursor()
        campos = [f"{k} = ?" for k in campos_update.keys()]
        valores = list(campos_update.values()) + [act_id]
        cursor.execute(f"UPDATE actividades SET {', '.join(campos)} WHERE id = ?", valores)
        conn.commit()
        conn.close()
        return True
    except Exception:
        return sucesso_mongo


def apagar_actividade(act_id: str) -> bool:
    """Remove uma actividade pelo ID no MongoDB Atlas e no espelho local."""
    apagou_mongo = False
    db = get_mongo_db()
    if db is not None:
        try:
            res = db.actividades.delete_one({"id": act_id})
            apagou_mongo = res.deleted_count > 0
        except Exception:
            pass

    try:
        conn = _get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM actividades WHERE id = ?", (act_id,))
        conn.commit()
        apagou_sqlite = cursor.rowcount > 0
        conn.close()
        return apagou_mongo or apagou_sqlite
    except Exception:
        return apagou_mongo


def contar_irrigacoes_hoje(agricultor_id: str) -> int:
    """Conta irrigações concluídas hoje no MongoDB Atlas."""
    hoje = datetime.now().strftime('%Y-%m-%d')
    db = get_mongo_db()
    if db is not None:
        try:
            return db.actividades.count_documents({
                "agricultor_id": agricultor_id,
                "tipo": "Irrigação",
                "data": hoje,
                "estado": "Concluída",
            })
        except Exception:
            pass

    conn = _get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM actividades WHERE agricultor_id = ? AND tipo = 'Irrigação' AND data = ? AND estado = 'Concluída'",
        (agricultor_id, hoje)
    )
    count = cursor.fetchone()[0]
    conn.close()
    return count


def calcular_agua_total(agricultor_id: str) -> float:
    """Calcula o total de água utilizada (litros) por um agricultor no MongoDB Atlas."""
    db = get_mongo_db()
    if db is not None:
        try:
            pipeline = [
                {"$match": {"agricultor_id": agricultor_id, "estado": "Concluída"}},
                {"$group": {"_id": None, "total": {"$sum": "$quantidade_agua_litros"}}},
            ]
            res = list(db.actividades.aggregate(pipeline))
            return float(res[0]["total"]) if res else 0.0
        except Exception:
            pass

    conn = _get_sqlite_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COALESCE(SUM(quantidade_agua_litros), 0) FROM actividades WHERE agricultor_id = ? AND estado = 'Concluída'",
        (agricultor_id,)
    )
    total = cursor.fetchone()[0]
    conn.close()
    return float(total)


def calcular_streak_irrigacao(agricultor_id: str) -> int:
    """Calcula dias consecutivos com pelo menos uma irrigação concluída."""
    datas = []
    db = get_mongo_db()
    if db is not None:
        try:
            datas_distintas = db.actividades.distinct("data", {
                "agricultor_id": agricultor_id,
                "tipo": "Irrigação",
                "estado": "Concluída",
            })
            datas = sorted(datas_distintas, reverse=True)
        except Exception:
            datas = []

    if not datas:
        conn = _get_sqlite_connection()
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
    dia_esperado = datetime.now().date()

    for data_str in datas:
        data = datetime.strptime(data_str, '%Y-%m-%d').date()
        if data == dia_esperado:
            streak += 1
            dia_esperado -= timedelta(days=1)
        elif data == dia_esperado - timedelta(days=1):
            dia_esperado = data
            streak += 1
            dia_esperado -= timedelta(days=1)
        else:
            break

    return streak
