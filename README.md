# gold-cart-backend
The gold cart backend, written in Django.


# API documentation
## Endpoints
1. token/ 
    - description: This endpoint is used to obtain user token to authorize user to make api calls
    - methods: POST
    - parameters: email, password
    - returned data: access(user's access token), refresh(user's refresh token.)

2. token/refresh/
    - description: This endpoint is used to refresh user access and refresh tokens. User tokens expire after 30 days
    - methods: POST
    - parameters: refresh(ie refresh token)
    - returned data: access(user's access token), refresh(user's refresh token.)

3. user/
    - description: This endpoint is used to manipulate user data
    - methods:
        1. POST
            - description: This method is used to create a new user
            - parameters: email, password, first_name, last_name
            - returned data: email, password, first_name, last_name, location
        2. PATCH
            - description: This method is used to update user information. (eg user location)
                - user locations: 
                    1. Gh: Ghana
                    2. Ng: Nigeria
                    3. Usa: USA
            - parameters: location
            - returned data: email, password, first_name, last_name, location
    
4. items/
    - description: This method is endpoint lists all items in our Square catalog.
    - parameters: None
    - returned data: 
        1. a list of all items in catalog if the user hasn't already set a location
        2. a list of all items in catalog related to the current location the user has set