# API Architecture Overview

This document provides a visual overview of the Snake Showdown API architecture.

## API Endpoint Structure

```mermaid
graph TB
    subgraph "Client (React Frontend)"
        A[Snake Showdown App]
    end
    
    subgraph "API Server"
        B[/auth/signup<br/>POST]
        C[/auth/login<br/>POST]
        D[/auth/logout<br/>POST]
        E[/auth/me<br/>GET]
        F[/game/score<br/>POST]
        G[/game/leaderboard<br/>GET]
        H[/game/live<br/>GET]
        I[/player/profile<br/>GET]
    end
    
    subgraph "Auth Required"
        D
        E
        F
        I
    end
    
    subgraph "Public Endpoints"
        B
        C
        G
        H
    end
    
    A -->|Register| B
    A -->|Login| C
    A -->|Logout| D
    A -->|Get Current User| E
    A -->|Submit Score| F
    A -->|View Leaderboard| G
    A -->|Watch Live Games| H
    A -->|View Profile| I
    
    B -->|Returns JWT Token| A
    C -->|Returns JWT Token| A
    
    style D fill:#ff6b6b
    style E fill:#ff6b6b
    style F fill:#ff6b6b
    style I fill:#ff6b6b
    style B fill:#4ecdc4
    style C fill:#4ecdc4
    style G fill:#4ecdc4
    style H fill:#4ecdc4
```

## Data Flow: Score Submission

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Database
    
    User->>Frontend: Completes Game
    Frontend->>API: POST /game/score<br/>{score: 250, mode: "walls"}
    API->>API: Validate JWT Token
    API->>Database: Insert Score Record
    Database->>API: Success
    API->>Database: Check if New High Score
    Database->>API: isNewHighScore: true
    API->>Database: Calculate Rank
    Database->>API: rank: 5
    API->>Frontend: {message, isNewHighScore, rank}
    Frontend->>User: Display Success Toast
```

## Data Flow: Leaderboard Query

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Database
    
    User->>Frontend: Views Leaderboard Page
    Frontend->>API: GET /game/leaderboard?mode=walls&limit=10
    API->>Database: Query Top Scores
    Database->>API: Return Ranked Entries
    API->>Frontend: {entries: [...], total: 150}
    Frontend->>User: Display Leaderboard
```

## Authentication Flow

```mermaid
flowchart TD
    A[User Visits App] --> B{Has Token?}
    B -->|No| C[Show Login/Signup]
    B -->|Yes| D[GET /auth/me]
    D --> E{Valid Token?}
    E -->|Yes| F[Show Authenticated UI]
    E -->|No| C
    C --> G{Login or Signup?}
    G -->|Login| H[POST /auth/login]
    G -->|Signup| I[POST /auth/signup]
    H --> J[Receive JWT Token]
    I --> J
    J --> K[Store Token]
    K --> F
    F --> L{User Action}
    L -->|Logout| M[POST /auth/logout]
    M --> N[Clear Token]
    N --> C
    L -->|Play Game| O[Access Protected Routes]
```

## Data Models Relationships

```mermaid
erDiagram
    AuthUser ||--|| Player : "has-profile"
    Player ||--o{ LeaderboardEntry : "appears-in"
    Player ||--o{ LiveGame : "plays"
    LiveGame ||--|| GameState : "contains"
    GameState ||--|| Snake : "has"
    GameState ||--|| Position : "has-food-at"
    Snake ||--o{ Position : "body-segments"
    
    AuthUser {
        uuid id PK
        string username
        string email
    }
    
    Player {
        uuid id PK
        string username
        int score
        int highScore
        int gamesPlayed
    }
    
    LeaderboardEntry {
        int rank
        string username
        int score
        datetime date
    }
    
    LiveGame {
        uuid id PK
        Player player FK
        GameState gameState
        datetime startedAt
    }
    
    GameState {
        Snake snake
        Position food FK
        int score
        bool isGameOver
        bool isPaused
        GameMode mode
    }
    
    Snake {
        Position[] body
        Direction direction
    }
    
    Position {
        int x
        int y
    }
```

## Tech Stack Recommendation

```mermaid
graph LR
    subgraph "Frontend (Existing)"
        A[React + TypeScript]
        B[React Query]
        C[Tailwind CSS]
    end
    
    subgraph "Backend (To Implement)"
        D[Node.js/Express<br/>or<br/>Python/FastAPI]
        E[JWT Auth]
        F[REST API]
    end
    
    subgraph "Database"
        G[PostgreSQL<br/>or<br/>MongoDB]
    end
    
    subgraph "Optional (Future)"
        H[WebSocket Server<br/>for Real-time]
        I[Redis Cache<br/>for Sessions]
    end
    
    A --> F
    B --> F
    F --> E
    F --> G
    F -.-> H
    E -.-> I
```
