"""Reusable HTML components for the redesigned dashboard."""

from __future__ import annotations

import html
import uuid

import streamlit as st
import streamlit.components.v1 as components


TONE_COLORS = {
    "cyan": "#22d3ee",
    "blue": "#60a5fa",
    "violet": "#a78bfa",
    "emerald": "#34d399",
    "amber": "#fbbf24",
    "red": "#fb7185",
}


def _safe(value: object) -> str:
    return html.escape(str(value))


def hero(title: str, eyebrow: str, body: str, pill: str) -> None:
    """Render the top dashboard header."""
    st.markdown(
        f"""
<div class="app-shell">
    <div class="topline">
        <div>
            <div class="eyebrow">{_safe(eyebrow)}</div>
            <h1>{_safe(title)}</h1>
            <p>{_safe(body)}</p>
        </div>
        <div class="status-pill">{_safe(pill)}</div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )


def auto_expand_sidebar_on_load() -> None:
    """Open Streamlit's sidebar once per page boot if the browser restores it collapsed."""
    components.html(
        """
<!doctype html>
<html>
<body>
<script>
(function () {
    const doc = window.parent.document;
    const marker = "retentionSidebarAutoOpened";

    function isSidebarOpen() {
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (!sidebar) return false;
        const rect = sidebar.getBoundingClientRect();
        const styles = window.parent.getComputedStyle(sidebar);
        return rect.width > 160 && styles.visibility !== "hidden" && styles.display !== "none";
    }

    function openSidebarIfNeeded() {
        if (doc.body.dataset[marker] === "true") return;
        if (isSidebarOpen()) {
            doc.body.dataset[marker] = "true";
            return;
        }

        const selectors = [
            'button[aria-label="Open sidebar"]',
            'button[title="Open sidebar"]',
            '[data-testid="stSidebarCollapsedControl"] button'
        ];
        const opener = selectors.map((selector) => doc.querySelector(selector)).find(Boolean);
        if (opener) {
            opener.click();
            doc.body.dataset[marker] = "true";
        }
    }

    [120, 450, 900, 1400].forEach((delay) => {
        window.setTimeout(openSidebarIfNeeded, delay);
    });
})();
</script>
</body>
</html>
""",
        height=0,
        scrolling=False,
    )


def section_heading(title: str, subtitle: str | None = None) -> None:
    """Render a compact section heading."""
    subtitle_html = f'<p class="section-subtitle">{_safe(subtitle)}</p>' if subtitle else ""
    st.markdown(
        f"""
<div>
    <h3 class="section-title">{_safe(title)}</h3>
    {subtitle_html}
</div>
""",
        unsafe_allow_html=True,
    )


def animated_metric(
    label: str,
    value: float,
    *,
    prefix: str = "",
    suffix: str = "",
    decimals: int = 0,
    caption: str = "",
    tone: str = "cyan",
    height: int = 132,
) -> None:
    """Render a glass metric card with a JavaScript count-up animation."""
    target_id = f"metric_{uuid.uuid4().hex}"
    color = TONE_COLORS.get(tone, TONE_COLORS["cyan"])
    safe_label = _safe(label)
    safe_prefix = _safe(prefix)
    safe_suffix = _safe(suffix)
    safe_caption = _safe(caption)
    components.html(
        f"""
<!doctype html>
<html>
<head>
<style>
html, body {{
    margin: 0;
    background: transparent;
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}
.card {{
    box-sizing: border-box;
    height: {height - 6}px;
    padding: 16px 16px 14px;
    border-radius: 8px;
    border: 1px solid rgba(148, 163, 184, 0.18);
    background:
        linear-gradient(135deg, rgba(15, 30, 52, 0.86), rgba(7, 19, 36, 0.72)),
        linear-gradient(90deg, rgba(34, 211, 238, 0.08), rgba(167, 139, 250, 0.05));
    color: #eef6ff;
    box-shadow: 0 18px 55px rgba(0, 0, 0, 0.23), inset 0 1px 0 rgba(255,255,255,0.04);
    overflow: hidden;
    position: relative;
    animation: rise 560ms cubic-bezier(.2,.8,.2,1) both;
    transition: transform 160ms ease, border-color 160ms ease, box-shadow 160ms ease;
}}
.card:hover {{
    transform: translateY(-2px);
    border-color: color-mix(in srgb, {color} 45%, rgba(148, 163, 184, 0.2));
    box-shadow: 0 24px 72px rgba(0, 0, 0, 0.30);
}}
.card:before {{
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.07), transparent);
    transform: translateX(-100%);
    animation: shimmer 1.65s 120ms ease-out 1;
}}
.label {{
    color: #91a7c2;
    font-size: 12px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 800;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}
.value {{
    margin-top: 10px;
    font-size: clamp(28px, 6vw, 42px);
    line-height: 1;
    letter-spacing: 0;
    font-weight: 900;
    color: #eef6ff;
}}
.accent {{
    width: 42px;
    height: 3px;
    border-radius: 999px;
    background: {color};
    box-shadow: 0 0 24px {color};
    margin-top: 12px;
}}
.caption {{
    margin-top: 10px;
    color: #b8c7db;
    font-size: 12px;
    line-height: 1.35;
}}
@keyframes rise {{
    from {{ opacity: 0; transform: translateY(12px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes shimmer {{
    to {{ transform: translateX(100%); }}
}}
</style>
</head>
<body>
<div class="card">
    <div class="label">{safe_label}</div>
    <div class="value"><span id="{target_id}">0</span></div>
    <div class="accent"></div>
    <div class="caption">{safe_caption}</div>
</div>
<script>
const el = document.getElementById("{target_id}");
const target = Number({float(value):.10f});
const decimals = Number({int(decimals)});
const prefix = "{safe_prefix}";
const suffix = "{safe_suffix}";
const start = performance.now();
const duration = 1100;
function formatNumber(v) {{
    const opts = {{
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    }};
    return prefix + new Intl.NumberFormat("en-US", opts).format(v) + suffix;
}}
function easeOutCubic(t) {{
    return 1 - Math.pow(1 - t, 3);
}}
function step(now) {{
    const t = Math.min((now - start) / duration, 1);
    el.textContent = formatNumber(target * easeOutCubic(t));
    if (t < 1) requestAnimationFrame(step);
}}
requestAnimationFrame(step);
</script>
</body>
</html>
""",
        height=height,
        scrolling=False,
    )


def status_card(title: str, value: str, caption: str, *, tone: str = "cyan") -> None:
    """Render a non-numeric status card."""
    color = TONE_COLORS.get(tone, TONE_COLORS["cyan"])
    st.markdown(
        f"""
<div class="detail-card" style="border-left: 3px solid {color}; min-height: 132px;">
    <h4>{_safe(title)}</h4>
    <div style="font-size:2rem; font-weight:900; color:#eef6ff; line-height:1.1;">{_safe(value)}</div>
    <p style="margin-top:12px;">{_safe(caption)}</p>
</div>
""",
        unsafe_allow_html=True,
    )


def animated_gauge(probability: float, risk_label: str, *, height: int = 350) -> None:
    """Render an animated semi-circle gauge for churn probability."""
    score = max(0.0, min(100.0, probability * 100))
    angle = -90 + (score / 100) * 180
    if score >= 60:
        color = TONE_COLORS["red"]
    elif score >= 35:
        color = TONE_COLORS["amber"]
    else:
        color = TONE_COLORS["emerald"]

    components.html(
        f"""
<!doctype html>
<html>
<head>
<style>
html, body {{
    margin: 0;
    background: transparent;
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}
.wrap {{
    box-sizing: border-box;
    height: {height - 6}px;
    border-radius: 8px;
    border: 1px solid rgba(148, 163, 184, 0.18);
    background: linear-gradient(135deg, rgba(15, 30, 52, 0.86), rgba(7, 19, 36, 0.72));
    box-shadow: 0 18px 55px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.04);
    padding: 18px;
    color: #eef6ff;
    animation: rise 560ms cubic-bezier(.2,.8,.2,1) both;
}}
.title {{
    color: #91a7c2;
    text-transform: uppercase;
    letter-spacing: .08em;
    font-size: 12px;
    font-weight: 800;
}}
.gauge {{
    position: relative;
    margin: 16px auto 0;
    width: min(100%, 430px);
    aspect-ratio: 2 / 1;
    overflow: hidden;
}}
.ring {{
    position: absolute;
    inset: 0;
    width: 100%;
    aspect-ratio: 1 / 1;
    border-radius: 50%;
    background:
        conic-gradient(from 270deg,
            #34d399 0deg 63deg,
            #fbbf24 63deg 108deg,
            #fb7185 108deg 180deg,
            rgba(148,163,184,0.13) 180deg 360deg);
    box-shadow: inset 0 0 38px rgba(255,255,255,0.04);
}}
.ring::after {{
    content: "";
    position: absolute;
    inset: 13%;
    border-radius: 50%;
    background: #081527;
    border: 1px solid rgba(148, 163, 184, 0.14);
}}
.needle {{
    position: absolute;
    left: 50%;
    bottom: 0;
    width: 4px;
    height: 78%;
    background: linear-gradient(to top, #eef6ff, {color});
    border-radius: 999px;
    transform-origin: 50% 100%;
    transform: rotate(-90deg);
    animation: sweep 1.15s cubic-bezier(.16, 1, .3, 1) forwards;
    box-shadow: 0 0 24px {color};
    z-index: 3;
}}
.hub {{
    position: absolute;
    left: calc(50% - 13px);
    bottom: -13px;
    width: 26px;
    height: 26px;
    border-radius: 50%;
    background: #eef6ff;
    border: 5px solid #081527;
    box-shadow: 0 0 28px rgba(34, 211, 238, 0.3);
    z-index: 4;
}}
.readout {{
    text-align: center;
    margin-top: 12px;
}}
.value {{
    font-size: clamp(42px, 8vw, 70px);
    line-height: 1;
    font-weight: 950;
    letter-spacing: 0;
}}
.risk {{
    margin-top: 8px;
    display: inline-flex;
    padding: 7px 12px;
    border-radius: 999px;
    background: color-mix(in srgb, {color} 18%, transparent);
    border: 1px solid color-mix(in srgb, {color} 44%, transparent);
    color: #eef6ff;
    font-weight: 800;
    font-size: 12px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}}
.ticks {{
    display: flex;
    justify-content: space-between;
    max-width: 430px;
    margin: 8px auto 0;
    color: #8ea3bd;
    font-size: 12px;
}}
@keyframes sweep {{
    to {{ transform: rotate({angle:.2f}deg); }}
}}
@keyframes rise {{
    from {{ opacity: 0; transform: translateY(12px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
</style>
</head>
<body>
<div class="wrap">
    <div class="title">Churn Risk Gauge</div>
    <div class="gauge">
        <div class="ring"></div>
        <div class="needle"></div>
        <div class="hub"></div>
    </div>
    <div class="ticks"><span>0%</span><span>35%</span><span>60%</span><span>100%</span></div>
    <div class="readout">
        <div class="value"><span id="gauge_value">0.0</span>%</div>
        <div class="risk">{_safe(risk_label)}</div>
    </div>
</div>
<script>
const el = document.getElementById("gauge_value");
const target = {score:.8f};
const start = performance.now();
const duration = 1120;
function easeOutCubic(t) {{
    return 1 - Math.pow(1 - t, 3);
}}
function step(now) {{
    const t = Math.min((now - start) / duration, 1);
    el.textContent = (target * easeOutCubic(t)).toFixed(1);
    if (t < 1) requestAnimationFrame(step);
}}
requestAnimationFrame(step);
</script>
</body>
</html>
""",
        height=height,
        scrolling=False,
    )


def recommendation_cards(actions: list[str], *, tone: str) -> None:
    """Render recommendation action cards."""
    tone_class = {"red": "risk-high", "amber": "risk-medium", "emerald": "risk-low"}.get(tone, "")
    cards = "\n".join(
        f"""
<div class="detail-card recommendation {tone_class}">
    <h4>Action {index}</h4>
    <p>{_safe(action)}</p>
</div>
"""
        for index, action in enumerate(actions, start=1)
    )
    st.markdown(f'<div class="inline-grid">{cards}</div>', unsafe_allow_html=True)


def insight_card(title: str, body: str, *, color: str = "#22d3ee") -> None:
    """Render a compact insight callout."""
    st.markdown(
        f"""
<div class="detail-card" style="border-left: 3px solid {color};">
    <h4>{_safe(title)}</h4>
    <p>{body}</p>
</div>
""",
        unsafe_allow_html=True,
    )
