import ssl
import celery
from celery import Celery
from dotenv import load_dotenv
from .utilities.logging import create_celery_logger_handler


def create_celery_app(
        tasks: dict[str, dict],
        celery_redis_url,
        env_path: str | None = None,
        override_env: bool = True,
        celery_kwargs: dict | None = None,
        celery_conf_kwargs: dict | None = None,
) -> Celery:
    if env_path:
        load_dotenv(dotenv_path=env_path, override=override_env)

    task_routes = {
        task_key: {'queue': task_value.get('queue')} if task_value.get('queue') else {}
        for task_key, task_value in tasks.items()
    }

    beat_schedule = {
        task_key: {
            'task': task_key,
            'schedule': task_value.get('schedule'),
            'args': (),
        }
        for task_key, task_value in tasks.items()
        if task_value.get('schedule')
    }

    celery_dict = {
        'main': 'dealer_tower_celery_app',
        'broker': celery_redis_url,
        'backend': celery_redis_url,
        'task_serializer': "json",
        'result_serializer': "json",
        'timezone': 'America/Los_Angeles',
        'task_track_started': True,
        'result_persistent': True,
        'worker_prefetch_multiplier': 1,
    }

    if celery_redis_url.startswith('rediss'):
        celery_dict['broker_use_ssl'] = {
            'ssl_cert_reqs': ssl.CERT_NONE
        }
        celery_dict['redis_backend_use_ssl'] = {
            'ssl_cert_reqs': ssl.CERT_NONE
        }

    if celery_kwargs is not None:
        celery_dict.update(celery_kwargs)

    celery_app = Celery(**celery_dict)

    celery_conf_dict = dict(
        broker_transport_options={
            'global_keyprefix': 'celery-broker:'
        },
        result_backend_transport_options={
            'global_keyprefix': 'celery-backend:'
        },
        enable_utc=False,
        broker_connection_retry=True,
        broker_connection_max_retries=0,
        broker_connection_retry_on_startup=True,
        result_expires=3600,
        task_routes=task_routes,
        beat_schedule=beat_schedule,
        beat_max_loop_interval=300,
        redbeat_redis_url=celery_redis_url,
        beat_scheduler='redbeat.RedBeatScheduler',
        redbeat_key_prefix='celery-beat:',
        redbeat_lock_key='celery-beat::lock',
    )

    if celery_conf_kwargs is not None:
        celery_conf_dict.update(celery_conf_kwargs)

    celery_app.conf.update(**celery_conf_dict)
    celery_app.autodiscover_tasks(list(task_routes.keys()))

    return celery_app


@celery.signals.after_setup_task_logger.connect
def after_setup_celery_task_logger(logger, **kwargs):
    create_celery_logger_handler(logger, True)


@celery.signals.after_setup_logger.connect
def after_setup_celery_logger(logger, **kwargs):
    create_celery_logger_handler(logger, False)
