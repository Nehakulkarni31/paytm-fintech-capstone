import os
import json
import re
from disclosure_snippets import DISCLOSURE_SNIPPETS

def extract_signals(snippet: str) -> dict:
    mock_mode = os.getenv("MOCK_LLM", "1")
    
    if mock_mode == "1":
        # Graded Baseline: Keyword/Regex Rules
        snippet_lower = snippet.lower()
        
        # 1. Risk Flags
        risk_flags = []
        if "litigation" in snippet_lower or "regulatory" in snippet_lower or "customer concentration" in snippet_lower or "top three customers" in snippet_lower:
            risk_flags.append("Identified potential legal/regulatory/concentration risk.")
            
        # 2. Hedging Detected
        hedging_keywords = ["assuming", "cautiously", "visibility"]
        hedging_detected = any(word in snippet_lower for word in hedging_keywords)
        
        # 3. Sentiment
        if "confident" in snippet_lower or "approved" in snippet_lower:
            sentiment = "confident"
        elif hedging_detected:
            sentiment = "cautious"
        else:
            sentiment = "neutral"
            
        return {
            "risk_flags": risk_flags,
            "hedging_detected": hedging_detected,
            "sentiment": sentiment
        }
    else:
        # Optional LLM path skipped
        return {}

if __name__ == "__main__":
    print("--- DISCLOSURE EXTRACTION RUN SCRIPT ---")
    for doc in DISCLOSURE_SNIPPETS:
        print(f"\nAnalyzing: {doc[:60]}...")
        result = extract_signals(doc)
        print(json.dumps(result, indent=2))