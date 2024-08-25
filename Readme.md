# Capstone Project: Privacy Policy AI Agent

In this project, we’d like to develop an agent that could help users generate customized privacy policies for their products/webs/apps following specific Data Protection Regulations.

## Environment Setup
**Make Sure your computer has a GPU with at least 12GB VRAM!**
```bash
pip install -r requirements.txt
docker-compose up
```
Fill your `OPENAI_API_KEY` in [.env](.env) file.

## Launch
```bash
docker start capstone-privacy_policy_ai_agent-text-generation-inference-1
streamlit run start_frontend.py
python start_backend.py
```