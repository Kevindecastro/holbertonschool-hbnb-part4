

# 🌐 HBnB Technical Documentation

## 🎯 Objective
This document compiles all the UML diagrams and explanatory notes regarding the architecture and design of the HBnB project. It serves as a technical reference for the implementation and development of the application.

## 📑 Table of Contents
    1. Introduction
    2. General Architecture
    3. Business Logic Layer
    4. API Interaction Flow

---

# 1. 🏗️ General Architecture

## 📦 Package Diagram

This diagram illustrates the overall structure of the application and how the main components interact with each other.

```
classDiagram
    class PresentationLayer {
        <<Interface>>
        +UserService() 
        +PlaceService() 
        +ReviewService() 
        +AmenityService() 
    }

    class BusinessLogicLayer {
        +UserModel() 
        +PlaceModel() 
        +ReviewModel() 
        +AmenityModel() 
    }

    class PersistenceLayer {
        +UserRepository() 
        +PlaceRepository() 
        +ReviewRepository() 
        +AmenityRepository() 
    }

    PresentationLayer --> BusinessLogicLayer : Use (Facade Pattern)
    BusinessLogicLayer --> PersistenceLayer : Interact with (Database Operations)
```
[Diagram Package:](https://github.com/Noam72T/holbertonschool-hbnb/blob/main/part1/DiagrammeHautlevel.png)

### Explanation
- **PresentationLayer**: Interfaces for user services like registration, place management, reviews, etc.
- **BusinessLogicLayer**: Contains the core business logic such as user, place, review, and amenity models.
- **PersistenceLayer**: Manages data storage, typically through repositories interacting with the database.

---

# 2. 💼 Business Logic Layer

## 📚 Class Diagram

This diagram describes the main classes used in the business logic layer of the application.

```
classDiagram
    class User {
        +UUID id
        +String firstName
        +String lastName
        +String email
        +String password
        +Boolean isAdmin
        +Date createdAt
        +Date updatedAt
        +void register()
        +void updateProfile()
        +void deleteAccount()
    }
    
    class Place {
        +UUID id
        +String title
        +String description
        +Float price
        +Float latitude
        +Float longitude
        +UUID ownerId
        +List<Amenity> amenities
        +Date createdAt
        +Date updatedAt
        +void create()
        +void update()
        +void delete()
        +List<Place> list()
    }
    
    class Review {
        +UUID id
        +UUID placeId
        +UUID userId
        +Int rating
        +String comment
        +Date createdAt
        +Date updatedAt
        +void create()
        +void update()
        +void delete()
        +List<Review> listByPlace(UUID placeId)
    }
    
    class Amenity {
        +UUID id
        +String name
        +String description
        +Date createdAt
        +Date updatedAt
        +void create()
        +void update()
        +void delete()
        +List<Amenity> list()
    }
    
    User "1" --> "*" Place : owns
    User "1" --> "*" Review : writes
    Place "1" --> "*" Review : has
    Place "*" -- "*" Amenity : includes
```
[Diagram de Class:](https://github.com/Noam72T/holbertonschool-hbnb/blob/main/part1/DiagrammeClass.png)

### 📝 Explanation
- **User**: Represents a user with their information and possible actions such as registration, profile updates, and account deletion.
- **Place**: Represents a place with its characteristics like title, description, price, location, and amenities.
- **Review**: Allows users to leave reviews on places.
- **Amenity**: Represents the amenities associated with places.

---

# 3. ⚡ API Interaction Flow

## Sequence Diagrams

These diagrams show the interactions between users and the system during key actions.

### 👤 User Authentication

```
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
```
[Diagram de Sequence 1:](https://github.com/Noam72T/holbertonschool-hbnb/blob/main/part1/DiagrammeSequence1.png)

### 🏠 Creating a Place

```
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: API Call (Create Place)
    API->>BusinessLogic: Validate Place Data
    BusinessLogic->>Database: Save Place Data
    Database-->>BusinessLogic: Confirm Save
    BusinessLogic-->>API: Return Success/Failure
    API-->>User: Return Success/Failure
```
[Diagram de Sequence 2:](https://github.com/Noam72T/holbertonschool-hbnb/blob/main/part1/DiagrammeSequence2.png)

### ✍️ Submitting a Review

```
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: API Call (Submit Review)
    API->>BusinessLogic: Validate Review Data
    BusinessLogic->>Database: Save Review Data
    Database-->>BusinessLogic: Confirm Save
    BusinessLogic-->>API: Return Success/Failure
    API-->>User: Return Success/Failure
```
[Diagram de Sequence 3:](https://github.com/Noam72T/holbertonschool-hbnb/blob/main/part1/DiagrammeSequence3.png)

### 🗺️ Fetching List of Places

```
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: API Call (Fetch List of Places)
    API->>BusinessLogic: Filter Places (Criteria)
    BusinessLogic->>Database: Query Places Data
    Database-->>BusinessLogic: Return Places List
    BusinessLogic-->>API: Return Places List
    API-->>User: Return List of Places
```
[Diagram de Sequence 4:](https://github.com/Noam72T/holbertonschool-hbnb/blob/main/part1/DiagrammeSequence4.png)


[Diagram de Sequence Global:](https://github.com/Noam72T/holbertonschool-hbnb/blob/main/part1/DiagrameSequence.png)

### 📝 Explanation
- These sequence diagrams illustrate the interactions between the user, API, business logic, and database during key actions such as user registration, place creation, review submission, and fetching places.


## 🧑‍💻 Authors

- [@Noam](https://www.github.com/Noam72T)
- [@Kevin](https://github.com/Kevindecastro)
