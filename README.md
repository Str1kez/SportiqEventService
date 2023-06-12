# Event Microservice for Sportiq Project

This microservice is responsible for CRUD operations on events. It receives the `User`-header from API Gateway and uses it as the authorization key.

![Microservice Architecture](assets/diagram-dark.png#gh-dark-mode-only)
![Microservice Architecture](assets/diagram.png#gh-light-mode-only)

## Related Sportiq services

- [API Gateway](https://github.com/Str1kez/SportiqAPIGateway)
- [User Service](https://github.com/Str1kez/SportiqUserService)
- [Subscription Service](https://github.com/Str1kez/SportiqSubscriptionService)
- [Frontend App](https://github.com/Str1kez/SportiqReactApp)

## Documentation

OpenAPI - https://str1kez.github.io/SportiqEventService

## Caching

The cache is used in `GET`-requests on list of events on the map or specific event. \
It drops after removing of event or ttl elapsing (by default 1 minute for event and 10 minutes for sport types). \
The cache is updated after next `GET` or `PATCH` requests.

## Microservice

Microservice uses message query to interact with the subscription microservice. \
It uses RabbitMQ with persistent delivery mode to maintain delivering and handling guarantee.

### Startup

1. Create `.env` file and fill it:
   ```commandline
   make env
   ```
2. Run migrations:
   ```commandline
   make upgrade head
   ```
3. Create Docker-image:
   ```commandline
   make build
   ```
4. Run the microservice:
   ```commandline
   make up
   ```

`make down` - to stop
