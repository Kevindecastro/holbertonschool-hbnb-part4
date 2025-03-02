# HBnB - Part 2: Business Logic and API Implementation

## Table of Contents
- [Project Overview](#project-overview)
- [Objectives](#objectives)
- [Project Structure](#project-structure)
- [Business Logic Implementation](#business-logic-implementation)
- [API Endpoints](#api-endpoints)
- [Testing and Validation](#testing-and-validation)
- [Recommended Resources](#recommended-resources)
- [How to Run the Project](#how-to-run-the-project)

## Project Overview
In this phase of the HBnB Project, we implement the business logic and API endpoints using Python and Flask. The focus is on setting up the core functionality, creating and managing users, places, reviews, and amenities, while adhering to best practices in API design.

This part does not include JWT authentication and role-based access control, which will be addressed in the next phase. The service layer is built using Flask and `flask-restx` to create RESTful APIs.

## Objectives
By the end of this project, you should be able to:

1. **Set Up the Project Structure:**
   - Organize the project into a modular architecture.
   - Create necessary packages for the Presentation and Business Logic layers.
2. **Implement the Business Logic Layer:**
   - Develop core classes: `User`, `Place`, `Review`, `Amenity`.
   - Implement relationships between entities.
   - Apply the facade pattern to simplify layer communication.
3. **Build RESTful API Endpoints:**
   - Implement CRUD operations for Users, Places, Reviews, and Amenities.
   - Use `flask-restx` for API documentation.
   - Implement data serialization for nested relationships.
4. **Test and Validate the API:**
   - Ensure endpoints function correctly and handle edge cases.
   - Use Postman or cURL for testing.

## Project Structure
```
hbnb/
├── run.py                     # Main entry point
├── models/                    # Business Logic Layer
│   ├── __init__.py
│   ├── base_model.py
│   ├── user.py
│   ├── place.py
│   ├── review.py
│   ├── amenity.py
├── api/                        # Presentation Layer
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── places.py
│   │   ├── reviews.py
|   │   ├── amenities.py
|── services/
|   ├── __init__.py
|   ├──facade.py
├── persistence/                 # In-Memory Persistence Layer
│   ├── __init__.py
│   ├── repositoru.py
├── tests/                      # API Testing
│   ├── test_users.py
│   ├── test_places.py
│   ├── test_reviews.py
│   ├── test_amenities.py
├── config.py
├── requirements.txt
├── README.md
```

## Business Logic Implementation
Each entity is defined as a class in `models/`:
- **User**: Represents application users.
- **Place**: Represents rental properties.
- **Review**: Represents user reviews.
- **Amenity**: Represents amenities available at places.

Relationships between these entities are established, ensuring data integrity and proper interactions.

## API Endpoints
### User Endpoints
- `POST /api/v1/users/` - Create a new user.
- `GET /api/v1/users/` - Retrieve all users.
- `GET /api/v1/users/{id}` - Retrieve a specific user.
- `PUT /api/v1/users/{id}` - Update user information.

### Place Endpoints
- `POST /api/v1/places/` - Create a new place.
- `GET /api/v1/places/` - Retrieve all places.
- `GET /api/v1/places/{id}` - Retrieve a specific place.
- `PUT /api/v1/places/{id}` - Update place details.

### Review Endpoints
- `POST /api/v1/reviews/` - Create a new review.
- `GET /api/v1/reviews/` - Retrieve all reviews.
- `GET /api/v1/reviews/{id}` - Retrieve a specific review.
- `PUT /api/v1/reviews/{id}` - Update a review.

### Amenity Endpoints
- `POST /api/v1/amenities/` - Create a new amenity.
- `GET /api/v1/amenities/` - Retrieve all amenities.
- `GET /api/v1/amenities/{id}` - Retrieve a specific amenity.
- `PUT /api/v1/amenities/{id}` - Update an amenity.

## Testing and Validation
- Use **Postman** or **cURL** to test API endpoints.
- Ensure **CRUD operations** work as expected.
- Validate **data serialization** for relationships.
- Check for **edge cases** and handle errors gracefully.

## Recommended Resources
- [Flask Documentation](https://flask.palletsprojects.com/en/stable/)
- [Flask-RESTx Documentation](https://flask-restx.readthedocs.io/en/latest/)
- [REST API Best Practices](https://restfulapi.net/)
- [Python Object-Oriented Programming](https://realpython.com/python3-object-oriented-programming/)
- [Facade Pattern in Python](https://refactoring.guru/design-patterns/facade/python/example)

## How to Run the Project
### Prerequisites
- Python 3.x installed
- `pip install -r requirements.txt`

### Running the Application
1. Clone the repository:
   ```sh
   git clone https://github.com/Noam72T/holbertonschool-hbnb.git
   cd holbertonschool-hbnb/part2
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Start the Flask API:
   ```sh
   python app.py
   ```
4. Access API via:
   ```sh
   http://127.0.0.1:5000/api/v1/
   ```

## Authors

- [@Noam](https://www.github.com/Noam72T)
- [@Kevin](https://github.com/Kevindecastro)