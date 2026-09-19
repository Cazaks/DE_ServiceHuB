def get_role(user):
    if not user or not user.is_authenticated:
        return None
    if user.is_staff:
        return 'admin'
    if hasattr(user, 'customer'):
        return 'customer'
    if hasattr(user, 'provider'):
        return 'provider'
    return None