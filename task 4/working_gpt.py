import requests
import json
import time

# --- CONFIGURATION ---
# 1. Replace with your actual key
API_KEY = "AIzaSyCtnYYfuqfOBev6JDuNHUwxTanhdyJjwZo" 

# 2. Use a 2026-supported model. 
# Options: 'gemini-2.5-flash' (Best balance) or 'gemini-3-flash-preview' (Latest)
MODEL_NAME = "gemini-2.5-flash" 
# ---------------------

def ask_ai(question):
    # Updated to 'v1' stable endpoint for better reliability in 2026
    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL_NAME}:generateContent?key={API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": question}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        result = response.json()
        
        if response.status_code == 200:
            if 'candidates' in result and result['candidates']:
                return result['candidates'][0]['content']['parts'][0]['text']
            return "Error: AI response structure was empty."
        
        # Specific fix for 404 (Model Not Found)
        elif response.status_code == 404:
            return f"Error (404): The model '{MODEL_NAME}' is not available for your project. Try 'gemini-3-flash-preview'."
            
        elif response.status_code == 429:
            return "Error (429): Rate limit exceeded. Please wait 10-20 seconds."
            
        else:
            error_msg = result.get('error', {}).get('message', 'Unknown Error')
            return f"API Error ({response.status_code}): {error_msg}"
        
    except Exception as e:
        return f"System Error: {str(e)}"

def main():
    print(f"--- {MODEL_NAME.upper()} Text Generator ---")
    
    if "PASTE_YOUR_KEY" in API_KEY:
        print("!!! ERROR: Please paste your API key inside the script first.")
        return

    while True:
        user_input = input("\nYour Question (type 'exit' to quit): ")
        if user_input.lower() in ['exit', 'quit']: break
        if not user_input.strip(): continue

        print("Generating...")
        answer = ask_ai(user_input)
        print(f"\nAnswer:\n{answer}")
        
        # Respecting free tier limits
        time.sleep(2)

if __name__ == "__main__":
    main()