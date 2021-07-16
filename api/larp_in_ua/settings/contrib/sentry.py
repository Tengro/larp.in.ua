import sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration

from ..environment import env


USE_SENTRY = env.bool("LARP_IN_UA_USE_SENTRY", default=True)
if USE_SENTRY:  # pragma: no cover
    SENTRY_DSN = env.str("LARP_IN_UA_SENTRY_DSN")
    SENTRY_ENVIRONMENT = env.str("LARP_IN_UA_SENTRY_ENVIRONMENT")
    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[DjangoIntegration()], environment=SENTRY_ENVIRONMENT)
