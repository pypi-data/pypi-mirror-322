import ssl
from celery import Celery, signals
from dataclasses import dataclass
from dotenv import load_dotenv
from ..databases.redis import RedisUtility
from ..utilities.logging import create_celery_logger_handler
from ..utilities.settings import get_settings


@dataclass
class MainWorker:
    tasks: dict[str, dict]
    env_path: str | None = None
    override_env: bool = True
    celery_kwargs: dict | None = None
    celery_conf_kwargs: dict | None = None

    def create(self) -> Celery:
        if self.env_path:
            load_dotenv(dotenv_path=self.env_path, override=self.override_env)

        redis_utility = RedisUtility()
        celery_redis_url = redis_utility.get_redis_url()

        task_routes = {
            task_key: {'queue': task_value.get('queue')} if task_value.get('queue') else {}
            for task_key, task_value in self.tasks.items()
        }

        beat_schedule = {
            task_key: {
                'task': task_key,
                'schedule': task_value.get('schedule'),
                'args': (),
            }
            for task_key, task_value in self.tasks.items()
            if task_value.get('schedule')
        }

        celery_dict = {
            'main': f'dt_celery_app_{get_settings("service_name")}',
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

        if self.celery_kwargs is not None:
            celery_dict.update(self.celery_kwargs)

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

        if self.celery_conf_kwargs is not None:
            celery_conf_dict.update(self.celery_conf_kwargs)

        celery_app.conf.update(**celery_conf_dict)
        celery_app.autodiscover_tasks(list(task_routes.keys()))

        return celery_app


@signals.after_setup_task_logger.connect
def after_setup_celery_task_logger(logger, **kwargs):
    create_celery_logger_handler(logger, True)


@signals.after_setup_logger.connect
def after_setup_celery_logger(logger, **kwargs):
    create_celery_logger_handler(logger, False)
