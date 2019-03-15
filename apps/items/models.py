from django.db import models
from ..users.models import User

class ItemManager(models.Manager):
    def validate(self,form):
        errors = []
        if len(form['name']) < 3:
            errors.append("Item name must be at least 3 characters long.")
        try: 
            self.get(name=form['name'])
            errors.append('Item already added.')
        except:
            pass
        return errors

    def create_item(self,item_data):
        creator = User.objects.get(id=item_data['creator'])
        user_wished = User.objects.get(id=item_data['user_wished'])
        
        item = self.create(
            name=item_data['name'],
            creator=creator
        )
        item.user_wished.add(user_wished)

        return item

    def add_wish(self, wish_data):
        items = Item.objects.get(id=wish_data['item_id'])
        users_wish = User.objects.get(id=wish_data['user_id'])
        wish_list_add = items.user_wished.add(users_wish)
        return wish_list_add

    def remove_wish(self, remove_data):
        items = Item.objects.get(id=remove_data['item_id'])
        users_remove = User.objects.get(id=remove_data['user_id'])
        wish_list_remove = items.user_wished.remove(users_remove)
        return wish_list_remove
    
    def delete_wish(self, delete_data):
        items_delete = Item.objects.get(id=delete_data['item_id'])
        delete_item = items_delete.delete()
        return delete_item

class Item(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="items") 
    user_wished = models.ManyToManyField(User, related_name="wished_item")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager() 