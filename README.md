# 🛡️ Sentinel WhatsApp - Data Intelligence and Conversion Optimization

🇬🇧 **English** · 🇪🇨 [Español](README.es.md)

> **Intelligent analytics and automation system for WhatsApp Business on self-hosted WAHA infrastructure**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

> **Status: paused since 6 Nov 2026** (see [PLAN.md](PLAN.md)).

## 🎯 The problem

WhatsApp is currently a **"black box"** in our sales operations:

- ❌ **Unknown drop-off rate**: we do not know at what exact point the customer stops replying
- ❌ **Lost golden window**: we lose sales by taking more than 10 minutes to reply
- ❌ **Data leakage**: the information lives on salespeople's phones, not in centralized systems
- ❌ **No metrics**: impossible to optimize without measuring

## 💡 The solution

**Sentinel WhatsApp** is an intelligence system that turns WhatsApp into a measurable, optimizable sales channel:

### ✨ Main features

1. **📊 Historical audit**
   - Bulk extraction of past conversations
   - Analysis of success and drop-off patterns
   - Identification of critical points in the funnel

2. **🤖 Human-like automation**
   - Replies that mimic human behavior
   - Realistic typing times
   - Smart use of emojis, voice notes and reactions

3. **📈 Real-time analytics**
   - Conversion-metrics dashboard
   - Alerts for "hot" customers
   - Tracking of critical KPIs

4. **🎯 Intent classification**
   - **High**: keywords such as "precio", "pago", "envío" (price, payment, shipping) → immediate reply
   - **Medium**: technical or warranty questions → assigned to an expert
   - **Low**: greetings or spam → filtered automatically

## 🚧 Current status

Work in progress. What is already in the code:

| Module | Status |
|---|---|
| `utils/waha_client.py`: WAHA client (session, chats, messages, send, typing..., reactions, webhook) | ✅ |
| `extractors/`: history extraction, response times, frequent questions, message types | ✅ |
| `classifiers/`: keyword-based intent classifier (high / medium / low) and priority | ✅ |
| `response/`: reply engine with templates, human-like delay and typing time | ✅ |
| `webhooks/`: `POST /webhooks/waha`, `POST /webhooks/test`, `GET /webhooks/status` | ✅ |
| `analytics/` (routes and dashboard), database and migrations, automated tests | ⏳ pending |

> `main.py` already imports `sentinel.analytics.routes`; until that module exists, comment out that line to start
> the server with the webhooks only.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    WhatsApp Business API                     │
│                   (waha.compumax.tech)                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  SENTINEL WHATSAPP                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Extractor   │  │  Classifier  │  │   Response   │      │
│  │   Module     │──│    Engine    │──│   Engine     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                  │              │
│         ▼                  ▼                  ▼              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Analytics & Dashboard                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Project phases

### Phase I: Diagnosis (backlog analysis)
**Goal**: understand what is happening

- Bulk message extraction through the API
- Processing of the full history
- Identification of the 5 questions that kill or close sales
- Analysis of response time vs. conversion

**Deliverable**: insights report with success/failure patterns

### Phase II: Automation
**Goal**: reply faster and better

- Real-time webhook setup
- Human-like reply engine
- Intent-detection system
- Smart assignment to salespeople

**Deliverable**: automatic reply system running 24/7

### Phase III: Monitoring
**Goal**: continuous optimization

- Real-time dashboard
- Conversion metrics per salesperson
- Opportunity alerts
- A/B testing of replies

**Deliverable**: control panel with full visibility of the funnel

## 💰 Competitive advantages

| Aspect | Traditional solution | Sentinel WhatsApp |
|---------|---------------------|-------------------|
| **Cost** | $0.005–0.05 per message | Self-hosted infrastructure (fixed cost) |
| **Control** | Data on third-party servers | 100% on our servers |
| **Privacy** | Shared with providers | Full privacy |
| **Scalability** | Cost grows with volume | Unlimited at no extra cost |
| **Customization** | Limited by the external API | Full control of the code |

## 🛠️ Tech stack

