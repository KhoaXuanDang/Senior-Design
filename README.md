# Recipe Sharing Web Application – Team KTN

A microservice-based web application for University of Cincinnati students to share, browse, and manage recipes with secure authentication, scalable search, and personalized digital cookbooks.

---

## 📌 Table of Contents
1. [Team & Abstract](#team--abstract)  
2. [Project Description](#project-description)  
3. [User Stories](#user-stories)  
4. [Design Diagrams Overview](#design-diagrams-overview)  
5. [Project Tasks](#project-tasks)  
6. [Timeline](#timeline)  
7. [Effort Matrix](#effort-matrix)  
8. [ABET Concerns Essay](#abet-concerns-essay)  
9. [PPT Slideshow Summary](#ppt-slideshow-summary)  
10. [Self-Assessments](#self-assessments)  
11. [Professional Biographies](#professional-biographies)  
12. [Budget](#budget)  
13. [Appendix](#appendix)

---

## Team & Abstract

**Team Name:** KTN (Khoa, Thao, Nhat)  
**Members:**
- **Khoa Xuan Dang** – System Architect  
- **Thao Hoang** – Front-End Lead  
- **Nhat Pham** – Back-End Lead  
**Advisor:** *Khoa Pham*

### Project Abstract
Team KTN is developing a Recipe Sharing Web Application for UC students using a microservice architecture. The application provides secure authentication, recipe CRUD, Elasticsearch-powered search, and personalized digital cookbooks. Focus areas include scalability, security (Auth0), cloud deployment (AWS/Azure), and cultural inclusivity.

---

## Project Description
This project is a microservice-based platform where UC students can:

- Submit personal recipes  
- Search recipes from the community  
- Organize collections via personalized digital cookbooks  

The architecture includes separate services for authentication, recipe management, and search, ensuring scalability, security, and community-focused usability.

---

## User Stories

1. **As a UC student**, I want to browse recipes so I can find quick, affordable dishes.  
2. **As a home cook**, I want to submit my own recipes to share them with others.  
3. **As a user**, I want to save recipes to a personal collection.  
4. **As a recipe creator**, I want to edit/manage my previously submitted recipes.

---

## Design Diagrams Overview

### 1. System-Level View (Context Diagram)
Shows the interactions between:
- **Recipe Sharing System**
- **UC Student**
- **Cloud Provider (Deployment/Monitoring)**
<img width="975" height="240" alt="image" src="https://github.com/user-attachments/assets/ca7c249b-ee24-4776-b83f-37209c07b63e" />

### 2. Subsystem View (Container Diagram)
Architecture includes:
- **Web UI** → **API Gateway**
- **User Service** ↔ User Database  
- **Recipe Service** ↔ Recipe DB + Image Storage  
- **Search Service** ↔ Elasticsearch Index  
<img width="975" height="96" alt="image" src="https://github.com/user-attachments/assets/032fe3cd-1385-4b84-84a9-2ed25978db6e" />

### 3. Detailed Component View (Recipe Submission Flow)
Workflow:
- Web UI → API Gateway → Recipe Service  
- Components: Validation, Image Upload, DB Repository  
- Emits **New Recipe Event** → Search Service updates the index
<img width="975" height="372" alt="image" src="https://github.com/user-attachments/assets/966cfa63-f477-4951-b51b-3d66b8ed2069" />

---

## Project Tasks

| # | Task Description | Owner |
|---|------------------|--------|
|1|Define microservice communication protocols|Khoa|
|2|Design cloud infrastructure (AWS/Azure)|Khoa|
|3|Develop CI/CD pipeline|Khoa|
|4|Refine architectural diagrams|Khoa|
|5|Integrate third-party APIs (Auth0, hosting)|Khoa|
|6|Write deployment runbook|Khoa|
|7|Design User Service DB schema|Nhat|
|8|Implement Recipe Service CRUD|Nhat|
|9|Implement Elasticsearch search|Nhat|
|10|Achieve 90%+ backend unit tests|Nhat|
|11|Develop user cookbook features|Nhat|
|12|Implement API security (RBAC + Auth0)|Nhat|
|13|Design UI wireframes|Thao|
|14|Create core FE component library|Thao|
|15|Build user registration/login UI|Thao|
|16|Build recipe submission UI|Thao|
|17|Document FE structure|Thao|
|18|User testing|Thao|
|19|Integrate FE with backend APIs|Thao & Nhat|
|20|Final system validation under load|Khoa & Nhat|

---

## Timeline

| Milestone | Description | Date | Duration |
|----------|-------------|-------|----------|
|M1|Architectural Blueprint & Fall Scope|Oct 24, 2025|3 weeks|
|M2|Backend Services (Alpha)|Nov 21, 2025|7 weeks|
|M3|Fall Final Review|Dec 12, 2025|10 weeks|
|M4|Feature Integration (Beta)|Feb 27, 2026|21 weeks|
|M5|Feature Complete|Mar 27, 2026|25 weeks|
|M6|System Validation & Documentation|Apr 28, 2026|30 weeks|

---

## Effort Matrix

| Task # | Khoa | Nhat | Thao |
|--------|------|------|-------|
|1|70%|20%|10%|
|2|80%|10%|10%|
|3|80%|15%|5%|
|4|60%|20%|20%|
|5|70%|25%|5%|
|6|60%|20%|20%|
|7|10%|85%|5%|
|8|5%|90%|5%|
|9|15%|75%|10%|
|10|5%|90%|5%|
|11|5%|85%|10%|
|12|20%|70%|10%|
|13|10%|10%|80%|
|14|5%|5%|90%|
|15|5%|10%|85%|
|16|5%|15%|80%|
|17|10%|10%|80%|
|18|10%|10%|80%|
|19|10%|45%|45%|
|20|50%|40%|10%|

---

## ABET Concerns Essay
Constraints from several topical areas will significantly shape the viable solutions for our
microservice-based recipe application. Security is paramount, as we are dealing with user data,
making robust authentication and data protection a primary concern. We must implement
Auth0 (as planned) and strict role-based access control to prevent unauthorized access and
protect against common web vulnerabilities, such as injection attacks, ensuring privacy is
maintained. From a legal perspective, we must address intellectual property regarding the
recipes themselves; while we encourage user submissions, we must clearly state in our terms of
service that users are responsible for ensuring they have the right to share the content they
upload, mitigating any potential copyright disputes. The economic constraint influences our
technology stack, as we are relying on a combination of cost-effective cloud services (like
AWS/Azure services) and open-source frameworks (e.g., FastAPI, Next.js) to keep costs low, as
we do not have a large external budget. This economic decision is closely linked to our
professional goal, as delivering a highly scalable, yet budget-conscious microservice solution
directly enhances our professional marketability and demonstrates specialized expertise in
cloud-native development. Furthermore, the diversity and cultural impact is a key feature, as
the platform is designed to allow UC students to share recipes from diverse cultural
backgrounds and lifestyles, requiring our front-end design to support multiple languages and
our categorization system to be inclusive of various dietary needs (e.g., vegan, halal, gluten-
free). Finally, the social benefit is central to our project's motivation, as the application serves
the public interest of the UC community by enhancing students' quality of life through
accessible and affordable meal ideas, fostering social connection through shared culinary
experiences.

### Security
- Strong authentication (Auth0)
- Role-based access control  
- Protection from web vulnerabilities

### Legal
- Users must own rights to uploaded recipes  
- Terms of service must clarify copyright responsibility

### Economic
- Uses cloud free tiers + open-source frameworks  
- Costs minimized due to lack of external funding

### Professional
- Demonstrates modern cloud-native engineering proficiency

### Diversity & Cultural Impact
- Supports multilingual content  
- Inclusive dietary filters: vegan, halal, gluten-free

### Social
- Provides accessible meal ideas to UC students  
- Encourages cultural exchange and community engagement

---

## PPT Slideshow Summary

1. Title & Goals  
2. Team & Contact Info  
3. Project Abstract  
4. User Stories + D0 Diagram  
5. ABET Constraints  
6. Current Progress  
7. Expected Accomplishments  
8. Effort Matrix Overview  
9. Expected Demo for Expo  

---

## Self-Assessments
My senior design project is a microservice-based web application for University of
Cincinnati students to share and manage recipes. From my individual academic
perspective, this is the ultimate opportunity to apply everything I've learned in my
Computer Science curriculum and through my extensive co-op experiences. The project is
more than just a coding exercise; it’s about architecting a scalable, robust, and
maintainable system from the ground up, a challenge that requires integrating concepts
from software design, database management, and cloud infrastructure. I see this as a
chance to transition from a student who learns concepts to a professional who applies
them to solve a tangible problem. This project will allow me to demonstrate my ability to
handle a full-stack development lifecycle, from initial design and planning to final
deployment, and to create something valuable for my peers while solidifying my
professional skills.
My collective college experiences have provided a robust foundation for this project’s
development, starting with the curriculum. My courses at the University of Cincinnati have
been particularly formative, equipping me with the technical skills needed for this
endeavor. Software Engineering course gave me a deep understanding of structured
development processes and team collaboration, which are crucial for a group project of
this scale. In Database Systems class, I learned how to design efficient and normalized
database schemas using PostgreSQL and SQL Server, a skill I will apply directly to
structuring the data for our recipes and user profiles. The principles of object-oriented
design from Data Structures and Algorithms class will guide my approach to writing clean,
modular code that is easy to maintain. These courses were not just about learning syntax;
they were about understanding the core principles behind creating scalable, reliable
software, which will guide every design decision we make.
My co-op experiences have been equally influential, providing me with practical, nontechnical skills that complement my academic knowledge. As a Software Engineering
Intern at Matson Money, I gained valuable experience in building secure, scalable
controllers and automating workflows using Azure, C#, and .NET, skills that are directly
transferable to building our project's backend services. My time at Sharedi as a Software
Engineering Intern taught me how to write robust, mock-based tests to ensure backend
reliability, achieving 95% test coverage—a practice I will enforce to prevent critical bugs in
our system. Furthermore, my co-op at Picon Technology exposed me to FastAPI and
PostgreSQL, while my time at Hybrid Technologies involved building an e-commerce
platform with Django and AWS. This diverse experience with different languages,
frameworks, and cloud platforms gives me the flexibility to choose the right tools for our
project and a solid understanding of full-stack development. I will apply these skills to not
only write code but also to manage the project workflow, communicate effectively with my
team, and ensure we deliver a high-quality product on time.
My motivation for this project is a genuine desire to create a useful and meaningful
application for the UC community. I am personally excited about this project because I am
passionate about cooking, and I believe a platform for students to share their culinary
creations and discoveries will foster a stronger sense of community. Our preliminary
approach to designing a solution involves a meticulous, step-by-step process. We will
begin with an agile methodology to break down the project into smaller, manageable
sprints, focusing first on core functionalities like user authentication and basic recipe
submission. We will utilize a microservice architecture to ensure flexibility and scalability,
with each service (e.g., Recipe Service, User Service) developed independently using
technologies I have experience with, such as Next.js, FastAPI, and PostgreSQL. This is a
direct application of the skills I’ve honed in my co-op roles and projects like the Cookbook
App and Mind Map Generator, where I worked with similar technologies like Docker,
Kubernetes, and serverless architecture.
Self-evaluation is a critical component of this project to ensure a high-quality deliverable. I
will know I am "done" with my individual contributions when my assigned features are fully
implemented, thoroughly tested, and seamlessly integrated with my teammates' work. This
means my code must pass all unit, integration, and end-to-end tests, a practice I learned
to value at Sharedi and Matson Money. I will know I have done a "good job" by the quality of
my work and the feedback from my team and our advisor. Quality, in this context, means
my code is clean, well-documented, and follows best practices; the features are robust
and free of critical bugs; and the design is scalable and maintainable for future
enhancements. Beyond technical metrics, a good job also means I have been a reliable
and communicative team member, actively participating in meetings, providing
constructive feedback, and helping my teammates when needed. I will evaluate my work
not just by what I produced, but by how my contributions positively impacted the entire
team's success.

---

## Professional Biographies

# Khoa Xuan Dang
---
I'm a dedicated and results-driven computer science student at the **University of Cincinnati**. With a strong foundation in computer science principles and extensive hands-on experience, I specialize in **full-stack development**, **cloud technologies**, and **machine learning**. I have a proven track record of building robust, scalable systems that solve real-world problems and significantly improve operational efficiency.
---
## Contact Information
* **Email:** `dangkx@mail.uc.edu`
* **GitHub:** [github.com/KhoaXuanDang](https://github.com/KhoaXuanDang)
---
## Co-op Work Experience
### **Matson Money** | Software Engineering Intern
*March 2025 - Present*
* Built and maintained over **30 scalable controllers** using **Azure**, **React.js**, **C#**, and **.NET**.
* Refactored a 12-year-old legacy architecture to improve performance by **85%**.
* Collaborated with business stakeholders to deliver a self-service solution that reduced turnaround time from **7 days to 1-2 hours**.
### **Sharedi** | Software Engineering Intern
*May 2024 - December 2024*
* Designed and developed core full-stack modules using **Java Spring Boot**, **CockroachDB**, and **ReactJS**.
* Wrote comprehensive mock-based tests and DB sanity checks, achieving **95% test coverage**.
---
## Project Sought
For my capstone project, I am seeking to build a **microservice-based cookbook or recipe application**. I aim to design a system with decoupled services for user authentication, recipe management, and search. This project would allow me to apply my skills in **Docker**, **Kubernetes**, **Flask**, and **Redis** to create a scalable and resilient architecture. My goal is to develop a production-grade application that demonstrates my expertise in full-stack and DevOps practices.
---

## Budget

- **Software Licenses:** $0 (FOSS)  
- **Development Tools:** $0  
- **Cloud Infrastructure:** ~$200 (free-tier credits)  
- **Expenses to Date:** $0  

---

## Appendix

- References and technical documentation  
- Repositories:  
  - Main Project  
  - User Service  
  - Recipe Service  
  - Front-End  
- Weekly meeting notes  
- Evidence of 45 required hours:
  - Khoa: Tasks 1–6  
  - Nhat: Tasks 7–10  
  - Thao: Tasks 11–15  

