from dotenv import load_dotenv
import os
from src.workflow import Workflow
from src.langsmith_config import langsmith_config
import time

load_dotenv()

# Initialize LangSmith

def display_company_background(background):
    print("\n🏢 Company Information")
    print("=" * 40)
    print(f"- Size: {background.company_size}")
    print(f"- Industry: {background.industry}")
    print(f"- Culture: {background.company_culture}")
    if background.values:
        print(f"- Values: {', '.join(background.values)}")
    if background.recent_news:
        print("- Recent News:")
        for news in background.recent_news[:3]:
            print(f"  • {news}")

def display_interview_process(process):
    print("\n📋 Interview Process")
    print("=" * 40)
    print(f"- Duration: {process.duration}")
    print("- Stages:")
    for i, stage in enumerate(process.typical_stages, 1):
        print(f"  {i}. {stage}")
    
    print("\n🔍 Assessment Methods:")
    if process.technical_assessment:
        print("  • Technical Assessments")
    if process.coding_challenges:
        print("  • Coding Challenges")
    if process.system_design:
        print("  • System Design")
    if process.behavioral_focus:
        print("  • Behavioral Interviews")
    if process.take_home_projects:
        print("  • Take-home Projects")
    
    if process.common_questions:
        print("\n❓ Common Questions:")
        for i, question in enumerate(process.common_questions[:5], 1):
            print(f"  {i}. {question}")

def display_preparation_guide(guide):
    print("\n📚 Preparation Guide")
    print("=" * 40)
    
    if guide.technical_topics:
        print("- Technical Topics to Focus On:")
        for i, topic in enumerate(guide.technical_topics[:5], 1):
            print(f"  {i}. {topic}")
    
    if guide.behavioral_topics:
        print("\n- Behavioral Areas to Prepare:")
        for i, topic in enumerate(guide.behavioral_topics[:3], 1):
            print(f"  {i}. {topic}")
    
    if guide.resources:
        print("\n- Recommended Resources:")
        for i, resource in enumerate(guide.resources[:3], 1):
            print(f"  {i}. {resource}")
    
    if guide.strategy:
        print("\n💡 Preparation Strategy:")
        print(f"  {guide.strategy}")
    
    if guide.common_pitfalls:
        print("\n⚠️ Common Pitfalls to Avoid:")
        for i, pitfall in enumerate(guide.common_pitfalls[:3], 1):
            print(f"  {i}. {pitfall}")

def main():
    # Initialize LangSmith
    langsmith_config.setup()
    
    workflow = Workflow()
    print("\n" + "=" * 50)
    print("🌟 Interview Research Agent")
    print("=" * 50)
    
    while True:
        print("\n" + "-" * 50)
        print("ℹ️  Type 'quit' or 'exit' at any prompt to end the program")
        print("-" * 50)
        print("\nPlease provide the company and job role:")
        
        company = input("🏢 Company: ").strip()
        if company.lower() in {"quit", "exit"}:
            print("\n👋 Exiting Interview Research Agent. Good luck with your interview preparation!")
            break
            
        role = input("💼 Job Role: ").strip()
        if role.lower() in {"quit", "exit"}:
            print("\n👋 Exiting Interview Research Agent. Good luck with your interview preparation!")
            break

        if company and role:
            # Create tracing config
            config = langsmith_config.create_config(
                company=company, 
                role=role,
                tags=["research-agent", "interview-prep"]
            )
            
            try:
                start_time = time.time()
                print(f"\n🔍 Starting research for {role} at {company}...")
                
                # Execute research workflow
                result = workflow.run(company, role, config=config)
                
                print(f"\n✅ Research completed in {time.time() - start_time:.1f} seconds")
                print("=" * 60)
                
                # Display results
                if result.background:
                    display_company_background(result.background)
                
                if result.interview_process:
                    display_interview_process(result.interview_process)
                
                if result.preparation_guide:
                    display_preparation_guide(result.preparation_guide)
                    
                # LangSmith trace link
                if langsmith_config.is_enabled:
                    print("\n" + "=" * 80)
                    print(f"🔍 Research trace available at: https://smith.langchain.com/")
                    
            except Exception as e:
                print(f"❌ Research failed: {e}")
                if langsmith_config.is_enabled:
                    print("Check LangSmith for detailed error traces")
        else:
            print("⚠️ Please provide both company and job role")

if __name__ == "__main__":
    main()