<div align="center">
  <h1>🍰 Velvet & Whisk</h1>
  <p>A premium, modern, and full-stack E-Commerce Web Application built with Flask for ordering artisan cakes and custom baked goods.</p>

  ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
  ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
  ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
  ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
</div>

<br />

## 🌟 Overview

**Velvet & Whisk** is a beautifully designed, fully functional e-commerce platform that allows users to browse exquisite cakes, add them to a cart, place orders, and even request custom-designed cakes. It features a robust backend powered by Flask and SQLAlchemy, complete with user authentication and an interactive Admin Dashboard.

---

## ✨ Features

### 🛒 Customer Experience
- **User Authentication:** Secure registration and login functionality.
- **Dynamic Catalog:** Browse an elegant catalog of cakes with a flavor filtering system.
- **Cart & Wishlist:** Easily manage items you want to buy or save for later.
- **Seamless Checkout:** Collect address details and process simulated payments.
- **Custom Orders:** A dedicated page allowing users to request custom cakes by uploading their own design inspiration images.

### 🛡️ Admin Dashboard
- **Role-Based Access:** Secure admin-only routes to protect sensitive data.
- **Inventory Management:** Add, edit, or delete cakes directly from the dashboard with secure image uploading.
- **Order Management:** View customer orders and instantly confirm or cancel them.
- **Custom Request Tracking:** View custom cake requests along with user-uploaded reference images.
- **User Insights:** Monitor registered users seamlessly.

---

## 🛠️ Tech Stack

- **Backend Architecture:** Python, Flask
- **Database:** SQLite with SQLAlchemy ORM
- **Frontend Design:** HTML5, Vanilla CSS (Glassmorphism & Modern UI), JavaScript, Jinja2 Templating
- **Authentication & Security:** Flask-Login, Werkzeug Security
- **File Handling:** Secure local image handling and storage

---

## 🚀 Getting Started

Follow these steps to set up the project locally on your machine.

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/velvet-and-whisk.git
cd velvet-and-whisk
```

### 2️⃣ Create a Virtual Environment
Isolate your dependencies to avoid conflicts:
```bash
python -m venv venv

# For macOS/Linux:
source venv/bin/activate
# For Windows:
venv\Scripts\activate
```

### 3️⃣ Install Dependencies
Install all the required Python packages:
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application
Start the Flask development server:
```bash
python app.py
```

### 5️⃣ Access the Application
Open your web browser and navigate to:
```text
http://127.0.0.1:5000/
```

---

## 🔐 Admin Access

To access the admin dashboard, create an account with the exact username `admin`. 

Once registered and logged in as `admin`, you will gain access to the restricted routes:
- **Admin Dashboard:** `http://127.0.0.1:5000/admin_dashboard`
- **Add New Cake:** `http://127.0.0.1:5000/admin_add_cake`

---

## 🗂️ Project Structure

```text
velvet-and-whisk/
│
├── app.py                  # Main application & routing
├── models.py               # SQLAlchemy database models
├── config.py               # App configuration & settings
├── requirements.txt        # Python dependencies
│
├── instance/
│   └── cake_new.db         # SQLite database file
│
├── templates/              # Jinja2 HTML Templates
│   ├── base.html           # Master layout
│   ├── index.html          # Homepage / Catalog
│   ├── admin_dashboard.html# Admin interface
│   └── ...                 # Other templates
│
├── static/                 # Static Assets
│   ├── css/
│   │   └── style.css       # Global stylesheet
│   └── uploads/            # User & Admin uploaded images
│
└── README.md               # Project documentation
```

---

## 🔮 Future Roadmap

- [ ] Integration with a live payment gateway (Stripe / Razorpay).
- [ ] Automated email confirmations for placed orders.
- [ ] Product ratings and customer reviews.
- [ ] Live order tracking features.
- [ ] Deployment to cloud services (AWS, Render, or Vercel).

---

<div align="center">
  <p>Built as a high-quality, real-world E-Commerce application.</p>
</div>
