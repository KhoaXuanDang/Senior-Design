# Recipe Share: Technical User Manual 🛠️

This manual provides detailed technical instructions for power users, developers, and system administrators regarding the installation, configuration, and operation of the Recipe Share system.

---

## 📌 Technical Overview
Recipe Share is built on a **Microservice Architecture** to ensure scalability and modularity for the UC student community.

* **Frontend:** Next.js (React) - Handles the user interface and client-side routing.
* **API Gateway:** Nginx / Spring Cloud Gateway - Manages traffic routing and request filtering.
* **Backend Services:** FastAPI (Python) and Spring Boot (Java) - Handles core business logic.
* **Data Layers:** PostgreSQL (Relational Data), Elasticsearch (Search Index).
* **Auth:** Auth0 (OpenID Connect) - Handles secure login and identity management.

---

## 🛠️ Installation & Setup (Developer Mode)

### Prerequisites
Before starting, ensure you have the following installed:
* **Docker & Docker Compose:** For containerized service orchestration.
* **Node.js v18+:** For local frontend development.
* **Python 3.9+:** For local backend service development.

### 1. Clone the Repository
```bash
git clone [[https://github.com/TeamKTN/recipe-share.git](https://github.com/TeamKTN/recipe-share.git)](https://github.com/KhoaXuanDang/Senior-Design.git)

```

### 2. Environment Variables

Create a `.env` file in the root directory and populate it with your credentials:

```env
AUTH0_DOMAIN=your-domain.auth0.com
AUTH0_CLIENT_ID=your-client-id
DATABASE_URL=postgresql://user:pass@localhost:5432/recipes
ELASTICSEARCH_URL=http://localhost:9200

```

### 3. Launch with Docker

Run the following command to build and start all microservices:

```bash
docker-compose up --build

```

The application will be available at `http://localhost:3000`.

---

## 🖥️ Feature Operations

### Advanced Search Syntax

The search bar is powered by **Elasticsearch** and supports advanced logic:

* `+chicken -onions`: Find recipes with chicken but specifically exclude onions.
* `"quick breakfast"`: Use double quotes to find an exact phrase.

### Image Management

Images are stored in an **AWS S3 Bucket**. If an image fails to load:

1. Check the `Image_URL` in the Recipe Database via the API.
2. Verify S3 Bucket permissions and CORS (Cross-Origin Resource Sharing) settings.

---

## 🛡️ Security & Privacy

### Authentication Flow

The system utilizes a secure JWT-based flow:

1. **Request:** User requests login → Redirected to **Auth0 Bearer Token flow**.
2. **Token:** Auth0 returns a **JWT (JSON Web Token)**.
3. **Client-Side:** The Frontend attaches this JWT to the `Authorization` header for all API requests.
4. **Verification:** The API Gateway validates the token before forwarding the request to internal microservices.

### Data Backup

The PostgreSQL database performs automated snapshots every 24 hours. In case of data loss, contact the **System Architect (Khoa)**.

---

## 🚑 Troubleshooting

| Issue | Potential Cause | Resolution |
| --- | --- | --- |
| **Login Fails** | Expired Session | Clear browser cookies and attempt login again. |
| **Search is Slow** | Indexing Lag | Wait 30 seconds for the Message Broker to update Elasticsearch. |
| **Image Upload Fails** | File Size/Format | Ensure image is under 5MB and in `.jpg` or `.png` format. |
| **"Service Unavailable"** | Microservice Crash | Check Docker logs (`docker logs [container_id]`) for the service. |

---

