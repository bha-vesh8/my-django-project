from django.shortcuts import redirect

def simple_middleware(get_response):
    
 def middleware(request):
    returnUrl = request.META['PATH_INFO']
    if not request.session.get('customer'):
        return redirect(f'loginn/?return_url={returnUrl}')
    response = get_response(request)
    return response
 return middleware