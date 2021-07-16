from ..environment import env


REDIS_URL = env.str("LARP_IN_UA_REDIS_URL", default="redis://redis:6380/2")
