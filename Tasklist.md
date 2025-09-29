# Tasklist for Team KTN: Recipe Sharing Web Application

This task list outlines the activities required to complete the project, with primary responsibility assigned to the System Architect (Khoa), Back-End Lead (Nhat), and Front-End Lead (Thao).

| # | Task Description | Primary Responsibility |
|---|---|---|
| **Architecture & Infrastructure (Khoa)** | | |
| 1 | **Specify** the communication protocols (e.g., REST, gRPC) and data contracts between all microservices. | Khoa |
| 2 | **Design** the overall cloud infrastructure (AWS/Azure) including virtual networks and security groups for all services. | Khoa |
| 3 | **Develop** the CI/CD pipeline configuration (e.g., using Jenkins or GitHub Actions) for automated deployment of all services. | Khoa |
| 4 | **Refine** the initial architectural diagram (D0, D1, D2) based on technology selection and implementation constraints. | Khoa |
| 5 | **Obtain** all necessary third-party API keys and credentials (e.g., Auth0, image hosting) and integrate them into the configuration service. | Khoa |
| 6 | **Document** the microservice system's deployment runbook, including steps for scaling and recovery. | Khoa |
| **Back-End Development (Nhat)** | | |
| 7 | **Design** the relational database schema (e.g., PostgreSQL) for storing user profile and authentication data within the User Service. | Nhat |
| 8 | **Develop** the core API endpoints for the Recipe Service, enabling creation, retrieval, updating, and deletion of recipes. | Nhat |
| 9 | **Investigate** and implement the efficient search functionality using a dedicated tool like Elasticsearch for the Search Service. | Nhat |
| 10 | **Test** and ensure 90%+ unit test coverage for all backend business logic within the User and Recipe services. | Nhat |
| 11 | **Develop** the backend logic for user collections and personalized digital cookbook management. | Nhat |
| 12 | **Validate** all API endpoint security by implementing Auth0 integration and role-based access control. | Nhat |
| **Front-End Development (Thao)** | | |
| 13 | **Design** the user interface (UI/UX) wireframes for the recipe browsing and detailed recipe view pages. | Thao |
| 14 | **Develop** the main component library (e.g., using React/Vue) to ensure consistent styling and responsiveness across the application. | Thao |
| 15 | **Implement** the front-end forms and logic for user registration, login, and profile management using the User Service APIs. | Thao |
| 16 | **Develop** the recipe submission interface, including image upload handling and form validation. | Thao |
| 17 | **Document** the front-end component structure and state management approach for future maintainability. | Thao |
| 18 | **Conduct** end-to-end user testing and gather feedback on the front-end flow and usability. | Thao |
| **Integration & Finalization (Shared)** | | |
| 19 | **Integrate** the front-end application with all documented backend API endpoints via the API Gateway. | Thao, Nhat |
| 20 | **Conduct** final system validation and performance testing on the integrated, deployed system under expected load conditions. | Khoa, Nhat |
