# 🤖 AI Product Advisor

An AI-powered product recommendation platform that helps users discover products based on their requirements and provides detailed AI-generated analysis before making a purchase decision.

---

## 📌 Project Overview

Finding the right product online can be difficult due to the large number of available options, conflicting reviews, and overwhelming specifications.

AI Product Advisor simplifies this process using a multi-stage AI workflow that:

* Understands user requirements in natural language
* Extracts structured product preferences
* Generates personalized recommendations
* Analyzes selected products against user needs
* Provides match scores, pros & cons, and purchase insights

The project is built using Flask, Python, Jinja2, and Google Gemini AI.

---

## ✨ Key Features

### 🧠 Agent 1 – Requirement Analysis

Users describe their requirements in natural language.

**Example Input**

> I need a gaming laptop under ₹70,000 with good battery life and at least 16GB RAM. Prefer ASUS.

The AI extracts:

* Product Category
* Budget
* Purpose
* Important Features
* Preferred Brands

---

### 🎯 Agent 2 – Recommendation Generation

Based on the analyzed requirements, the AI generates:

* Top Picks
* Alternative Recommendations

Each recommendation includes:

* Product Name
* Estimated Price
* Recommendation Reason

---

### 📊 Agent 3 – Product Analysis

When a user selects a product, the AI performs a detailed evaluation and generates:

* Overall Match Percentage
* Budget Match Score
* Feature Match Score
* Brand Match Score
* Purpose Match Score
* Value for Money Analysis
* Pros
* Cons
* Final Verdict

---

## 🔄 Application Workflow

```text
User Query
      ↓
Agent 1 - Requirement Analysis
      ↓
Structured User Requirements
      ↓
Agent 2 - Recommendation Generation
      ↓
Top Picks Dashboard
      ↓
User Selects Product
      ↓
Agent 3 - Product Analysis
      ↓
Match Score + AI Insights
```

---

## 🏗️ Project Architecture

### Agent 1: Requirement Analysis

**Input**

* Natural language query

**Output**

```json
{
  "category": "...",
  "budget": "...",
  "purpose": "...",
  "important_features": [],
  "preferred_brands": []
}
```

---

### Agent 2: Recommendation Engine

Uses the structured requirements from Agent 1 to generate:

* Top Recommendations
* Alternative Recommendations

---

### Agent 3: Product Analysis Engine

Compares the selected product against user requirements and generates detailed purchase guidance.

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask

### Frontend

* HTML
* CSS
* Jinja2

### AI Integration

* Google Gemini API

### Data Handling

* JSON Parsing
* Session Management

### Development Tools

* Git
* GitHub

---

## 📂 Project Structure

```text
AI-Product-Advisor/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── index.html
│   ├── understanding.html
│   ├── dashboard.html
│   └── product_analysis.html
│
└── static/
```

---

## 🚀 Installation

### Clone Repository

```bash
git clone <your-repository-url>
cd AI-Product-Advisor
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
SECRET_KEY=YOUR_SECRET_KEY
```

---

## ▶️ Run the Application

```bash
python app.py
```

Application will start at:

```text
http://localhost:5000
```

---

## 📸 Screenshots

Add screenshots here:

### Home Page

[Insert Screenshot]

### Requirement Analysis Page

[Insert Screenshot]

### Recommendations Dashboard

[Insert Screenshot]

### Product Analysis Page

[Insert Screenshot]

---



## 📚 Learning Outcomes

This project helped me gain practical experience in:

* Flask Web Development
* API Integration
* Google Gemini AI
* Prompt Engineering
* Session Management
* Form Handling
* Jinja Templating
* JSON Parsing
* Multi-Agent AI Workflows
* Frontend + Backend Integration

---


## 👨‍💻 Author
Dhankeerth

Developed as a personal learning project to explore AI-powered recommendation systems and multi-agent application design.

---

## ⭐ Project Status

**Version:** V1.0

**Status:** Completed MVP

Core Features Implemented:

* ✅ Requirement Analysis Agent
* ✅ Recommendation Agent
* ✅ Product Analysis Agent
* ✅ Error Handling
* ✅ Responsive User Interface
* ✅ Gemini AI Integration
