from google import genai
import os

# --- SETUP AI CLIENT ---
# Replace with your actual Gemini API Key
api_key = "" 

try:
    client = genai.Client(api_key=api_key)
    AI_AVAILABLE = True
except Exception as e:
    AI_AVAILABLE = False

def check_scam(text):
    """
    1. Uses Expanded Keyword Heuristics (Fast Check).
    2. Uses Gemini to analyze tone/intent (Deep Check).
    """
    # 1. Safety Check: If text is empty
    if not text: 
        return {
            "score": 0,
            "risk_level": "SAFE",
            "triggers": [],
            "ai_analysis": "No text provided."
        }

    # --- 2. HEURISTIC CHECK (Massive Keyword List) ---
    triggers = [
        "urgent", "immediately", "suspended", "verify your account",
        "irs", "social security", "gift card", "bitcoin", "western union",
        "inheritance", "lottery", "winner", "click here", "password expired",
        "unusual activity", "bank of america", "wellsfargo", "chase", 
        "kindly", "dear customer", "security alert", "respond now", "immediate action required",
        "account locked", "unauthorized login", "login to continue", "confirm identity", "update details",
        "change password", "recover account", "trusted message", "secure link", "security portal", "risk-free",
        "limited time offer", "act now", "binance", "coinbase", "instant payout", "guaranteed profits", "secret trading strategy",
        "last warning", "your account will be closed", "critical alert", "security breach", "fraud detected",
        "identity verification required", "reactivate your account", "unusual payment attempt", "unable to process your payment",
        "failure to respond", "take action", "unclaimed funds", "refund availible", "overpayment", "temporary hold",
        "your device", "malware detected", "security report", "call support immediately", "microsoft technician",
        "virus removal", "system compromised", "cashapp", "venmo", "zelle", "wire transfer", "paypal",
        "i need your help", "high paying", "no experience required", "easy money", "court notice", "arrest warrant",
        "legal action pending", "violation notice", "pay immediately", "apple id", "google account", "microsoft account team",
        "amazon billing", "norton", "mcafee", "secure login page", "verify ownership", "unlock access", "click the link"
    ]
    
    text_lower = text.lower()
    found_triggers = [word for word in triggers if word in text_lower]
    
    # Base score: 10 points per keyword (Lowered from 15 to prevent false positives)
    score = len(found_triggers) * 10 
    
    # Cap heuristic score at 60. 
    # We want keywords to warn the user, but only AI can trigger "100% Critical".
    if score > 60: score = 60

    # --- 3. AI ANALYSIS (Gemini) ---
    ai_analysis = "AI Neural Link Offline. Relying on keyword heuristics."
    
    if AI_AVAILABLE:
        try:
            # STRICT PROMPT: Forces AI to start with a specific Verdict tag
            prompt = (
                f"Analyze this text for scam potential: '{text}'. "
                "1. Start your answer with exactly 'VERDICT: DANGER' or 'VERDICT: SAFE'. "
                "2. Then explain the psychological trick being used (e.g., false urgency, authority bias) or why it seems normal. "
                "Keep it under 50 words."
            )
            
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )
            ai_analysis = response.text.strip()
            
            # --- LOGIC FIX ---
            # Only trigger MAX SCORE if AI explicitly says DANGER.
            if "VERDICT: DANGER" in ai_analysis.upper():
                score = 100  # AI confirms it is a scam
            elif "VERDICT: SAFE" in ai_analysis.upper():
                score = 0    # AI confirms it is safe (overrides keywords)
                
        except Exception:
            ai_analysis = "AI Connection Failed. Using local database."

    # Determine Risk Label
    risk_level = "SAFE"
    if score >= 80: risk_level = "CRITICAL"
    elif score >= 30: risk_level = "MODERATE"

    # --- 4. RETURN DATA ---
    return {
        "score": score,
        "risk_level": risk_level,
        "triggers": found_triggers,
        "ai_analysis": ai_analysis 
    }

# --- TEST BLOCK ---
if __name__ == "__main__":
    print("🛑 TESTING SCAM INTERCEPTOR...")
    
    # Test a scam text
    scam_text = "URGENT: Your Wells Fargo account is suspended. Click here to verify immediately."
    print(f"\n🧪 Testing Text: '{scam_text}'")
    
    result = check_scam(scam_text)
    print(f"   Risk Level: {result['risk_level']} (Score: {result['score']})")
    print(f"   Triggers: {result['triggers']}")
    print(f"   🤖 AI Analysis: {result['ai_analysis']}")
    

    print("\n✅ SCAM TOOL TEST COMPLETE.")
