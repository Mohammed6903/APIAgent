# 🚀 API Agent: Intelligent API Testing & Documentation

## Table of Contents

* [🚀 API Agent: Intelligent API Testing & Documentation](#-api-agent-intelligent-api-testing--documentation)

  * [Table of Contents](#table-of-contents)
  * [✨ Project Overview](#-project-overview)
  * [💡 Key Features](#-key-features)
  * [📂 Project Structure](#-project-structure)
  * [🛠️ Technologies Used](#%EF%B8%8F-technologies-used)
  * [📊 API Testing Report Highlights](#-api-testing-report-highlights)
  * [📈 Recommendations & Future Improvements](#-recommendations--future-improvements)
  * [🏃‍♀️ Getting Started](#%EF%B8%8F-getting-started)
  * [🤝 Contributing](#-contributing)
  * [📄 License](#-license)
  * [📞 Contact](#-contact)

## ✨ Project Overview

The **API Agent** is an innovative, AI-powered system designed to **automate and streamline the rigorous process of API testing and documentation generation**. This project leverages intelligent agents to systematically analyze API structures, execute comprehensive tests, validate data integrity against documented schemas, and dynamically generate precise OpenAPI documentation.

Our goal is to ensure high API quality, consistency, and reliability by identifying discrepancies between API behavior and its documentation, thereby significantly reducing manual effort and improving developer efficiency.

## 💡 Key Features

* **Intelligent API Testing**: Automated execution of GET, POST, PUT, DELETE, and other HTTP requests across all identified endpoints.
* **Strict Data Type Validation**: Rigorous comparison of actual API response data types against documented OpenAPI schemas, flagging mismatches at a field level.
* **Dynamic Documentation Generation**: Automatically generates and saves OpenAPI 3.0 compliant JSON documentation based on code analysis, providing accurate parameter, request body, and response schemas.
* **Comprehensive Reporting**: Produces detailed Markdown reports summarizing API health, per-endpoint validation results, data type compliance issues, and actionable recommendations.
* **Systematic Endpoint Tracking**: Utilizes a persistent tracker to manage endpoint testing status (pending, tested, failed, skipped), ensuring full coverage and preventing duplicate tests.
* **Error Handling & Resilience**: Gracefully manages network timeouts, connection errors, and distinguishes between API failures and infrastructure issues, ensuring continuous testing.
* **Modular Agent Architecture**: Built with a clear separation of concerns using `agno.agent` and `agno.team`, allowing for scalable and maintainable development.

## 📂 Project Structure

```
mohammed6903-apiagent/
├── api_documentation.json        # Automatically generated OpenAPI documentation
├── api_testing_report.md         # Detailed markdown report of API test results
├── Documentor.py                 # Agent responsible for generating and saving API documentation
├── main.py                       # Main orchestration script for the API testing team
├── tmp/
│   └── memory.db                 # SQLite database for persistent agent memory
└── Tools/
    ├── api.py                    # Tool for sending HTTP API requests
    ├── endpoints.py              # Tool for tracking and managing API endpoints
    └── file.py                   # Utility tools for file system operations (e.g., directory tree, save file)
```

## 🛠️ Technologies Used

* **Python 3.x**
* **Agno Framework**: For building multi-agent systems and orchestrating workflows.
* **Google Gemini Models**: `gemini-2.5-flash-preview-04-17` for intelligent agent capabilities.
* **`requests` Library**: For making HTTP requests to API endpoints.
* **SQLite**: For persistent memory storage (`tmp/memory.db`).
* **OpenAPI/Swagger**: For API documentation specification.

## 🏃‍♀️ Getting Started

To run this project locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mohammed6903/apiagent
   cd APIAgent
   ```
2. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
4. **Run the main script:**

   ```bash
   python main.py
   ```

   The `main.py` script will orchestrate the `documentor` and `tester` agents to interact with the specified API (e.g., `http://127.0.0.1:8000`). It will generate `api_documentation.json` and `api_testing_report.md` in the project root.

*Note: Ensure you have an API running at `http://127.0.0.1:8000` with an accessible OpenAPI specification at `http://127.0.0.1:8000/openapi.json` for the full testing suite to execute.*

## 🤝 Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.
