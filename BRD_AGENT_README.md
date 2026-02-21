# 🏆 BRD Agent – Multi-Channel Requirements Generator

> **Hackathon Project** | Built on top of [LLM Minutes of Meeting](https://github.com/motalib-code/LLM-Minutes-of-Meeting)

Extract Business Requirements Documents (BRDs) from noisy emails, meeting transcripts, and chat messages using LLM-powered intelligence.

---

## 📐 Architecture Diagram (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        BRD AGENT - SYSTEM ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐    │
│  │                     🖥️  FRONTEND (Streamlit)                        │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │    │
│  │  │  Home    │ │  Upload  │ │ Process  │ │ View BRD │ │Dashboard │ │    │
│  │  │  Page    │ │  Page    │ │  Page    │ │  Page    │ │  Page    │ │    │
│  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ │    │
│  └───────┼─────────────┼───────────┼─────────────┼─────────────┼───────┘    │
│          │             │           │             │             │             │
│          ▼             ▼           ▼             ▼             ▼             │
│  ┌──────────────────────────────────────────────────────────────────────┐    │
│  │                     🔌 REST API (Flask)                              │    │
│  │                                                                      │    │
│  │  POST /api/ingest     ──→  Upload emails/transcripts/chats          │    │
│  │  POST /api/process    ──→  Extract BRD from communication           │    │
│  │  GET  /api/brd/<id>   ──→  Retrieve extracted BRD                   │    │
│  │  GET  /api/brds       ──→  List all BRDs with search                │    │
│  │  GET  /api/datasets   ──→  List dataset sources                     │    │
│  │  GET  /api/visualize  ──→  Stakeholder graph JSON                   │    │
│  │  POST /api/refine     ──→  AI-suggested edits                       │    │
│  └──────────────────────────┬───────────────────────────────────────────┘    │
│                              │                                               │
│          ┌───────────────────┼───────────────────────┐                      │
│          ▼                   ▼                        ▼                      │
│  ┌──────────────┐   ┌──────────────────┐   ┌────────────────────┐          │
│  │  📥 DATA     │   │  🧠 BACKEND      │   │  💾 DATABASE       │          │
│  │  INGESTION   │   │  EXTRACTION      │   │  (SQLite +         │          │
│  │              │   │                  │   │   SQLAlchemy)       │          │
│  │ load_enron() │   │ filter_noise()   │   │                    │          │
│  │ load_ami()   │   │ classify_channel │   │ users              │          │
│  │ load_mtg()   │   │ extract_brd()    │   │ communications     │          │
│  │ gen_chats()  │   │ detect_conflicts │   │ brd_extractions    │          │
│  │ preprocess() │   │ cluster_topics() │   │ (FTS5 search)      │          │
│  └──────┬───────┘   └────────┬─────────┘   └────────┬───────────┘          │
│         │                    │                        │                      │
│         ▼                    ▼                        ▼                      │
│  ┌──────────────────────────────────────────────────────────────────────┐    │
│  │                    📊 DATASETS (External Sources)                    │    │
│  │                                                                      │    │
│  │  📧 Enron Email Dataset ─── kaggle.com/wcukierski/enron-email-dataset│    │
│  │  🎙️ AMI Meeting Corpus ─── huggingface.co/datasets/knkarthick/AMI   │    │
│  │  📝 Meeting Transcripts ── kaggle.com/abhishekunnam/meeting-transcripts│   │
│  └──────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐    │
│  │                    🏆 WINNING FEATURES                               │    │
│  │                                                                      │    │
│  │  🕸️ Stakeholder Graph ── NetworkX visualization of relationships     │    │
│  │  📈 Timeline Gantt     ── Plotly chart of project milestones         │    │
│  │  🔀 Conflict Detection ── Sentiment analysis on feedback             │    │
│  │  🎯 Multi-Topic Cluster── KMeans on sentence embeddings             │    │
│  │  ✅ Ground Truth Eval  ── AMI summaries for accuracy scoring         │    │
│  └──────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
LLM-Minutes-of-Meeting/
│
├── brd_agent/                    # 🆕 BRD Agent App (NEW)
│   ├── __init__.py
│   ├── config.py                 # Configuration & environment variables
│   ├── data_ingest.py            # Module 1: Data ingestion & preprocessing
│   ├── backend.py                # Module 2: LLM extraction engine
│   ├── db_setup.py               # Module 3: Database schema & operations
│   ├── api.py                    # Module 4: REST API endpoints
│   ├── frontend.py               # Module 5: Streamlit UI
│   └── visualizations.py         # Module 6: Graphs & charts
│
├── app.py                        # Original repo Flask app (kept for reference)
├── summary.py                    # Original repo summary (base for backend.py)
├── speech.py                     # Original repo speech-to-text
├── tasks.py                      # Original repo Celery tasks
│
├── brd_agent_setup.py            # 🆕 One-click setup script
├── .env.template                 # 🆕 Environment variables template
├── requirements_brd.txt          # 🆕 Dependencies for BRD Agent
├── BRD_AGENT_README.md           # 🆕 This file
└── ...
```

---

## 🚀 Quick Start (A-Z Setup)

### Prerequisites
- **Python 3.10+** installed
- **pip** package manager
- **Git** installed

### Step 1: Clone & Navigate
```bash
git clone https://github.com/motalib-code/LLM-Minutes-of-Meeting.git
cd LLM-Minutes-of-Meeting
```

### Step 2: Create Virtual Environment
```bash
python -m venv brd_env
# Windows:
brd_env\Scripts\activate
# Linux/Mac:
source brd_env/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements_brd.txt
```

### Step 4: Configure Environment
```bash
copy .env.template .env
# Edit .env with your API keys (Google Gemini recommended for free tier)
```

### Step 5: Initialize Database
```bash
python -c "from brd_agent.db_setup import init_database; init_database()"
```

### Step 6: Run the App
```bash
# Option A: Streamlit UI (Recommended for hackathon demo)
streamlit run brd_agent/frontend.py

# Option B: Flask API only
python -m brd_agent.api
```

### Step 7 (Optional): Load Sample Datasets
```bash
python -c "from brd_agent.data_ingest import load_sample_data; load_sample_data()"
```

---

## 🧩 Module-by-Module Build Guide

| # | Module | File | What It Does | Build Time |
|---|--------|------|-------------|------------|
| 1 | **Data Ingestion** | `data_ingest.py` | Load Enron/AMI/Meeting data, preprocess, chunk | ~30 min |
| 2 | **Backend Engine** | `backend.py` | LLM extraction, noise filtering, conflict detection | ~45 min |
| 3 | **Database** | `db_setup.py` | SQLite schema, CRUD, full-text search | ~20 min |
| 4 | **REST API** | `api.py` | Flask endpoints for all features | ~30 min |
| 5 | **Frontend** | `frontend.py` | Streamlit UI with all pages | ~45 min |
| 6 | **Visualizations** | `visualizations.py` | Stakeholder graph, timeline charts | ~20 min |

**Total estimated build time: ~3 hours** (for a beginner following step-by-step)

---

## 📊 Dataset Sources & Licenses

| Dataset | Source | License |
|---------|--------|---------|
| Enron Email Dataset | [Kaggle](https://www.kaggle.com/datasets/wcukierski/enron-email-dataset) | Public Domain |
| AMI Meeting Corpus | [HuggingFace](https://huggingface.co/datasets/knkarthick/AMI) | CC BY 4.0 |
| Meeting Transcripts | [Kaggle](https://www.kaggle.com/datasets/abhishekunnam/meeting-transcripts) | Check Kaggle License |

---

## 🏆 Hackathon-Winning Features

1. **Multi-Channel Ingestion** – Emails, transcripts, chats in one pipeline
2. **Intelligent Noise Filtering** – TF-IDF + regex to remove irrelevant content
3. **Structured BRD Output** – Requirements, decisions, stakeholders, timelines
4. **Stakeholder Graph** – NetworkX-powered relationship visualization
5. **Conflict Detection** – Sentiment analysis flags disagreements
6. **Multi-Topic Clustering** – KMeans groups related requirements
7. **Ground Truth Validation** – AMI summaries score extraction accuracy
8. **AI-Suggested Edits** – Re-prompt LLM for refinements
9. **Full-Text Search** – SQLite FTS5 across all BRDs
10. **Timeline Gantt Charts** – Visual project milestones with Plotly
