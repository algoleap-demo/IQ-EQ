import json
try:
    with open('data.json', 'r') as f:
        data = json.load(f)
        
    ws = data.get('whitespace', {})
    
    print("--- ACME-EU-90001 ---")
    for a in ws.get('top_accounts', []):
        if a['account_id'] == 'ACME-EU-90001':
            print(json.dumps(a, indent=2))
            
    print("\n--- CAMPAIGN BRIEFS ---")
    print(json.dumps(ws.get('campaign_briefs', []), indent=2))
except Exception as e:
    print(e)
