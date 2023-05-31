from uuid import uuid4

from square.client import Client
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class Square:
    def __init__(
        self,
    ):
        self.access_token = settings.SQUARE["ACCESS_TOKEN"]
        self.environment = "sandbox" if settings.DEBUG else "production"
        self.client = Client(
            access_token=self.access_token, environment=self.environment
        )

    def __convert_amount(self, amount):
        return amount / 100

    def __get_item_images(self, result):
        """Retrieve image urls for items with images"""
        images = {}
        for object in result.body["objects"]:
            if object["type"] == "IMAGE":
                images[object["id"]] = object["image_data"]["url"]
        logger.info("Images retrieved successfully")
        return images
    

    def list_all_items(self, **kwargs):
        result = self.client.catalog.list_catalog(types="ITEM,IMAGE")
        images = self.__get_item_images(result)
        if result.is_success():
            items = []
            for object in result.body["objects"]:
                if object["type"] == "ITEM": 
                    price_money = object["item_data"]["variations"][0][
                        "item_variation_data"
                    ]["price_money"]
                    image_id = object["item_data"].get("image_ids", [None])
                        
                    if object["type"] == "ITEM":
                        item_details = {
                            "id": object["id"],
                            "name": object["item_data"]["name"],
                            "description": object["item_data"]["description"],
                            "price": self.__convert_amount(price_money["amount"]),
                            "currency": price_money["currency"],
                            "image_url": images.get(image_id[0]),
                        }
                        items.append(item_details)
            logger.info("Items successfully returned to api views")
            return items
        else:
            logger.info("An error occured. No items returned to api views.")
            logger.error(result.errors)
            return None

    def view_catalog_item(self, **kwargs):
        ...

    def list_catalog_items(self, **kwargs):
        ...
