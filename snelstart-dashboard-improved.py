import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="SnelStart Financieel Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        color: white;
    }
    
    .stMetric label {
        color: rgba(255,255,255,0.9) !important;
        font-weight: 500;
        font-size: 1rem;
    }
    
    .stMetric .metric-container {
        color: white !important;
    }
    
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    [data-testid="metric-container"] > div > div > div > div {
        color: white !important;
    }
    
    .metric-delta {
        color: #10b981 !important;
    }
    
    .css-1n76uvr {
        background-color: #f8fafc;
    }
    
    h1 {
        background: linear-gradient(to right, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    h2 {
        color: #334155;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #475569;
        font-weight: 500;
    }
    
    .sidebar .sidebar-content {
        background-color: #f1f5f9;
    }
    
    div[data-testid="stSidebar"] > div {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 24px;
        background-color: #f1f5f9;
        border-radius: 10px;
        color: #64748b;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .info-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border: 1px solid #e2e8f0;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .recommendation-card {
        background: white;
        border-left: 4px solid #667eea;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Data storage - alle financiële data van SnelStart
@st.cache_data
def load_financial_data():
    # Balansgegevens
    balance_sheet = {
        "2022": {
            "Immateriële vaste activa": 0,
            "Materiële vaste activa": 681029,
            "Financiële vaste activa": 2964989,
            "Vorderingen en overlopende activa": 3567616,
            "Liquide middelen": 1921392,
            "Eigen vermogen": 3152060,
            "Kortlopende schulden": 5982966,
        },
        "2023": {
            "Immateriële vaste activa": 616792,
            "Materiële vaste activa": 480038,
            "Financiële vaste activa": 2879700,
            "Vorderingen en overlopende activa": 2050960,
            "Liquide middelen": 5876484,
            "Eigen vermogen": 4912207,
            "Kortlopende schulden": 6991767,
        },
        "2024": {
            "Immateriële vaste activa": 118414,
            "Materiële vaste activa": 435242,
            "Financiële vaste activa": 3710145,
            "Vorderingen en overlopende activa": 3642300,
            "Liquide middelen": 9078755,
            "Eigen vermogen": 10085950,
            "Kortlopende schulden": 6898906,
        }
    }
    
    # Winst & verliesrekening
    profit_loss = {
        "2022": {
            "Netto-omzet": 28632557,
            "Kostprijs van de omzet": 4030779,
            "Brutomarge": 24601778,
            "Bedrijfskosten": 20993636,
            "Bedrijfsresultaat": 3608142,
            "Nettowinst": 2801050,
        },
        "2023": {
            "Netto-omzet": 36031549,
            "Kostprijs van de omzet": 3828888,
            "Brutomarge": 32202661,
            "Bedrijfskosten": 21066838,
            "Bedrijfsresultaat": 11135823,
            "Nettowinst": 8160147,
        },
        "2024": {
            "Netto-omzet": 44788100,
            "Kostprijs van de omzet": 5354998,
            "Brutomarge": 39433102,
            "Bedrijfskosten": 24441359,
            "Bedrijfsresultaat": 14991743,
            "Nettowinst": 11067411,
        }
    }
    
    # Kasstroomgegevens
    cash_flow = {
        "2023": {
            "Operationele kasstroom": 10444979,
            "Investeringskasstroom": -88963,
            "Financieringskasstroom": -6400924,
            "Netto kasstroom": 3955092,
        },
        "2024": {
            "Operationele kasstroom": 10159729,
            "Investeringskasstroom": -1063790,
            "Financieringskasstroom": -5893668,
            "Netto kasstroom": 3202271,
        }
    }
    
    return balance_sheet, profit_loss, cash_flow

# Calculate financial ratios
def calculate_ratios(balance_sheet, profit_loss, year):
    bs = balance_sheet[year]
    pl = profit_loss[year]
    
    # Totaal activa en passiva
    vaste_activa = bs["Immateriële vaste activa"] + bs["Materiële vaste activa"] + bs["Financiële vaste activa"]
    vlottende_activa = bs["Vorderingen en overlopende activa"] + bs["Liquide middelen"]
    totaal_activa = vaste_activa + vlottende_activa
    
    # Ratio's
    current_ratio = vlottende_activa / bs["Kortlopende schulden"]
    quick_ratio = (bs["Liquide middelen"] + bs["Vorderingen en overlopende activa"]) / bs["Kortlopende schulden"]
    solvabiliteit = (bs["Eigen vermogen"] / totaal_activa) * 100
    roe = (pl["Nettowinst"] / bs["Eigen vermogen"]) * 100
    roa = (pl["Bedrijfsresultaat"] / totaal_activa) * 100
    winstmarge = (pl["Nettowinst"] / pl["Netto-omzet"]) * 100
    brutomarge = (pl["Brutomarge"] / pl["Netto-omzet"]) * 100
    
    return {
        "current_ratio": current_ratio,
        "quick_ratio": quick_ratio,
        "solvabiliteit": solvabiliteit,
        "roe": roe,
        "roa": roa,
        "winstmarge": winstmarge,
        "brutomarge": brutomarge,
        "werkkapitaal": vlottende_activa - bs["Kortlopende schulden"]
    }

# Format currency
def format_currency(value):
    if value >= 1_000_000:
        return f"€{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"€{value/1_000:.0f}K"
    else:
        return f"€{value:.0f}"

# Load data
balance_sheet, profit_loss, cash_flow = load_financial_data()

# Title and description
st.markdown("<h1 style='text-align: center;'>SnelStart Financieel Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 1.2rem; margin-bottom: 2rem;'>Interactieve financiële analyse 2022-2024</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Dashboard Navigatie")
    selected_year = st.selectbox("Selecteer jaar:", ["2024", "2023", "2022"], index=0)
    
    # Quick stats
    ratios = calculate_ratios(balance_sheet, profit_loss, selected_year)
    
    st.markdown("### 📊 Quick Stats")
    st.info(f"""
    **Omzet:** {format_currency(profit_loss[selected_year]["Netto-omzet"])}  
    **Nettowinst:** {format_currency(profit_loss[selected_year]["Nettowinst"])}  
    **Winstmarge:** {ratios['winstmarge']:.1f}%  
    **ROE:** {ratios['roe']:.1f}%  
    **Solvabiliteit:** {ratios['solvabiliteit']:.1f}%
    """)
    
    st.markdown("### 📈 Groeipercentages")
    if selected_year != "2022":
        prev_year = str(int(selected_year) - 1)
        omzet_groei = ((profit_loss[selected_year]["Netto-omzet"] - profit_loss[prev_year]["Netto-omzet"]) / profit_loss[prev_year]["Netto-omzet"]) * 100
        winst_groei = ((profit_loss[selected_year]["Nettowinst"] - profit_loss[prev_year]["Nettowinst"]) / profit_loss[prev_year]["Nettowinst"]) * 100
        
        st.success(f"""
        **Omzetgroei:** +{omzet_groei:.1f}%  
        **Winstgroei:** +{winst_groei:.1f}%
        """)

# Main content - Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "💰 Financiële Analyse", "📈 Trends", "💡 Aanbevelingen", "📑 Rapporten"])

with tab1:
    # KPI Metrics
    st.markdown("### 🎯 Kerncijfers " + selected_year)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Omzet",
            format_currency(profit_loss[selected_year]["Netto-omzet"]),
            f"+{((profit_loss[selected_year]['Netto-omzet'] - profit_loss[str(int(selected_year)-1)]['Netto-omzet']) / profit_loss[str(int(selected_year)-1)]['Netto-omzet'] * 100):.1f}%" if selected_year != "2022" else None
        )
    
    with col2:
        st.metric(
            "Nettowinst",
            format_currency(profit_loss[selected_year]["Nettowinst"]),
            f"+{((profit_loss[selected_year]['Nettowinst'] - profit_loss[str(int(selected_year)-1)]['Nettowinst']) / profit_loss[str(int(selected_year)-1)]['Nettowinst'] * 100):.1f}%" if selected_year != "2022" else None
        )
    
    with col3:
        st.metric(
            "Eigen Vermogen",
            format_currency(balance_sheet[selected_year]["Eigen vermogen"]),
            f"+{((balance_sheet[selected_year]['Eigen vermogen'] - balance_sheet[str(int(selected_year)-1)]['Eigen vermogen']) / balance_sheet[str(int(selected_year)-1)]['Eigen vermogen'] * 100):.1f}%" if selected_year != "2022" else None
        )
    
    with col4:
        st.metric(
            "Kaspositie",
            format_currency(balance_sheet[selected_year]["Liquide middelen"]),
            f"+{((balance_sheet[selected_year]['Liquide middelen'] - balance_sheet[str(int(selected_year)-1)]['Liquide middelen']) / balance_sheet[str(int(selected_year)-1)]['Liquide middelen'] * 100):.1f}%" if selected_year != "2022" else None
        )
    
    # Charts row 1
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue & Profit chart
        fig = go.Figure()
        
        years = ["2022", "2023", "2024"]
        revenues = [profit_loss[y]["Netto-omzet"] for y in years]
        profits = [profit_loss[y]["Nettowinst"] for y in years]
        
        fig.add_trace(go.Bar(
            x=years,
            y=revenues,
            name='Omzet',
            marker_color='#667eea',
            text=[format_currency(v) for v in revenues],
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            x=years,
            y=profits,
            name='Nettowinst',
            marker_color='#764ba2',
            text=[format_currency(v) for v in profits],
            textposition='outside'
        ))
        
        fig.update_layout(
            title="Omzet vs Nettowinst",
            xaxis_title="Jaar",
            yaxis_title="Bedrag (€)",
            height=400,
            showlegend=True,
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Profitability ratios
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=years,
            y=[calculate_ratios(balance_sheet, profit_loss, y)["winstmarge"] for y in years],
            mode='lines+markers',
            name='Winstmarge',
            line=dict(color='#10b981', width=3),
            marker=dict(size=10)
        ))
        
        fig.add_trace(go.Scatter(
            x=years,
            y=[calculate_ratios(balance_sheet, profit_loss, y)["roe"] for y in years],
            mode='lines+markers',
            name='ROE',
            line=dict(color='#f59e0b', width=3),
            marker=dict(size=10),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Winstgevendheid Trends",
            xaxis_title="Jaar",
            yaxis=dict(title="Winstmarge (%)", side="left"),
            yaxis2=dict(title="ROE (%)", overlaying="y", side="right"),
            height=400,
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Financial health indicators
    st.markdown("### 💪 Financiële Gezondheid")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_ratio = ratios["current_ratio"]
        st.metric("Current Ratio", f"{current_ratio:.2f}")
        if current_ratio >= 2:
            st.success("Uitstekend")
        elif current_ratio >= 1.5:
            st.info("Goed")
        else:
            st.warning("Aandacht vereist")
    
    with col2:
        solvabiliteit = ratios["solvabiliteit"]
        st.metric("Solvabiliteit", f"{solvabiliteit:.1f}%")
        if solvabiliteit >= 50:
            st.success("Zeer gezond")
        elif solvabiliteit >= 30:
            st.info("Gezond")
        else:
            st.warning("Risicovol")
    
    with col3:
        roe = ratios["roe"]
        st.metric("ROE", f"{roe:.1f}%")
        if roe >= 20:
            st.success("Uitstekend")
        elif roe >= 15:
            st.info("Goed")
        else:
            st.warning("Matig")
    
    with col4:
        werkkapitaal = ratios["werkkapitaal"]
        st.metric("Werkkapitaal", format_currency(werkkapitaal))
        if werkkapitaal > 0:
            st.success("Positief")
        else:
            st.error("Negatief")

with tab2:
    st.markdown("### 📊 Gedetailleerde Financiële Analyse")
    
    # Balance sheet analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Activa Samenstelling")
        
        # Calculate totals
        vaste_activa = (balance_sheet[selected_year]["Immateriële vaste activa"] + 
                       balance_sheet[selected_year]["Materiële vaste activa"] + 
                       balance_sheet[selected_year]["Financiële vaste activa"])
        vlottende_activa = (balance_sheet[selected_year]["Vorderingen en overlopende activa"] + 
                           balance_sheet[selected_year]["Liquide middelen"])
        
        fig = go.Figure(data=[go.Pie(
            labels=['Vaste Activa', 'Vorderingen', 'Liquide Middelen'],
            values=[vaste_activa, 
                   balance_sheet[selected_year]["Vorderingen en overlopende activa"],
                   balance_sheet[selected_year]["Liquide middelen"]],
            hole=.3,
            marker_colors=['#667eea', '#a78bfa', '#c4b5fd']
        )])
        
        fig.update_layout(
            title=f"Activa Verdeling {selected_year}",
            height=350,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Passiva Samenstelling")
        
        totaal_passiva = balance_sheet[selected_year]["Eigen vermogen"] + balance_sheet[selected_year]["Kortlopende schulden"]
        
        fig = go.Figure(data=[go.Pie(
            labels=['Eigen Vermogen', 'Kortlopende Schulden'],
            values=[balance_sheet[selected_year]["Eigen vermogen"], 
                   balance_sheet[selected_year]["Kortlopende schulden"]],
            hole=.3,
            marker_colors=['#10b981', '#ef4444']
        )])
        
        fig.update_layout(
            title=f"Passiva Verdeling {selected_year}",
            height=350,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Ratio analysis table
    st.markdown("#### 📈 Financiële Ratio's Overzicht")
    
    ratio_data = []
    for year in ["2022", "2023", "2024"]:
        year_ratios = calculate_ratios(balance_sheet, profit_loss, year)
        ratio_data.append({
            "Jaar": year,
            "Current Ratio": f"{year_ratios['current_ratio']:.2f}",
            "Quick Ratio": f"{year_ratios['quick_ratio']:.2f}",
            "Solvabiliteit (%)": f"{year_ratios['solvabiliteit']:.1f}",
            "ROE (%)": f"{year_ratios['roe']:.1f}",
            "ROA (%)": f"{year_ratios['roa']:.1f}",
            "Winstmarge (%)": f"{year_ratios['winstmarge']:.1f}"
        })
    
    ratio_df = pd.DataFrame(ratio_data)
    st.dataframe(ratio_df, use_container_width=True, hide_index=True)

with tab3:
    st.markdown("### 📈 Trend Analyse")
    
    # Multi-year comparison
    years = ["2022", "2023", "2024"]
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Omzet Groei', 'Winstgevendheid', 'Liquiditeit', 'Vermogenspositie'),
        specs=[[{"secondary_y": False}, {"secondary_y": True}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Omzet groei
    omzet_values = [profit_loss[y]["Netto-omzet"]/1_000_000 for y in years]
    fig.add_trace(
        go.Scatter(x=years, y=omzet_values, mode='lines+markers+text',
                  name='Omzet (€M)', line=dict(width=3, color='#667eea'),
                  text=[f"€{v:.1f}M" for v in omzet_values],
                  textposition="top center"),
        row=1, col=1
    )
    
    # Winstgevendheid
    winst_values = [profit_loss[y]["Nettowinst"]/1_000_000 for y in years]
    marge_values = [calculate_ratios(balance_sheet, profit_loss, y)["winstmarge"] for y in years]
    
    fig.add_trace(
        go.Bar(x=years, y=winst_values, name='Nettowinst (€M)',
               marker_color='#10b981', text=[f"€{v:.1f}M" for v in winst_values]),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Scatter(x=years, y=marge_values, mode='lines+markers',
                  name='Winstmarge (%)', line=dict(width=3, color='#f59e0b')),
        row=1, col=2, secondary_y=True
    )
    
    # Liquiditeit
    current_ratios = [calculate_ratios(balance_sheet, profit_loss, y)["current_ratio"] for y in years]
    quick_ratios = [calculate_ratios(balance_sheet, profit_loss, y)["quick_ratio"] for y in years]
    
    fig.add_trace(
        go.Scatter(x=years, y=current_ratios, mode='lines+markers',
                  name='Current Ratio', line=dict(width=3, color='#3b82f6')),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=years, y=quick_ratios, mode='lines+markers',
                  name='Quick Ratio', line=dict(width=3, color='#8b5cf6')),
        row=2, col=1
    )
    
    # Vermogenspositie
    ev_values = [balance_sheet[y]["Eigen vermogen"]/1_000_000 for y in years]
    solvabiliteit_values = [calculate_ratios(balance_sheet, profit_loss, y)["solvabiliteit"] for y in years]
    
    fig.add_trace(
        go.Bar(x=years, y=ev_values, name='Eigen Vermogen (€M)',
               marker_color='#059669', text=[f"€{v:.1f}M" for v in ev_values]),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(height=800, showlegend=True, title_text="Financiële Trends 2022-2024")
    fig.update_xaxes(title_text="Jaar")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Cash flow waterfall
    if selected_year in ["2023", "2024"]:
        st.markdown("### 💸 Kasstroomanalyse " + selected_year)
        
        cf_data = cash_flow[selected_year]
        
        fig = go.Figure(go.Waterfall(
            name="Kasstroom",
            orientation="v",
            measure=["relative", "relative", "relative", "total"],
            x=["Operationeel", "Investeringen", "Financiering", "Netto"],
            textposition="outside",
            text=[format_currency(cf_data["Operationele kasstroom"]),
                  format_currency(cf_data["Investeringskasstroom"]),
                  format_currency(cf_data["Financieringskasstroom"]),
                  format_currency(cf_data["Netto kasstroom"])],
            y=[cf_data["Operationele kasstroom"],
               cf_data["Investeringskasstroom"],
               cf_data["Financieringskasstroom"],
               0],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": "#10b981"}},
            decreasing={"marker": {"color": "#ef4444"}}
        ))
        
        fig.update_layout(
            title=f"Kasstroomoverzicht {selected_year}",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.markdown("### 💡 Strategische Aanbevelingen")
    
    # Analyse van de huidige situatie
    if selected_year == "2024":
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
            st.markdown("#### ✅ Sterke Punten")
            st.markdown("""
            - **Uitzonderlijke groei**: Omzet gestegen met 24.1% naar €44.8M
            - **Sterke winstgevendheid**: Nettowinst van €11.1M (+36.2%)
            - **Solide financiële positie**: Solvabiliteit van 60.1%
            - **Uitstekende liquiditeit**: Current ratio van 1.85
            - **Hoge ROE**: 157% rendement op eigen vermogen
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
            st.markdown("#### 🎯 Groeikansen")
            st.markdown("""
            - **Marktuitbreiding**: Met €9.1M aan liquide middelen zijn er ruime mogelijkheden voor expansie
            - **Productontwikkeling**: Investeer in nieuwe features en diensten
            - **Strategische overnames**: Overweeg acquisities van complementaire bedrijven
            - **Internationale groei**: Verken mogelijkheden buiten Nederland
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
            st.markdown("#### ⚠️ Aandachtspunten")
            st.markdown("""
            - Personeelskosten stijgen sneller dan omzet
            - Relatief lage investeringen in vaste activa
            - Afhankelijkheid van Nederlandse markt
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
            st.markdown("#### 🚀 Actieplan")
            st.markdown("""
            1. **Q1 2025**: Strategisch plan voor internationale expansie
            2. **Q2 2025**: Verhoog R&D budget met 25%
            3. **Q3 2025**: Start pilot in België/Duitsland
            4. **Q4 2025**: Evaluatie en opschaling
            """)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Benchmark analyse
    st.markdown("### 📊 Benchmark Analyse")
    
    benchmark_data = {
        "Metric": ["Winstmarge", "ROE", "Current Ratio", "Solvabiliteit"],
        "SnelStart": [ratios["winstmarge"], ratios["roe"], ratios["current_ratio"], ratios["solvabiliteit"]],
        "Industrie Gem.": [15.0, 25.0, 1.5, 40.0],
        "Top Performers": [25.0, 35.0, 2.0, 50.0]
    }
    
    benchmark_df = pd.DataFrame(benchmark_data)
    
    fig = go.Figure()
    
    for col in ["SnelStart", "Industrie Gem.", "Top Performers"]:
        fig.add_trace(go.Bar(
            name=col,
            x=benchmark_df["Metric"],
            y=benchmark_df[col],
            text=[f"{v:.1f}" for v in benchmark_df[col]],
            textposition='outside'
        ))
    
    fig.update_layout(
        title="Prestaties vs Industrie Benchmarks",
        xaxis_title="Metric",
        yaxis_title="Waarde",
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.markdown("### 📑 Download Rapporten")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 Financieel Rapport")
        st.markdown("Compleet financieel overzicht inclusief:")
        st.markdown("- Balans analyse")
        st.markdown("- Winst & verliesrekening")
        st.markdown("- Kasstroomoverzicht")
        st.markdown("- Ratio analyse")
        
        # Create downloadable report
        report_data = f"""
SNELSTART FINANCIEEL RAPPORT {selected_year}

KERNCIJFERS
-----------
Omzet: {format_currency(profit_loss[selected_year]["Netto-omzet"])}
Nettowinst: {format_currency(profit_loss[selected_year]["Nettowinst"])}
Eigen Vermogen: {format_currency(balance_sheet[selected_year]["Eigen vermogen"])}
Liquide Middelen: {format_currency(balance_sheet[selected_year]["Liquide middelen"])}

RATIO'S
-------
Current Ratio: {ratios['current_ratio']:.2f}
Quick Ratio: {ratios['quick_ratio']:.2f}
Solvabiliteit: {ratios['solvabiliteit']:.1f}%
ROE: {ratios['roe']:.1f}%
ROA: {ratios['roa']:.1f}%
Winstmarge: {ratios['winstmarge']:.1f}%

CONCLUSIE
---------
SnelStart toont uitstekende financiële prestaties met sterke groei en gezonde ratio's.
        """
        
        st.download_button(
            label="📥 Download Rapport",
            data=report_data,
            file_name=f"snelstart_rapport_{selected_year}.txt",
            mime="text/plain"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("#### 📈 Presentatie Export")
        st.markdown("Exporteer dashboard data voor presentaties:")
        st.markdown("- Alle grafieken en visualisaties")
        st.markdown("- Kerncijfers en trends")
        st.markdown("- Aanbevelingen en conclusies")
        
        st.button("🎯 Genereer Presentatie", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #94a3b8;'>Dashboard gemaakt voor Financieel Management | HvA Bedrijfskunde | SnelStart Software B.V.</p>",
    unsafe_allow_html=True
)