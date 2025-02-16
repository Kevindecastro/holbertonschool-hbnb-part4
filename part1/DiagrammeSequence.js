```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: API Call (Register User)
API->>BusinessLogic: Validate User Data
BusinessLogic->>Database: Check if User Exists
Database-->>BusinessLogic: User Exists Check Response
BusinessLogic->>Database: Save User Data
Database-->>BusinessLogic: Confirm Save
BusinessLogic-->>API: Return Success/Failure
API-->>User: Return Success/Failure

User->>API: API Call (Create Place)
API->>BusinessLogic: Validate Place Data
BusinessLogic->>Database: Save Place Data
Database-->>BusinessLogic: Confirm Save
BusinessLogic-->>API: Return Success/Failure
API-->>User: Return Success/Failure

User->>API: API Call (Submit Review)
API->>BusinessLogic: Validate Review Data
BusinessLogic->>Database: Save Review Data
Database-->>BusinessLogic: Confirm Save
BusinessLogic-->>API: Return Success/Failure
API-->>User: Return Success/Failure


User->>API: API Call (Fetch List of Places)
API->>BusinessLogic: Filter Places (Criteria)
BusinessLogic->>Database: Query Places Data
Database-->>BusinessLogic: Return Places List
BusinessLogic-->>API: Return Places List
API-->>User: Return List of Places
```