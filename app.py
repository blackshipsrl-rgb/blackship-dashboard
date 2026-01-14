import streamlit as st
import time

# ---------------------------------------------------------
# CONFIGURAZIONE PAGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Blackship Group | Dashboard",
    page_icon="🏴‍☠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# STILE VISIVO (CSS Semplice per sembrare Pro)
# ---------------------------------------------------------
st.markdown("""
<style>
    .metric-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
        text-align: center;
    }
    .stApp {
        background-color: #0e1117;
    }
    h1, h2, h3 {
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR (Colonna sinistra)
# ---------------------------------------------------------
with st.sidebar:
    st.title("🏴‍☠️ BLACKSHIP")
    st.markdown("---")
    st.write("**Benvenuto, Trader.**")
    
    account_id = st.text_input("Inserisci Account ID", value="DEMO-12345")
    
    if st.button("🔄 Aggiorna Dati"):
        with st.spinner('Connessione a Bybit in corso...'):
            time.sleep(1) # Simuliamo il tempo di caricamento
        st.success("Dati aggiornati!")
    
    st.markdown("---")
    st.info("💡 Stato Sistema: **ONLINE**")

# ---------------------------------------------------------
# CORPO PRINCIPALE (Main Dashboard)
# ---------------------------------------------------------

st.title("📊 Trading Dashboard")
st.markdown("Monitoraggio in tempo reale del tuo conto **Hybrid**.")

# SIMULIAMO DEI DATI (Presto collegheremo Bybit qui)
balance = 50000.00
equity = 51250.50
profit = equity - balance
profit_percent = (profit / balance) * 100
target = 57500.00 # Target 15%
drawdown_limit = 45000.00 # Max DD 10%

# CREIAMO 3 COLONNE PER I NUMERI
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="💰 Balance", value=f"${balance:,.2f}")

with col2:
    st.metric(label="📈 Equity (Live)", value=f"${equity:,.2f}", delta=f"{profit:,.2f} ({profit_percent:.2f}%)")

with col3:
    distance_target = target - equity
    st.metric(label="🎯 Distanza dal Target", value=f"${distance_target:,.2f}")

st.markdown("---")

# BARRA DI PROGRESSO E GRAFICO
st.subheader("Stato della Challenge")

# Calcolo progresso
progress = profit_percent / 15 # 15% è il target
if progress < 0: progress = 0
if progress > 1: progress = 1

st.write(f"Progresso verso il Target ($ {target:,.0f}):")
st.progress(progress)

# Messaggio Dinamico
if equity < drawdown_limit:
    st.error("❌ HARD BREACH: Hai superato il limite di Drawdown. Conto Squalificato.")
elif equity >= target:
    st.success("🏆 COMPLIMENTI! Hai superato la Fase 1.")
else:
    st.info("✅ Il conto è ATTIVO e in buona salute. Continua a tradare.")