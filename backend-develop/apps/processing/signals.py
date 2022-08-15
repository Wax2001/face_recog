from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from apps.processing.models import User, Image, Record
from apps.processing import publisher
from apps.processing import logger

from datetime import timedelta
from django.db import transaction

from rest_framework.authtoken.models import Token

@receiver(post_save, sender=Image)
def send_new_photo(sender, instance, created, *args, **kwargs):
    # send latest added Image instance
    try:
        logger.info(f'image sent to redis:\n{instance.user.id} {instance.img.url}')
        publisher.rpush('redis-channel', f'{instance.user.id} {instance.img.url}')
    except Exception as e:
        logger.error(f'error on Image signal: {e}')

@receiver(post_save, sender=Record)
def process_total_hours(sender, instance, created, *args, **kwargs):
    # Get latest created Record. Used to compute total worked hours of user instance.
    try:
        if instance.get_in_time() and instance.get_out_time() and instance.completed == False:
            net_work_hours = timedelta(hours=instance.get_out_time().hour, minutes=instance.get_out_time().minute) - timedelta(hours=instance.get_in_time().hour, minutes=instance.get_in_time().minute)
            if net_work_hours.days == 0:
                instance.user.salary.total_work_hours += round(float(net_work_hours.total_seconds()/3600), 2)
                instance.completed = True
                logger.info(
                    f'add work_hours to user ({instance.user}): {round(float(net_work_hours.total_seconds()/3600), 2)}'
                    )
                instance.save()
                instance.user.salary.save()
                # salary computation
                # instance.user.salary.hourly_rate * instance.user.salary.hours_up_work * (instance.user.salary.allowance/100)
    except Exception as e:
        logger.error(f'error on Record signal: {e}')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)