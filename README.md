# PubMed Research Paper Retrieval Tool

A command-line tool for searching PubMed research papers and identifying authors affiliated with pharmaceutical or biotech companies. This tool helps researchers and industry professionals find papers with industry connections.

## 🚀 Features

- **PubMed API Integration**: Search PubMed using NCBI's E-utilities
- **Affiliation Analysis**: Automatically identify pharmaceutical/biotech company affiliations
- **CSV Export**: Save results in structured CSV format
- **Flexible Search**: Support for full PubMed query syntax
- **Debug Mode**: Detailed execution information for troubleshooting
- **Rate Limiting**: Respects NCBI API rate limits with optional API key support

## 📋 Requirements

- Python 3.8 or higher
- Poetry for dependency management
- Internet connection for PubMed API access

## 🛠️ Installation

### Prerequisites

1. **Install Poetry** (if not already installed):
   ```bash
   pip install poetry
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/backend-takehome.git
   cd backend-takehome
   ```

### Setup

1. **Install dependencies**:
   ```bash
   poetry install
   ```

2. **Verify installation**:
   ```bash
   poetry run get-papers-list --help
   ```

## 🎯 Usage

### Basic Usage

```bash
# Search for papers with pharma/biotech affiliations
poetry run get-papers-list "cancer treatment"

# Search with debug information
poetry run get-papers-list "Pfizer vaccine" -d

# Save results to CSV file
poetry run get-papers-list "Moderna vaccine" -f results.csv

# Limit number of results
poetry run get-papers-list "diabetes research" --max-results 10
```

### Advanced Usage

```bash
# Use with NCBI API key for higher rate limits
poetry run get-papers-list "cancer immunotherapy" --api-key YOUR_API_KEY --email your.email@example.com

# Combine multiple options
poetry run get-papers-list "COVID-19 vaccine" -d --max-results 20 -f covid_vaccine_papers.csv
```

### Command Line Options

- `query`: Search query for PubMed (supports full PubMed query syntax)
- `-d, --debug`: Print debug information during execution
- `-f FILE, --file FILE`: Save results to CSV file
- `--max-results MAX_RESULTS`: Maximum number of results (default: 100)
- `--api-key API_KEY`: NCBI API key for higher rate limits
- `--email EMAIL`: Email address for NCBI (required for API key usage)

## 📊 Output Format

The tool outputs results in CSV format with the following columns:

| Column | Description |
|--------|-------------|
| `PubmedID` | PubMed identifier |
| `Title` | Paper title |
| `Publication Date` | Publication date |
| `Non-academic Author(s)` | Authors with industry affiliations |
| `Company Affiliation(s)` | Pharmaceutical/biotech companies |
| `Corresponding Author Email` | Contact information |

### Example Output

```csv
PubmedID,Title,Publication Date,Non-academic Author(s),Company Affiliation(s),Corresponding Author Email
37039318,Vaccine co-administration in adults: An effective way to improve vaccination coverage.,Dec 2023,Balaisyte-Jazone Lina; Posiuniene Inga; Zatoński Maciej,"GSK, Wavre, Belgium.; GSK, Wavre, Belgium.; GSK, London, UK.",
37440125,20‑Valent Pneumococcal Conjugate Vaccine: Pediatric First Approval.,Sep 2023,Shirley Matt,"Mairangi Bay, Private Bag Auckland, New Zealand.",
```

## 🏗️ Code Organization

### Project Structure

```
backend_takehome/
├── pyproject.toml          # Poetry configuration and dependencies
├── poetry.lock            # Locked dependency versions
├── cli.py                 # Main CLI entry point
├── get_papers/            # Core package
│   ├── __init__.py
│   ├── pubmed_api.py      # PubMed API client
│   └── affiliation_analyzer.py  # Affiliation analysis logic
├── tests/                 # Test suite
│   ├── test_pubmed_api.py
│   └── test_affiliation_analyzer.py
├── README.md             # This documentation
└── *.csv                 # Example output files
```

### Core Components

1. **`cli.py`**: Command-line interface with argument parsing and main execution logic
2. **`get_papers/pubmed_api.py`**: PubMed API client using NCBI E-utilities
3. **`get_papers/affiliation_analyzer.py`**: Logic for identifying pharmaceutical/biotech affiliations
4. **`tests/`**: Comprehensive test suite for all components

### Key Classes and Functions

- **`PubMedAPI`**: Handles PubMed API communication
- **`AffiliationAnalyzer`**: Analyzes author affiliations for industry connections
- **`parse_arguments()`**: CLI argument parsing
- **`main()`**: Main execution flow

## 🔧 Development

### Setting Up Development Environment

```bash
# Install all dependencies including development tools
poetry install

# Activate virtual environment
poetry shell

# Run tests
poetry run pytest

# Run linting
poetry run black .
poetry run flake8 .

# Run type checking
poetry run mypy get_papers/
```

### Adding Dependencies

```bash
# Add production dependency
poetry add package-name

# Add development dependency
poetry add --group dev package-name

# Add documentation dependency
poetry add --group docs package-name
```

### Testing

```bash
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=get_papers

# Run specific test file
poetry run pytest tests/test_pubmed_api.py
```

## 🤖 AI Tools Used in Development

This project was developed with assistance from the following AI tools:

### **Large Language Models (LLMs)**
- **Claude (Anthropic)**: Used for code generation, problem-solving, and architectural decisions
- **ChatGPT (OpenAI)**: Assisted with debugging, documentation, and code optimization
- **GitHub Copilot**: Provided real-time code completion and suggestions

### **Development Tools**
- **Cursor AI**: Enhanced code editing and refactoring capabilities
- **CodeWhisperer (AWS)**: Additional code completion and documentation assistance

### **AI-Assisted Features**
- **Code Generation**: Initial project structure and boilerplate code
- **Documentation**: README and inline code documentation
- **Testing**: Test case generation and edge case identification
- **Code Review**: Automated suggestions for code improvements
- **Dependency Management**: Poetry configuration and dependency resolution

### **Relevant Links**
- [Claude AI](https://claude.ai/) - Anthropic's AI assistant
- [ChatGPT](https://chat.openai.com/) - OpenAI's conversational AI
- [GitHub Copilot](https://github.com/features/copilot) - AI-powered code completion
- [Cursor AI](https://cursor.sh/) - AI-enhanced code editor
- [AWS CodeWhisperer](https://aws.amazon.com/codewhisperer/) - AI-powered coding companion

## 📚 Dependencies

### Production Dependencies
- `requests>=2.25.0` - HTTP library for API calls
- `urllib3>=1.26.0` - HTTP client library

### Development Dependencies
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `black>=22.0.0` - Code formatting
- `flake8>=5.0.0` - Linting
- `mypy>=1.0.0` - Type checking
- `pre-commit>=2.20.0` - Git hooks
- `pytest-mock>=3.14.1` - Mocking for tests

### Documentation Dependencies
- `sphinx>=5.0.0` - Documentation generator
- `sphinx-rtd-theme>=1.0.0` - ReadTheDocs theme

## 🚀 Deployment

### Building the Package

```bash
# Build the package
poetry build

# Install in development mode
poetry install
```

### Publishing

```bash
# Publish to PyPI (if configured)
poetry publish
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `poetry run pytest`
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **NCBI**: For providing the PubMed API
- **Poetry**: For modern Python dependency management
- **AI Tools**: For accelerating development and improving code quality

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review the test suite for usage examples

---

**Note**: This tool respects NCBI's rate limits and terms of service. For high-volume usage, consider obtaining an NCBI API key. 