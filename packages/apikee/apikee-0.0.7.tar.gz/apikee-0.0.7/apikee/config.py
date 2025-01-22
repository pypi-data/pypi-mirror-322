import os

# Configuration settings
config = {
    'secret': os.getenv('APIKEE_SECRET'),
    'host': os.getenv('APIKEE_HOST', None),
    'token': os.getenv('APIKEE_TOKEN', None),
    'project': os.getenv('APIKEE_PROJECT', None),
}

def configure_apikee(custom_config: dict):
    """
    Configure ApiKee with a custom configuration.
    Validates that if one of `host`, `token`, or `project` is provided, all must be present.
    Ensures `APIKEE_SECRET` is mandatory.
    """
    config.update(custom_config)

    # Ensure `APIKEE_SECRET` is provided
    if not config['secret']:
        raise ValueError(
            "Configuration Error: `APIKEE_SECRET` is mandatory and cannot be empty. Please set it in the environment or pass it in the configuration."
        )

    # Validation logic: Ensure consistency for `host`, `token`, and `project`
    host, token, project = config['host'], config['token'], config['project']
    if (host or token or project) and not (host and token and project):
        raise ValueError(
            "Incomplete configuration: If one of `host`, `token`, or `project` is provided, all three must be specified."
        )
