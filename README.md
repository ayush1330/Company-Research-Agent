# Company Research Agent

A powerful AI-powered tool that helps job seekers research companies and prepare for interviews by providing detailed insights into company backgrounds and interview processes. The agent uses web research and AI analysis to generate comprehensive preparation guides.

## 🚀 Features

- **Company Background Research**: Get detailed information about a company's size, industry, culture, values, and recent news.
- **Interview Process Insights**: Learn about typical interview stages, duration, assessment methods, and common questions.
- **Comprehensive Preparation Guide**: Receive a personalized preparation guide including:
  - Preparation timeline with actionable steps
  - Technical topics and resources
  - Behavioral interview preparation
  - Company-specific tips
  - Interview day advice
  - Follow-up strategies
- **Web Research Integration**: Automatically gathers and analyzes information from multiple sources.
- **Structured Data Output**: Returns well-structured data in JSON format for easy processing.
- **Robust Error Handling**: Gracefully handles errors and provides fallback content.

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/company-research-agent.git
   cd company-research-agent
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the `.env` file with your API keys:
     ```
     # OpenAI API Key (required)
     OPENAI_API_KEY=your_openai_api_key_here
     
     # Firecrawl API Key (if required)
     FIRECRAWL_API_KEY=your_firecrawl_api_key_here
     
     # LangSmith Configuration (optional)
     LANGCHAIN_TRACING_V2=true
     LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
     LANGCHAIN_API_KEY=your_langsmith_api_key_here
     LANGCHAIN_PROJECT=your_project_name_here
     ```

## 🛠 Usage

### Command Line Interface

Run the main application:
```bash
python main.py
```

Follow the interactive prompts to enter the company name and job role.

### Programmatic Usage

You can also use the workflow programmatically:

```python
from src.workflow import Workflow

# Initialize the workflow
workflow = Workflow()

# Run the workflow
result = workflow.run(
    company="Google",
    role="Software Engineer"
)

# Access the results
print("Company Background:", result.background)
print("Interview Process:", result.interview_process)
print("Preparation Guide:", result.preparation_guide)
```

### Test Script

A test script is provided to quickly test the workflow:

```bash
# Test with default values (Google, Software Engineer)
python test_workflow.py

# Test with custom company and role
python test_workflow.py "Microsoft" "Data Scientist"
```

3. Example usage:
   ```
   ==================================================
   🌟 Interview Research Agent
   ==================================================
   
   Please provide the company and job role:
   🏢 Company: Google
   💼 Job Role: Software Engineer
   ```

## 🏗 Project Structure

- `main.py`: Entry point of the application
- `src/`: Source code directory
  - `workflow.py`: Main workflow logic
  - `models.py`: Data models
  - `prompts.py`: Prompt templates
  - `firecrawl.py`: Web scraping utilities
  - `langsmith_config.py`: LangSmith configuration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python and LangChain
- Uses Firecrawl for web scraping
- Inspired by the challenges of technical interview preparation