# 🤖 fran-with-ai

> **AI Learning & Experimentation Hub** - A comprehensive repository for exploring AI technologies, automation workflows, and intelligent systems

[![AI](https://img.shields.io/badge/AI-Learning-blue?style=for-the-badge)](#)
[![LLM](https://img.shields.io/badge/LLM-Experiments-green?style=for-the-badge)](#)
[![RAG](https://img.shields.io/badge/RAG-Implementation-orange?style=for-the-badge)](#)
[![Automation](https://img.shields.io/badge/Automation-n8n-purple?style=for-the-badge)](#)

## 🎯 **About This Repository**

This repository serves as a **practical AI learning playground** where I experiment with cutting-edge AI technologies, automation workflows, and intelligent systems. It's designed to showcase hands-on experience with:

- 🧠 **Large Language Models (LLMs)**
- 🔍 **Retrieval-Augmented Generation (RAG)**
- 🤖 **AI Agents & Autonomous Systems**
- 🔗 **Workflow Automation with n8n**
- 🌐 **Web Scraping & Data Collection**
- 💬 **WhatsApp Automation & Webhooks**
- 📊 **Vector Databases & Embeddings**

---

## 📁 **Repository Structure**

```
fran-with-ai/
├── 🔧 n8n/                    # Workflow Automation & AI Orchestration
│   ├── archivos/               # Document storage & processing
│   │   ├── cargados/          # Processed documents for RAG
│   │   └── por cargar/        # Documents queue for processing
│   ├── n8n-qdrant/           # Vector database integration
│   ├── n8n_data/             # n8n workflow data & configs
│   ├── ollama_works_v1.json   # LLM integration workflow
│   ├── qdrant_embed_test.json # Embedding experiments
│   ├── qdrant_query.json     # Vector search workflows
│   └── docker-compose.yaml   # Containerized AI stack
│   
├── 🕷️ scrapping/              # Web Scraping & Data Collection
│   ├── drivers/               # Browser automation drivers
│   ├── archivos/              # Scraped data storage
│   ├── envios_usar.py         # WhatsApp automation script
│   ├── cargar_data.py         # Data processing utilities
│   └── *.csv                  # Extracted datasets
│   
├── 📱 wp-webhook/             # WhatsApp Integration & Webhooks
│   ├── index.js               # WhatsApp Web.js integration
│   ├── package.json           # Node.js dependencies
│   └── node_modules/          # (ignored) Dependencies
│   
└── 📝 .gitignore              # Clean repository management
```

---

## 🔧 **Technologies & Tools**

### **AI & Machine Learning**
- **🦙 Ollama** - Local LLM deployment (Phi-3, Llama, etc.)
- **🔍 Qdrant** - Vector database for embeddings
- **🧠 LangChain** - AI agent frameworks
- **📊 RAG Systems** - Document retrieval & generation

### **Automation & Orchestration**
- **🔗 n8n** - Visual workflow automation
- **🐳 Docker** - Containerized AI services
- **🪝 Webhooks** - Event-driven integrations
- **⚡ API Integrations** - External service connections

### **Web Technologies**
- **🌐 Node.js** - Backend automation services
- **🕷️ Selenium** - Web scraping & browser automation
- **📱 WhatsApp Web.js** - WhatsApp integration
- **🐍 Python** - Data processing & ML scripts

### **Data & Storage**
- **📄 CSV/JSON** - Structured data formats
- **🗃️ Vector Databases** - Semantic search capabilities
- **📚 Document Processing** - Text extraction & analysis

---

## 🚀 **Key Projects & Experiments**

### **1. 🧠 AI Agent Workflows (n8n)**
- **LLM Integration**: Direct integration with Ollama models
- **Memory Management**: Conversational context retention
- **Webhook Endpoints**: API-driven AI interactions
- **Multi-modal Processing**: Text, document, and data analysis

### **2. 🔍 RAG Implementation**
- **Document Ingestion**: Automated text processing pipeline
- **Vector Embeddings**: Semantic document representation
- **Intelligent Retrieval**: Context-aware information extraction
- **Query Processing**: Natural language to database queries

### **3. 📱 WhatsApp Automation**
- **Web Scraping**: Automated data collection from websites
- **Message Broadcasting**: Bulk messaging with personalization
- **QR Authentication**: Seamless WhatsApp Web integration
- **Contact Management**: CSV-based contact processing

### **4. 🕷️ Intelligent Scraping**
- **Dynamic Web Scraping**: JavaScript-rendered content extraction
- **Data Processing**: CSV manipulation and cleaning
- **Browser Automation**: Human-like interaction patterns
- **Error Handling**: Robust scraping with recovery mechanisms

---

## 🎓 **Learning Objectives**

This repository demonstrates practical experience with:

✅ **LLM Integration** - Working with various language models  
✅ **Vector Databases** - Implementing semantic search systems  
✅ **AI Agents** - Building autonomous decision-making systems  
✅ **Workflow Automation** - Creating complex AI-driven processes  
✅ **API Development** - Building webhooks and integrations  
✅ **Data Engineering** - Processing and transforming datasets  
✅ **Web Automation** - Browser-based task automation  
✅ **Containerization** - Docker-based AI service deployment  

---

## 🛠️ **Getting Started**

### **Prerequisites**
- 🐳 Docker & Docker Compose
- 🟢 Node.js (v16+)
- 🐍 Python (v3.8+)
- 🦙 Ollama (for local LLM inference)

### **Quick Setup**

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/fran-with-ai.git
   cd fran-with-ai
   ```

2. **Start AI Services**
   ```bash
   cd n8n
   docker-compose up -d
   ```

3. **Install Dependencies**
   ```bash
   # WhatsApp integration
   cd wp-webhook
   npm install
   
   # Python scraping tools
   cd ../scrapping
   pip install selenium pandas
   ```

4. **Access n8n Workflow Designer**
   ```
   http://localhost:5678
   ```

---

## 📚 **Use Cases & Applications**

- **🤖 Customer Service Automation** - AI-powered WhatsApp bots
- **📊 Data Intelligence** - Automated data collection & analysis
- **🔍 Document Q&A Systems** - RAG-based information retrieval
- **⚡ Business Process Automation** - n8n workflow orchestration
- **📱 Social Media Management** - Automated messaging & engagement
- **🧠 AI Research & Experimentation** - Testing new models & techniques

---

## 🔮 **Future Experiments**

- [ ] **Multi-modal AI Agents** - Vision + Language models
- [ ] **Advanced RAG Techniques** - Graph-based retrieval
- [ ] **Voice AI Integration** - Speech-to-text workflows
- [ ] **Fine-tuning Experiments** - Custom model training
- [ ] **Edge AI Deployment** - Optimized inference pipelines
- [ ] **Autonomous Data Pipelines** - Self-managing ETL systems

---

## 🤝 **Contributing**

This is a personal learning repository, but feel free to:
- 🐛 Report bugs or issues
- 💡 Suggest improvements or new experiments
- 🔄 Fork and create your own AI learning journey
- 📚 Share knowledge and best practices

---

## 📄 **License**

This project is for educational and experimental purposes. Feel free to use and modify for your own learning!

---

## 🏷️ **Tags**

`#AI` `#MachineLearning` `#LLM` `#RAG` `#Automation` `#n8n` `#WhatsApp` `#WebScraping` `#VectorDB` `#Ollama` `#LangChain` `#Python` `#NodeJS` `#Docker` `#Embeddings` `#AIAgents`

---

**⭐ Star this repo if you find it useful for your AI learning journey!**

