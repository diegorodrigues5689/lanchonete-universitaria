import streamlit as st
import pandas as pd
import psycopg2

# URL de conexão com o Supabase (Porta 6543 - Session Pooler)
DB_URL = "postgresql://postgres.kmfhqphghqyhhbisltca:novalanchonete@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"

st.title("🍔 Lanchonete Universitária")
st.write("Painel de Visualização - Integrado com Supabase.")

st.divider()
st.subheader("📋 Relatório de Pedidos em Tempo Real")

# Botão para atualizar os dados da tela
if st.button("🔄 Atualizar Lista"):
    st.rerun()

try:
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = True
    
    # Consulta SQL fazendo o JOIN entre Pedido e Cliente
    query = 'SELECT Cliente.nome AS "Cliente", Pedido.item AS "Produto Pedido" FROM Pedido JOIN Cliente ON Pedido.id_cliente = Cliente.id_cliente'
    
    df = pd.read_sql(query, conn)
    conn.close()
    
    # Exibe a tabela de forma interativa
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
