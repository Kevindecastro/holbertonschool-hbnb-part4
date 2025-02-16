```mermaid
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
