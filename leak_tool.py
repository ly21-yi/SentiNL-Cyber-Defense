import json
import os
import requests
from google import genai

# --- CONFIGURATION ---
# 1. GOOGLE GEMINI KEY (For AI Advice)
# Replace with your actual key
GOOGLE_API_KEY = "" 

# 2. BREACH DIRECTORY API KEY (For Real Data)
# Get this from RapidAPI: https://rapidapi.com/rohan-patra/api/breachdirectory
# If you don't have one, leave it as "" and the app will use the local file.
BREACH_DIRECTORY_KEY = "" 

# --- SETUP AI CLIENT ---
try:
    client = genai.Client(api_key=GOOGLE_API_KEY)
    AI_AVAILABLE = True
except Exception:
    AI_AVAILABLE = False

# --- 1. REAL API CHECK ---
def check_api_breach(email):
    """
    Queries BreachDirectory via RapidAPI.
    Returns: (sources_list, data_types_list) or None if failed.
    """
    if not BREACH_DIRECTORY_KEY or BREACH_DIRECTORY_KEY == "8a5957d047msh0daec309200b5f7p10332bjsn83f642970d6f":
        return None # API not configured

    url = "https://breachdirectory.p.rapidapi.com/"
    querystring = {"func":"auto", "term": email}
    
    headers = {
        "X-RapidAPI-Key": BREACH_DIRECTORY_KEY,
        "X-RapidAPI-Host": "breachdirectory.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if 'result' exists and is not empty
            if "result" in data and len(data["result"]) > 0:
                sources = []
                leaked_types = set()
                
                for entry in data["result"]:
                    # Extract Source Name
                    if "sources" in entry:
                        sources.extend(entry["sources"])
                    
                    # Extract Data Types
                    if "password" in entry and entry["password"]:
                        leaked_types.add("Password")
                    if "hash" in entry and entry["hash"]:
                        leaked_types.add("Password Hash")
                    if "sha1" in entry:
                        leaked_types.add("SHA1 Hash")
                        
                # If no specific types found but entry exists, assume basics
                if not leaked_types:
                    leaked_types = {"Email Address", "Unknown Data"}
                    
                return list(set(sources)), list(leaked_types)
            else:
                # API worked, but no breaches found (Safe)
                return [], []
                
    except Exception as e:
        print(f"API Error: {e}")
        return None # Fallback to local on error

    return None

# --- 2. LOCAL DATABASE (Fallback) ---
def load_local_db():
    try:
        with open("breaches.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# --- 3. MAIN FUNCTION ---
def check_email_leak(email):
    """
    Hybrid Check:
    1. Try Real API.
    2. If API fails/empty/no key, check Local DB (breaches.json).
    3. Generate AI Advice.
    """
    found = False
    sources = []
    data_leaked = []
    
    # A. Try Real API
    print(f"🔎 Checking API for {email}...")
    api_result = check_api_breach(email)
    
    if api_result is not None:
        # API Call Successful
        sources, data_leaked = api_result
        if len(sources) > 0:
            found = True
    else:
        # B. API Failed -> Fallback to Local File
        print("⚠️ API Unavailable/Empty. Using Local Database.")
        db = load_local_db()
        email_key = email.lower().strip()
        
        if email_key in db:
            found = True
            sources = db[email_key]['sources']
            data_leaked = db[email_key]['data_leaked']

    # --- 4. AI ADVICE ---
    ai_advice = "No leaks found. Stay vigilant."
    
    if found and AI_AVAILABLE:
        try:
            leaked_str = ", ".join(data_leaked[:5]) # Limit length
            prompt = (
                f"A user's data was found in a breach. The leaked fields are: {leaked_str}. "
                "Give 1 sentence of specific, urgent advice on what they must do immediately. "
                "Be serious."
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )
            ai_advice = response.text.strip()
        except Exception:
            ai_advice = "Critical data exposed. Rotate credentials immediately."

    return {
        "found": found,
        "sources": sources,
        "data_leaked": data_leaked,
        "ai_advice": ai_advice
    }

# --- TEST BLOCK ---
if __name__ == "__main__":
    print("📡 TESTING HYBRID LEAK TOOL...")
    
    # Test an email (Try your own if you have API key, or 'judge@hackathon.com' for local)
    test_email = "judge@hackathon.com" 
    print(f"\n🧪 Scanning: {test_email}")
    
    result = check_email_leak(test_email)
    
    if result['found']:
        print(f"   ⚠️ LEAK FOUND!")
        print(f"   Sources: {result['sources']}")
        print(f"   Data: {result['data_leaked']}")
        print(f"   🤖 AI Advice: {result['ai_advice']}")
    else:

        print("   ✅ Clean.")
