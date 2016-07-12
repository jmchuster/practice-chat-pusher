from django.http import JsonResponse


class JsonStatus:
    def Ok(message='', data={}):
        return JsonResponse({**data, **{'status': 'OK', 'message': message}})

    def Noop(message='', data={}):
        return JsonResponse({**data, **{'status': 'NOOP', 'message': message}})

    def Error(message='', data={}):
        return JsonResponse({**data, **{'status': 'ERROR', 'message': message}})
