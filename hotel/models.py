from django.db import models

from userauths.models import User
from shortuuid.django_fields import ShortUUIDField
from django_ckeditor_5.fields import CKEditor5Field
from django.template.defaultfilters import escape
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.core.validators import MinValueValidator, MaxValueValidator
from taggit.managers import TaggableManager
import shortuuid
import requests
 

HOTEL_STATUS = (
    ("Draft", "Draft"),
    ("Disabled", "Disabled"),
    ("Rejected", "Rejected"),
    ("In Review", "In Review"),
    ("Live", "Live"),
)

RATING = (
    ( 1,  "★☆☆☆☆"),
    ( 2,  "★★☆☆☆"),
    ( 3,  "★★★☆☆"),
    ( 4,  "★★★★☆"),
    ( 5,  "★★★★★"),
)

ICON_TPYE = (
    ('Bootstap Icons', 'Bootstap Icons'),
    ('Fontawesome Icons', 'Fontawesome Icons'),
    ('Box Icons', 'Box Icons'),
    ('Remi Icons', 'Remi Icons'),
    ('Flat Icons', 'Flat Icons')
)

NOTIFICATION_TYPE = (
    ("Booking Confirmed", "Booking Confirmed"),
    ("Booking Cancelled", "Booking Cancelled"),
)

PAYMENT_STATUS = (
    ("paid", "Paid"),
    ("pending", "Pending"),
    ("processing", "Processing"),
    ("cancelled", "Cancelled"),
    ("initiated", 'Initiated'),
    ("failed", 'failed'),
    ("refunding", 'refunding'),
    ("refunded", 'refunded'),
    ("unpaid", 'unpaid'),
    ("expired", 'expired'),
)

# Create your models here.
# class Hotel(models.Model):
#     user =models.ForeignKey(User, on_delete= models.SET_NULL, null= True, related_name='create_hotel')
#     name = models.CharField(max_length=100)
#     description = CKEditor5Field(config_name='extends', null=True, blank=True)
#     image = models.FileField(upload_to="hotel_gallery")
#     address = models.CharField(max_length=200)
#     mobile = models.CharField(max_length=20)
#     email = models.CharField(max_length=20)
#     status = models.CharField(choices=HOTEL_STATUS, max_length=10, default="Live", null=True, blank=True)


#     tags = TaggableManager(blank = True)
#     views = models.IntegerField(default=0)
#     featured = models.BooleanField(default=False)
#     hid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
#     slug = models.SlugField(unique=True)
#     date = models.DateTimeField(auto_now_add=True)


#     def __str__(self):
#         return self.name
    
#     def save(self, *args, **kwargs):
#         if self.slug == "" or self.slug == None:
#             uuid_key = shortuuid.uuid()
#             uniqueid = uuid_key[:4]
#             self.slug = slugify(self.name) + "-" + str(uniqueid.lower())
            
#         super(Hotel, self).save(*args, **kwargs)

#     def thumbnail(self):
#         return mark_safe('<img src="%s" width="50px" height="50px" style="object-fit:cover; border-radius: 6px;" />' % (self.image.url))

#     def hotel_gallery(self):
#         return HotelGallery.objects.filter(hotel=self)
    
#     # def hotel_features(self):
#     #     return HotelFeatures.objects.filter(hotel=self)

#     # def hotel_faqs(self):
#     #     return HotelFAQs.objects.filter(hotel=self)

#     def hotel_room_types(self):
#         return RoomType.objects.filter(hotel=self)
    
#     def average_rating(self):
#         average_rating = Review.objects.filter(hotel=self).aggregate(avg_rating=models.Avg("rating"))
#         return average_rating['avg_rating']
    
#     def rating_count(self):
#         rating_count = Review.objects.filter(hotel=self).count()
#         return rating_count
    
#     # Add the save method with hotel validation
#     def save(self, *args, **kwargs):
#         if not self.user:
#             raise ValueError("user must be provided.")
#         super().save(*args, **kwargs)

import shortuuid
from django.utils.text import slugify

GEOAPIFY_API_KEY = 'b6c977ce7ff54985a263958fcb4ca782'

def geocode_address(address):
    url = f'https://api.geoapify.com/v1/geocode/search?text={address}&apiKey={b6c977ce7ff54985a263958fcb4ca782}'
    response = requests.get(url)
    data = response.json()
    
    if len(data['features']) > 0:
        coordinates = data['features'][0]['geometry']['coordinates']
        return coordinates[1], coordinates[0]  # returns latitude, longitude
    return None, None

