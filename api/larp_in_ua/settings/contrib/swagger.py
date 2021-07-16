from ..environment import env


SWAGGER_SETTINGS = {
    "DEFAULT_API_URL": env.str("LARP_IN_UA_BASE_API_URL", default="https://larp.in.ua"),
}
