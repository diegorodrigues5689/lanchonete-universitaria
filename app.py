import streamlit as st
import pandas as pd
import psycopg2

# URL de conexão com o Supabase (Porta 6543 - Session Pooler)
DB_URL = "postgresql://postgres.kmfhqphghqyhhbisltca:novalanchonete@aws-0-sa-east-1.pooler.supabase.co:6543/postgres"

st.title("🍔 Lanchonete Universitária")
st.write("Interface integrada com Supabase.")

st.subheader("➕ Novo Pedido")
with st.form("form_pedido"):
    id_pedido = st.number_input("ID do Pedido (Ex: 1, 2, 3...)", min_value=1, step=1, format="%d")
    item_pedido = st.text_input("Nome do Lanche / Item (ex: X-Burguer)")
    id_cliente = st.number_input("ID do Cliente (Ex: 1 ou 2)", min_value=1, step=1, format="%d")
    enviar = st.form_submit_button("Cadastrar Pedido")

    if enviar:
        if item_pedido.strip() == "":
            st.warning("⚠️ Digite o item.")
        else:
            try:
                conn = psycopg2.connect(DB_URL)
                conn.autocommit = True
                cursor = conn.cursor()
                # Informando explicitamente o id_pedido que o usuário digitou
                cursor.execute(
                    "INSERT INTO pedido (id_pedido, item, id_cliente) VALUES (%s, %s, %s);", 
                    (id_pedido, item_pedido, id_cliente)
                )
                cursor.close()
                conn.close()
                st.success(f"✅ Pedido #{id_pedido} ('{item_pedido}') cadastrado com sucesso!")
            except Exception as e:
                st.error(f"Erro: {e}")

st.divider()
st.subheader("📋 Relatório de Pedidos em Tempo Real")
if st.button("🔄 Atualizar Lista"):
    st.rerun()

try:
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = True
    # Consulta ajustada para as letras minúsculas exatas das tabelas criadas no SQL
    query = 'SELECT cliente.nome AS "Cliente", pedido.item AS "Produto Pedido" FROM pedido JOIN cliente ON pedido.id_cliente = cliente.id_cliente'
    df = pd.read_sql(query, conn)
    conn.close()
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error(f"Erro: {e}")
