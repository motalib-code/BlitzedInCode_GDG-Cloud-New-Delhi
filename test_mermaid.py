"""
Test mermaid diagram generation
"""
import os
import sys

# Force Groq configuration
os.environ["LLM_PROVIDER"] = "groq"

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_mermaid_generation():
    """Test if mermaid diagrams are generated properly"""
    try:
        from brd_agent.backend import BRDExtractionEngine
        
        # Initialize engine
        engine = BRDExtractionEngine()
        print(f"✅ Engine initialized with {engine.llm_provider} ({engine.model_name})")
        
        # Test extraction with mermaid
        sample_text = """
        Project Alpha Requirements:
        1. User authentication system by March 15th
        2. API integration with payment gateway
        3. Dashboard for analytics
        
        Decisions:
        - Use OAuth2 for authentication
        - Budget approved: $50,000
        
        Stakeholders:
        - John (Project Manager)
        - Sarah (Lead Developer)
        """
        
        print("🔄 Testing BRD extraction with mermaid generation...")
        result = engine.extract_brd(sample_text)
        
        # Check if mermaid code was generated
        mermaid_code = result.get("mermaid_code", "")
        print(f"Result keys: {list(result.keys())}")
        print(f"Mermaid code: '{mermaid_code}'")
        print(f"Mermaid code type: {type(mermaid_code)}")
        print(f"Mermaid code empty? {not mermaid_code or not mermaid_code.strip()}")
        
        if mermaid_code and mermaid_code.strip():
            print("✅ Mermaid diagram generated successfully!")
            print(f"Mermaid code length: {len(mermaid_code)} characters")
            print("Sample mermaid code:")
            print(mermaid_code[:200] + "..." if len(mermaid_code) > 200 else mermaid_code)
            return True
        else:
            print("❌ No mermaid code generated")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Mermaid Diagram Generation")
    print("=" * 50)
    success = test_mermaid_generation()
    print("=" * 50)
    if success:
        print("🎉 Mermaid generation working!")
    else:
        print("⚠️  Issues with mermaid generation.")
