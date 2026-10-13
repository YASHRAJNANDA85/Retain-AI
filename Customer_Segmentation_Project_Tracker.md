# 📊 Customer Segmentation & Retention Analysis
### Telco Customer Churn Dataset | Data Science Resume Project

> **How to use this file:**
> - `[ ]` = Not started &nbsp;|&nbsp; `[~]` = In Progress &nbsp;|&nbsp; `[x]` = Done
> - Update the **Status**, **Notes**, and **Key Metrics** fields as you go.
> - The **💡 Idea** tag marks optional enhancements that can be picked up later.

---

## 🗂️ Project Overview

| Field | Details |
|---|---|
| **Project Title** | Customer Segmentation and Retention Analysis |
| **Dataset** | [Telco Customer Churn — Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) |
| **Core Pillars** | Churn Prediction · CLV Estimation · Behavior Analysis · Customer Segmentation |
| **Target Audience** | Recruiters in Data Science / ML / Analytics roles |
| **Status** | 🟢 Phase 7 : Deployment Completed |

---

## 📁 Folder Structure

```
telco-churn-analysis/
├── data/
│   ├── raw/                  ← Original downloaded dataset
│   └── processed/            ← Cleaned, engineered dataset
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_Preprocessing.ipynb
│   ├── 03_Segmentation.ipynb
│   ├── 04_Churn_Prediction.ipynb
│   ├── 05_CLV_Estimation.ipynb
│   └── 06_Insights_Summary.ipynb
├── src/
│   ├── preprocessing.py      ← Reusable cleaning functions
│   ├── features.py           ← Feature engineering logic
│   └── evaluation.py         ← Metrics and plotting helpers
├── reports/
│   ├── figures/              ← All saved plots
│   └── project_summary.pdf   ← Final report (optional)
├── app/                      ← Dashboard / Streamlit app (optional)
└── README.md                 ← Written like a consulting report
```

---

## 🗺️ Phase-wise Roadmap

---

### ✅ Phase 0 — Setup & Preparation
> *Goal: Get the environment ready and understand the data before touching any model.*

| # | Task | Status | Notes |
|---|---|---|---|
| 0.1 | Download Telco Churn dataset from Kaggle | `[x]` | |
| 0.2 | Set up virtual environment (`venv` or `conda`) | `[x]` | |
| 0.3 | Install required libraries (see stack below) | `[x]` | |
| 0.4 | Initialize Git repo and push to GitHub | `[ ]` | Make it public for resume linking |
| 0.5 | Read dataset description and understand all 21 columns | `[x]` | Know what each column means before coding |
| 0.6 | Write project brief in README.md (problem + approach) | `[x]` | Write for a non-technical reader |

**Tech Stack to Install:**
```
pandas, numpy, matplotlib, seaborn, plotly,
scikit-learn, xgboost, imbalanced-learn (SMOTE),
shap, lifelines (survival analysis), streamlit (optional)
```

---

### 📊 Phase 1 — Exploratory Data Analysis (EDA) ✅
> *Goal: Understand distributions, relationships, and business signals before any modelling.*

| # | Task | Status | Notes |
|---|---|---|---|
| 1.1 | Check shape, dtypes, null values, duplicates | `[x]` | Note the `TotalCharges` string issue |
| 1.2 | Plot churn distribution (class balance check) | `[x]` | ~26% churn — note class imbalance |
| 1.3 | Churn rate by contract type (bar chart) | `[x]` | Strongest signal: ~42% vs ~3% |
| 1.4 | Tenure distribution split by churn (KDE plot) | `[x]` | Shows early-life churn vulnerability |
| 1.5 | Monthly charges vs. tenure scatter (colored by churn) | `[x]` | Reveals high-price, low-tenure danger zone |
| 1.6 | Churn rate by payment method, internet service, senior citizen | `[x]` | |
| 1.7 | Correlation heatmap on numeric features | `[x]` | Check multicollinearity |
| 1.8 | Box plots: MonthlyCharges & TotalCharges by churn | `[x]` | |
| 1.9 | Write 3–5 key EDA findings as markdown cells in notebook | `[x]` | Business language, not stats jargon |

