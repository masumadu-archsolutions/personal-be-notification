import inspect

from flask import Response, json


def caller_info() -> str:
    info = inspect.getframeinfo(inspect.stack()[2][0])
    return f"{info.filename}:{info.function}:{info.lineno}"


def handle_result(result, schema=None, many=False):
    if schema:
        return Response(
            schema(many=many).dumps(result.value),
            status=result.status_code,
            mimetype="application/json",
        )
    else:
        return Response(
            json.dumps(result.value),
            status=result.status_code,
            mimetype="application/json",
        )
