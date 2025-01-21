import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env if present

class Config:
    secret = os.getenv("APIKEE_SECRET", "")
    host = os.getenv("APIKEE_HOST")
    token = os.getenv("APIKEE_TOKEN")
    project = os.getenv("APIKEE_PROJECT")

    @classmethod
    def validate(cls):
        """Validate that the required config values are set."""
        if (cls.host or cls.token or cls.project) and not (cls.host and cls.token and cls.project):
            raise ValueError("If `host`, `token`, or `project` is set, all three must be provided.")

    @classmethod
    def configure(cls, secret=None, host=None, token=None, project=None):
        """Update configuration dynamically."""
        if secret:
            cls.secret = secret
        if host:
            cls.host = host
        if token:
            cls.token = token
        if project:
            cls.project = project
        cls.validate()
