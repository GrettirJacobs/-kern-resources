# Kern Resources - AI-Powered Development Platform

**A comprehensive AI development platform featuring CrewAI integration, advanced memory systems, and professional GUI interfaces.**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.121.1-green.svg)](https://crewai.com)
[![ChainLit](https://img.shields.io/badge/ChainLit-2.5.5-orange.svg)](https://chainlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 **Key Features**

### **🤖 AI Agent Management**
- **CrewAI Integration**: Multi-agent teams with advanced coordination
- **Multiple LLM Support**: OpenAI, Anthropic, Google Gemini, Grok
- **Memory-Aware Agents**: Persistent learning and context retention
- **Professional GUI**: Desktop application with standalone executable

### **🧠 Advanced Memory System**
- **Four-Layer Architecture**: Exact duplicates, machine tags, AI summaries, meta-commentaries
- **Dual Search**: Vector similarity + relational tag comparison
- **Real-Time Indexing**: Automatic content processing and categorization
- **Qdrant Integration**: High-performance vector database

### **🖥️ Professional Interfaces**
- **CrewAI GUI**: Complete web-based management interface
- **ChainLit Integration**: Conversational AI interface
- **Standalone Executable**: 511MB PyInstaller-built desktop app
- **Desktop Integration**: Start menu shortcuts and system tray

### **🔧 DevOps & Deployment**
- **GitLab Integration**: Local and cloud CI/CD pipelines
- **Docker Support**: Containerized memory system
- **Render.com Ready**: Cloud deployment configuration
- **Automated Testing**: Comprehensive test suites

## 📁 **Project Structure**

```
kern_resources/
├── creative_lab/
│   ├── crew_ai/                    # CrewAI integration and agents
│   │   ├── gui/                    # Professional GUI interface
│   │   │   ├── apps/               # Organized by functionality
│   │   │   ├── api/                # REST API endpoints
│   │   │   ├── core/               # Core functionality
│   │   │   ├── runners/            # Application launchers
│   │   │   ├── templates/          # HTML templates
│   │   │   ├── static/             # CSS, JS, assets
│   │   │   ├── tests/              # Test suites
│   │   │   └── dist/               # Standalone executable
│   │   ├── agents/                 # AI agent definitions
│   │   ├── providers/              # LLM provider integrations
│   │   ├── tools/                  # Custom CrewAI tools
│   │   └── examples/               # Usage examples
│   ├── chainlit_ui/                # ChainLit interface
│   └── memory_system/              # Advanced memory architecture
├── memory_system/                  # Core memory implementation
├── kern_resources/                 # Main package
├── documentation/                  # Comprehensive docs
└── scripts/                        # Utility scripts
```

## 🏃 **Quick Start**

### **Prerequisites**
- Python 3.10+
- Anaconda/Miniconda
- Docker (for memory system)
- Git

### **Installation**

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/kern-resources.git
cd kern-resources
```

2. **Set up environment**
```bash
conda create -n kern_resources python=3.10
conda activate kern_resources
pip install -r requirements.txt
```

3. **Configure API keys**
```bash
cp creative_lab/crew_ai/.env.example creative_lab/crew_ai/.env
# Edit .env with your API keys
```

4. **Start Docker (for memory system)**
```bash
docker-compose up -d
```

5. **Launch the GUI**
```bash
# Option 1: Development mode
python creative_lab/crew_ai/gui/runners/launch_crewai_gui.py

# Option 2: Standalone executable
./creative_lab/crew_ai/gui/dist/CrewAI_GUI.exe
```

## 🎯 **Usage Examples**

### **CrewAI Team Creation**
```python
from creative_lab.crew_ai.memory_crew_factory import MemoryCrewFactory

# Create a research team with memory integration
crew = MemoryCrewFactory.create_research_crew(
    models=['gpt-4', 'claude-3-opus', 'gemini-1.5-pro'],
    memory_enabled=True
)

result = crew.kickoff({
    "topic": "AI development best practices",
    "depth": "comprehensive"
})
```

### **Memory System Integration**
```python
from memory_system.layer2 import MemoryManager

# Search across all memory layers
manager = MemoryManager()
results = manager.dual_search(
    query="CrewAI implementation patterns",
    vector_weight=0.7,
    tag_weight=0.3
)
```

### **GUI Integration**
```python
from creative_lab.crew_ai.gui.apps.crewai.crewai_gui import CrewAIGUI

# Launch professional GUI
gui = CrewAIGUI(host="127.0.0.1", port=5000)
gui.run()
```

## 🔧 **Configuration**

### **API Keys**
Configure in `creative_lab/crew_ai/.env`:
```env
# OpenAI
OPENAI_API_KEY=your_openai_key

# Anthropic
ANTHROPIC_API_KEY=your_anthropic_key

# Google
GOOGLE_API_KEY=your_google_key

# Grok
GROQ_API_KEY=your_groq_key
```

### **Memory System**
Configure in `memory_system/config.json`:
```json
{
  "qdrant_host": "localhost",
  "qdrant_port": 6333,
  "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
  "vector_size": 384
}
```

## 🧪 **Testing**

```bash
# Run all tests
python -m pytest tests/

# Test specific components
python creative_lab/crew_ai/gui/tests/test_gui_integration.py
python tests/test_memory_integration.py

# Test standalone executable
python creative_lab/crew_ai/gui/test_executable.py
```

## 📚 **Documentation**

- **[API Reference](documentation/api_reference.md)** - Complete API documentation
- **[Memory System Guide](documentation/memory_system_guide.md)** - Advanced memory features
- **[CrewAI Integration](documentation/crewai_integration.md)** - Agent management
- **[Deployment Guide](documentation/deployment_guide.md)** - Production deployment
- **[Development SOP](NEW_DEVELOPMENT_SOP_COMPLETE.md)** - Development methodology

## 🚀 **Deployment**

### **Local Development**
```bash
# Start all services
docker-compose up -d
python creative_lab/crew_ai/gui/runners/launch_crewai_gui.py
```

### **Production (Render.com)**
```bash
# Deploy to Render.com
git push origin main
# Automatic deployment via GitHub integration
```

### **Standalone Distribution**
```bash
# Build executable
cd creative_lab/crew_ai/gui
python build_executable.py

# Install on target system
dist/install_crewai_gui.bat
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **CrewAI Team** - For the excellent multi-agent framework
- **ChainLit** - For the conversational UI framework
- **Qdrant** - For the high-performance vector database
- **OpenAI, Anthropic, Google** - For the powerful LLM APIs

## 📞 **Support**

- **Issues**: [GitHub Issues](https://github.com/yourusername/kern-resources/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/kern-resources/discussions)
- **Email**: erik.jacobs@gmail.com

---

**Built with ❤️ by Erik Jacobs - Empowering AI development through intelligent automation**
