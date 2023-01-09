import json

from django.urls import reverse


class CookiesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_path = request.path
        token_refresh_path = reverse('token_refresh')
        token_destroy_path = reverse('token_destroy')

        if request.method == "POST" and request_path in [token_refresh_path,
                                                         token_destroy_path]:
            cookies = request.COOKIES
            refresh_token_cookies = cookies.get('refresh', None)

            if refresh_token_cookies:
                request_body = json.loads(request.body)
                request_body.update({
                    'refresh': refresh_token_cookies,
                })
                request._body = json.dumps(request_body).encode('utf-8')

        response = self.get_response(request)

        return response
