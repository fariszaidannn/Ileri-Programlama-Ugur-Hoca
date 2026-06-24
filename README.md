# 🧭 Seyahatify — Minimalist Trip Planner

Seyahatify is a lightweight, responsive travel workspace application built with **Streamlit** and driven by a relational **SQLite3** engine. Designed with a sleek, iOS-inspired glassmorphic bento block layout, it helps travelers concurrently coordinate dynamic destination data profiles alongside synchronized task management pipelines.

---

## 🛠️ Tech Stack & Integrations

* **Frontend Engine:** Streamlit (Custom styled layout leveraging modern CSS styling vectors).
* **Database Infrastructure:** Local SQLite3 instance tracking relational schema instances.
* **Live Context APIs:**
* **OpenWeatherMap API:** Dynamic data extraction for temperature trends, feels-like thresholds, local cloud parameters, and metric tracking.
* **SerpApi TripAdvisor Engine:** Automatically processes descriptive strings, tourist evaluations, location review analytics, and structural lodging alternatives.
* **SerpApi Google Images Light Engine:** Direct visual item lookups routing dynamic discoveries straight into custom UI asset blocks.



---

## 💾 Relational Data Architecture

The application runs a normalized backend data layout to safeguard user profiles and active itineraries across active sessions:

```text
  [users] ───(1:N)───> [trips] ───(1:N)───> [trip_items]
   ├── id (PK)          ├── id (PK)           ├── id (PK)
   ├── username         ├── user_id (FK)      ├── trip_id (FK)
   └── password         └── city              ├── item (TEXT)
                                              └── checked (BOOLEAN)

```

---

## 📈 System Architecture & Interaction Flow

The architectural lifecycle below highlights user validation pathing, asynchronous data ingestion channels, panel segmentation matrices, and state recovery cycles:

```mermaid
flowchart TD
    Start([Launch App]) --> AuthPage[🔐 Auth Page: Sign In / Register]
    AuthPage --> LoginCheck{Credentials Valid?}
    LoginCheck -- No --> AuthPage
    LoginCheck -- Yes --> InitSession[Initialize User Session State]
    
    InitSession --> PageRouter{st.session_state.page?}
    
    %% Main Dashboard Pipeline
    PageRouter -- "main" --> MainDashboard[🧭 Main Dashboard View]
    
    subgraph Sidebar [Interactive Checklist Panel]
        MainDashboard --> ManageChecklist[Manage Current Tasks: Add / Check / Clear]
        ManageChecklist --> SaveLayout{Click 💾 Save Journey Layout?}
        SaveLayout -- Yes --> SQLitesave[(SQLite DB: Commits Trip & relational Items)]
        ManageChecklist --> ViewArchive[Click 📋 View Archive History]
        ViewArchive --> RouteToHistory[Set page = 'history']
    end
    
    subgraph Engine [Asynchronous Data Exploration Core]
        MainDashboard --> SearchCity[/Input: Enter City Name/]
        SearchCity --> Explore{Click Explore Button?}
        Explore -- Yes --> FetchAPIs[Concurrent REST API Ingestion]
        
        FetchAPIs --> WeatherAPI(OpenWeatherMap API)
        FetchAPIs --> SerpImages(SerpApi Google Images Light)
        FetchAPIs --> SerpTrip(SerpApi TripAdvisor Engine)
        
        WeatherAPI --> Bento1[🌤️ Weather Report Bento]
        SerpImages --> Bento2[📸 Destinations/Ideas Bento]
        SerpTrip --> Bento3[✨ Destination Overview Bento]
        SerpTrip --> Bento4[🏨 Hotels & Recommendations Bento]
    end
    
    %% Archive Storage Management
    RouteToHistory --> HistoryPage[Saved Journeys Archive]
    PageRouter -- "history" --> HistoryPage
    
    subgraph Archive [Archive Management & Restoration Core]
        HistoryPage --> SortFilter[/Apply Order Sequence Filter/]
        HistoryPage --> DeleteLog[Click ✕: Drop Trip Row from SQLite Cascade]
        HistoryPage --> BackBtn[Click ← Back: Set page = 'main']
        HistoryPage --> LoadEdit[Click ✏️ Load & Edit Journey]
        
        LoadEdit --> RestoreState[Rehydrate Workspace State with Stored Task States]
        RestoreState --> RefreshAPIs[Fetch Fresh API Context for Target City]
        RefreshAPIs --> SetMainPage[Set page = 'main']
    end
    
    BackBtn --> MainDashboard
    SetMainPage --> MainDashboard

```

---

## 🌟 Core Functional Capabilities

### 1. Robust Access Shield

Employs an isolated user directory infrastructure allowing custom traveler account registrations. Session data states maintain distinct user operational profiles, shielding private itineraries from concurrent platform connections.

### 2. Multi-Panel Destination Matrix

* **Weather Report:** Monitors temperatures, humidity levels, and cloud configurations in real time.
* **Destinations/Ideas:** Leverages targeted, low-latency visual queries to show key location details complete with social media sharing utilities.
* **Destination Overview & Lodging:** Ingests traveler sentiment scores and localized review snippets, exposing multiple hospitality choices side by side.

### 3. State Rehydration & Edit Pipeline

The **Load & Edit Journey** protocol lets users load legacy checklists back into the primary panel loop instantly. Selecting it maps old checkboxes back to their exact historical states while executing live data fetches—allowing old travel strategies to instantly receive fresh updates.
