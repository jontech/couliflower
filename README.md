cauliflower project was meant only for **learning** purpose to better understand how real web framework works. It uses WebOB request/response library which is simply just request and response objects used to bypass all WSGI environment handling (definitely next project).

And basic application looks like this:

```
from webob import Response

from cauliflower.router import Router
hello_router = Router()


@hello_router.route('/')
def hello(request):
    return Response('Hello world!')


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 8080, hello_router)
    server.serve_forever()
```

You can use this code however you like ON YOUR OWN RISK.
