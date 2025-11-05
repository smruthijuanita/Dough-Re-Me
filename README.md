# 🍰 Dough-Re-Me – AI-Powered Cloud Bakehouse

**Dough-Re-Me** is an elegant, AI-driven bakery and cloud kitchen web platform that blends technology with the warmth of homemade desserts.  
It offers seamless online ordering, personalized recommendations, and predictive inventory management — all within a cozy, cream-beige aesthetic that captures the essence of baking with love.

**Now with PostgreSQL database integration!**

---

## 🌟 Features

### 🧁 Customer-Facing
- **Conversational Ordering:** Chatbot-based system for placing custom cake and bakery orders naturally.  
- **Smart Recommendations:** AI-powered suggestions based on purchase history and preferences.  
- **Semantic Search:** Understands intent beyond keywords using vector similarity.  
- **Personalization:** Takes into account allergies, diets, and favourite flavours.

### 👩‍🍳 Kitchen & Admin
- **Real-Time Inventory Tracking:** Auto-updates ingredient quantities with every order.  
- **Predictive Analytics:** Forecasts demand using time-series models (SARIMA / Prophet).  
- **Dashboard Insights:** Visual analytics for sales, orders, and top-selling items.  
- **Low-Stock Alerts:** Re-order suggestions and seasonal trend insights.

### 💬 Design & Experience
- **Beige-cream colour palette** for a calming, aesthetic bakery theme.  
- **Fully responsive layout** with smooth transitions and clear navigation.  
- **Optimized UI** built for clarity, emotion, and storytelling.

---

## Tech Stack

| Layer | Technologies |
|-------|---------------|
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla DOM) |
| **Backend (Planned)** | FastAPI / Flask |
| **Database** | PostgreSQL with pgVector / MongoDB |
| **AI & Analytics** | TF-IDF, Cosine Similarity, Apriori, SARIMA, Prophet |
| **Version Control** | Git + GitHub |
| **Deployment** | (Planned) Vercel / Netlify / Render |
| **Database** | PostgreSQL with SQLAlchemy ORM |

---

## 🚀 Getting Started with PostgreSQL

### Prerequisites
- Python 3.8+
- PostgreSQL 12+

### Setup Instructions

1. **Install PostgreSQL**: Download from [postgresql.org](https://www.postgresql.org/download/)

2. **Create Database**:
```powershell
psql -U postgres
CREATE DATABASE dough_re_me;
\q
```

3. **Configure Environment**: Copy `.env.example` to `.env` and update credentials
```powershell
cp .env.example .env
```

4. **Install Dependencies**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

5. **Initialize Database**:
```powershell
python scripts\init_db.py
python scripts\seed_db.py
```

6. **Run Application**:
```powershell
python -m app.main
```

Access at:
- **Frontend**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs

### API Endpoints
- `GET/POST /api/v1/products` - Product management
- `GET/POST /api/v1/orders` - Order management

---
## 💡 Future Enhancements

- **Voice-enabled chatbot for hands-free ordering**
- **Loyalty & rewards system for repeat customers**
- **Real-time delivery tracking dashboard**

---
## ❤️ About Me

Baking has always been my love language — a way to create joy, warmth, and connection.
Dough-Re-Me was born from a simple wish to make people smile through something sweet.
Every cake, cookie, and crumble that leaves my kitchen is handmade with care, sprinkled with love, and baked to bring comfort to your day.
Because here, it’s never just about dessert — it’s about happiness, shared one bite at a time <3

---
## 📬 Connect

- **Instagram:** _.dough.re.me._
- **Email:** hello@doughremi.in
- **Location:** Bengaluru, India
