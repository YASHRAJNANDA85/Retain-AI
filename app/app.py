"""
Premium Streamlit dashboard redesign for Customer Segmentation & Retention Analysis.

This file is intentionally independent from app/streamlit_app.py so the original
implementation remains untouched.
"""

from __future__ import annotations

import re
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from ui_redesign.components import (
    auto_expand_sidebar_on_load,
    animated_gauge,
    animated_metric,
    hero,
    insight_card,
    recommendation_cards,
    section_heading,
    status_card,
)
from ui_redesign.theme import COLORS, SEGMENT_COLORS, apply_theme, chart_layout


APP_DIR = Path(__file__).resolve().parent
BASE = APP_DIR.parent
SRC = BASE / "src"
DATA = BASE / "data" / "processed"

THRESHOLD = 0.44
SCALE_RANGES = {
    "tenure": (0, 72),
    "MonthlyCharges": (18.25, 118.75),
    "TotalCharges": (0, 8684.8),
}


st.set_page_config(
    page_title="RetainAI | Telco Churn Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()
auto_expand_sidebar_on_load()


def clean_segment_name(value: object) -> str:
    """Strip decorative symbols from segment labels while preserving the text."""
    text = str(value)
    for label in SEGMENT_COLORS:
        if label in text:
            return label
    text = re.sub(r"^[^\w]+", "", text).strip()
    return text or str(value)


def hex_to_rgba(hex_color: str, opacity: float = 0.16) -> str:
    """Convert a 6-digit hex color into an rgba string for Plotly fills."""
    value = str(hex_color).lstrip("#")
    if len(value) != 6:
        return str(hex_color)
    red, green, blue = (int(value[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({red}, {green}, {blue}, {opacity})"


def minmax_scale(value: float, column: str) -> float:
    """Scale raw input values to the original preprocessing range."""
    minimum, maximum = SCALE_RANGES[column]
    return (value - minimum) / (maximum - minimum) if maximum != minimum else 0.0


@st.cache_resource(show_spinner=False)
def load_models():
    """Load persisted model artifacts."""
    churn_model = joblib.load(SRC / "best_churn_model.pkl")
    if hasattr(churn_model, "feature_names_in_"):
        feature_cols = list(churn_model.feature_names_in_)
    else:
        feature_cols = list(joblib.load(SRC / "feature_columns.pkl"))
    kmeans_model = joblib.load(SRC / "kmeans_model.pkl")
    cluster_scaler = joblib.load(SRC / "cluster_scaler.pkl")
    cluster_features = list(cluster_scaler.feature_names_in_)
    return churn_model, feature_cols, kmeans_model, cluster_scaler, cluster_features


@st.cache_data(show_spinner=False)
def load_data():
    """Load processed app datasets."""
    segmented = pd.read_csv(DATA / "telco_segmented.csv")
    clv = pd.read_csv(DATA / "telco_clv.csv")
    segmented["segment_clean"] = segmented["segment_name"].map(clean_segment_name)
    clv["segment_clean"] = clv["Cluster"].map(clean_segment_name)
    return segmented, clv


model, FEATURE_COLS, kmeans, cluster_scaler, cluster_features = load_models()
seg_df, clv_df = load_data()


def segment_color_map(values: pd.Series | list[str]) -> dict[str, str]:
    """Map actual dataset labels to the theme colors."""
    mapping: dict[str, str] = {}
    for value in values:
        clean = clean_segment_name(value)
        mapping[str(value)] = SEGMENT_COLORS.get(clean, COLORS["blue"])
    return mapping


def preprocess_input(inputs: dict) -> pd.DataFrame:
    """Convert raw user inputs into the feature vector expected by the model."""
    gender = 1 if inputs["gender"] == "Male" else 0
    senior = inputs["senior_citizen"]
    partner = 1 if inputs["partner"] == "Yes" else 0
    dependents = 1 if inputs["dependents"] == "Yes" else 0
    phone = 1 if inputs["phone_service"] == "Yes" else 0
    paperless = 1 if inputs["paperless_billing"] == "Yes" else 0

    service_cols = [
        "multiple_lines",
        "online_security",
        "online_backup",
        "device_protection",
        "tech_support",
        "streaming_tv",
        "streaming_movies",
    ]
    service_values = [1 if inputs[column] == "Yes" else 0 for column in service_cols]
    (
        multiple_lines,
        online_security,
        online_backup,
        device_protection,
        tech_support,
        streaming_tv,
        streaming_movies,
    ) = service_values

    tenure_raw = inputs["tenure"]
    monthly_raw = inputs["monthly_charges"]
    total_raw = inputs["total_charges"]

    internet = inputs["internet_service"]
    internet_dsl = 1 if internet == "DSL" else 0
    internet_fiber = 1 if internet == "Fiber optic" else 0
    internet_no = 1 if internet == "No" else 0

    contract = inputs["contract"]
    contract_month = 1 if contract == "Month-to-month" else 0
    contract_one_year = 1 if contract == "One year" else 0
    contract_two_year = 1 if contract == "Two year" else 0

    payment = inputs["payment_method"]
    payment_bank = 1 if payment == "Bank transfer (automatic)" else 0
    payment_card = 1 if payment == "Credit card (automatic)" else 0
    payment_echeck = 1 if payment == "Electronic check" else 0
    payment_mail = 1 if payment == "Mailed check" else 0

    charge_per_month = monthly_raw if tenure_raw == 0 else total_raw / tenure_raw
    services_count = sum(service_values)
    contract_risk = contract_month * 2 + contract_one_year
    support_engagement = tech_support + online_security
    value_tier = 0 if monthly_raw <= 40 else (1 if monthly_raw <= 75 else 2)

    tenure_scaled = minmax_scale(tenure_raw, "tenure")
    monthly_scaled = minmax_scale(monthly_raw, "MonthlyCharges")
    total_scaled = minmax_scale(total_raw, "TotalCharges")
    charge_per_month_scaled = np.clip(charge_per_month / 118.75, 0, 1)

    row = {
        "gender": gender,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure_scaled,
        "PhoneService": phone,
        "MultipleLines": multiple_lines,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "PaperlessBilling": paperless,
        "MonthlyCharges": monthly_scaled,
        "TotalCharges": total_scaled,
        "InternetService_DSL": internet_dsl,
        "InternetService_Fiber optic": internet_fiber,
        "InternetService_No": internet_no,
        "Contract_Month-to-month": contract_month,
        "Contract_One year": contract_one_year,
        "Contract_Two year": contract_two_year,
        "PaymentMethod_Bank transfer (automatic)": payment_bank,
        "PaymentMethod_Credit card (automatic)": payment_card,
        "PaymentMethod_Electronic check": payment_echeck,
        "PaymentMethod_Mailed check": payment_mail,
        "charge_per_month_ratio": charge_per_month_scaled,
        "services_count": services_count,
        "contract_risk_score": contract_risk,
        "support_engagement": support_engagement,
        "value_tier": value_tier,
    }
    return pd.DataFrame([row])


def score_customer(inputs: dict) -> dict:
    """Score a customer and return model-ready artifacts for display."""
    raw_features = preprocess_input(inputs)
    cluster_matrix = pd.DataFrame(
        cluster_scaler.transform(raw_features[cluster_features]),
        columns=cluster_features,
    )
    cluster_label = int(kmeans.predict(cluster_matrix)[0])
    raw_features["cluster_label"] = cluster_label
    final_features = raw_features.reindex(columns=FEATURE_COLS, fill_value=0)
    probability = float(model.predict_proba(final_features)[0][1])

    segment_lookup = (
        seg_df.groupby("cluster_label")["segment_clean"]
        .agg(lambda values: values.mode().iat[0] if not values.mode().empty else str(values.iloc[0]))
        .to_dict()
    )
    segment = segment_lookup.get(cluster_label, f"Cluster {cluster_label}")
    segment_clv = clv_df.loc[clv_df["cluster_label"] == cluster_label, "CLV"].mean()

    return {
        "probability": probability,
        "prediction": "Will Churn" if probability >= THRESHOLD else "Will Stay",
        "risk_label": risk_details(probability)[0],
        "risk_tone": risk_details(probability)[1],
        "cluster_label": cluster_label,
        "segment": segment,
        "segment_clv": float(segment_clv) if pd.notna(segment_clv) else 0.0,
        "features": final_features,
        "raw_features": raw_features,
    }


def risk_details(probability: float) -> tuple[str, str]:
    """Return display label and tone for a churn probability."""
    if probability >= 0.60:
        return "High Risk", "red"
    if probability >= 0.35:
        return "Medium Risk", "amber"
    return "Low Risk", "emerald"


def recommendation_actions(probability: float) -> list[str]:
    """Return retention recommendations matching the risk band."""
    if probability >= 0.60:
        return [
            "Offer an annual-contract incentive with a targeted loyalty discount.",
            "Schedule a retention call within 48 hours and review open service issues.",
            "Bundle Tech Support or Online Security to increase service stickiness.",
            "Route the customer to a priority save workflow before renewal.",
        ]
    if probability >= 0.35:
        return [
            "Trigger proactive outreach with a personalized upgrade or bundle offer.",
            "Enroll the customer in a satisfaction pulse survey for early warning signals.",
            "Recommend support-heavy services that reduce churn vulnerability.",
        ]
    return [
        "Use low-touch monitoring and keep the customer in standard retention nurture.",
        "Consider premium-service upsell offers aligned to current usage patterns.",
        "Re-score next quarter or after any major billing or contract change.",
    ]


def style_chart(fig: go.Figure, *, height: int = 420, show_legend: bool = False) -> go.Figure:
    """Apply the app's chart styling."""
    fig.update_layout(**chart_layout(height))
    fig.update_layout(showlegend=show_legend, transition={"duration": 500, "easing": "cubic-in-out"})
    fig.update_xaxes(gridcolor="rgba(148, 163, 184, 0.10)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(148, 163, 184, 0.10)", zeroline=False)
    return fig


def sidebar() -> str:
    """Render sidebar navigation."""
    with st.sidebar:
        st.markdown(
            """
<div class="sidebar-brand">
    <div class="name">RetainAI</div>
    <div class="meta">Random Forest churn scoring, behavioral segmentation, and CLV intelligence.</div>
</div>
""",
            unsafe_allow_html=True,
        )
        page = st.radio(
            "Navigation",
            ["Churn Risk Studio", "Segment Command Center"],
            index=0,
        )
        st.markdown("---")
        st.markdown(
            f"""
<div class="detail-card">
    <h4>Model Snapshot</h4>
    <p>AUC 0.84<br>Recall 81.6%<br>Decision threshold {THRESHOLD:.2f}</p>
</div>
""",
            unsafe_allow_html=True,
        )
    return page


def render_churn_studio() -> None:
    """Render the churn prediction page."""
    hero(
        "Churn Risk Studio",
        "RetainAI  //  LIVE RETENTION SCORING",
        "Score individual customer profiles with the same preprocessing, clustering, and Random Forest workflow used in the project.",
        "Threshold tuned for recall",
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        animated_metric("Model AUC", 0.84, decimals=2, caption="Random Forest classifier", tone="cyan")
    with c2:
        animated_metric("Recall", 81.6, suffix="%", decimals=1, caption="Tuned churn capture", tone="emerald")
    with c3:
        animated_metric("Decision Threshold", THRESHOLD, decimals=2, caption="Recall-prioritized cutoff", tone="amber")
    with c4:
        animated_metric("Segments", 3, decimals=0, caption="Behavioral clusters", tone="violet")

    section_heading("Customer Inputs", "Enter a profile to produce a churn score, segment assignment, and retention playbook.")
    with st.form("premium_churn_form"):
        st.markdown('<div class="section-title">Customer Profile</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            gender = st.selectbox("Gender", ["Male", "Female"])
        with col2:
            senior = st.selectbox("Senior Citizen", [0, 1], format_func=lambda value: "Yes" if value else "No")
        with col3:
            partner = st.selectbox("Partner", ["Yes", "No"])
        with col4:
            dependents = st.selectbox("Dependents", ["Yes", "No"])

        st.markdown('<div class="section-title">Account Economics</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            tenure = st.slider("Tenure (months)", 0, 72, 12)
        with col2:
            monthly = st.slider("Monthly Charges ($)", 18.25, 118.75, 50.0, step=0.25)
        with col3:
            total = st.number_input(
                "Total Charges ($)",
                min_value=0.0,
                max_value=9000.0,
                value=float(tenure * monthly),
                step=10.0,
                help="Defaults to tenure multiplied by monthly charges.",
            )

        st.markdown('<div class="section-title">Contract and Billing</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        with col2:
            payment = st.selectbox(
                "Payment Method",
                [
                    "Electronic check",
                    "Mailed check",
                    "Bank transfer (automatic)",
                    "Credit card (automatic)",
                ],
            )
        with col3:
            paperless = st.selectbox("Paperless Billing", ["Yes", "No"])

        st.markdown('<div class="section-title">Services</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            phone_svc = st.selectbox("Phone Service", ["Yes", "No"])
            multi_ln = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
        with col2:
            internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
            security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
        with col3:
            backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
            device = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
        with col4:
            tech = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
            tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])

        streaming_mv = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
        submitted = st.form_submit_button("Predict Churn Risk", use_container_width=True)

    if not submitted:
        st.markdown(
            """
<div class="surface shimmer">
    <h3 class="section-title">Prediction Workspace</h3>
    <p class="section-subtitle">Submit a profile to reveal the animated risk gauge, segment context, and recommended actions.</p>
</div>
""",
            unsafe_allow_html=True,
        )
        return

    inputs = {
        "gender": gender,
        "senior_citizen": senior,
        "partner": partner,
        "dependents": dependents,
        "tenure": tenure,
        "monthly_charges": monthly,
        "total_charges": total,
        "contract": contract,
        "payment_method": payment,
        "paperless_billing": paperless,
        "phone_service": phone_svc,
        "internet_service": internet,
        "multiple_lines": multi_ln,
        "online_security": security,
        "online_backup": backup,
        "device_protection": device,
        "tech_support": tech,
        "streaming_tv": tv,
        "streaming_movies": streaming_mv,
    }
    result = score_customer(inputs)

    section_heading("Prediction Result", "The score combines customer inputs, cluster assignment, and the tuned churn model.")
    gauge_col, detail_col = st.columns([1.12, 1])
    with gauge_col:
        animated_gauge(result["probability"], result["risk_label"])
    with detail_col:
        k1, k2 = st.columns(2)
        with k1:
            animated_metric(
                "Churn Probability",
                result["probability"] * 100,
                suffix="%",
                decimals=1,
                caption="Predicted probability",
                tone=result["risk_tone"],
            )
        with k2:
            animated_metric(
                "Confidence",
                max(result["probability"], 1 - result["probability"]) * 100,
                suffix="%",
                decimals=1,
                caption="Distance from 50/50",
                tone="blue",
            )
        s1, s2 = st.columns(2)
        with s1:
            status_card("Prediction", result["prediction"], "Compared with the tuned 0.44 threshold.", tone=result["risk_tone"])
        with s2:
            status_card("Assigned Segment", result["segment"], f"Cluster {result['cluster_label']}", tone="violet")
        animated_metric(
            "Segment Avg CLV",
            result["segment_clv"],
            prefix="$",
            decimals=0,
            caption="Mean CLV for this assigned cluster",
            tone="emerald",
        )

    section_heading("Recommended Actions")
    recommendation_cards(recommendation_actions(result["probability"]), tone=result["risk_tone"])

    with st.expander("Model feature vector"):
        st.dataframe(result["features"].T.rename(columns={0: "Value"}), use_container_width=True)


def segment_profile() -> pd.DataFrame:
    """Build the segment profile table."""
    profile = (
        seg_df.groupby(["segment_name", "segment_clean"])
        .agg(
            customers=("Churn_Binary", "count"),
            churn_rate=("Churn_Binary", "mean"),
            avg_tenure=("tenure", "mean"),
            avg_monthly=("MonthlyCharges", "mean"),
            avg_services=("services_count", "mean"),
            avg_risk=("contract_risk_score", "mean"),
            avg_support=("support_engagement", "mean"),
        )
        .reset_index()
    )
    profile["pct"] = profile["customers"] / profile["customers"].sum() * 100
    profile["churn_rate_pct"] = profile["churn_rate"] * 100
    return profile.sort_values("customers", ascending=False)


def render_segment_command_center() -> None:
    """Render the segment explorer page."""
    hero(
        "Segment Command Center",
        "RetainAI  //  PORTFOLIO INTELLIGENCE",
        "Explore customer segments, churn concentration, lifetime value distribution, and the behavioral shape of each cluster.",
        "7,043 customer portfolio",
    )

    profile = segment_profile()
    total_clv = clv_df["CLV"].sum()
    top20_share = (
        clv_df.nlargest(max(int(len(clv_df) * 0.2), 1), "CLV")["CLV"].sum() / total_clv * 100
        if total_clv
        else 0
    )

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        animated_metric("Customers", len(seg_df), decimals=0, caption="Total modeled base", tone="cyan")
    with k2:
        animated_metric("Overall Churn", seg_df["Churn_Binary"].mean() * 100, suffix="%", decimals=1, caption="Observed churn rate", tone="red")
    with k3:
        animated_metric("Avg CLV", clv_df["CLV"].mean(), prefix="$", decimals=0, caption="Mean customer value", tone="emerald")
    with k4:
        animated_metric("Top 20% CLV", top20_share, suffix="%", decimals=1, caption="Share of revenue", tone="amber")

    tab_profiles, tab_clv, tab_churn, tab_radar = st.tabs(
        ["Segment Profiles", "CLV Distribution", "Churn Analysis", "Radar Comparison"]
    )

    color_map = segment_color_map(profile["segment_name"].tolist())

    with tab_profiles:
        section_heading("Segment Summary", "Behavioral cluster sizes, churn rates, and engagement indicators.")
        display = profile.rename(
            columns={
                "segment_clean": "Segment",
                "customers": "Customers",
                "pct": "% of Total",
                "churn_rate_pct": "Churn Rate %",
                "avg_tenure": "Avg Tenure (scaled)",
                "avg_monthly": "Avg Monthly (scaled)",
                "avg_services": "Avg Services",
                "avg_risk": "Avg Contract Risk",
                "avg_support": "Avg Support Engagement",
            }
        )
        display_cols = [
            "Segment",
            "Customers",
            "% of Total",
            "Churn Rate %",
            "Avg Tenure (scaled)",
            "Avg Monthly (scaled)",
            "Avg Services",
            "Avg Contract Risk",
            "Avg Support Engagement",
        ]
        st.dataframe(
            display[display_cols].style.format(
                {
                    "Customers": "{:,}",
                    "% of Total": "{:.1f}%",
                    "Churn Rate %": "{:.1f}%",
                    "Avg Tenure (scaled)": "{:.3f}",
                    "Avg Monthly (scaled)": "{:.3f}",
                    "Avg Services": "{:.1f}",
                    "Avg Contract Risk": "{:.2f}",
                    "Avg Support Engagement": "{:.2f}",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

        col_a, col_b = st.columns(2)
        with col_a:
            fig_donut = px.pie(
                profile,
                values="customers",
                names="segment_name",
                hole=0.58,
                color="segment_name",
                color_discrete_map=color_map,
                title="Segment Distribution",
            )
            fig_donut.update_traces(
                textposition="outside",
                textinfo="label+percent",
                marker={"line": {"color": "#07111f", "width": 2}},
                hovertemplate="<b>%{label}</b><br>Customers: %{value:,}<br>Share: %{percent}<extra></extra>",
            )
            st.plotly_chart(style_chart(fig_donut, height=430), use_container_width=True, config={"displayModeBar": False})

        with col_b:
            fig_bar = px.bar(
                profile,
                x="segment_clean",
                y="churn_rate_pct",
                color="segment_name",
                color_discrete_map=color_map,
                title="Churn Rate by Segment",
                text="churn_rate_pct",
            )
            fig_bar.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside",
                marker_line_color="#07111f",
                marker_line_width=1.5,
                hovertemplate="<b>%{x}</b><br>Churn rate: %{y:.1f}%<extra></extra>",
            )
            fig_bar.update_layout(xaxis_title="", yaxis_title="Churn Rate (%)")
            st.plotly_chart(style_chart(fig_bar, height=430), use_container_width=True, config={"displayModeBar": False})

        section_heading("Segment Deep Dive")
        cards = []
        for _, row in profile.iterrows():
            color = SEGMENT_COLORS.get(row["segment_clean"], COLORS["blue"])
            cards.append(
                f"""
<div class="detail-card" style="border-left: 3px solid {color};">
    <h4>{row["segment_clean"]}</h4>
    <p>{int(row["customers"]):,} customers ({row["pct"]:.1f}%)<br>
    Churn {row["churn_rate_pct"]:.1f}% | Services {row["avg_services"]:.1f} |
    Contract risk {row["avg_risk"]:.2f}</p>
</div>
"""
            )
        st.markdown(f'<div class="inline-grid">{"".join(cards)}</div>', unsafe_allow_html=True)

    with tab_clv:
        section_heading("Customer Lifetime Value", "Portfolio revenue concentration and CLV-risk intersections.")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            animated_metric("Total Portfolio CLV", total_clv, prefix="$", decimals=0, caption="Projected customer value", tone="emerald")
        with c2:
            animated_metric("Median CLV", clv_df["CLV"].median(), prefix="$", decimals=0, caption="Middle customer value", tone="cyan")
        with c3:
            animated_metric("Max CLV", clv_df["CLV"].max(), prefix="$", decimals=0, caption="Highest customer value", tone="violet")
        with c4:
            animated_metric("Pareto Revenue", top20_share, suffix="%", decimals=1, caption="Top 20% CLV share", tone="amber")

        fig_box = px.box(
            clv_df,
            x="Cluster",
            y="CLV",
            color="Cluster",
            color_discrete_map=segment_color_map(clv_df["Cluster"].unique().tolist()),
            points="outliers",
            title="CLV Distribution by Segment",
        )
        fig_box.update_traces(marker={"opacity": 0.55}, hovertemplate="<b>%{x}</b><br>CLV: $%{y:,.0f}<extra></extra>")
        fig_box.update_layout(xaxis_title="", yaxis_title="CLV ($)")
        st.plotly_chart(style_chart(fig_box, height=500), use_container_width=True, config={"displayModeBar": False})

        clv_summary = (
            clv_df.groupby("Cluster")
            .agg(
                customers=("CLV", "count"),
                mean_clv=("CLV", "mean"),
                median_clv=("CLV", "median"),
                min_clv=("CLV", "min"),
                max_clv=("CLV", "max"),
                avg_churn=("churn_proba", "mean"),
            )
            .reset_index()
        )
        st.dataframe(
            clv_summary.rename(
                columns={
                    "Cluster": "Segment",
                    "customers": "Customers",
                    "mean_clv": "Mean CLV",
                    "median_clv": "Median CLV",
                    "min_clv": "Min CLV",
                    "max_clv": "Max CLV",
                    "avg_churn": "Avg Churn Prob",
                }
            ).style.format(
                {
                    "Customers": "{:,}",
                    "Mean CLV": "${:,.2f}",
                    "Median CLV": "${:,.2f}",
                    "Min CLV": "${:,.2f}",
                    "Max CLV": "${:,.2f}",
                    "Avg Churn Prob": "{:.1%}",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

        section_heading("CLV Tier x Churn Risk")
        crosstab = pd.crosstab(clv_df["clv_tier"], clv_df["churn_tier"])
        row_order = ["High", "Mid", "Low"]
        col_order = ["Low Risk", "Medium Risk", "High Risk"]
        crosstab = crosstab.reindex(index=row_order, columns=col_order, fill_value=0)
        fig_heat = px.imshow(
            crosstab.values,
            labels={"x": "Churn Risk", "y": "CLV Tier", "color": "Customers"},
            x=col_order,
            y=row_order,
            text_auto=True,
            color_continuous_scale=["#081527", COLORS["blue"], COLORS["red"]],
            title="CLV Tier vs. Churn Risk",
        )
        st.plotly_chart(style_chart(fig_heat, height=400), use_container_width=True, config={"displayModeBar": False})

    with tab_churn:
        section_heading("Churn Concentration", "Which segment contributes the most churn and where retention should focus.")
        churn = seg_df.groupby(["segment_name", "segment_clean"])["Churn_Binary"].agg(["sum", "count"]).reset_index()
        churn.columns = ["Segment Raw", "Segment", "Churners", "Total"]
        churn["Churn Rate"] = churn["Churners"] / churn["Total"] * 100
        total_churners = churn["Churners"].sum()
        churn["% of All Churn"] = churn["Churners"] / total_churners * 100 if total_churners else 0

        col_l, col_r = st.columns(2)
        with col_l:
            fig_contrib = px.bar(
                churn,
                x="Segment",
                y="% of All Churn",
                color="Segment Raw",
                color_discrete_map=segment_color_map(churn["Segment Raw"].tolist()),
                text="% of All Churn",
                title="Share of Total Churn",
            )
            fig_contrib.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig_contrib.update_layout(xaxis_title="", yaxis_title="% of All Churn")
            st.plotly_chart(style_chart(fig_contrib, height=420), use_container_width=True, config={"displayModeBar": False})

        with col_r:
            fig_count = go.Figure()
            fig_count.add_bar(name="Churners", x=churn["Segment"], y=churn["Churners"], marker_color=COLORS["red"])
            fig_count.add_bar(name="Total", x=churn["Segment"], y=churn["Total"], marker_color=COLORS["blue"])
            fig_count.update_layout(title="Churners vs. Segment Size", barmode="group", xaxis_title="", yaxis_title="Customers")
            st.plotly_chart(style_chart(fig_count, height=420, show_legend=True), use_container_width=True, config={"displayModeBar": False})

        st.dataframe(
            churn[["Segment", "Churners", "Total", "Churn Rate", "% of All Churn"]].style.format(
                {
                    "Churners": "{:,}",
                    "Total": "{:,}",
                    "Churn Rate": "{:.1f}%",
                    "% of All Churn": "{:.1f}%",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

        at_risk = churn[churn["Segment"].str.contains("At-Risk", case=False, na=False)]
        if not at_risk.empty:
            row = at_risk.iloc[0]
            body = (
                f'The <strong>At-Risk Churners</strong> segment represents '
                f'<strong>{row["Total"] / len(seg_df) * 100:.1f}%</strong> of all customers but contributes '
                f'<strong>{row["% of All Churn"]:.1f}%</strong> of churn. This is the highest-leverage retention pool.'
            )
            insight_card("Critical Retention Insight", body, color=COLORS["red"])

    with tab_radar:
        section_heading("Behavioral DNA", "A radar comparison of engagement, risk, tenure, and spend signals.")
        radar_features = ["services_count", "contract_risk_score", "support_engagement", "tenure", "MonthlyCharges"]
        radar_labels = ["Services", "Contract Risk", "Support Engagement", "Tenure", "Monthly Charges"]
        fig_radar = go.Figure()
        for segment_name in sorted(seg_df["segment_name"].unique(), key=clean_segment_name):
            subset = seg_df[seg_df["segment_name"] == segment_name]
            values = [subset[column].mean() for column in radar_features]
            clean_name = clean_segment_name(segment_name)
            color = SEGMENT_COLORS.get(clean_name, COLORS["blue"])
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=values + [values[0]],
                    theta=radar_labels + [radar_labels[0]],
                    fill="toself",
                    name=clean_name,
                    line={"color": color, "width": 2},
                    fillcolor=hex_to_rgba(color, 0.14),
                    hovertemplate="<b>%{theta}</b><br>%{r:.3f}<extra></extra>",
                )
            )
        fig_radar.update_layout(
            polar={
                "bgcolor": "rgba(0,0,0,0)",
                "angularaxis": {"gridcolor": "rgba(148, 163, 184, 0.14)", "linecolor": "rgba(148, 163, 184, 0.16)"},
                "radialaxis": {
                    "gridcolor": "rgba(148, 163, 184, 0.12)",
                    "linecolor": "rgba(148, 163, 184, 0.16)",
                    "tickfont": {"color": COLORS["muted"], "size": 10},
                    "range": [0, max(seg_df[radar_features].mean().max() * 1.3, 1)],
                },
            },
            title="Segment Radar - Behavioral Feature Means",
        )
        st.plotly_chart(style_chart(fig_radar, height=560, show_legend=True), use_container_width=True, config={"displayModeBar": False})
        insight_card(
            "Reading the Pattern",
            "Wider shapes signal higher engagement across services, support, tenure, and spend. The high-risk profile combines short tenure, flexible contracts, and lower service attachment.",
            color=COLORS["cyan"],
        )


def main() -> None:
    page = sidebar()
    if page == "Churn Risk Studio":
        render_churn_studio()
    else:
        render_segment_command_center()


if __name__ == "__main__":
    main()
