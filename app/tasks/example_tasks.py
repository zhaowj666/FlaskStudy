import time
from app.extensions import celery
from app.models import User
from flask import current_app


@celery.task(bind=True)
def long_running_task(self, user_id, request_id_from_web):
    self.update_state(state='PROGRESS', meta={'current_task': 1, 'total': 5})

    for i in range(2, 6):
        time.sleep(3)
        self.update_state(state='PROGRESS', meta={'current_task': i, 'total': 5})

        current_app.logger.info(
            f"[后台任务执行中] {i}/5 | "
            f"用户ID： {user_id} | "
            f"请求ID： {request_id_from_web} | "
        )

    return {
        'result': '任务完成',
        'user_id': user_id,
        'request_id': request_id_from_web,
    }