class Hotel(models.Model):
    # user = mob6c977ce7ff54985a263958fcb4ca782dels.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='create_hotel')
    name = models.CharField(max_length=100)
    description = CKEditor5Field(config_name='extends', null=True, blank=True)
    image = models.FileField(upload_to="hotel_gallery")
    address = models.CharField(max_length=200)
    latitude = models.FloatField(null=True, blank=True)  # Auto-populated after geocoding
    longitude = models.FloatField(null=True, blank=True)
    mobile = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    status = models.CharField(choices=HOTEL_STATUS, max_length=10, default="Live", null=True, blank=True)

    tags = TaggableManager(blank=True)
    views = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    hid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    slug = models.SlugField(unique=True, blank=True)  # Allow blank slugs
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    # Single save method to handle slug generation and user validation
    def save(self, *args, **kwargs):
        # Ensure the user is provided
        if not self.user:
            raise ValueError("User must be provided.")
        
        # Generate the slug if it is not already set
        if not self.slug:
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:4]
            self.slug = slugify(self.name) + "-" + str(uniqueid.lower())

        super(Hotel, self).save(*args, **kwargs)

    def thumbnail(self):
        return mark_safe('<img src="%s" width="50px" height="50px" style="object-fit:cover; border-radius: 6px;" />' % (self.image.url))

    def hotel_gallery(self):
        return HotelGallery.objects.filter(hotel=self)

    def hotel_room_types(self):
        return RoomType.objects.filter(hotel=self)

    def average_rating(self):
        average_rating = Review.objects.filter(hotel=self).aggregate(avg_rating=models.Avg("rating"))
        return average_rating['avg_rating']

    def rating_count(self):
        rating_count = Review.objects.filter(hotel=self).count()
        return rating_count

# class HotelOwner():
#     is_hotel_owner = models.BooleanField(default=False)


