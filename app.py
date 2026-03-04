import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ──────────────────────────────────────────────
# Page Config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Monte Carlo Portfolio Simulator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Custom CSS — Premium dark theme
# ──────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Global ── */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #0f172a 100%);
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #1e293b 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.15);
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #94a3b8;
        font-size: 0.85rem;
    }

    /* ── Headers ── */
    h1 {
        background: linear-gradient(135deg, #818cf8 0%, #6366f1 40%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        letter-spacing: -0.03em;
    }
    h2, h3 {
        color: #c7d2fe !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }

    /* ── Metric cards ── */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(139,92,246,0.05));
        border: 1px solid rgba(99,102,241,0.18);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.15);
    }
    [data-testid="stMetricValue"] {
        font-weight: 700;
        font-size: 1.6rem !important;
        color: #a5b4fc !important;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 500;
        text-transform: uppercase;
        font-size: 0.7rem !important;
        letter-spacing: 0.08em;
    }
    [data-testid="stMetricDelta"] {
        font-weight: 600;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.65rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: 0.02em;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #818cf8, #a78bfa);
        box-shadow: 0 6px 25px rgba(99, 102, 241, 0.45);
        transform: translateY(-1px);
        color: white;
    }
    .stButton > button:active {
        transform: translateY(0px);
    }

    /* ── Slider ── */
    .stSlider > div > div > div > div {
        background-color: #6366f1;
    }
    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"] {
        color: #64748b;
    }

    /* ── Number input, selectbox ── */
    .stNumberInput input, .stSelectbox > div > div {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(99,102,241,0.2) !important;
        border-radius: 8px !important;
    }
    .stNumberInput input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99,102,241,0.2) !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: rgba(30, 41, 59, 0.5);
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 500;
        padding: 0.5rem 1.25rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(99, 102, 241, 0.15) !important;
        color: #a5b4fc !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: transparent !important;
    }

    /* ── Divider ── */
    hr {
        border-color: rgba(99, 102, 241, 0.12) !important;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background-color: rgba(30, 41, 59, 0.5);
        border-radius: 8px;
        color: #c7d2fe !important;
    }

    /* ── Data-frame / Table ── */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(99, 102, 241, 0.12);
        border-radius: 10px;
        overflow: hidden;
    }

    /* ── Badge-style helper class ── */
    .badge {
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.04em;
    }
    .badge-green  { background: rgba(34,197,94,0.15); color: #4ade80; }
    .badge-red    { background: rgba(239,68,68,0.15); color: #f87171; }
    .badge-blue   { background: rgba(99,102,241,0.15); color: #a5b4fc; }
    .badge-amber  { background: rgba(245,158,11,0.15); color: #fbbf24; }

    /* ── Info box ── */
    .info-box {
        background: linear-gradient(135deg, rgba(99,102,241,0.06), rgba(139,92,246,0.04));
        border: 1px solid rgba(99,102,241,0.12);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin: 0.75rem 0;
        font-size: 0.88rem;
        line-height: 1.6;
        color: #cbd5e1;
    }

    /* ── Footer ── */
    .footer {
        text-align: center;
        color: #475569;
        font-size: 0.75rem;
        padding: 2rem 0 1rem;
        letter-spacing: 0.04em;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Plotly theme helper
# ──────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#94a3b8"),
    title_font=dict(size=16, color="#c7d2fe"),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(size=11, color="#94a3b8"),
    ),
    margin=dict(l=40, r=40, t=50, b=40),
    hoverlabel=dict(
        bgcolor="#1e293b",
        font_size=12,
        font_color="#e2e8f0",
        bordercolor="#6366f1",
    ),
)

ACCENT      = "#818cf8"
ACCENT_LIGHT = "#a5b4fc"
GREEN       = "#4ade80"
RED         = "#f87171"
AMBER       = "#fbbf24"
GRID_COLOR  = "rgba(148, 163, 184, 0.08)"

TRADING_DAYS = 252


# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 0.5rem 0 0.25rem;">
    <span style="font-size:2.4rem;">📊</span>
</div>
""", unsafe_allow_html=True)
st.title("Monte Carlo Portfolio Simulator")
st.markdown(
    '<p style="text-align:center; color:#64748b; margin-top:-0.8rem; font-size:1.05rem;">'
    'Forecast portfolio outcomes using stochastic simulation &nbsp;·&nbsp; Geometric Brownian Motion</p>',
    unsafe_allow_html=True,
)
st.markdown("")


# ──────────────────────────────────────────────
# Sidebar — Inputs
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<p style="font-size:1.2rem; font-weight:700; color:#c7d2fe; margin-bottom:0.25rem;">'
        '⚙️ &nbsp;Simulation Parameters</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#64748b; font-size:0.8rem; margin-top:-0.5rem;">'
        'Adjust the inputs below and hit <b>Run Simulation</b>.</p>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # ── Portfolio Settings ──
    st.markdown("**💰 Portfolio**")
    initial_investment = st.number_input(
        "Initial Investment ($)",
        min_value=1_000,
        max_value=10_000_000,
        value=100_000,
        step=5_000,
        format="%d",
    )
    monthly_contribution = st.number_input(
        "Monthly Contribution ($)",
        min_value=0,
        max_value=100_000,
        value=500,
        step=100,
        format="%d",
    )

    st.markdown("")
    st.markdown("**📅 Time Horizon**")
    time_horizon_years = st.slider(
        "Investment Period (Years)",
        min_value=1,
        max_value=40,
        value=10,
    )

    st.markdown("")
    st.markdown("**📈 Market Assumptions**")
    expected_annual_return = st.slider(
        "Expected Annual Return (%)",
        min_value=-10.0,
        max_value=30.0,
        value=8.0,
        step=0.5,
        format="%.1f%%",
    ) / 100.0

    annual_volatility = st.slider(
        "Annual Volatility / Std Dev (%)",
        min_value=1.0,
        max_value=60.0,
        value=16.0,
        step=0.5,
        format="%.1f%%",
    ) / 100.0

    st.markdown("")
    st.markdown("**🔢 Simulation**")
    num_simulations = st.select_slider(
        "Number of Simulations",
        options=[100, 250, 500, 1_000, 2_500, 5_000, 10_000],
        value=1_000,
    )
    confidence_level = st.select_slider(
        "Confidence Interval (%)",
        options=[80, 90, 95, 99],
        value=90,
    )

    st.markdown("---")
    run_sim = st.button("🚀  Run Simulation", use_container_width=True)

    # About
    with st.expander("ℹ️  About this tool"):
        st.markdown("""
This simulator uses **Geometric Brownian Motion (GBM)** to model
the stochastic behaviour of asset prices.

Each path is generated as:

$$dS = \\mu S \\, dt + \\sigma S \\, dW$$

where *μ* is the drift (expected return), *σ* is volatility,
and *dW* is a Wiener process increment.

Monthly contributions are added at each calendar-month boundary.
""")


# ──────────────────────────────────────────────
# Simulation Engine
# ──────────────────────────────────────────────
def run_monte_carlo(initial_val, monthly_contrib, years, mu, sigma, sims):
    """Run GBM Monte Carlo with optional monthly contributions."""
    num_days = years * TRADING_DAYS
    dt = 1 / TRADING_DAYS
    daily_drift = (mu - 0.5 * sigma**2) * dt
    daily_vol = sigma * np.sqrt(dt)

    # Generate random shocks
    Z = np.random.standard_normal((num_days, sims))
    log_returns = daily_drift + daily_vol * Z

    # Build price paths
    price_paths = np.zeros((num_days + 1, sims))
    price_paths[0] = initial_val

    # Pre-compute which days are month boundaries (approx every 21 trading days)
    month_days = set(range(21, num_days + 1, 21))

    for t in range(1, num_days + 1):
        price_paths[t] = price_paths[t - 1] * np.exp(log_returns[t - 1])
        if t in month_days:
            price_paths[t] += monthly_contrib

    return price_paths


# ──────────────────────────────────────────────
# Run simulation on button press or first load
# ──────────────────────────────────────────────
if run_sim or "sim_data" not in st.session_state:
    with st.spinner("Running simulation…"):
        paths = run_monte_carlo(
            initial_investment,
            monthly_contribution,
            time_horizon_years,
            expected_annual_return,
            annual_volatility,
            num_simulations,
        )
        st.session_state["sim_data"] = paths
        st.session_state["params"] = dict(
            initial=initial_investment,
            monthly=monthly_contribution,
            years=time_horizon_years,
            mu=expected_annual_return,
            sigma=annual_volatility,
            sims=num_simulations,
            ci=confidence_level,
        )


# ──────────────────────────────────────────────
# Helper functions
# ──────────────────────────────────────────────
def fmt_dollar(v):
    if abs(v) >= 1_000_000:
        return f"${v / 1_000_000:,.2f}M"
    return f"${v:,.0f}"


def fmt_pct(v):
    return f"{v:+,.1f}%"


# ──────────────────────────────────────────────
# Display
# ──────────────────────────────────────────────
if "sim_data" in st.session_state:
    data = st.session_state["sim_data"]
    params = st.session_state["params"]
    final_values = data[-1, :]
    total_invested = params["initial"] + params["monthly"] * 12 * params["years"]

    ci_lo = (100 - params["ci"]) / 2
    ci_hi = 100 - ci_lo

    median_val   = np.percentile(final_values, 50)
    p_lo         = np.percentile(final_values, ci_lo)
    p_hi         = np.percentile(final_values, ci_hi)
    mean_val     = np.mean(final_values)
    min_val      = np.min(final_values)
    max_val      = np.max(final_values)
    prob_profit  = np.mean(final_values > total_invested) * 100
    prob_double  = np.mean(final_values > 2 * params["initial"]) * 100

    # ── Key metrics ──
    st.markdown("### 🏆 Key Outcomes")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Median Final Value", fmt_dollar(median_val),
                  fmt_pct((median_val / total_invested - 1) * 100))
    with c2:
        st.metric(f"Worst Case ({ci_lo:.0f}th %ile)", fmt_dollar(p_lo),
                  fmt_pct((p_lo / total_invested - 1) * 100), delta_color="inverse")
    with c3:
        st.metric(f"Best Case ({ci_hi:.0f}th %ile)", fmt_dollar(p_hi),
                  fmt_pct((p_hi / total_invested - 1) * 100))
    with c4:
        st.metric("Total Invested", fmt_dollar(total_invested),
                  f"{params['years']}y @ {fmt_dollar(params['monthly'])}/mo")

    st.markdown("")

    c5, c6, c7, c8 = st.columns(4)
    with c5:
        st.metric("Mean Final Value", fmt_dollar(mean_val))
    with c6:
        color = "green" if prob_profit >= 50 else "red"
        st.metric("Probability of Profit", f"{prob_profit:.1f}%")
    with c7:
        st.metric("Prob. of Doubling", f"{prob_double:.1f}%")
    with c8:
        sharpe = (params["mu"] - 0.04) / params["sigma"] if params["sigma"] else 0
        st.metric("Implied Sharpe Ratio", f"{sharpe:.2f}")

    st.markdown("---")

    # ── Tabs ──
    tab_paths, tab_dist, tab_stats, tab_drawdown = st.tabs([
        "📈  Simulation Paths",
        "📊  Distribution",
        "📋  Statistics",
        "📉  Drawdown Analysis",
    ])

    # ── Shared x-axis ──
    x_years = np.linspace(0, params["years"], num=data.shape[0])

    # ═══════════════════════════════════════════
    # TAB 1 — Simulation Paths
    # ═══════════════════════════════════════════
    with tab_paths:
        max_lines = min(params["sims"], 300)
        plot_subset = data[:, :max_lines]

        fig = go.Figure()

        # Confidence band
        lo_band = np.percentile(data, ci_lo, axis=1)
        hi_band = np.percentile(data, ci_hi, axis=1)
        fig.add_trace(go.Scatter(
            x=x_years, y=hi_band, mode="lines",
            line=dict(width=0), showlegend=False, hoverinfo="skip",
        ))
        fig.add_trace(go.Scatter(
            x=x_years, y=lo_band, mode="lines",
            line=dict(width=0), fill="tonexty",
            fillcolor="rgba(99, 102, 241, 0.10)",
            name=f"{params['ci']}% Confidence Band",
        ))

        # Individual paths
        for i in range(max_lines):
            fig.add_trace(go.Scatter(
                x=x_years, y=plot_subset[:, i], mode="lines",
                line=dict(width=0.6, color="rgba(129, 140, 248, 0.07)"),
                showlegend=False, hoverinfo="skip",
            ))

        # Median
        median_path = np.median(data, axis=1)
        fig.add_trace(go.Scatter(
            x=x_years, y=median_path, mode="lines",
            line=dict(width=2.5, color=GREEN),
            name="Median Path",
        ))

        # Mean
        mean_path = np.mean(data, axis=1)
        fig.add_trace(go.Scatter(
            x=x_years, y=mean_path, mode="lines",
            line=dict(width=2, color=AMBER, dash="dot"),
            name="Mean Path",
        ))

        # Initial investment line
        fig.add_hline(
            y=params["initial"], line_dash="dash",
            line_color="rgba(148,163,184,0.3)",
            annotation_text="Initial", annotation_font_color="#64748b",
        )

        fig.update_layout(
            **PLOTLY_LAYOUT,
            title=f"Simulated Portfolio Paths  ·  {max_lines:,} of {params['sims']:,} shown",
            xaxis=dict(title="Years", gridcolor=GRID_COLOR, zeroline=False),
            yaxis=dict(title="Portfolio Value ($)", gridcolor=GRID_COLOR, zeroline=False,
                       tickprefix="$", separatethousands=True),
            hovermode="x unified",
            height=520,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ═══════════════════════════════════════════
    # TAB 2 — Distribution
    # ═══════════════════════════════════════════
    with tab_dist:
        col_hist, col_box = st.columns([3, 1])

        with col_hist:
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Histogram(
                x=final_values, nbinsx=60,
                marker_color="rgba(99,102,241,0.5)",
                marker_line=dict(width=0.5, color="rgba(129,140,248,0.6)"),
                hovertemplate="Value: $%{x:,.0f}<br>Count: %{y}<extra></extra>",
            ))
            fig_hist.add_vline(x=median_val, line_dash="dash", line_color=GREEN,
                               annotation_text="Median", annotation_font_color=GREEN)
            fig_hist.add_vline(x=p_lo, line_dash="dot", line_color=RED,
                               annotation_text=f"{ci_lo:.0f}th", annotation_font_color=RED)
            fig_hist.add_vline(x=p_hi, line_dash="dot", line_color=ACCENT_LIGHT,
                               annotation_text=f"{ci_hi:.0f}th", annotation_font_color=ACCENT_LIGHT)
            fig_hist.add_vline(x=total_invested, line_dash="dash",
                               line_color="rgba(148,163,184,0.4)",
                               annotation_text="Invested", annotation_font_color="#64748b")

            fig_hist.update_layout(
                **PLOTLY_LAYOUT,
                title="Distribution of Final Portfolio Values",
                xaxis=dict(title="Final Value ($)", gridcolor=GRID_COLOR,
                           tickprefix="$", separatethousands=True),
                yaxis=dict(title="Frequency", gridcolor=GRID_COLOR),
                bargap=0.03,
                height=480,
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        with col_box:
            fig_box = go.Figure()
            fig_box.add_trace(go.Box(
                y=final_values,
                marker_color=ACCENT,
                line_color=ACCENT_LIGHT,
                fillcolor="rgba(99,102,241,0.15)",
                boxmean="sd",
                name="Final Values",
            ))
            fig_box.update_layout(
                **PLOTLY_LAYOUT,
                title="Box Plot",
                yaxis=dict(title="Value ($)", gridcolor=GRID_COLOR,
                           tickprefix="$", separatethousands=True),
                height=480,
                showlegend=False,
            )
            st.plotly_chart(fig_box, use_container_width=True)

        # CDF
        sorted_vals = np.sort(final_values)
        cdf = np.arange(1, len(sorted_vals) + 1) / len(sorted_vals)
        fig_cdf = go.Figure()
        fig_cdf.add_trace(go.Scatter(
            x=sorted_vals, y=cdf, mode="lines",
            line=dict(width=2.5, color=ACCENT),
            fill="tozeroy", fillcolor="rgba(99,102,241,0.08)",
            hovertemplate="Value: $%{x:,.0f}<br>Cum. Prob: %{y:.1%}<extra></extra>",
        ))
        fig_cdf.add_hline(y=0.5, line_dash="dash", line_color="rgba(148,163,184,0.25)")
        fig_cdf.add_vline(x=total_invested, line_dash="dash",
                           line_color="rgba(148,163,184,0.3)",
                           annotation_text="Invested", annotation_font_color="#64748b")
        fig_cdf.update_layout(
            **PLOTLY_LAYOUT,
            title="Cumulative Distribution Function (CDF)",
            xaxis=dict(title="Final Value ($)", gridcolor=GRID_COLOR,
                       tickprefix="$", separatethousands=True),
            yaxis=dict(title="Cumulative Probability", gridcolor=GRID_COLOR,
                       tickformat=".0%"),
            height=380,
        )
        st.plotly_chart(fig_cdf, use_container_width=True)

    # ═══════════════════════════════════════════
    # TAB 3 — Statistics Table
    # ═══════════════════════════════════════════
    with tab_stats:
        st.markdown("#### 📋 Detailed Statistical Summary")

        percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
        pct_vals = [np.percentile(final_values, p) for p in percentiles]
        pct_returns = [(v / total_invested - 1) * 100 for v in pct_vals]

        stats_df = pd.DataFrame({
            "Percentile": [f"{p}th" for p in percentiles],
            "Final Value": [fmt_dollar(v) for v in pct_vals],
            "Total Return": [fmt_pct(r) for r in pct_returns],
            "Annualized Return": [
                fmt_pct(((v / params["initial"]) ** (1 / params["years"]) - 1) * 100)
                if v > 0 else "N/A"
                for v in pct_vals
            ],
        })
        st.dataframe(stats_df, use_container_width=True, hide_index=True)

        st.markdown("")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("#### Risk Metrics")
            # Value at Risk
            var_95 = total_invested - np.percentile(final_values, 5)
            var_99 = total_invested - np.percentile(final_values, 1)
            cvar_95_vals = final_values[final_values <= np.percentile(final_values, 5)]
            cvar_95 = total_invested - np.mean(cvar_95_vals) if len(cvar_95_vals) > 0 else 0

            risk_data = {
                "Metric": [
                    "Value at Risk (95%)",
                    "Value at Risk (99%)",
                    "Conditional VaR (95%)",
                    "Max Simulated Loss",
                    "Std Dev of Final Values",
                    "Skewness",
                    "Kurtosis",
                ],
                "Value": [
                    fmt_dollar(var_95),
                    fmt_dollar(var_99),
                    fmt_dollar(cvar_95),
                    fmt_dollar(max(0, total_invested - min_val)),
                    fmt_dollar(np.std(final_values)),
                    f"{pd.Series(final_values).skew():.3f}",
                    f"{pd.Series(final_values).kurtosis():.3f}",
                ],
            }
            st.dataframe(pd.DataFrame(risk_data), use_container_width=True, hide_index=True)

        with col_s2:
            st.markdown("#### Return Metrics")
            median_annual = (median_val / params["initial"]) ** (1 / params["years"]) - 1
            mean_annual = (mean_val / params["initial"]) ** (1 / params["years"]) - 1

            return_data = {
                "Metric": [
                    "Mean Final Value",
                    "Median Final Value",
                    "Mean Annualized Return",
                    "Median Annualized Return",
                    "Probability of Profit",
                    "Probability of Doubling",
                    "Probability of Loss > 20%",
                ],
                "Value": [
                    fmt_dollar(mean_val),
                    fmt_dollar(median_val),
                    fmt_pct(mean_annual * 100),
                    fmt_pct(median_annual * 100),
                    f"{prob_profit:.1f}%",
                    f"{prob_double:.1f}%",
                    f"{np.mean(final_values < total_invested * 0.8) * 100:.1f}%",
                ],
            }
            st.dataframe(pd.DataFrame(return_data), use_container_width=True, hide_index=True)

    # ═══════════════════════════════════════════
    # TAB 4 — Drawdown Analysis
    # ═══════════════════════════════════════════
    with tab_drawdown:
        st.markdown("#### 📉 Maximum Drawdown Analysis")

        # Compute drawdown for median path
        median_path = np.median(data, axis=1)
        running_max = np.maximum.accumulate(median_path)
        drawdown_pct = (median_path - running_max) / running_max * 100

        fig_dd = go.Figure()
        fig_dd.add_trace(go.Scatter(
            x=x_years, y=drawdown_pct, mode="lines",
            line=dict(width=2, color=RED),
            fill="tozeroy", fillcolor="rgba(248, 113, 113, 0.1)",
            hovertemplate="Year: %{x:.1f}<br>Drawdown: %{y:.1f}%<extra></extra>",
            name="Median Path Drawdown",
        ))
        fig_dd.update_layout(
            **PLOTLY_LAYOUT,
            title="Drawdown from Peak — Median Path",
            xaxis=dict(title="Years", gridcolor=GRID_COLOR),
            yaxis=dict(title="Drawdown (%)", gridcolor=GRID_COLOR, ticksuffix="%"),
            height=360,
        )
        st.plotly_chart(fig_dd, use_container_width=True)

        # Max drawdown distribution across all sims
        max_drawdowns = []
        for i in range(data.shape[1]):
            rm = np.maximum.accumulate(data[:, i])
            dd = (data[:, i] - rm) / rm
            max_drawdowns.append(np.min(dd) * 100)
        max_drawdowns = np.array(max_drawdowns)

        fig_mdd = go.Figure()
        fig_mdd.add_trace(go.Histogram(
            x=max_drawdowns, nbinsx=50,
            marker_color="rgba(248, 113, 113, 0.45)",
            marker_line=dict(width=0.5, color="rgba(248,113,113,0.7)"),
            hovertemplate="Max DD: %{x:.1f}%<br>Count: %{y}<extra></extra>",
        ))
        fig_mdd.add_vline(x=np.median(max_drawdowns), line_dash="dash",
                           line_color=AMBER,
                           annotation_text=f"Median: {np.median(max_drawdowns):.1f}%",
                           annotation_font_color=AMBER)
        fig_mdd.update_layout(
            **PLOTLY_LAYOUT,
            title="Distribution of Maximum Drawdowns Across All Simulations",
            xaxis=dict(title="Max Drawdown (%)", gridcolor=GRID_COLOR, ticksuffix="%"),
            yaxis=dict(title="Frequency", gridcolor=GRID_COLOR),
            height=380,
        )
        st.plotly_chart(fig_mdd, use_container_width=True)

        c_dd1, c_dd2, c_dd3 = st.columns(3)
        with c_dd1:
            st.metric("Median Max Drawdown", f"{np.median(max_drawdowns):.1f}%")
        with c_dd2:
            st.metric("Worst Max Drawdown", f"{np.min(max_drawdowns):.1f}%")
        with c_dd3:
            st.metric("Avg Max Drawdown", f"{np.mean(max_drawdowns):.1f}%")

    # ── Footer ──
    st.markdown("---")
    st.markdown(
        '<div class="footer">'
        'Monte Carlo Portfolio Simulator &nbsp;·&nbsp; '
        'Powered by Geometric Brownian Motion &nbsp;·&nbsp; '
        f'{params["sims"]:,} simulations &nbsp;·&nbsp; {params["years"]} year horizon'
        '</div>',
        unsafe_allow_html=True,
    )
