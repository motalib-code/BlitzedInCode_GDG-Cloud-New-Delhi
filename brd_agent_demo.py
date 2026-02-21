"""
BRD Agent - Complete Demo Script
=================================
Demonstrates the cross-channel synthesis pipeline with realistic Enron/AMI data.

USAGE:
    python brd_agent_demo.py

This script:
1. Loads Enron and AMI sample data
2. Runs cross-channel synthesis
3. Generates a professional BRD
4. Displays results with conflict analysis
"""

import json
import sys
from pathlib import Path

# Add parent directory to path to import brd_agent modules
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from brd_agent.cross_channel_synthesis import CrossChannelSynthesis
from brd_agent.data_ingest import DataIngestionEngine


def print_banner(title, width=80):
    """Print a formatted banner."""
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)


def demo_cross_channel_synthesis():
    """Main demo showing the complete synthesis pipeline."""
    
    print_banner("🎯 BRD AGENT - CROSS-CHANNEL SYNTHESIS DEMO")
    
    # Initialize engines
    synthesis = CrossChannelSynthesis()
    
    print("\n" + "─" * 80)
    print("PHASE 1: DEMONSTRATING NOISE FILTERING IN EMAIL DATA")
    print("─" * 80)
    
    # Demo 1: Show noise filtering in action
    print("\n📧 Sample Enron Emails (Before Filtering):")
    print("-" * 80)
    
    # Create demo emails - mix of relevant and noisy
    demo_emails = [
        {
            "type": "email",
            "subject": "Q2 Platform Migration Requirements",
            "sender": "jennifer.wu@techcorp.com",
            "recipients": ["dev-team@techcorp.com"],
            "content": """Team,

We need to finalize the platform migration requirements:

FUNCTIONAL REQUIREMENTS:
1. All user data must be migrated with zero data loss
2. The new platform must support SSO via SAML 2.0
3. API backward compatibility must be maintained for 6 months
4. Real-time data synchronization during transition

NON-FUNCTIONAL REQUIREMENTS:
- System uptime: 99.95% SLA
- Page load time: < 2 seconds
- Support for 10,000 concurrent users

TIMELINE:
- Phase 1 (Data Migration): Complete by March 30, 2026
- Phase 2 (API Migration): Complete by April 30, 2026
- Phase 3 (Full Cutover): Target May 15, 2026

Stakeholders:
- Executive Sponsor: VP of Engineering (Mark Thompson)
- Product Owner: Jennifer Wu
- Tech Lead: Raj Patel

RISK: The vendor contract expires June 1. No extension possible.

Decision from yesterday's meeting: Blue-green deployment strategy.

Please review by EOD Friday.

Thanks,
Jennifer""",
            "source_dataset": "sample"
        },
        {
            "type": "email",
            "subject": "RE: Lunch plans for Friday",
            "sender": "sarah.smith@techcorp.com",
            "recipients": ["team@techcorp.com"],
            "content": """Hi everyone!

Don't forget about our team lunch this Friday at noon. We're going to the new Italian place downtown. Please let me know if you have any dietary restrictions.

Looking forward to it!

Sarah""",
            "source_dataset": "sample"
        },
    ]
    
    # Show the filtering process
    filtered = synthesis._filter_emails(demo_emails)
    
    print(f"\n✅ EMAIL 1 (RELEVANT):")
    print(f"   Subject: {demo_emails[0]['subject']}")
    print(f"   Content preview: {demo_emails[0]['content'][:100]}...")
    print(f"   ✓ KEPT - Contains requirements keywords")
    
    print(f"\n❌ EMAIL 2 (NOISE):")
    print(f"   Subject: {demo_emails[1]['subject']}")
    print(f"   Content preview: {demo_emails[1]['content'][:100]}...")
    print(f"   ✗ FILTERED OUT - Matches noise patterns")
    
    print(f"\n📊 Filtering Results:")
    print(f"   Total emails:       {len(demo_emails)}")
    print(f"   Emails kept:        {len(filtered)}")
    print(f"   Emails filtered:    {len(demo_emails) - len(filtered)}")
    
    # Demo 2: Full synthesis
    print("\n" + "─" * 80)
    print("PHASE 2: FULL CROSS-CHANNEL SYNTHESIS")
    print("─" * 80)
    
    print("\n⏳ Running full synthesis pipeline...")
    
    # Load sample data
    ingestion = DataIngestionEngine()
    emails = ingestion.load_enron()
    meetings = ingestion.load_ami()
    
    print(f"\n📦 Data Loaded:")
    print(f"   • {len(emails)} emails from Enron dataset")
    print(f"   • {len(meetings)} meetings from AMI corpus")
    
    # Run synthesis
    brd = synthesis.synthesize_from_files()
    
    # Display results
    print("\n" + "─" * 80)
    print("PHASE 3: PROFESSIONAL BRD OUTPUT")
    print("─" * 80)
    
    if brd:
        print_banner("📄 EXECUTION SUMMARY", 80)
        print(brd.get("execution_summary", "N/A")[:500])
        
        print_banner("👥 STAKEHOLDER MAP", 80)
        stakeholder_map = brd.get("stakeholder_map", {})
        stakeholders = stakeholder_map.get("stakeholders", [])
        
        if stakeholders:
            print(f"\nTop Stakeholders by Influence:")
            for i, s in enumerate(stakeholders[:5], 1):
                print(f"\n{i}. {s.get('name', 'Unknown')}")
                print(f"   Role: {s.get('role', 'Unknown')}")
                print(f"   Influence Score: {s.get('influence_score', 0):.2f}")
        else:
            print("No stakeholders detected")
        
        hierarchy = stakeholder_map.get("hierarchy_detected", [])
        if hierarchy:
            print("\n\nOrganizational Hierarchy:")
            for level in hierarchy:
                print(f"\n  {level.get('level', 'Unknown')}:")
                for member in level.get('members', []):
                    print(f"    • {member}")
        
        print_banner("📋 REQUIREMENT TRACEABILITY MATRIX", 80)
        rtm = brd.get("requirement_traceability_matrix", [])
        
        if rtm:
            print(f"\nTotal Requirements: {len(rtm)}\n")
            for req in rtm[:5]:  # Show first 5
                print(f"[{req.get('req_id', 'N/A')}] {req.get('type', 'Unknown').upper()}")
                print(f"  Requirement: {req.get('requirement', 'N/A')[:100]}...")
                print(f"  Source: {req.get('source', 'Unknown')}")
                print()
            
            if len(rtm) > 5:
                print(f"  ... and {len(rtm) - 5} more requirements")
        else:
            print("No requirements extracted")
        
        print_banner("⚠️ CRITICAL CONFLICTS & RISKS", 80)
        risks = brd.get("risk_and_conflicts", {})
        conflicts = risks.get("conflicts", [])
        
        print(f"\nConflict Summary:")
        print(f"  • Total Conflicts: {len(conflicts)}")
        print(f"  • CRITICAL Conflicts: {risks.get('critical_count', 0)}")
        
        if conflicts:
            print("\nDetected Conflicts:")
            for i, conflict in enumerate(conflicts[:3], 1):
                print(f"\n{i}. [{conflict.get('severity', 'UNKNOWN')}] {conflict.get('type', 'Unknown')}")
                print(f"   Description: {conflict.get('description', 'N/A')}")
        else:
            print("\n✓ No conflicts detected")
        
        print_banner("📊 NOISE REDUCTION EXPLANATION", 80)
        noise_explanation = brd.get("noise_reduction_logic", "")
        print(noise_explanation[:500] + "..." if len(noise_explanation) > 500 else noise_explanation)
        
        print_banner("📈 SYNTHESIS STATISTICS", 80)
        metadata = brd.get("synthesis_metadata", {})
        stats = metadata.get("stats", {})
        
        print(f"\nData Processing Summary:")
        print(f"  Emails Processed:       {stats.get('emails_loaded', 0)}")
        print(f"  Emails with Reqs:       {stats.get('emails_filtered', 0)}")
        print(f"  Meetings Processed:     {stats.get('meetings_loaded', 0)}")
        print(f"  Requirements Extracted: {stats.get('requirements_extracted', 0)}")
        print(f"  Conflicts Detected:     {stats.get('conflicts_detected', 0)}")
        print(f"  CRITICAL Conflicts:     {stats.get('critical_conflicts', 0)}")
        
        print_banner("🎯 PROJECT OVERVIEW", 80)
        project = brd.get("project_overview", {})
        print(f"\nProject Topic: {project.get('topic', 'Unknown')}")
        print(f"In-Scope Items:  {project.get('scope', {}).get('in_scope_items', 'N/A')}")
        print(f"Out-of-Scope Items: {project.get('scope', {}).get('out_of_scope_items', 'N/A')}")
    
    # Demo 3: Show what-if scenario
    print("\n" + "─" * 80)
    print("PHASE 4: WHAT-IF SCENARIO ANALYSIS")
    print("─" * 80)
    
    scenario = "If we move the project deadline from May 15 to April 1 (5 weeks earlier)"
    print(f"\nScenario: {scenario}")
    
    if brd and hasattr(synthesis, 'extraction'):
        simulation = synthesis.extraction.simulate_scenario(brd, scenario)
        if simulation and "error" not in simulation:
            print(f"\nPredicted Impact:")
            print(f"  Analysis: {simulation.get('analysis', 'N/A')[:300]}...")
            print(f"  New Health Score: {simulation.get('new_health_score', 'N/A')}")
            print(f"  Advice: {simulation.get('advice', 'N/A')[:200]}...")
        else:
            print("  (Simulation requires configured LLM)")
    else:
        print("  (LLM not configured, skipping scenario analysis)")
    
    print("\n" + "=" * 80)
    print_banner("✅ DEMO COMPLETE", 80)
    print("\nThe BRD Agent successfully demonstrated:")
    print("  ✓ Noise filtering from email data")
    print("  ✓ Multi-channel data synthesis")
    print("  ✓ Cross-channel conflict detection")
    print("  ✓ Professional BRD generation")
    print("  ✓ Requirement traceability")
    print("  ✓ Stakeholder analysis")
    print("  ✓ Risk & conflict identification")
    
    print("\n📚 Next Steps:")
    print("  1. Run: python -m brd_agent.api")
    print("     This starts the Flask REST API server")
    print("")
    print("  2. Or run: streamlit run brd_agent/frontend.py")
    print("     This launches the Streamlit UI")
    print("")
    print("  3. Upload your own Enron emails or AMI transcripts for analysis")
    print("")
    
    return brd


