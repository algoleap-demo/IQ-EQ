import json

with open("app/modules/targeting/reasoning_agent.py", "r", encoding="utf-8") as f:
    content = f.read()

new_prompt = """REASONING_PROMPT = \"\"\"You are an elite Strategic Reasoning Agent and Presentation Engine for IQ-EQ. 
Your objective is to ingest raw data about an institutional account (FAM/PIAO) and generate a comprehensive, highly-structured 5-part dossier. This dossier will be rendered directly into a UI popup window.

### STRICT GROUNDING & ANTI-HALLUCINATION RULES:
**CRITICAL**: You are operating as a data-driven reasoning engine. 
- **ZERO HALLUCINATION**: Every single number, feature value, name, and calculation returned in your JSON must exactly match the raw input data provided to you. Do not invent, assume, or hallucinate data.
- **NO FAKE DATA**: If a value is 0, missing, or null, report it exactly as such. Do not invent filler data to make the narrative sound better.
- **EXACT MATH**: The formulas for Confidence and Engagement Score must be executed using the exact mathematical variables provided. 
- **ANOMALY PREVENTION**: Do not inject external knowledge about the client. Do not fabricate strategic movements that are not explicitly proven by the `launch_indicator`, `tier_1_conf_count`, or historical performance data.

### INSTRUCTIONS:

**1. Raw Input Features**
- List the exact raw features provided in the input context.
- Append the Engagement Score logic note: "Base Score + (5 * total conferences) + (10 * high signal conferences)".

**2. ML Propensity Scoring**
- State the model name: "XGBoost Model (xgb_propensity_v1.pkl)".
- Format the propensity score as a percentage.

**3. Confidence Calculation**
- Explicitly write out the 4-step mathematical breakdown for confidence based on distance from the 0.5 boundary exactly as provided in the input context.
- Define the constants (0.5 Decision Boundary, 0.55 Base Confidence, 0.4 Scaling Factor, 0.98 Hard Cap).

**4. Business Assessment Logic**
- Synthesize the historical win rate and deal size into a narrative (e.g., "flawless historical win rate", "poor historical win rate").
- Synthesize current activity (Conferences and Launch Indicators) into bullet points (e.g., "Hyper-Engagement", "Strategic Movement").
- Explicitly state why the priority bucket was assigned.
- Provide a sharp 1-sentence "Agent Rationale".
- List the Priority Buckets & SLAs Definition.

**5. Entity Summary**
- Extract and list the Contact Person, Country, Segment, Fund Size, and Strategic Priority.

### INPUT CONTEXT:
- Account ID: {account_id}
- Account Name: {account_name}
- Contact Person: {contact_person}
- Segment: {segment}
- Country: {country}
- Fund Size EUR: {fund_size_eur}
- Strategic Priority: {strategic_priority}
- ML Propensity Score: {ml_score_pct}
- ML Confidence Level: {confidence_pct}

**Features:**
{features_json}

**Math Steps:**
{math_steps_json}

### OUTPUT FORMAT (Strict JSON):
{{
  "priority_bucket": "A|B|C",
  "rationale_text": "...",
  "suggested_nba": {{
    "action_type": "...",
    "description": "...",
    "reasoning": "...",
    "due_in_days": 10
  }},
  "popup_data": {{
    "section_1_raw_features": {{
      "features": {{ ... }},
      "logic_note": "Engagement Score logic: Base Score + (5 * total conferences) + (10 * high signal conferences)"
    }},
    "section_2_ml_scoring": {{
      "model_context": "XGBoost Model (xgb_propensity_v1.pkl) evaluated the 9 features above and predicted:",
      "propensity_score_text": "Propensity Score = ..."
    }},
    "section_3_confidence_calculation": {{
      "intro": "The Confidence Level is deterministically calculated based on distance from the 0.5 decision boundary.",
      "formula": "Formula = min(0.98, (abs(Propensity - 0.5) / 0.5) * 0.4 + 0.55)",
      "math_steps": [ ... ],
      "final_confidence_text": "Final Confidence = ...",
      "definitions": [
        "0.5 (Decision Boundary): Represents 50% probability, the point of maximum uncertainty.",
        "0.55 (Base Confidence): The minimum confidence floor (55%). Ensures the score never drops to 0%, avoiding perceived technical errors.",
        "0.4 (Scaling Factor): The distance from the center boosts the final score by up to 40%, scaling smoothly up to 95%.",
        "0.98 (Hard Cap): Enforces a strict 98% ceiling, preserving a margin for human review even for extreme ML predictions."
      ]
    }},
    "section_4_business_assessment": {{
      "historical_narrative": "...",
      "current_activity_intro": "While the historical data proves they are a great client, the Agent Mesh's LLM Reasoning layer detected their current activity levels right now:",
      "activity_bullets": [ "..." ],
      "bucket_assignment": "...",
      "agent_rationale": "...",
      "slas": [
        "Bucket A (High Priority): Call this week (5-day SLA). Strong quantitative ML scores and/or highly active contextual signals.",
        "Bucket B (Medium Priority): Send targeted product brief (10-day SLA). Mixed signals requiring continued nurturing.",
        "Bucket C (Low Priority): Schedule quarterly check-in (90-day SLA). Weak current intent or a poor historical baseline."
      ]
    }},
    "section_5_entity_summary": {{
      "Contact Person": "...",
      "Country": "...",
      "Segment": "...",
      "Fund Size": "...",
      "Strategic Priority": "..."
    }}
  }}
}}\"\"\""""

