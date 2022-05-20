from celery import shared_task


@shared_task
def pay_date_expired(*args, **kwargs):
    print('task celery')
