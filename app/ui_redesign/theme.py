"""Visual theme utilities for the redesigned Streamlit app."""

from __future__ import annotations

import streamlit as st


COLORS = {
    "bg": "#07111f",
    "panel": "rgba(10, 20, 38, 0.72)",
    "panel_soft": "rgba(15, 30, 52, 0.54)",
    "stroke": "rgba(148, 163, 184, 0.18)",
    "muted": "#8ea3bd",
    "text": "#eef6ff",
    "cyan": "#22d3ee",
    "blue": "#60a5fa",
    "violet": "#a78bfa",
    "emerald": "#34d399",
    "amber": "#fbbf24",
    "red": "#fb7185",
}

SEGMENT_COLORS = {
    "At-Risk Churners": "#fb7185",
    "High-Value Loyalists": "#34d399",
    "New Potentials": "#fbbf24",
}


def apply_theme() -> None:
    """Inject global CSS for the premium dark dashboard."""
    st.markdown(
        f"""
<style>
:root {{
    --bg: {COLORS["bg"]};
    --panel: {COLORS["panel"]};
    --panel-soft: {COLORS["panel_soft"]};
    --stroke: {COLORS["stroke"]};
    --text: {COLORS["text"]};
    --muted: {COLORS["muted"]};
    --cyan: {COLORS["cyan"]};
    --blue: {COLORS["blue"]};
    --violet: {COLORS["violet"]};
    --emerald: {COLORS["emerald"]};
    --amber: {COLORS["amber"]};
    --red: {COLORS["red"]};
}}

html, body, [class*="css"] {{
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}

.stApp {{
    color: var(--text);
    background:
        linear-gradient(135deg, #07111f 0%, #0c1b30 28%, #121a38 56%, #071c25 100%),
        linear-gradient(90deg, rgba(34, 211, 238, 0.08), rgba(167, 139, 250, 0.06));
}}

.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    opacity: 0.22;
    background-image:
        linear-gradient(rgba(148, 163, 184, 0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(148, 163, 184, 0.08) 1px, transparent 1px);
    background-size: 56px 56px;
    mask-image: linear-gradient(to bottom, rgba(0,0,0,0.9), rgba(0,0,0,0.2));
}}

section.main > div {{
    position: relative;
    z-index: 1;
}}

.block-container {{
    max-width: 1440px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}}

section[data-testid="stSidebar"] {{
    background: rgba(5, 11, 24, 0.92);
    border-right: 1px solid var(--stroke);
}}

section[data-testid="stSidebar"] > div {{
    padding-top: 1.35rem;
}}

section[data-testid="stSidebar"] * {{
    color: var(--text);
}}

h1, h2, h3, h4, h5, h6 {{
    color: var(--text) !important;
    letter-spacing: 0;
}}

p, label, span {{
    color: inherit;
}}

[data-testid="stMarkdownContainer"] p {{
    color: #c8d7eb;
}}

.app-shell {{
    animation: fade-in-up 520ms cubic-bezier(.2,.8,.2,1) both;
}}

.topline {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    padding: 18px 20px;
    margin-bottom: 18px;
    border: 1px solid var(--stroke);
    border-radius: 8px;
    background: linear-gradient(135deg, rgba(13, 27, 48, 0.88), rgba(10, 24, 36, 0.72));
    box-shadow: 0 22px 70px rgba(0, 0, 0, 0.28);
}}

.topline h1 {{
    margin: 0;
    font-size: clamp(2rem, 4vw, 3.5rem);
    line-height: 1;
    letter-spacing: 0;
}}

.topline p {{
    margin: 8px 0 0 0;
    max-width: 760px;
    color: #b8c7db;
    font-size: 1rem;
}}

.eyebrow {{
    color: var(--cyan);
    font-size: 0.78rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-weight: 800;
}}

.status-pill {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    white-space: nowrap;
    border: 1px solid rgba(34, 211, 238, 0.3);
    background: rgba(34, 211, 238, 0.1);
    color: #dffcff;
    border-radius: 999px;
    padding: 8px 12px;
    font-size: 0.78rem;
    font-weight: 700;
}}

.surface {{
    border: 1px solid var(--stroke);
    border-radius: 8px;
    background: var(--panel);
    box-shadow: 0 18px 60px rgba(0, 0, 0, 0.24);
    backdrop-filter: blur(18px);
    padding: 20px;
    margin: 14px 0 20px 0;
    animation: fade-in-up 560ms cubic-bezier(.2,.8,.2,1) both;
}}

.section-title {{
    margin: 0 0 12px 0;
    color: var(--text);
    font-size: 1.02rem;
    font-weight: 800;
}}

.section-subtitle {{
    margin: -4px 0 14px 0;
    color: var(--muted);
    font-size: 0.92rem;
}}

.inline-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 12px;
}}

.detail-card {{
    border: 1px solid var(--stroke);
    border-radius: 8px;
    background: rgba(15, 30, 52, 0.62);
    padding: 16px;
    min-height: 112px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
    animation: fade-in-up 540ms cubic-bezier(.2,.8,.2,1) both;
    transition: transform 160ms ease, border-color 160ms ease, background 160ms ease;
}}

.detail-card:hover {{
    transform: translateY(-2px);
    border-color: rgba(34, 211, 238, 0.34);
    background: rgba(18, 38, 64, 0.72);
}}

.detail-card h4 {{
    margin: 0 0 8px 0;
    font-size: 0.98rem;
}}

.detail-card p {{
    margin: 0;
    color: #b8c7db;
    line-height: 1.55;
    font-size: 0.9rem;
}}

.recommendation {{
    border-left: 3px solid var(--cyan);
}}

.risk-high {{ border-left-color: var(--red); }}
.risk-medium {{ border-left-color: var(--amber); }}
.risk-low {{ border-left-color: var(--emerald); }}

.sidebar-brand {{
    border: 1px solid var(--stroke);
    border-radius: 8px;
    padding: 14px;
    background: rgba(15, 30, 52, 0.68);
    margin-bottom: 14px;
}}

.sidebar-brand .name {{
    color: var(--text);
    font-weight: 900;
    font-size: 1rem;
    line-height: 1.2;
}}

.sidebar-brand .meta {{
    color: var(--muted);
    font-size: 0.78rem;
    margin-top: 8px;
    line-height: 1.45;
}}

div[data-testid="stForm"] {{
    border: 1px solid var(--stroke);
    border-radius: 8px;
    background: rgba(10, 20, 38, 0.68);
    padding: 20px;
    box-shadow: 0 18px 60px rgba(0,0,0,0.22);
}}

div[data-baseweb="select"] > div,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {{
    color: var(--text) !important;
    background: rgba(5, 12, 24, 0.88) !important;
    border-color: rgba(148, 163, 184, 0.22) !important;
    border-radius: 8px !important;
}}

div[data-testid="stSlider"] [data-baseweb="slider"] > div {{
    color: var(--cyan);
}}

.stButton > button,
button[kind="primaryFormSubmit"] {{
    width: 100%;
    color: #06111f !important;
    background: linear-gradient(135deg, #67e8f9 0%, #93c5fd 48%, #c4b5fd 100%) !important;
    border: 0 !important;
    border-radius: 8px !important;
    min-height: 46px;
    font-weight: 900 !important;
    box-shadow: 0 16px 38px rgba(34, 211, 238, 0.22);
    transition: transform 160ms ease, box-shadow 160ms ease, filter 160ms ease;
}}

.stButton > button:hover,
button[kind="primaryFormSubmit"]:hover {{
    transform: translateY(-2px);
    filter: brightness(1.05);
    box-shadow: 0 22px 56px rgba(96, 165, 250, 0.28);
}}

.stButton > button:active,
button[kind="primaryFormSubmit"]:active {{
    transform: translateY(0);
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
    border-bottom: 1px solid var(--stroke);
}}

.stTabs [data-baseweb="tab"] {{
    height: 42px;
    border-radius: 8px 8px 0 0;
    background: rgba(15, 30, 52, 0.48);
    border: 1px solid rgba(148, 163, 184, 0.12);
    color: #aac0d8;
    padding-inline: 16px;
}}

.stTabs [aria-selected="true"] {{
    background: rgba(34, 211, 238, 0.14);
    color: var(--text) !important;
    border-color: rgba(34, 211, 238, 0.34);
}}

div[data-testid="stDataFrame"] {{
    border: 1px solid var(--stroke);
    border-radius: 8px;
    overflow: hidden;
}}

details {{
    border: 1px solid var(--stroke) !important;
    border-radius: 8px !important;
    background: rgba(10, 20, 38, 0.7) !important;
}}

hr {{
    border-color: var(--stroke) !important;
}}

.shimmer {{
    position: relative;
    overflow: hidden;
}}

.shimmer::after {{
    content: "";
    position: absolute;
    inset: 0;
    transform: translateX(-100%);
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    animation: shimmer 1.55s infinite;
}}

#MainMenu, footer {{
    visibility: hidden;
}}

header[data-testid="stHeader"] {{
    visibility: visible;
    background: transparent;
    backdrop-filter: none;
    pointer-events: none;
}}

div[data-testid="stToolbar"] {{
    visibility: visible;
    pointer-events: auto;
}}

header[data-testid="stHeader"] button,
header[data-testid="stHeader"] a {{
    pointer-events: auto;
}}

[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {{
    display: none;
}}

button[title="Open sidebar"],
button[title="Close sidebar"],
button[aria-label="Open sidebar"],
button[aria-label="Close sidebar"],
[data-testid="stSidebarCollapseButton"] button,
[data-testid="stSidebarCollapsedControl"] button {{
    visibility: visible !important;
    pointer-events: auto !important;
    color: var(--text) !important;
    background: rgba(10, 20, 38, 0.88) !important;
    border: 1px solid rgba(34, 211, 238, 0.28) !important;
    border-radius: 8px !important;
    box-shadow: 0 12px 32px rgba(0,0,0,0.26), 0 0 22px rgba(34,211,238,0.12);
    transition: transform 160ms ease, border-color 160ms ease, background 160ms ease;
}}

button[title="Open sidebar"]:hover,
button[title="Close sidebar"]:hover,
button[aria-label="Open sidebar"]:hover,
button[aria-label="Close sidebar"]:hover,
[data-testid="stSidebarCollapseButton"] button:hover,
[data-testid="stSidebarCollapsedControl"] button:hover {{
    transform: translateY(-1px);
    border-color: rgba(34, 211, 238, 0.46) !important;
    background: rgba(15, 30, 52, 0.94) !important;
}}

@keyframes fade-in-up {{
    from {{ opacity: 0; transform: translateY(14px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes shimmer {{
    100% {{ transform: translateX(100%); }}
}}

@media (max-width: 780px) {{
    .topline {{
        flex-direction: column;
        align-items: flex-start;
        padding: 16px;
    }}
    .topline h1 {{
        font-size: 2rem;
    }}
    .surface {{
        padding: 16px;
    }}
}}
</style>
""",
        unsafe_allow_html=True,
    )


def chart_layout(height: int = 420) -> dict:
    """Shared Plotly layout values."""
    return {
        "height": height,
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(6, 16, 31, 0.28)",
        "font": {"color": COLORS["text"], "family": "Inter, sans-serif"},
        "margin": {"t": 54, "b": 36, "l": 52, "r": 24},
        "legend": {
            "bgcolor": "rgba(0,0,0,0)",
            "font": {"color": "#c8d7eb", "size": 12},
        },
    }