import re
content = re.sub(r'REASONING_PROMPT = """[\s\S]*?}}"""', new_prompt, content)

# Also update process_account_reasoning
new_func = """async def process_account_reasoning(acc_id, s_res, raw_data, i, total, trace_id=None):
    accounts_df = raw_data["accounts"]
    acc_info = accounts_df[accounts_df.account_id == acc_id].iloc[0]
    feat = compute_features(acc_id, raw_data)
    
    # Pre-calculate math for LLM to avoid hallucinations
    prop = s_res["propensity_score"]
    distance = abs(prop - 0.5)
    normalized = distance / 0.5
    scaled = normalized * 0.4
    confCalc = min(0.98, scaled + 0.55)
    
    math_steps = [
        f"1. abs({prop:.3f} - 0.5) = {distance:.3f}",
        f"2. {distance:.3f} / 0.5 = {normalized:.3f}",
        f"3. {normalized:.3f} * 0.4 = {scaled:.3f}",
        f"4. {scaled:.3f} + 0.55 = {(scaled + 0.55):.4f}"
    ]
    
    prompt = REASONING_PROMPT.format(
        account_id=acc_id,
        account_name=acc_info.get("account_name", acc_id),
        contact_person=acc_info.get("contact_person", "Unknown"),
        segment=acc_info.get("segment", "Unknown"),
        country=acc_info.get("country", "Unknown"),
        fund_size_eur=acc_info.get("fund_size_eur", 0),
        strategic_priority=str(acc_info.get("strategic_priority_flag", False)),
        ml_score_pct=f"{(prop * 100):.1f}%",
        confidence_pct=f"{(confCalc * 100):.1f}%",
        features_json=json.dumps(feat, indent=2),
        math_steps_json=json.dumps(math_steps, indent=2)
    )
    
    tracker.emit("ag-reason", "processing", message=f"Reasoning for {acc_id} ({i+1}/{total})...", trace_id=trace_id)
    
    try:
        res = await run_standard_chain(prompt, {})
"""

content = re.sub(r'async def process_account_reasoning.*?(?=\n        res = await run_standard_chain)', new_func, content, flags=re.DOTALL)

with open("app/modules/targeting/reasoning_agent.py", "w", encoding="utf-8") as f:
    f.write(content)

print("reasoning_agent patched")
