import streamlit as st
import ccxt
import pandas as pd
import time

# ---------------------------------------------------------
# CONFIGURAZIONE PAGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Blackship | Live Tracker",
    page_icon="🏴‍☠️",
    layout="wide"
)

# CSS PER STILE DARK PRO
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00ff00; }
    .css-1544g2n { padding: 2rem 1rem; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# FUNZIONI DI CONNESSIONE (IL MOTORE)
# ---------------------------------------------------------
def get_bybit_data(api_key, api_secret):
    try:
        # Connessione a Bybit
        exchange = ccxt.bybit({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
        })
        
        # Scarica il Bilancio (Unified Account)
        balance_data = exchange.fetch_balance()
        
        # Cerchiamo i dati USDT
        if 'USDT' in balance_data['total']:
            total_balance = balance_data['total']['USDT'] # Saldo Wallet
            equity = balance_data['total']['USDT'] # In UTA spesso coincide se non ci sono posizioni aperte
            
            # Se ci sono posizioni aperte, l'equity cambia. 
            # Per semplicità ora prendiamo il total
            return total_balance, equity
        else:
            return 0.0, 0.0
            
    except Exception as e:
        return None, str(e)

# ---------------------------------------------------------
# SIDEBAR - INGRESSO DATI
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/pirate.png", width=50)
    st.title("BLACKSHIP")
    st.caption("Investor Dashboard v1.2")
    st.markdown("---")
    
    st.write("🔑 **Inserisci API Key Bybit**")
    user_key = st.text_input("API Key", type="password")
    user_secret = st.text_input("API Secret", type="password")
    
    st.info("ℹ️ Usa chiavi 'Read-Only'. Il sistema non ha permessi di prelievo.")

# ---------------------------------------------------------
# DASHBOARD PRINCIPALE
# ---------------------------------------------------------
st.title("📡 Live Trading Monitor")

# SE L'UTENTE HA MESSO LE CHIAVI -> CONNESSIONE VERA
if user_key and user_secret:
    with st.spinner('Connessione al satellite Bybit...'):
        balance, equity = get_bybit_data(user_key, user_secret)
        
    if balance is None:
        st.error(f"Errore di connessione: {equity}")
        st.warning("Controlla che le chiavi siano corrette e di tipo 'Unified Trading'.")
    else:
        # DATI REALI
        start_balance = 50000.00 # Simuliamo che la challenge sia da 50k
        profit = equity - start_balance
        profit_pct = (profit / start_balance) * 100
        
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Wallet Balance", f"${balance:,.2f}")
        col2.metric("📈 Live Equity", f"${equity:,.2f}", f"{profit:,.2f} ({profit_pct:.2f}%)")
        col3.metric("🎯 Target (Investor)", "$60,000.00", "20%")
        
        st.markdown("---")
        
        # BARRA PROGRESSO
        target_val = 60000
        progress = (equity - start_balance) / (target_val - start_balance)
        if progress < 0: progress = 0.0
        if progress > 1: progress = 1.0
        
        st.write(f"Progresso verso il Target:")
        st.progress(progress)
        
        if equity < (start_balance * 0.90):
            st.error("🚫 STOP OUT: Il conto ha superato il limite di perdita.")
        else:
            st.success("✅ CONTO ATTIVO: Trading consentito.")

# SE NON HA MESSO LE CHIAVI -> MOSTRA DEMO
else:
    st.warning("⚠️ Inserisci le tue API Key a sinistra per vedere i dati reali.")
    st.markdown("### Dati Demo (Esempio)")
    c1, c2, c3 = st.columns(3)
    c1.metric("Balance", "$50,000.00")
    c2.metric("Equity", "$51,250.00", "+2.5%")
    c3.metric("Target", "$60,000.00")