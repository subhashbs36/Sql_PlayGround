import io
import random
import string
from datetime import date, datetime, timedelta

from django.core.cache import cache
from django.core.mail import send_mail

from explorer import app_settings
from explorer.exporters import get_exporter_class
from explorer.models import Query, QueryLog


if app_settings.ENABLE_TASKS:
    from celery import shared_task
    from celery.utils.log import get_task_logger

    from explorer.utils import s3_upload
    logger = get_task_logger(__name__)
else:
    import logging

    from explorer.utils import noop_decorator as shared_task
    logger = logging.getLogger(__name__)


@shared_task
def execute_query(query_id, email_address):
    q = Query.objects.get(pk=query_id)
    send_mail('[SQL Explorer] Your query is running...',
              f'{q.title} is running and should be in your inbox soon!',
              app_settings.FROM_EMAIL,
              [email_address])

    exporter = get_exporter_class('csv')(q)
    random_part = ''.join(
        random.choice(
            string.ascii_uppercase + string.digits
        ) for _ in range(20)
    )
    try:
        url = s3_upload(f'{random_part}.csv', convert_csv_to_bytesio(exporter))
        subj = f'[SQL Explorer] Report "{q.title}" is ready'
        msg = f'Download results:\n\r{url}'
    except Exception as e:
        subj = f'[SQL Explorer] Error running report {q.title}'
        msg = f'Error: {e}\nPlease contact an administrator'
        logger.exception(f'{subj}: {e}')
    send_mail(subj, msg, app_settings.FROM_EMAIL, [email_address])


# I am sure there is a much more efficient way to do this but boto3 expects a binary file basically
def convert_csv_to_bytesio(csv_exporter):
    csv_file_io = csv_exporter.get_file_output()
    csv_file_io.seek(0)
    csv_data: str = csv_file_io.read()
    bio = io.BytesIO(bytes(csv_data, 'utf-8'))
    return bio


@shared_task
def snapshot_query(query_id):
    try:
        logger.info(f"Starting snapshot for query {query_id}...")
        q = Query.objects.get(pk=query_id)
        exporter = get_exporter_class('csv')(q)
        k = 'query-{}/snap-{}.csv'.format(
            q.id,
            date.today().strftime('%Y%m%d-%H:%M:%S')
        )
        logger.info(f"Uploading snapshot for query {query_id} as {k}...")
        url = s3_upload(k, convert_csv_to_bytesio(exporter))
        logger.info(
            f"Done uploading snapshot for query {query_id}. URL: {url}"
        )
    except Exception as e:
        logger.warning(
            f"Failed to snapshot query {query_id} ({e}). Retrying..."
        )
        snapshot_query.retry()


@shared_task
def snapshot_queries():
    logger.info("Starting query snapshots...")
    qs = Query.objects.filter(snapshot=True).values_list('id', flat=True)
    logger.info(
        f"Found {len(qs)} queries to snapshot. Creating snapshot tasks..."
    )
    for qid in qs:
        snapshot_query.delay(qid)
    logger.info("Done creating tasks.")


@shared_task
def truncate_querylogs(days):
    qs = QueryLog.objects.filter(
        run_at__lt=datetime.now() - timedelta(days=days)
    )
    logger.info(
        f'Deleting {qs.count} QueryLog objects older than {days} days.'
    )
    qs.delete()
    logger.info('Done deleting QueryLog objects.')


@shared_task
def build_schema_cache_async(connection_alias):
    from .schema import build_schema_info, connection_schema_cache_key
    ret = build_schema_info(connection_alias)
    cache.set(connection_schema_cache_key(connection_alias), ret)
    return ret
