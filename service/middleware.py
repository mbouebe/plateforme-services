class DebugCookiesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log avant la requête
        print("\n=== INCOMING REQUEST ===")
        print(f"Path: {request.path}")
        print(f"Method: {request.method}")
        print("Headers:")
        for header, value in request.headers.items():
            print(f"  {header}: {value}")
        print("Cookies:", request.COOKIES)
        print("Session:", {k: v for k, v in request.session.items()})
        print(f"User: {request.user} (Auth: {request.user.is_authenticated})")

        response = self.get_response(request)

        # Log après la réponse
        print("\n=== OUTGOING RESPONSE ===")
        print(f"Status: {response.status_code}")
        print("Headers:")
        for header, value in response.items():
            print(f"  {header}: {value}")
        
        return response
