from django.db import models

# Create your models here.

class Order(models.Model):
    OrderId = models.CharField(max_length=255)
    OrderUserId = models.CharField(max_length=255)
    OrderAmount = models.CharField(max_length=255)
    OrderShipName = models.CharField(max_length=255)
    OrderShipAddress = models.CharField(max_length=255)
    OrderShipAddress2 = models.CharField(max_length=255)
    OrderCity = models.CharField(max_length=255)
    OrderState = models.CharField(max_length=255)
    OrderZip = models.CharField(max_length=255)
    OrderCountry = models.CharField(max_length=255)
    OrderPhone = models.CharField(max_length=255)
    OrderShipping = models.CharField(max_length=255)
    OrderEmail = models.CharField(max_length=255)
    OrderDate = models.CharField(max_length=255)
    OrderShipped = models.BooleanField(default = False)
    OrderTrackingNumber = models.CharField(max_length=255)

class Product(models.Model):
    ProductId = models.CharField(max_length=255)
    ProductPrice = models.CharField(max_length=255)
    ProductName = models.CharField(max_length=255)
    ProductCartDesc = models.TextField()
    ProductShortDesc = models.TextField()
    ProductLongDesc = models.TextField()
    ProductQNA = models.TextField()
    ProductThumb = models.CharField(max_length=255)
    ProductImage = models.CharField(max_length=255)
    ProductImage1 = models.CharField(max_length=255)
    ProductImage2 = models.CharField(max_length=255)
    ProductImage3 = models.CharField(max_length=255)
    ProductCategoryId = models.CharField(max_length=255)
    ProductUpdateDate = models.CharField(max_length=255)
    ProductStock = models.CharField(max_length=255)
    # ProductLocation = models.CharField(max_length=255)

class ProductCategorie(models.Model):
    categoryId = models.CharField(max_length=255)
    categoryName = models.CharField(max_length=255)


class OrderDetails(models.Model):
    DetailId = models.CharField(max_length=255)
    DetailOrderId = models.CharField(max_length=255)
    DetailProductId = models.CharField(max_length=255)
    DetailName = models.CharField(max_length=255)
    DetailPrice = models.CharField(max_length=255) 
    DetailQuantity = models.CharField(max_length=255)

class User(models.Model):
    UserID = models.CharField(max_length=255)
    UserEmail = models.CharField(max_length=255)
    UserPassword = models.CharField(max_length=255)
    UserFirstName = models.CharField(max_length=255)
    UserLastName = models.CharField(max_length=255)
    UserCity = models.CharField(max_length=255)
    UserState = models.CharField(max_length=255)
    UserZip = models.CharField(max_length=255)
    UserEmailVerified = models.BooleanField(default=False)
    UserRegistrationCode = models.CharField(max_length=255)
    UserVerificationCode = models.CharField(max_length=255)
    UserPhone = models.CharField(max_length=255)
    UserCountry = models.CharField(max_length=255)
    UserAddress = models.CharField(max_length=255)
    UserAddress2 = models.CharField(max_length=255)