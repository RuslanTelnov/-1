# WB Dashboard Project

This folder contains the source code for the Wildberries Dashboard integration.

## Structure

- `moysklad-automation/`: Python scripts for data fetching and synchronization.
- `moysklad-web/`: Next.js web application for the dashboard.
- `documentation/`: Project artifacts, plans, and walkthroughs.

## Setup

### 1. Automation (Python)

Navigate to `moysklad-automation`:
```bash
cd moysklad-automation
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
*(Note: You may need to create a requirements.txt if it doesn't exist, based on imports)*

### 2. Web Dashboard (Next.js)

Navigate to `moysklad-web`:
```bash
cd moysklad-web
npm install
npm run dev
```

## Environment Variables

Ensure you have `.env` files in both directories with the necessary API keys (Supabase, MoySklad, etc.).
