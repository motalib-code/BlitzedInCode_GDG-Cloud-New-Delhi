"""
Test sample data extraction specifically
"""
import os
import sys

# Force Groq configuration
os.environ["LLM_PROVIDER"] = "groq"

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_sample_data_extraction():
    """Test extraction with the exact sample data from frontend"""
    try:
        from brd_agent.backend import BRDExtractionEngine
        
        # Initialize engine
        engine = BRDExtractionEngine()
        print(f"✅ Engine initialized with {engine.llm_provider} ({engine.model_name})")
        
        # Get the exact sample email from frontend
        sample_email = """From: Jeff Skilling <jeff.skilling@enron.com>
To: Kenneth Lay <kenneth.lay@enron.com>
Date: Mon, 15 Jan 2026 09:00:00 -0800
Subject: FW: Project Raptor - Q1 Strategy & Lunch

Ken, read this. We need to move fast on the LJM partnership. 
Also, don't forget we have the all-hands lunch tomorrow. 

[ENRON CORPUS 2026 ID# 48592]
---
1. Lunch update: We are serving Italian at 12 PM in the main hall.
2. PROJECT RAPTOR REQUIREMENT: The partnership terms must be finalized by March 1. 
3. Weather update: Expect rain this weekend, bring umbrellas.
4. DECISION: Budget approved for $50M for Q1 implementation.
5. STAKEHOLDER: John Smith will lead the technical team.
---
"""
        
        print("🔄 Testing sample email extraction...")
        print(f"Sample text length: {len(sample_email)} characters")
        
        result = engine.extract_brd(sample_email)
        
        print("✅ Extraction completed!")
        print(f"Result keys: {list(result.keys())}")
        print(f"Requirements: {len(result.get('requirements', []))}")
        print(f"Decisions: {len(result.get('decisions', []))}")
        print(f"Stakeholders: {len(result.get('stakeholders', []))}")
        print(f"Confidence: {result.get('confidence_score', 0):.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Sample Extraction Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Sample Data Extraction")
    print("=" * 50)
    success = test_sample_data_extraction()
    print("=" * 50)
    if success:
        print("🎉 Sample data extraction working!")
    else:
        print("⚠️  Issues with sample data extraction.")
