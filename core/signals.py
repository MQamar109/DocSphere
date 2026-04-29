import logging

from django.dispatch import receiver
from djstripe.models import Subscription
from djstripe.signals import WEBHOOK_SIGNALS, webhook_post_process

logger = logging.getLogger(__name__)


@receiver(webhook_post_process)
def log_webhook_processed(sender, instance, **kwargs):
    logger.info(
        "dj-stripe processed webhook: type=%s id=%s",
        instance.event.type if instance.event else "unknown",
        instance.id,
    )


@receiver(WEBHOOK_SIGNALS["checkout.session.completed"])
def handle_checkout_completed(sender, event, **kwargs):
    session = event.data["object"]
    logger.info(
        "Checkout completed: customer=%s subscription=%s payment_status=%s",
        session.get("customer"),
        session.get("subscription"),
        session.get("payment_status"),
    )


@receiver(WEBHOOK_SIGNALS["customer.subscription.updated"])
def handle_subscription_updated(sender, event, **kwargs):
    """
    Fires when a subscription changes — upgrade, downgrade, trial ending etc.
    """
    stripe_subscription = event.data["object"]
    subscription_id = stripe_subscription.get("id")
    new_status = stripe_subscription.get("status")

    logger.info("Subscription %s updated - status=%s", subscription_id, new_status)

    try:
        subscription = Subscription.objects.get(id=subscription_id)
        organization = subscription.customer.subscriber
        logger.info("Organization %s subscription is now %s.", organization.name, new_status)
    except Subscription.DoesNotExist:
        logger.error("Subscription %s not found.", subscription_id)


@receiver(WEBHOOK_SIGNALS["customer.subscription.deleted"])
def handle_subscription_deleted(sender, event, **kwargs):
    """
    Fires when a subscription is cancelled and fully ends.
    """
    stripe_subscription = event.data["object"]
    subscription_id = stripe_subscription.get("id")
    logger.info("Subscription %s cancelled.", subscription_id)

    try:
        subscription = Subscription.objects.get(id=subscription_id)
        organization = subscription.customer.subscriber
        logger.info("Organization %s subscription deleted/cancelled.", organization.name)
    except Subscription.DoesNotExist:
        logger.error("Subscription %s not found.", subscription_id)


@receiver(WEBHOOK_SIGNALS["invoice.payment_failed"])
def handle_payment_failed(sender, event, **kwargs):
    """
    Fires when a subscription renewal payment fails.
    """
    invoice = event.data["object"]
    customer_id = invoice.get("customer")
    subscription_id = invoice.get("subscription")
    logger.warning("Payment failed: customer=%s subscription=%s", customer_id, subscription_id)