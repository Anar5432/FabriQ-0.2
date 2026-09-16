# FabriQ-Spring (Next-Gen Production ERP & Planning Studio)

FabriQ-Spring is an enterprise-grade Production ERP and Real-Time Planning Engine built with **Java 21** and **Spring Boot 3.3.1**. It manages multi-facility textile manufacturing operations spanning **Workwear (İş geyimləri)**, **Underwear (Alt geyimləri)**, and **Socks (Corab fabriki)**.

---

## 🚀 Key Features

### 1. Multi-Database Legacy ERP Synchronization
- **Dual MSSQL Integration**: 
  - `BTFERPDB`: Production data, department transfers (`sm_sob_trans`), and stage logs for Workwear & Underwear.
  - `BTFERPDB_CORABA`: Discrete production tickets (`sm_good_ist`, `sm_good_ist_el`), circular knitting phases (`sm_faza`), and raw yarn stock (`sm_mal_say`) for the Socks factory.
- **Resilient Fallback & In-Memory Data Initializer**: When legacy databases are offline, auto-initializes realistic mock factory datasets with all 3 production bands and live metrics.

### 2. Intelligent Production Planning Engine
- **Capacity & Bottleneck Balancing**: Computes daily throughput, cycle times, and operational constraints across sewing, cutting, knitting, and boarding departments.
- **BOM (Bill of Materials) & Material Allocation**: Verifies fabric, trim, and yarn stock balances (Cotton Ne, Polyamide, Elastane) before releasing orders to the factory floor.
- **Automated Queue Planning**: Dispatches and sequences sub-orders based on delivery deadlines, available workshop capacity, and worker team assignments.

### 3. Sub-Order Stage Tracking
- **Workwear & Underwear**: Tracks sub-orders across Design, Material Sourcing, Cutting, Sewing, Ironing/Finishing, and Warehouse dispatch.
- **Socks**: Tracks sub-orders across Yarn Sourcing (İplik Təchizatı), Knitting (Hörgü - Circular machines), Toe Closing (Rosso linking), Boarding (Forma - Steam heat setting), and Packaging/Finished stock.

### 4. Modular Modern UI Architecture
- **Vanilla ES6 Architecture**: Pure modular JavaScript without heavyweight bundle overhead:
  - `config.js`: Central configuration, stage definitions, and endpoints.
  - `state.js`: Reactive singleton application state store.
  - `utils.js`: Currency/date formatters, toast notifications, DOM helpers.
  - `api.js`: Unified REST API client with error handling and request caching.
  - `dashboard.js`: Stage columns, order cards, search/filter, and category toggles.
  - `planning.js`: Interactive planning studio, capacity meters, and schedule simulation.
- **Modular Component CSS**: Organized into `variables.css`, `layout.css`, `components.css`, `dashboard.css`, and `planning.css`.

---

## 🛠️ Tech Stack

- **Backend**: Java 21, Spring Boot 3.3.1, Spring Data JPA, Hibernate, Microsoft JDBC Driver
- **Frontend**: HTML5, Modular CSS3, Vanilla ES6 JavaScript
- **Build Tool**: Apache Maven (`mvnw`)
- **Testing**: JUnit 5, Mockito, AssertJ

---

## 🚦 Getting Started

### Prerequisites
- JDK 21 or higher installed
- Maven (or use the included `./mvnw` wrapper)

### Build & Run
```bash
# Clone the repository
git clone https://github.com/Anar5432/FabriQ-Spring.git
cd FabriQ-Spring

# Run tests
./mvnw test

# Start the application
./mvnw spring-boot:run
```

Once started, open your browser and navigate to:
```
http://localhost:8080
```

---

## 📂 Project Structure

```
FabriQ-Spring/
├── pom.xml
├── mvnw / mvnw.cmd
└── src/
    ├── main/
    │   ├── java/com/company/erp/
    │   │   ├── config/             # DataInitializer & App configurations
    │   │   ├── controller/         # REST Controllers (Orders, Planning, Sync)
    │   │   ├── dto/                # Data Transfer Objects
    │   │   ├── modules/
    │   │   │   ├── catalog/        # Material, ProductType, RecipeBOM
    │   │   │   ├── dashboard/      # OrderSnapshot, OrderSubItem
    │   │   │   ├── inventory/      # InventoryBalance
    │   │   │   └── planning/       # Baselines, Reserves, Teams
    │   │   ├── repository/         # Spring Data JPA Repositories
    │   │   └── service/            # PlanningService, LegacyService
    │   └── resources/
    │       ├── application.yml     # Database & Server configuration
    │       └── static/             # Modular Web Frontend
    │           ├── index.html
    │           ├── css/            # variables, layout, components, dashboard, planning
    │           └── js/             # config, state, utils, api, dashboard, planning, app
    └── test/
        └── java/com/company/erp/   # Automated Unit & Integration tests
```

---

## 📄 License
Internal proprietary software for factory operations.
