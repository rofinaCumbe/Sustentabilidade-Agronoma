"""
Script de Migração e Sincronização Completa para o MongoDB Atlas (sustentabilidadedb).
Transfere todos os agricultores, actividades, cidades de Moçambique e catálogos do sistema.
"""

from utils.database import inicializar_bd, get_mongo_db, MONGODB_URI, DB_NAME


def executar_migracao():
    print(f"A ligar ao cluster MongoDB Atlas (Base de Dados: {DB_NAME})...")
    inicializar_bd()
    db = get_mongo_db()
    if db is None:
        print(
            "\n[ATENÇÃO] O cluster MongoDB Atlas recusou o handshake TLS (TLSV1_ALERT_INTERNAL_ERROR).\n"
            "Isto acontece quando o IP actual ainda não está autorizado no painel do MongoDB Atlas.\n"
            "Para autorizar no MongoDB Atlas:\n"
            "  1. Aceda a https://cloud.mongodb.com -> Security -> Network Access\n"
            "  2. Clique em '+ ADD IP ADDRESS'\n"
            "  3. Clique em 'ALLOW ACCESS FROM ANYWHERE' (0.0.0.0/0) ou adicione o seu IP actual (41.220.201.132)\n"
            "  4. Clique em 'Confirm' e volte a executar: python migrar_mongodb.py"
        )
        return

    print("\n[SUCESSO] Ligação estabelecida e todos os dados foram inseridos no MongoDB Atlas!")
    print(f"  - Colecções criadas: {db.list_collection_names()}")
    print(f"  - Agricultores migrados: {db.agricultores.count_documents({})}")
    print(f"  - Actividades migradas: {db.actividades.count_documents({})}")
    print(f"  - Cidades de Moçambique: {db.cidades_mocambique.count_documents({})}")
    print(f"  - Configurações/Catálogos do Sistema: {db.configuracoes_sistema.count_documents({})}")


if __name__ == "__main__":
    executar_migracao()
