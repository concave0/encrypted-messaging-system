# FastAPI Encrypted Messaging System Backend 

### Functionality

This is a basic backend that takes in user messages JSON files stored in request headers encrypts them with a JWT then sends them to the designation. All requests are wrapped in HTTPS. 

- Rotating Self-Assigned Keys: It secures the JWT by rotating a self-signed public and private key.
- Account Creation:
    - It allows for an account creation through an endpoint that creates a password, and username.
    - This then creates a public and private key that creates a JWT.
    - The JWT, public, and private keys are stored in a JSON file along with the password/username.
- Messaging system authentication:
    - The backend also authenticates and authorizes users with the JWT, password, and username in a stored request header.
    - It will decrypt the JWT public key associated with that user.
- Messaging System:
    - Takes in following a request header: user username, password, JWT, message.
    - Reroute the the Messaging system authentication endpoint
    - After the sender's  is authenticated and authorized the messaging system endpoint will encrypt the users message and then pass it along the receiver.
        - The message is then passed in a JSON format with the username as the key and message value
            - The message is then encrypted with a users public key.
            - The encrypted message will become a JWT and is sent to the designation in request header along with the users public key.
