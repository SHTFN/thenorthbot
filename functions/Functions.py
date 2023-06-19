from config import ADMIN_ID


def check_admin(user_id):
    if user_id in ADMIN_ID:
        return True
    return False