**EDA Notebook:** `notebooks/01_EDA.ipynb`

**💡 Ideas to Add Later:**
- Sunburst chart: Contract → Internet Service → Churn (Plotly)
- Heatmap of churn rate across two categorical features simultaneously

---

### 🔧 Phase 2 — Data Preprocessing & Feature Engineering
> *Goal: Clean the data and create features that carry more signal than raw columns.*

#### 2A — Preprocessing

| # | Task | Status | Notes |
|---|---|---|---|
| 2.1 | Fix `TotalCharges`: convert to float, fill nulls (new customers → 0) | `[x]` | Mention this in resume as realistic data quality issue |
| 2.2 | Encode binary Yes/No columns as 0/1 | `[x]` | ~10 columns |
| 2.3 | One-hot encode multi-class categoricals (`InternetService`, `Contract`, `PaymentMethod`) | `[x]` | |
| 2.4 | Scale continuous features (`tenure`, `MonthlyCharges`, `TotalCharges`) | `[x]` | MinMaxScaler or StandardScaler |
| 2.5 | Handle class imbalance using SMOTE (apply only on training set) | `[x]` | From `imbalanced-learn` |
| 2.6 | Train/test split (80/20, stratified on `Churn`) | `[x]` | |

#### 2B — Feature Engineering

| # | Feature | Formula / Logic | Status | Business Meaning |
|---|---|---|---|---|
| 2.7 | `charge_per_month_ratio` | `TotalCharges / tenure` | `[x]` | Price sensitivity signal |
| 2.8 | `services_count` | Sum of all 8 add-on service columns | `[x]` | Customer stickiness |
| 2.9 | `contract_risk_score` | Month-to-month=2, 1yr=1, 2yr=0 | `[x]` | Churn vulnerability score |
| 2.10 | `support_engagement` | `TechSupport + OnlineSecurity` (binary sum) | `[x]` | Relationship depth |
| 2.11 | `value_tier` | Bin `MonthlyCharges` → Low / Mid / High | `[x]` | Segment anchor feature |

> ⚠️ **Key Rule:** Engineer features on the full dataset, then split. Apply SMOTE only after splitting, only to training data.

**Preprocessing Notebook:** `notebooks/02_Preprocessing.ipynb`
**Reusable code:** `src/preprocessing.py`, `src/features.py`

---

### 🔵 Phase 3 — Customer Segmentation (Clustering)
> *Goal: Group customers into meaningful behavioral segments. These clusters will feed into churn prediction and CLV as features.*

| # | Task | Status | Notes |
|---|---|---|---|
| 3.1 | Select clustering features: `services_count`, `charge_per_month_ratio`, `contract_risk_score`, `tenure`, `MonthlyCharges` | `[x]` | Scale before clustering |
| 3.2 | Run K-Means for K = 2 to 8, record inertia | `[x]` | Elbow Method |
| 3.3 | Compute Silhouette Score for each K | `[x]` | Pick K with highest score |
| 3.4 | Fit final K-Means model (expected: K=3 or K=4) | `[x]` | |
| 3.5 | Run Hierarchical Clustering + plot dendrogram | `[x]` | Visual validation of cluster choice |
| 3.6 | Profile each cluster: mean values per feature | `[x]` | |
| 3.7 | Plot cluster radar/spider chart (one line per cluster) | `[x]` | Best single visual for this phase |
| 3.8 | Name each cluster in plain English | `[x]` | See naming guide below |
| 3.9 | Add `cluster_label` as a new column in the dataset | `[x]` | Will be used as feature in Phase 4 & 5 |
| 3.10 | Plot churn rate per cluster (bar chart) | `[x]` | Closes the segmentation → churn loop |

**Cluster Naming Guide (adjust based on your actual results):**

| Suggested Name | Profile |
|---|---|
| 🟢 High-Value Loyalists | Long tenure, many services, low churn risk |
| 🔴 At-Risk Churners | Month-to-month, minimal services, high churn probability |
| 🟡 New Potentials | Short tenure, mid-spend, undecided |
| 🔵 Budget Basics | Long tenure, low charges, few services |