class HotelGallery(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    image = models.FileField(upload_to="hotel_gallery")
    hgid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")

    def __str__(self):
        return str(self.hotel.name)

    class Meta:
        verbose_name_plural = "Hotel Gallery"

    # Add the save method with hotel validation
    def save(self, *args, **kwargs):
        if not self.hotel:
            raise ValueError("Hotel must be provided.")
        super().save(*args, **kwargs)

class HotelFeatures(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    icon_type = models.CharField(max_length=100, null=True, blank=True, choices=ICON_TPYE)
    icon = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = "Hotel Features"

    # Add the save method with hotel validation
    def save(self, *args, **kwargs):
        if not self.hotel:
            raise ValueError("Hotel must be provided.")
        super().save(*args, **kwargs)

class HotelFaqs(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    question = models.CharField(max_length=1000)
    answer = models.TextField(max_length=1000, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    hfid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")

    def __str__(self):
        return str(self.question)
    
    class Meta:
        verbose_name_plural = "Hotel FAQs"
    # Add the save method with hotel validation
    def save(self, *args, **kwargs):
        if not self.hotel:
            raise ValueError("Hotel must be provided.")
        super().save(*args, **kwargs)

class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    number_of_beds = models.PositiveIntegerField(default=0)
    room_capacity = models.PositiveIntegerField(default=0)
    rtid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.hotel.name} - {self.price}"

    class Meta:
        verbose_name_plural = "RoomType"

    def rooms_count(self):
        Room.objects.filter(room_type=self).count()

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         base_slug = slugify(self.name)
    #         uniqueid = shortuuid.uuid()[:4]
    #         self.slug = f"{base_slug}-{uniqueid.lower()}"
            
    #         # Check for uniqueness
    #         while Hotel.objects.filter(slug=self.slug).exists():
    #             uniqueid = shortuuid.uuid()[:4]
    #             self.slug = f"{base_slug}-{uniqueid.lower()}"
        
    #     super(Hotel, self).save(*args, **kwargs)
    
    # def save(self, *args, **kwargs):
    #     if self.slug == "" or self.slug == None:
    #         uuid_key = shortuuid.uuid()
    #         uniqueid = uuid_key[:4]
    #         self.slug = slugify(self.type) + "-" + str(uniqueid.lower())
            
    #     super(RoomType, self).save(*args, **kwargs)
    
    # Add the save method with hotel validation
    def save(self, *args, **kwargs):
        if not self.hotel:
            raise ValueError("Hotel must be provided.")
        super().save(*args, **kwargs)


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=1000)
    is_available = models.BooleanField(default=True)
    rid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type.type} -  Room {self.room_number}"

    class Meta:
        verbose_name_plural = "Rooms"

    def price(self):
        return self.room_type.price
    
    def number_of_beds(self):
        return self.room_type.number_of_beds
    
    # Add the save method with hotel validation
    def save(self, *args, **kwargs):
        if not self.hotel:
            raise ValueError("Hotel must be provided.")
        super().save(*args, **kwargs)


class Coupon(models.Model):
    code = models.CharField(max_length=1000)
    type = models.CharField(max_length=100, default="Percentage")
    discount = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(100)])
    redemption = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    make_public = models.BooleanField(default=False)
    valid_from = models.DateField()
    valid_to = models.DateField()
    cid = ShortUUIDField(length=10, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz")

    
    def __str__(self):
        return self.code
    
    class Meta:
        ordering =['-id']


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS, default="initiated")
    

    full_name = models.CharField(max_length=1000)
    email = models.EmailField(max_length=1000)
    phone = models.CharField(max_length=1000)
    
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    room = models.ManyToManyField(Room)
    before_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    saved = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    
    total_days = models.PositiveIntegerField(default=0)
    num_adults = models.PositiveIntegerField(default=1)
    num_children = models.PositiveIntegerField(default=0)
    
    checked_in = models.BooleanField(default=False)
    checked_out = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=False)
    
    checked_in_tracker = models.BooleanField(default=False, help_text="DO NOT CHECK THIS BOX")
    checked_out_tracker = models.BooleanField(default=False, help_text="DO NOT CHECK THIS BOX")
    
    bid = ShortUUIDField(unique = True, length = 10, max_length = 20, alphabet="abcdefghijklmnopqrstuvxyz")
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    coupons = models.ManyToManyField("hotel.Coupon", blank=True)
    stripe_payment_intent = models.CharField(max_length=1000,null=True, blank=True)
    success_id = ShortUUIDField(length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz", null =True, blank = True)
    booking_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")


    def __str__(self):
        return f"{self.booking_id}"
    
    def rooms(self):
        return self.room.all().count()
    
    # Add the save method with hotel validation
    def save(self, *args, **kwargs):
        if not self.user:
            raise ValueError("User must be provided.")
        super().save(*args, **kwargs)

class ActivityLog(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    guest_out = models.DateTimeField()
    guest_in = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"(self.booking)"
    # Add the save method with hotel validation
    def save(self, *args, **kwargs):
        if not self.booking:
            raise ValueError("Booking must be provided.")
        super().save(*args, **kwargs)

class CouponUsers(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    
    full_name = models.CharField(max_length=1000)
    email = models.CharField(max_length=1000)
    mobile = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.coupon.code)
    
    class Meta:
        ordering =['-id']
    # Add the save method with hotel validation
    def save(self, *args, **kwargs):
        if not self.booking:
            raise ValueError("Booking must be provided.")
        super().save(*args, **kwargs)


class StaffOnDuty(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    staff_id = models.CharField(null=True, blank=True, max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.staff_id)
    
    # Add the save method with hotel validation
    def save(self, *args, **kwargs):
        if not self.booking:
            raise ValueError("Booking must be provided.")
        super().save(*args, **kwargs)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=100, default="new_order", choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    nid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    date= models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user.username)
    
    class Meta:
        ordering = ['-date']

    # Add the save method with hotel validation
    def save(self, *args, **kwargs):
        if not self.user:
            raise ValueError("user must be provided.")
        super().save(*args, **kwargs)


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    bid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    date= models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user.username)
    
    class Meta:
        ordering = ['-date']
    # Add the save method with hotel validation
    def save(self, *args, **kwargs):
        if not self.user:
            raise ValueError("user must be provided.")
        super().save(*args, **kwargs)


# class Review(models.Model):
#     user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
#     hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT, blank=True, null=True, related_name="reviews")
#     review = models.TextField(null=True, blank=True)
#     reply = models.CharField(null=True, blank=True, max_length=1000)
#     rating = models.IntegerField(choices=RATING, default=None)
#     active = models.BooleanField(default=False)
#     helpful = models.ManyToManyField(User, blank=True, related_name="helpful")
#     date = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name_plural = "Reviews & Rating"
#         ordering = ["-date"]
        
#     def __str__(self):
#         return f"{self.user.username} - {self.rating}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, blank=True, null=True, related_name="reviews")
    review = models.TextField(null=True, blank=True)
    reply = models.CharField(null=True, blank=True, max_length=1000)
    rating = models.IntegerField(choices=RATING, default=None)
    active = models.BooleanField(default=False)
    helpful = models.ManyToManyField(User, blank=True, related_name="helpful")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Reviews & Rating"
        ordering = ["-date"]
        
    def __str__(self):
        return f"{self.user.username} - {self.rating}"
    # Add the save method with hotel validation
    def save(self, *args, **kwargs):
        if not self.user:
            raise ValueError("user must be provided.")
        super().save(*args, **kwargs)