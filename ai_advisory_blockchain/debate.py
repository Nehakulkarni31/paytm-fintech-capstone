import os
from stock_universe import STOCK_UNIVERSE

def run_debate(ticker: str):
    data = STOCK_UNIVERSE[ticker]
    beta = data["beta"]
    er = data["analyst_expected_return"]
    std_dev = data["std_dev"]
    
    mock_mode = os.getenv("MOCK_LLM", "1")
    
    print(f"--- MULTI-AGENT DEBATE FOR {ticker} ---")
    
    if mock_mode == "1":
        # Graded Baseline: Template-based deterministic arguments
        bull_arg = f"[BULL AGENT]: With an expected return of {er:.1%} against a beta of {beta:.2f}, {ticker} offers highly attractive risk-adjusted upside for growth-oriented portfolios."
        
        bear_arg = f"[BEAR AGENT]: While the upside is notable, {ticker}'s extreme standard deviation of {std_dev:.1%} exposes investors to massive downside risk during market corrections."
        
        synthesizer = f"[SYNTHESIZER]: The Bull correctly highlights {ticker}'s strong {er:.1%} expected return. However, the Bear's warning regarding its {std_dev:.1%} volatility is valid. Recommendation: Limit {ticker} to a small satellite position rather than a core holding."
        
        print(f"\n{bull_arg}\n\n{bear_arg}\n\n{synthesizer}")
    else:
        print("Running LLM Debate...")

if __name__ == "__main__":
    run_debate("PAYTECH")