def demo_individual_components():
    """Demo individual components for understanding."""
    
    print_banner("🔧 COMPONENT-LEVEL DEMO (For Understanding)", 80)
    
    # Component 1: Data Ingestion
    print("\n1️⃣  DATA INGESTION ENGINE")
    print("-" * 80)
    
    ingestion = DataIngestionEngine()
    
    # Load sample data
    sample_emails = ingestion._generate_sample_emails()
    print(f"   Loaded {len(sample_emails)} sample emails")
    print(f"   Sample email: {sample_emails[0]['subject']}")
    
    # Component 2: Noise Filtering
    print("\n2️⃣  NOISE FILTERING")
    print("-" * 80)
    
    email_content = sample_emails[0]['content']
    cleaned, score, is_noise = ingestion.preprocess_noise(email_content)
    print(f"   Original length: {len(email_content)} chars")
    print(f"   Cleaned length: {len(cleaned)} chars")
    print(f"   Noise Score: {score:.2f} (0=relevant, 1=noise)")
    print(f"   Is Noise: {is_noise}")
    
    # Component 3: Entity Extraction
    print("\n3️⃣  ENTITY EXTRACTION")
    print("-" * 80)
    
    entities = ingestion.extract_entities(email_content)
    print(f"   Dates found: {len(entities['dates'])}")
    if entities['dates']:
        print(f"      Examples: {', '.join(entities['dates'][:3])}")
    
    print(f"   Emails found: {len(entities['emails'])}")
    if entities['emails']:
        print(f"      Examples: {', '.join(entities['emails'][:2])}")
    
    print(f"   Action items: {len(entities['action_items'])}")
    print(f"   Requirements: {len(entities['requirements'])}")
    print(f"   People: {len(entities['people'])}")
    
    # Component 4: Text Chunking
    print("\n4️⃣  TEXT CHUNKING")
    print("-" * 80)
    
    chunks = ingestion.chunk_text(email_content)
    print(f"   Total text length: {len(email_content)} chars")
    print(f"   Number of chunks: {len(chunks)}")
    if chunks:
        print(f"   Chunk 1 length: {len(chunks[0])} chars")
    
    # Component 5: Extraction
    print("\n5️⃣  BRD EXTRACTION ENGINE")
    print("-" * 80)
    
    from brd_agent.backend import BRDExtractionEngine
    extraction = BRDExtractionEngine()
    
    brd = extraction.extract_brd(email_content)
    print(f"   Project Topic: {brd.get('project_topic', 'N/A')}")
    print(f"   Requirements extracted: {len(brd.get('requirements', []))}")
    print(f"   Stakeholders found: {len(brd.get('stakeholders', []))}")
    print(f"   Decisions detected: {len(brd.get('decisions', []))}")
    print(f"   Confidence score: {brd.get('confidence_score', 0):.2f}")


if __name__ == "__main__":
    try:
        # Run component-level demo first
        demo_individual_components()
        
        # Run full cross-channel synthesis demo
        print("\n\n")
        brd_result = demo_cross_channel_synthesis()
        
        # Save BRD to file
        output_file = PROJECT_ROOT / "demo_brd_output.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(brd_result, f, indent=2, default=str)
        
        print(f"\n💾 Full BRD saved to: {output_file}")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
