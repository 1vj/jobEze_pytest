# 🚀 automation-framework

A **pytest-based test automation framework** for validating and assuring quality of web applications.

---

## 📋 System Prerequisites

- ✅ Python **3.7+**
- ✅ OS: **Ubuntu** / **macOS** / **Windows**
- ✅ Google **Chrome** and **Firefox** installed and added to system path

---

## ⚙️ Setup Instructions

1. **Clone the repo and navigate to it**  
   *(Skip if already inside the project folder)*

2. **Create a virtual environment**  
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**

   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```

   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## ✅ Running Tests with Pytest

### 🔹 Basic Command
```bash
pytest
```

### 🔹 Run in Headless Mode (no browser UI)
```bash
pytest --headless
```

### 🔹 Run Against Specific Environment (from `config/env.json`)
```bash
pytest --env=dev
```

### 🔹 Run with Both Options
```bash
pytest --env=dev --headless
```

### 🔹 Run Specific Test File
```bash
pytest path/to/test_file.py
```

### 🔹 Run Specific Test Case
```bash
pytest path/to/test_file.py::TestClass::test_method
```

### 🔹 Use Pytest Markers
```bash
pytest -m <marker_name>
```

---

## 📂 Test Environment Configuration

Test environment data is stored in:
```
config/env.json
```

Example:
```json
{
  "dev": {
    "url": "https://dev.jobeze.com"
  },
  "qa": {
    "url": "https://qa.jobeze.com"
  }
}
```

To target a specific environment:
```bash
pytest --env=qa
```

---

## 📈 Reports

### 📄 HTML Report
After a test run, open the HTML report at:
```
TestResults/PytestHTMLReport/ViewSMCTestAutomationReport.htm
```

### 📈 Allure Report

1. Generate the report:
   ```bash
   allure generate TestResults/AllureReports -o allure-report --clean
   ```

2. Open the report in browser:
   ```bash
   allure open allure-report
   ```

> ⚠️ Make sure Allure is [installed](https://docs.qameta.io/allure/#_installing_a_commandline) and added to your system path.

---
