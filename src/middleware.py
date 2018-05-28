import threading
from django.utils.deprecation import MiddlewareMixin


Thread_locals = threading.local()

def current_request():
    '''Retorna el request'''
    
    return Thread_locals


class GlobalCurrentRequestMiddleware(MiddlewareMixin):
    '''Coloca el request en el hilo local'''
    
    def process_request(self, request):
        Thread_locals.current_request = request