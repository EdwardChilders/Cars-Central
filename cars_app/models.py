from django.db import models
import re
import bcrypt
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


class UserManager(models.Manager):
    def register_validator(self, post_data):
        errors = {}
        
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name should be at least two characters'
        
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name should be at least two characters'
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email/password!"
        
        if len(post_data['password']) < 8:
            errors['password'] = 'Password should be at least eight characters'
        
        if (post_data['password'] != post_data['confirm_password']):
            errors['confirm_password'] = "Password confirm didn't match"

        user_list = User.objects.filter(email=post_data['email'])
        if len(user_list) > 0:
            errors['email_password'] = "Email/password is incorrect. Please try again."

        return errors

    def login_validator(self, post_data):
        errors = {}
        user_list = User.objects.filter(email=post_data['email'])
        if len(user_list) == 0:
            errors['email_password'] = "Email/password is incorrect. Please try again."
        else:
            if bcrypt.checkpw(
                post_data['password'].encode(),
                user_list[0].password.encode()
            ) != True:
                errors['email_password'] = "Email/password is incorrect. Please try again."
        return errors

    def car_validator(self, post_data):
        errors = {}
        if len(post_data['title']) < 4:
            errors['title'] = 'Title should be at least four characters'
        
        if len(post_data['desc']) < 4:
            errors['desc'] = 'Description should be at least ten characters'

        if len(post_data['make']) < 2:
            errors['make'] = 'Make should be at least two characters'
        
        if len(post_data['model']) < 2:
            errors['model'] = 'Model should be at least two characters'

        if int(post_data['year']) < 1886 or int(post_data['year']) > datetime.date.today().year:
            errors['year'] = 'Year has to be valid!'
        
        if len(post_data['mileage']) < 1:
            errors['mileage'] = 'Please enter mileage'
        
        if len(post_data['price']) < 1:
            errors['price'] = 'Please enter a price'

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    password = models.CharField(max_length=255)
    objects = UserManager()
    # cars
    # parts
    # messages
    # comments
    # message_likes
    # comment_likes
    # car_messages

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)    


class Car(models.Model):
    
    title = models.CharField(max_length=45)
    desc = models.CharField(max_length=255)
    make = models.CharField(max_length=45)
    model = models.CharField(max_length=45)
    year = models.PositiveIntegerField(default=current_year(), validators=[MinValueValidator(1886), max_value_current_year])
    mileage = models.IntegerField()
    salvage = models.BooleanField()
    img = models.ImageField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    user_id = models.ForeignKey(User, related_name="cars", on_delete=models.CASCADE)
    message = models.ManyToManyField(User, related_name="car_messages")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Part(models.Model):
    title = models.CharField(max_length=45)
    desc = models.CharField(max_length=255)
    new = models.BooleanField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    user_id = models.ForeignKey(User, related_name="parts", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    message = models.CharField(max_length=255)
    user_id = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    liked_m = models.ManyToManyField(User, related_name="message_likes")
    #comments

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comments(models.Model):
    comment = models.CharField(max_length=255)
    user_id = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    message_id = models.ForeignKey(Message, related_name="comments", on_delete=models.CASCADE)
    liked_c = models.ManyToManyField(User, related_name="comment_likes")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

