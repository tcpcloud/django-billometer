
from django.conf import settings

BILLING_CONFIG = {
  "currency": "CZK",
  "decimal_places": 3,
  "cache_expiration": 60 * 30
}

BILLING_CONFIG.update(getattr(settings, "BILLING_CONFIG", {}))

EXTRA_RESOURCES = getattr(settings, "BILLING_EXTRA_RESOURCES", {})
