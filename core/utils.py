import logging


def get_logger(name='django'):
    return logging.getLogger(name)


def get_request_str(request):
    meta = request.META
    return f"{request.method} {request.get_full_path()} {meta.get('SERVER_PROTOCOL')} {meta.get('HTTP_USER_AGENT')}"


def get_debug_str(request, user, errors):
    return (
        f"""
        request: {get_request_str(request)}
        user: {f"{user} ({user.id})" if user else ""}
        data: {request.data}
        errors: {errors}"""
    )