**💡 Ideas to Add Later:**
- UMAP or t-SNE 2D scatter plot colored by cluster (visually striking)
- Animate cluster formation with a GIF (for portfolio/blog post)

**Segmentation Notebook:** `notebooks/03_Segmentation.ipynb`

---

### 🔴 Phase 4 — Churn Prediction (Classification)
> *Goal: Predict which customers are likely to churn. Use three models and compare rigorously.*

| # | Task | Status | Notes |
|---|---|---|---|
| 4.1 | Add `cluster_label` (from Phase 3) to feature set | `[x]` | The key pipeline connection |
| 4.2 | Train Logistic Regression (baseline) | `[x]` | Use `class_weight='balanced'` |
| 4.3 | Train Random Forest Classifier | `[x]` | Tune `n_estimators`, `max_depth` |
| 4.4 | Train XGBoost Classifier | `[x]` | Tune with `GridSearchCV` or `Optuna` |
| 4.5 | Evaluate all 3 models: AUC-ROC, F1, Precision, Recall | `[x]` | Build a comparison table |
| 4.6 | Plot ROC curves for all 3 on one chart | `[x]` | |
| 4.7 | Plot Precision-Recall curve for best model | `[x]` | More informative than ROC for imbalanced data |
| 4.8 | Plot confusion matrix (best model) | `[x]` | |
| 4.9 | Generate SHAP summary plot (beeswarm) for best model | `[x]` | Single most impressive visualization |
| 4.10 | Extract top 5 churn drivers from SHAP values | `[x]` | Write as business insights |
| 4.11 | Save best model as `.pkl` file | `[x]` | For app deployment later |

**Target Metrics to Aim For:**

| Metric | Baseline (LogReg) | Target (XGBoost) | Achieved (Random Forest) |
|---|---|---|---|
| AUC-ROC | ~0.83 | ≥ 0.88 | 0.8389 |
| F1-Score (churn class) | ~0.60 | ≥ 0.68 | 0.6249 |
| Recall (churn class) | ~0.75 | ≥ 0.78 | 0.7594 |

> 📝 Fill in your actual achieved metrics above once models are trained.

**💡 Ideas to Add Later:**
- Threshold tuning: adjust classification threshold to prioritize recall (catching churners is more valuable than precision)
- LIME explanations for individual customer predictions

**Churn Notebook:** `notebooks/04_Churn_Prediction.ipynb`

---

### 💰 Phase 5 — Customer Lifetime Value (CLV) Estimation
> *Goal: Estimate future revenue potential per customer by combining tenure prediction with churn probability.*

#### CLV Formula Used:
```
CLV = MonthlyCharges × Expected_Tenure × (1 − Churn_Probability)
```

| # | Task | Status | Notes |
|---|---|---|---|
| 5.1 | Plot Kaplan-Meier survival curves using `lifelines` | `[x]` | Split by contract type for business story |
| 5.2 | Predict expected tenure using Random Forest Regressor | `[x]` | Target = `tenure` column |
| 5.3 | Pull churn probabilities from Phase 4 best model | `[x]` | Use `.predict_proba()[:, 1]` |
| 5.4 | Compute CLV for every customer using formula above | `[x]` | |
| 5.5 | Plot CLV distribution by cluster | `[x]` | Box plot or violin plot |
| 5.6 | Identify top 10% and bottom 10% CLV customers | `[x]` | |
| 5.7 | Cross-tabulate CLV tier vs. churn risk | `[x]` | 2x2 heatmap — key business insight |
| 5.8 | Write CLV-based retention recommendations per segment | `[x]` | See recommendations template below |

**CLV-Segment Recommendations Template:**

| Cluster | CLV Tier | Churn Risk | Recommended Action |
|---|---|---|---|
| High-Value Loyalists | High | Low | Upsell premium services |
| At-Risk Churners | Mid | High | Offer loyalty discount / contract upgrade |
| New Potentials | Mid | Medium | Onboarding outreach, bundle offers |
| Budget Basics | Low | Low | Low-touch retention, monitor |

> 📝 Fill this in with your actual cluster findings.

