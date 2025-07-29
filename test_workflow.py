import os
import sys
from dotenv import load_dotenv
from src.workflow import Workflow

# Load environment variables
load_dotenv()

def test_workflow(company: str, role: str):
    """Test the workflow with the given company and role."""
    print(f"🚀 Starting test workflow for {role} at {company}")
    print("-" * 50)
    
    # Initialize and run the workflow
    workflow = Workflow()
    result = workflow.run(company=company, role=role)
    
    # Print the results
    print("\n" + "="*50)
    print(f"✅ Workflow completed for {role} at {company}")
    print("="*50)
    
    # Print company background
    if hasattr(result, 'background') and result.background:
        print("\n📋 Company Background:")
        print("-" * 30)
        print(f"Size: {result.background.company_size}")
        print(f"Industry: {result.background.industry}")
        print(f"Culture: {result.background.company_culture}")
        print(f"Values: {', '.join(result.background.values[:3])}..." if result.background.values else "No values found")
    
    # Print interview process
    if hasattr(result, 'interview_process') and result.interview_process:
        print("\n📝 Interview Process:")
        print("-" * 30)
        print(f"Stages: {', '.join(result.interview_process.typical_stages[:3])}..." if result.interview_process.typical_stages else "No stages found")
        print(f"Duration: {result.interview_process.duration}")
        print(f"Technical Assessment: {'Yes' if result.interview_process.technical_assessment else 'No'}")
        print(f"System Design: {'Yes' if result.interview_process.system_design else 'No'}")
    
    # Print preparation guide overview
    if hasattr(result, 'preparation_guide') and result.preparation_guide:
        print("\n📚 Preparation Guide:")
        print("-" * 30)
        print(result.preparation_guide.overview[:500] + "..." if len(result.preparation_guide.overview) > 500 else result.preparation_guide.overview)
        
        # Print timeline if available
        if hasattr(result.preparation_guide, 'preparation_timeline') and result.preparation_guide.preparation_timeline:
            print("\n⏰ Preparation Timeline:")
            for i, step in enumerate(result.preparation_guide.preparation_timeline[:3], 1):
                print(f"{i}. {step[:100]}..." if len(step) > 100 else f"{i}. {step}")
    
    print("\n" + "="*50)
    print(f"🎉 Test completed for {role} at {company}")
    print("="*50)

if __name__ == "__main__":
    # Default test values
    test_company = "Google"
    test_role = "Software Engineer"
    
    # Use command line arguments if provided
    if len(sys.argv) > 1:
        test_company = sys.argv[1]
    if len(sys.argv) > 2:
        test_role = " ".join(sys.argv[2:])
    
    test_workflow(test_company, test_role)