- **Backend**: Python 3.9+ (FastAPI)
- **Database**: PostgreSQL + Redis
- **Analytics**: Pandas, NumPy, Scikit-learn
- **WhatsApp API**: WAHA (WhatsApp HTTP API)
- **Dashboard**: Streamlit / React
- **Infrastructure**: Compumax.tech VM

## 📦 Installation

### Prerequisites

- Python 3.9 or later
- A [WAHA](https://waha.devlike.pro) (WhatsApp HTTP API) instance with its API key
- PostgreSQL and Redis are for the next phases (analytics and caching)

### Quick setup

```bash
# Clone the repository
git clone https://github.com/COMPUMAX-EC/Sentinel-Waha.git
cd Sentinel-Waha

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials

# Start the server (the package is in src/)
PYTHONPATH=src python main.py   # On Windows PowerShell: $env:PYTHONPATH="src"; python main.py
```

## ⚙️ Configuration

Edit the `.env` file:

```env
# WAHA API Configuration
WAHA_API_URL=https://waha.compumax.tech
WAHA_API_KEY=your_api_key_here
WAHA_SESSION_NAME=default

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/sentinel_waha
REDIS_URL=redis://localhost:6379/0

# Features
ENABLE_AUTO_RESPONSE=true
ENABLE_ANALYTICS=true
RESPONSE_DELAY_MIN=2
RESPONSE_DELAY_MAX=5

# Webhooks
WEBHOOK_SECRET=your_secret_here
WEBHOOK_URL=https://your-domain.com/webhooks/waha
```

## 📊 Usage

### History extraction

```python
import asyncio
from sentinel.extractors import MessageExtractor

extractor = MessageExtractor()
messages = asyncio.run(extractor.extract_all_messages())
report = extractor.process_messages(messages)  # response times, frequent questions, message types
```

### Intent analysis

```python
from sentinel.classifiers import IntentClassifier

classifier = IntentClassifier()
intent = classifier.classify("Cuál es el precio del producto?")  # Spanish: "What is the price of the product?"

print(f"Intent: {intent.level}")  # Output: "high"
print(f"Confidence: {intent.confidence}")  # Output: 0.92
```

### Automated reply

```python
from sentinel.classifiers import IntentClassifier
from sentinel.response import ResponseEngine, ResponseContext

message = "Me interesa el producto"  # Spanish: "I'm interested in the product"
context = ResponseContext(
    customer_message=message,
    intent=IntentClassifier().classify(message),
    conversation_history=[],
)
response = ResponseEngine().generate_response(context, humanize=True)
print(response)  # text, delay and "typing..." duration
```

## 📈 Key metrics

The system automatically tracks:

- **Response rate**: % of messages answered
- **First response time**: average and 90th percentile
- **Drop-off rate**: per funnel stage
- **Conversion rate**: messages → closed sales
- **Hot words**: keywords with the highest conversion
- **Best times**: the best moment to get in touch

## 🧪 Testing

Automated tests are not written yet; `pytest` and `pytest-asyncio` are already in `requirements.txt` for when they
are added under `tests/`. With `APP_DEBUG=true`, the API can be tried by hand at `/docs` (Swagger).

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Roadmap

- [x] **Q4 2025**: Phase I - Diagnosis and historical analysis
- [ ] **Q1 2026**: Phase II - Reply automation
- [ ] **Q2 2026**: Phase III - Real-time dashboard and monitoring
- [ ] **Q3 2026**: Machine learning for automatic optimization
- [ ] **Q4 2026**: Multi-channel (Instagram, Telegram)

## 📄 License

This project is under the MIT License. See [LICENSE](LICENSE) for details.

## 👥 Team

Built with ❤️ by the Compumax.tech team

---

**Questions or suggestions?** Open an [issue](https://github.com/COMPUMAX-EC/Sentinel-Waha/issues).

---

*"We are not installing an annoying auto-reply bot. We are building a sales-intelligence system that lets us be present 24/7 with the same quality as if we were writing ourselves, but at the speed of an algorithm."*
