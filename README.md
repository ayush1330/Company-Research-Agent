# Company Research Agent

A powerful AI-powered tool that helps job seekers research companies and prepare for interviews by providing detailed insights into company backgrounds and interview processes.

## 🚀 Features

- **Company Background Research**: Get detailed information about a company's size, industry, culture, and recent news.
- **Interview Process Insights**: Learn about typical interview stages, assessment methods, and common questions.
- **Personalized Preparation Guide**: Receive tailored preparation advice including technical topics, behavioral areas, and recommended resources.
- **Command-Line Interface**: Simple and intuitive interface for easy interaction.
- **LangSmith Integration**: Built-in support for LangSmith for tracing and debugging.

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
   pip install -e .
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add your API keys:
   ```
   LANGCHAIN_API_KEY=your_langchain_api_key
   # Add other required API keys
   ```

## 🛠 Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Follow the interactive prompts:
   - Enter the company name you're interested in
   - Specify the job role you're applying for
   - Review the generated research and preparation guide

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