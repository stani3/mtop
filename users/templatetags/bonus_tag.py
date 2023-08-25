from django import template
from users.models import Bonus


register = template.Library()

@register.simple_tag
def get_sum(profile):
    bonuses = Bonus.objects.filter(profile_affiliate=profile, claimed=False)
    sum = 0
    for b in bonuses:
        sum += b.amount
    return sum


@register.simple_tag
def get_profit(prev_balance, new_balance, intrest):
    if prev_balance + prev_balance * intrest/100 == new_balance:
        return prev_balance*intrest/100
    else:
        return 0