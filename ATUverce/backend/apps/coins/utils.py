from django.conf import settings

def award_coins(user, reason, description=''):
    from apps.coins.models import CoinTransaction

    amounts = {
        'post_created': settings.COINS_FOR_POST,
        'helpful_answer': settings.COINS_FOR_HELPFUL_ANSWER,
        'activity': settings.COINS_FOR_ACTIVITY,
        'comment': settings.COINS_FOR_COMMENT,
        'story_posted': 3,
        'club_participation': 5,
        'admin_bonus': 0,
    }
    amount = amounts.get(reason, 0)
    if amount <= 0:
        return

    CoinTransaction.objects.create(user=user, amount=amount, reason=reason, description=description)
    user.ala_coins += amount
    user.save(update_fields=['ala_coins'])