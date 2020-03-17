from django.db import models

# Create your models here.

class Order:
    OrderId : int
    OrderUserId : int
    OrderAmount : int
    OrderShipName : str
    OrderShipAddress : str
    OrderShipAddress2 : str
    OrderCity : str
    OrderState : str
    OrderZip : int
    OrderCountry : str
    OrderPhone : int
    OrderShipping : str
    OrderEmail : str
    OrderDate : str
    OrderShipped : bool
    OrderTrackingNumber : str

class Product :
    ProductId : int
    ProductPrice : int
    ProductName : str
    ProductCartDesc : str
    ProductShortDesc : str
    ProductLongDesc : str
    ProductThumb : str
    ProductImage : str
    ProductCategoryId : str
    ProductUpdateDate : str
    ProductStock : str
    ProductLocation : str

class ProductCategories:
    categoryId : str
    categoryName : str


class OrderDetails:
    DetailId : int
    DetailOrderId : str
    DetailProductId : str
    DetailName : str
    DetailPrice : int 
    DetailQuantity : int

class User:
    UserID : int
    UserEmail : str
    UserPassword : str
    UserFirstName : str
    UserLastName : str
    UserCity : str
    UserState : str
    UserZip : str
    UserEmailVerified : bool
    UserRegistrationCode  : str
    UserVerificationCode : str
    UserPhone : int
    UserCountry : str
    UserAddress : str
    UserAddress2 : str