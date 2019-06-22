from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {}

crons = {
    '_1st': crontab(day_of_month=1),
    '_21th': crontab(day_of_month=21, hour="01", minute="00"),
    '_27th': crontab(day_of_month=27),
    'every_day_11_00pm': crontab(hour="23", minute="00",  day_of_week='*'),
    'every_day_11_30pm': crontab(hour="23", minute="30",  day_of_week='*'),
    'every_day': crontab(hour="23", minute="55",  day_of_week='*'),
    'every_day++': crontab(hour="23", minute="59", day_of_week='*'),
    'every_2_hours': crontab(minute=0, hour='*/2')
}


CELERY_BEAT_SCHEDULE['audit_price_control'] = {
    'task': 'addons.price_control.tasks.collect_pricecontrol_data',
    'schedule': crons['every_2_hours'],
}
