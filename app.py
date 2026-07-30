import streamlit as st
import pandas as pd
import psycopg2

# URL de conexão com o Supabase (Porta 6543 - Session Pooler)
DB_URL = "postgresql://postgres.dcsgnjfhjdfcgagqyrru:senhadalanchonete@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"

st.set_page_config(page_title="Lanchonete Universitária", page_icon="🍔", layout="centered")

st.title("🍔 Lanchonete Universitária — Sistema em Tempo Real")
st.write("Interface integrada com Supabase.")

# ==========================================
# PARTE 1: NOVO PEDIDO
# ==========================================
st.subheader("➕ Novo Pedido")
with st.form("form_pedido", clear_on_submit=True):
    item_pedido = st.text_input("Nome do Lanche / Item (ex: X-Burguer)")
    id_cliente = st.number_input("ID do Cliente (Ex: 1 ou 2)", min_value=1, step=1, format="%d")
    enviar = st.form_submit_button("Cadastrar Pedido")

    if enviar:
        if item_pedido.strip() == "":
            st.warning("⚠️ Digite o item do pedido.")
        else:
            try:
                conn = psycopg2.connect(DB_URL)
                conn.autocommit = True
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Pedido (item, cliente_id) VALUES (%s, %s);", (item_pedido, id_cliente))
                cursor.close()
                conn.close()
                st.success(f"✅ Pedido '{item_pedido}' cadastrado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

st.divider()

# ==========================================
# PARTE 2: RELATÓRIO EM FORMATO DE CARDS
# ==========================================
col1, col2 = st.columns([0.7, 0.3])
with col1:
    st.subheader("📋 Painel de Pedidos Ativos")
with col2:
    if st.button("🔄 Atualizar"):
        st.rerun()

try:
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = True
    query = 'SELECT Cliente.nome AS "Cliente", Pedido.item AS "Produto Pedido" FROM Pedido JOIN Cliente ON Pedido.cliente_id = Cliente.id'
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        st.info("Nenhum pedido cadastrado no momento.")
    else:
        # Exibe os dados em formato de lista visual / cards em vez de tabela crua
        for index, row in df.iterrows():
            with st.container(border=True):
                c_esq, c_dir = st.columns([0.6, 0.4])
                with c_esq:
                    st.markdown(f"**👤 Cliente:** `{row['Cliente']}`")
                with c_dir:
                    st.markdown(f"🍔 **Item:** `{row['Produto Pedido']}`")

except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
