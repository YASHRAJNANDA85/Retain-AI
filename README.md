# 📊 RetainAI: Customer Segmentation & Churn Prediction Platform

> **End-to-end data science project:** From raw telco data to actionable churn-reduction strategy — built with interpretable ML, customer segmentation, and lifetime value estimation.

Access here : [https://telco-data-customer-analysis.streamlit.app/](https://retainai-churn-prediction-platform-3glvq.streamlit.app/)

---

## 🧩 The Problem

A telecommunications company is losing customers — **26.5% of its 7,043 subscribers have churned**. But not all churn is equal: some departing customers are high-revenue, long-tenure loyalists; others are low-spend, short-lived accounts. The business needs answers to three questions:

1. **Who** is most likely to leave?
2. **Why** are they leaving?
3. **What** should we do about it — and for whom?

---

## 🔍 Approach

This project follows a structured, six-phase analytical pipeline:

| Phase | What It Does | Key Output |
|---|---|---|
| **Phase 1 — EDA** | Explores distributions, churn signals, and data quality | 9 publication-quality charts |
| **Phase 2 — Preprocessing** | Cleans data, engineers 5 business-logic features, handles class imbalance (SMOTE) | Production-ready feature matrix |
| **Phase 3 — Segmentation** | K-Means clustering (K=3, silhouette=0.42) to group customers by behavior | 3 named behavioral segments |
| **Phase 4 — Churn Prediction** | Compares Logistic Regression, Random Forest, and XGBoost; SHAP explainability | Best model: Random Forest (AUC 0.84) |
| **Phase 5 — CLV Estimation** | Combines survival analysis with churn probability to estimate future revenue | Per-customer lifetime value scores |
| **Phase 6 — Insights & Report** | Packages findings into business-ready recommendations | This README + summary notebook |

---

## 📈 Key Findings

### 1. Three Distinct Customer Segments Exist

Using K-Means clustering on behavioral features (services count, contract risk, tenure, charges), customers naturally fall into **3 segments**:

| Segment | Customers | Churn Rate | Avg Monthly | Profile |
|---|---|---|---|---|
| 🔴 **At-Risk Churners** | 3,730 (53.0%) | **42.2%** | Low-Mid | Month-to-month contracts, few services, short tenure |
| 🟢 **High-Value Loyalists** | 2,058 (29.2%) | 13.0% | High | Long-tenure, many services, strong engagement |
| 🟡 **New Potentials** | 1,255 (17.8%) | 2.2% | Low | New customers, low spend, yet to commit |

> **Critical insight:** The At-Risk segment represents 53% of customers but accounts for **84.2% of all churn**.

### 2. Contract Type Is the #1 Churn Driver

SHAP analysis reveals the **top 5 factors** pushing customers toward churn:

| Rank | Feature | SHAP Impact | Business Translation |
|---|---|---|---|
| 1 | `contract_risk_score` | 0.0479 | Month-to-month contracts → highest churn risk |
| 2 | `tenure` | 0.0452 | Shorter tenure → higher churn probability |
| 3 | `Contract_Two year` | 0.0391 | Two-year contracts are protective against churn |
| 4 | `Contract_Month-to-month` | 0.0387 | Confirms: monthly flexibility = flight risk |
| 5 | `InternetService_Fiber optic` | 0.0371 | Fiber customers churn more (possible service quality or price issue) |

### 3. The Churn Prediction Model Catches 82% of Churners

The **Random Forest classifier** — selected as the best-performing model — achieves:

| Metric | Value |
|---|---|
| AUC-ROC | 0.84 |
| F1-Score (churn class) | 0.63 |
| Recall (churn class, tuned) | **81.6%** |
| Precision (churn class) | 50.7% |
| Optimal Threshold | 0.44 (tuned from default 0.50) |

> **What this means:** The model correctly identifies ~82 out of every 100 customers who will churn. The threshold was tuned to prioritize catching churners over minimizing false alarms — because **the cost of losing a customer exceeds the cost of a retention offer**.

### 4. Customer Lifetime Value Varies by 5.2× Across Segments

| Segment | Median CLV | Mean CLV |
|---|---|---|
| 🔴 At-Risk Churners | $3,330 | $3,282 |
| 🟢 High-Value Loyalists | $599 | $682 |
| 🟡 New Potentials | $542 | $636 |

- **Total portfolio CLV:** $9.98 million
- **Pareto effect:** Top 20% of customers generate **54.2%** of total CLV
- **CLV range:** $11 — $7,856 per customer

> **Counterintuitive finding:** The "At-Risk" segment has the *highest* CLV because their high churn probability makes them valuable targets for retention — preventing even a fraction of this churn unlocks significant revenue.

---

## 💡 Business Recommendations

### Recommendation 1: Priority Retention for At-Risk Churners
**Target:** 3,730 customers (53% of base) generating 84.2% of all churn  
**Action:** Offer contract upgrade incentives (month-to-month → annual), loyalty discounts, or bundled service packages  
**Expected impact:** Even a 10% reduction in this segment's churn rate saves ~157 customers and preserves ~$515K in CLV

### Recommendation 2: Contract Lock-In Strategy
**Insight:** Contract type is the single strongest churn predictor (SHAP = 0.048)  
**Action:** Introduce compelling annual/biennial contract offers at signup — discounted first-month pricing, waived installation fees, or bundled streaming services  
**Rationale:** Two-year contract customers churn at ~3% vs. ~42% for month-to-month

### Recommendation 3: Early Tenure Intervention Program
**Insight:** Customers with tenure < 12 months are in a "danger zone" — short tenure is the #2 churn driver  
**Action:** Implement a 90-day onboarding sequence: welcome call at Day 7, satisfaction check at Day 30, value reinforcement at Day 60  
**Rationale:** Customers who survive the first year are dramatically more likely to stay

### Recommendation 4: Fiber Optic Service Quality Audit
**Insight:** Fiber optic customers churn at a higher rate despite paying premium prices  
**Action:** Investigate service reliability, speed consistency, and customer support experience for fiber subscribers  
**Rationale:** High-price + poor experience = fastest path to churn

### Recommendation 5: Nurture New Potentials Into Loyalists
**Target:** 1,255 new/low-engagement customers with only 2.2% churn  
**Action:** Cross-sell additional services (Online Security, Tech Support) to increase stickiness  
**Rationale:** Each additional service reduces churn probability; the `services_count` feature directly lowers predicted churn risk

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| **Data Processing** | Python, Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn, Plotly |
| **Machine Learning** | Scikit-learn, XGBoost, Imbalanced-learn (SMOTE) |
| **Explainability** | SHAP |
| **Survival Analysis** | Lifelines (Kaplan-Meier) |
| **Feature Engineering** | Custom (5 domain-specific features) |

---

## 📂 Project Structure

```
├── data/
│   ├── raw/                        ← Original Kaggle dataset (7,043 rows × 21 columns)
│   └── processed/                  ← Cleaned, engineered, segmented, and CLV-scored datasets
├── notebooks/
│   ├── 01_EDA.ipynb                ← Exploratory data analysis (9 charts)
│   ├── 02_Preprocessing.ipynb      ← Cleaning, encoding, SMOTE, feature engineering
│   ├── 03_Segmentation.ipynb       ← K-Means clustering (K=3, silhouette=0.42)
│   ├── 04_Churn_Prediction.ipynb   ← 3-model comparison, SHAP, threshold tuning
│   ├── 05_CLV_Estimation.ipynb     ← Survival analysis + CLV scoring
│   └── 06_Insights_Summary.ipynb   ← Clean narrative summary (no raw code)
├── src/
│   ├── best_churn_model.pkl        ← Serialized Random Forest model
│   ├── kmeans_model.pkl            ← Fitted K-Means segmentation model
│   └── *.pkl                       ← Scalers, SHAP values, feature columns
├── reports/
│   └── figures/                    ← 30 publication-quality charts (300 DPI)
└── README.md                       ← This file
```

---

## 📊 Selected Visualizations

| Chart | What It Shows |
|---|---|
| `14_radar_chart.png` | Cluster profiles at a glance — behavioral DNA of each segment |
| `18_roc_curves.png` | 3-model ROC comparison — Random Forest edges out XGBoost and LogReg |
| `21_shap_beeswarm.png` | SHAP beeswarm — the single most insightful chart in the project |
| `28_clv_churn_heatmap.png` | CLV tier × churn risk cross-tabulation — identifies high-value at-risk customers |
| `30_pareto_clv.png` | Pareto analysis — top 20% of customers = 54.2% of revenue |

---

## 🏆 Key Points

```
• Built end-to-end churn prediction pipeline using Random Forest, achieving AUC-ROC of 0.84
  and F1-score of 0.63; applied SHAP explainability to surface top 5 churn drivers.

• Segmented 7,043 customers into 3 behavioral clusters using K-Means (silhouette = 0.42);
  identified at-risk segment representing 53% of customers but 84.2% of predicted churn.

• Estimated Customer Lifetime Value (CLV) by combining Kaplan-Meier survival analysis
  with churn probability scores; highest-CLV cluster showed 5.2× revenue potential
  vs. lowest.

• Improved churner recall from 69.8% (Logistic Regression baseline) to 81.6% through
  threshold tuning and class imbalance handling (SMOTE) — a 16.9% improvement.
```

---

## 📋 Dataset

**Source:** [Telco Customer Churn — Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)  
**Size:** 7,043 customers × 21 features  
**Target variable:** `Churn` (Yes/No → binary)  
**Key features:** Contract type, tenure, monthly charges, internet service, payment method, add-on services

---

*Built as a portfolio project demonstrating the full data science lifecycle: from exploratory analysis through machine learning to actionable business recommendations.*
