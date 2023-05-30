from uuid import uuid4

from square import Client
from django.conf import settings


class Square:

    def __init__(self, ):
        self.access_token = settings.ACCESS_TOKEN
        self.location = 'production' if settings.DEBUG else 'sandbox'
        
    
    def create_catalog_item(self, **kwargs):
        ...
        
    def view_catalog_item(self, **kwargs):
        ...
        
    def list_catalog_items(self, **kwargs):
        ...
        