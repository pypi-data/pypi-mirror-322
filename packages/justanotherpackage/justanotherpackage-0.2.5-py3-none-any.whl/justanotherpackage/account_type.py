import ctypes

def check_account_type():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin() != 0:
            return "Admin"
        else:
            return "User"
    except Exception:
        return "None"