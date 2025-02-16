```meramaid
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