**💡 Ideas to Add Later:**
- Pareto analysis: what % of total CLV do top 20% customers represent?
- Survival curve by `InternetService` type

**CLV Notebook:** `notebooks/05_CLV_Estimation.ipynb`

---

### ✅ Phase 6 — Insights, Storytelling & Report
> *Goal: Package everything into a recruiter-readable narrative. This phase is as important as the modelling.*

| # | Task | Status | Notes |
|---|---|---|---|
| 6.1 | Write executive summary in README.md (non-technical language) | `[x]` | Problem → Approach → Findings → 5 Recommendations |
| 6.2 | Create insights summary notebook (`06_Insights_Summary.ipynb`) | `[x]` | 21-cell narrative notebook with embedded figures |
| 6.3 | List 3–5 business recommendations with supporting data | `[x]` | 5 recommendations with SHAP evidence + CLV impact |
| 6.4 | Export all key figures to `reports/figures/` | `[x]` | 30 PNG figures already exported at 300 DPI |
| 6.5 | Push final code to GitHub with clean commit history | `[x]` | Pushed |
| 6.6 | Add project to LinkedIn / portfolio with live link | `[x]` | Added |



---

### 🚀 Phase 7 — Deployment (Optional, Choose One Tier)

#### Tier 1 — Streamlit App *(Recommended: 2–4 hours)*

| # | Task | Status | Notes |
|---|---|---|---|
| 7.1 | Build "Churn Risk Calculator" page: input customer attributes → output churn probability | `[x]` | Full preprocessing pipeline + gauge chart + recommendations |
| 7.2 | Build "Segment Explorer" page: show cluster profiles and CLV distribution | `[x]` | 4 tabs: Profiles, CLV, Churn Analysis, Radar |
| 7.3 | Deploy to Streamlit Community Cloud (free) | `[x]` | Get a shareable URL  |

#### Tier 2 — Plotly Dash Dashboard *(1–2 days)*

| # | Task | Status | Notes |
|---|---|---|---|
| 7.4 | Interactive dashboard with segment, contract, tenure filters | `[ ]` | All charts update on filter change |
| 7.5 | Deploy on Render (free tier) | `[ ]` | |

#### Tier 3 — FastAPI + Docker *(3–5 days, signals MLOps awareness)*

| # | Task | Status | Notes |
|---|---|---|---|
| 7.6 | Wrap model in a FastAPI `/predict` endpoint | `[ ]` | Returns churn probability as JSON |
| 7.7 | Add simple HTML front-end | `[ ]` | |
| 7.8 | Containerize with Docker | `[ ]` | Write a clean `Dockerfile` |
| 7.9 | Deploy on Render or Railway (free) | `[ ]` | |

---

## 📈 Key Metrics Dashboard *(Update as you complete phases)*

| Metric | Target | Achieved | Notes |
|---|---|---|---|
| Churn Prediction AUC-ROC | ≥ 0.88 | **0.8389** | Random Forest — best of 3 models |
| Churn F1-Score | ≥ 0.68 | **0.6249** | Threshold tuned to 0.44 for recall |
| Churn Recall (tuned) | ≥ 0.78 | **0.8155** | 16.9% improvement over LogReg baseline |
| Number of Clusters (K) | 3–4 | **3** | Optimal via elbow + silhouette |
| Silhouette Score | ≥ 0.35 | **0.4150** | ✅ Exceeds target |
| CLV range (min–max) | — | **$11.06 – $7,855.53** | Avg: $1,417.33 per customer |
| Top churn driver (SHAP) | — | **contract_risk_score** | SHAP = 0.0479 |

---

## 🏁 Final Checklist Before Calling It Done

- [x] All notebooks run top-to-bottom without errors
- [x] `src/` contains reusable, clean Python functions
- [x] README.md tells the full story without opening a notebook
- [x] All charts saved in `reports/figures/` (30 figures)
- [x] At least one live deployment link exists
- [x] Resume bullets are quantified with actual model metrics
- [x] GitHub repo has a clear description, tags (`data-science`, `machine-learning`, `churn-prediction`), and pinned to profile

---

*Tracker last updated: June 26, 2026*
