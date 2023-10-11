from graphql_jwt.utils import jwt_payload_handler as base_jwt_payload_handler

def jwt_payload_handler(user, context=None):
    payload = base_jwt_payload_handler(user, context)
    # Add additional payload data if needed
    return payload