# Recipe Share: Technical User Manual 🛠️

This manual provides detailed technical instructions for power users, developers, and system administrators regarding the installation, configuration, and operation of the Recipe Share system.

---

## 📌 Technical Overview
Recipe Share is built on a **Microservice Architecture**.

* **Frontend:** Next.js (React) - Handles the user interface.
* **API Gateway:** Nginx / Spring Cloud Gateway - Manages traffic routing.
* **Backend Services:** FastAPI (Python) and Spring Boot (Java) - Handles logic.
* **Data Layers:** PostgreSQL (Relational Data), Elasticsearch (Search Index).
* **Auth:** Auth0 (OpenID Connect) - Handles secure login.

---

## 🛠️ Installation & Setup (Developer Mode)

### Prerequisites
Before starting, ensure you have the following installed:
* **Docker & Docker Compose:** For running the services in containers.
* **Node.js v18+:** For local frontend development.
* **Python 3.9+:** For local backend service development.

### 1. Clone the Repository
```bash
git clone [https://github.com/TeamKTN/recipe-share.git](https://github.com/TeamKTN/recipe-share.git)
cd recipe-share