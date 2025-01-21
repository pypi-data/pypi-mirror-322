import jwt
import datetime
import requests


class JWTHandler:
    TOKEN_ENDPOINT = "/iam/security/signin"

    def __init__(self, host, username, password):
        self.username = username
        self.password = password
        self.host = host
        self.jwt = None
        self.leeway = datetime.timedelta(minutes=2)

    def is_expired(self):
        if self.jwt is None:
            return True

        decoded_jwt = jwt.decode(self.jwt, options={"verify_signature": False})
        exp = decoded_jwt["exp"]
        exp_datetime = datetime.datetime.fromtimestamp(exp)
        now = datetime.datetime.now()
        leeway_expiry = exp_datetime - self.leeway

        return now > leeway_expiry

    def generate_tokens(self):
        """Generates a new JWT token by making an authentication request."""
        print("==========Avrio Token Call===========")

        url = "https://" + self.host + self.TOKEN_ENDPOINT

        payload = {
            "email": self.username,
            "password": self.password
        }
        try:
            response = requests.post(url, json=payload)
            data = response.json()
            self.jwt = data["accessToken"]
        except requests.RequestException as e:
            raise AuthenticationError(f"Failed to generate token: {str(e)}") from e
        except KeyError as e:
            raise AuthenticationError("Invalid response format: missing accessToken") from e

    def get_token(self):
        if self.is_expired():
            self.generate_tokens()

        return self.jwt


class AuthenticationError(Exception):
    """Custom exception for authentication-related errors."""
    pass
