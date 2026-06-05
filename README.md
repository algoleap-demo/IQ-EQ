# IQ-EQ Unified Agent Mesh

## 🎯 Objective of the Project
The primary objective of the **Unified Agent Mesh** is to systematically identify and unlock hidden revenue-generating opportunities within IQ-EQ's existing client portfolios. By combining deterministic Machine Learning with Generative AI reasoning, the system automates the prioritization of accounts, generates highly personalized strategic campaign briefs, and recommends specific cross-sell/upsell product pathways to maximize growth while optimizing sales team effort.

## 📊 Description of Raw Data
The system ingests and processes a wide range of structured and unstructured client data, including:
- **Firmographics & Identifiers:** Account names, regions, industry segments, and primary contacts.
- **Financial Metrics:** Assets Under Administration (AUA/AUM), current revenue, and historical growth trends.
- **Engagement & Activity:** Number of active entities, total products utilized, recent transaction histories, and CRM notes/activities.
- **Behavioral Footprint:** Fund administration data, regulatory compliance burdens, and prior marketing engagement.

## ⚙️ How the Process Works
The architecture is split into three core Proof of Concept (POC) pipelines that run sequentially:

1. **POC 1: Targeting & Triage** 
   - Evaluates the entire client base to identify *who* to target next. It blends mathematical probability with qualitative strategic context to assign accounts to actionable "Buckets" (e.g., Bucket A: Immediate Action).
2. **POC 2: Account Planning** 
   - Takes the prioritized accounts and automates the manual research phase. It identifies key decision-makers, evaluates specific financial upside, and uses LLMs to draft tailored outreach strategies.
3. **POC 3: Whitespace Analysis** 
   - Groups accounts into strategic behavioral "Clusters" to identify product gaps. It runs a Recommendation Engine to determine exactly *what* products should be pitched to which account based on similar high-performing profiles.

Finally, an overarching **Governance Agent** audits the data at every step, flagging logical anomalies (e.g., "Conflicts" where high propensity meets low potential).

## 🧠 Models Used
This project utilizes a hybrid AI architecture (the "Agent Mesh"):
- **Machine Learning (Predictive):**
  - **XGBoost:** Used to calculate the core ML Propensity Score (the statistical probability of a client making a purchase).
  - **Isotonic Regression / CalibratedClassifierCV:** Used for probability calibration of the ML predictions.
  - **K-Means / Clustering Algorithms:** Groups similar accounts together during the Whitespace Analysis to discover shared product needs.
- **Generative AI (Reasoning & NLP):**
  - **Large Language Models (LLMs):** Powered by the LangChain framework via OpenRouter (utilizing models like Claude 3.5 Sonnet / GPT-4o). These models analyze raw CRM context, summarize qualitative data, and generate the final strategic campaign briefs and messaging angles.

## 📈 Metrics and KPIs Generated
The system automatically computes and tracks several critical KPIs for each account:
- **ML Propensity Score:** Percentage likelihood (0-100%) that an account will buy.
- **LLM Context Level:** Categorical assessment (High/Medium/Low) of qualitative readiness based on recent events.
- **Whitespace Potential (EUR):** The estimated total Euro value of un-sold cross-sell opportunities for an account.
- **Account Rank / Bucket Assignment:** Prioritization tiers (Bucket A, B, C) guiding immediate sales focus.
- **Conflict Flags:** Governance metrics identifying contradictions between data sources (e.g., high propensity but no whitespace).
- **Cluster IDs:** Behavioral groupings linking accounts to specific product propensity models.

## 💼 Business Benefits
- **Revenue Maximization:** Uncovers hidden cross-sell/upsell pathways that might be missed by manual portfolio reviews.
- **Sales Efficiency:** Eliminates "gut-feeling" selling. Sales directors are handed pre-prioritized lists (Bucket A) so they only spend time on accounts mathematically likely to convert.
- **Time Savings:** Replaces hours of manual account research and drafting by auto-generating complete, personalized campaign briefs and outreach sequences.
- **Strategic Accuracy:** The Governance engine actively catches logical flaws (conflicts), preventing the business from wasting marketing spend on saturated accounts or misaligned product pitches.
