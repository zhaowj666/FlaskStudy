from app.models import Logs
from app.extensions import db


# 方案一： 同步保存日志
def save_log_to_db(log_data):
    if log_data is not None:
        log_entry = Logs(
            level=log_data['level'],
            request_id=log_data['request_id'],
            message=log_data['message'],
            created_at=log_data['created_at'],
        )
        db.session.add(log_entry)
        db.session.commit()
        print('日志记录成功！')


