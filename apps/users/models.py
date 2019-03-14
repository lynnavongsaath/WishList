from django.db import models
import bcrypt


class UserManager(models.Manager):
    def validate(self, form):
        errors = []
        if len(form['name']) < 3:
            errors.append('Name must be at least 3 characters long')
        if len(form['username']) < 3:
            errors.append('Username must be at least 3 characters long')
        if len(form['password']) < 8:
            errors.append('Password must be 8 characters long')
        if form['password'] != form['conf_pw']:
            errors.append('Password must match')
        try:
            self.get(username=form['username'])  
            errors.append('Username already in use')
        except:
            pass

        return errors
 
    def create_user(self, user_data):
        pw_hash = bcrypt.hashpw(user_data['password'].encode(), bcrypt.gensalt())
        user = self.create(
            name=user_data['name'],
            username=user_data['username'],
            pw_hash=pw_hash
        )
        return user
    
    def login(self, form):
        user_list = self.filter(username=form['username'])
        if len(user_list) > 0:
            user = user_list[0]
            if bcrypt.checkpw(form['password'].encode(),user.pw_hash.encode()):
                return (True, user.id)
            else:
                return (False, "Email or password incorrect.")
        else:
            return (False, "Email or password incorrect.")

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        name = self.name
        return name