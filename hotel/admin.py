from django.contrib import admin
from hotel.models import Hotel,Booking, Notification,ActivityLog, StaffOnDuty, Room, RoomType, HotelGallery, HotelFeatures, HotelFaqs, Coupon, Bookmark, Review
from django.contrib import admin
from userauths.models import User

class HotelGalleryInline(admin.TabularInline):
    model = HotelGallery

# Register your models here.
class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelGalleryInline]
    list_display = ['thumbnail', 'name', 'user', 'status']
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Hotel, HotelAdmin)
admin.site.register(Booking)
admin.site.register(ActivityLog)
admin.site.register(StaffOnDuty)
admin.site.register(Room)
admin.site.register(Coupon)
admin.site.register(RoomType)
admin.site.register(Notification)
admin.site.register(Bookmark)
admin.site.register(Review)


class HotelGalleryAdmin(admin.ModelAdmin):
  list_display = ('hotel', 'image')
  readonly_fields = ('hgid',)

admin.site.register(HotelGallery, HotelGalleryAdmin)


class HotelFeaturesAdmin(admin.ModelAdmin):
  list_display = ('hotel', 'icon_type', 'icon', 'name')
  list_filter = ('hotel',)

admin.site.register(HotelFeatures, HotelFeaturesAdmin)



class HotelFaqsAdmin(admin.ModelAdmin):
  list_display = ('hotel', 'question', 'date')
  list_filter = ('hotel',)
  readonly_fields = ('hfid',)

admin.site.register(HotelFaqs, HotelFaqsAdmin)


class RoomTypeAdmin(admin.ModelAdmin):
  list_display = ('hotel', 'type', 'price', 'number_of_beds', 'room_capacity', 'date')
  list_filter = ('hotel',)
  readonly_fields = ('rtid',)

# admin.site.register(RoomType, RoomTypeAdmin)


class RoomAdmin(admin.ModelAdmin):
  list_display = ('hotel', 'room_type', 'room_number', 'is_available', 'date')
  list_filter = ('hotel', 'room_type', 'is_available')
  readonly_fields = ('rid',)

# admin.site.register(Room, RoomAdmin)


class BookingAdmin(admin.ModelAdmin):
  list_display = ('user', 'hotel', 'room_type', 'check_in_date', 'check_out_date', 'total', 'payment_status', 'is_active')
  list_filter = ('hotel', 'room_type', 'payment_status', 'is_active')
  readonly_fields = ('bid', 'booking_id')

# admin.site.register(Booking, BookingAdmin)


class ActivityLogAdmin(admin.ModelAdmin):
  list_display = ('booking', 'guest_in', 'guest_out', 'date')
  list_filter = ('booking',)
  readonly_fields = ('date',)

# admin.site.register(ActivityLog, ActivityLogAdmin)


class StaffOnDutyAdmin(admin.ModelAdmin):
  list_display = ('booking', 'staff_id', 'date')
  list_filter = ('booking',)
  readonly_fields = ('date',)

# admin.site.register(StaffOnDuty, StaffOnDutyAdmin)

# from django.contrib import admin
# from hotel.models import Hotel, Room, Booking, HotelGallery, HotelFeatures, HotelFaqs, RoomType, ActivityLog, StaffOnDuty, Coupon, CouponUsers, Notification, Bookmark, Review
# from import_export.admin import ImportExportModelAdmin

# class HotelGallery_Tab(admin.TabularInline):
#     model = HotelGallery

# class HotelFeatures_Tab(admin.TabularInline):
#     model = HotelFeatures

# class HotelFAQs_Tab(admin.TabularInline):
#     model = HotelFaqs

# class Room_Tab(admin.TabularInline):
#     model = Room

# class RoomType_Tab(admin.TabularInline):
#     model = RoomType

# class ActivityLog_Tab(admin.TabularInline):
#     model = ActivityLog

# class StaffOnDuty_Tab(admin.TabularInline):
#     model = StaffOnDuty

# class CouponUsers_Tab(admin.TabularInline):
#     model = CouponUsers

# class HotelAdmin(ImportExportModelAdmin):
#     inlines = [HotelGallery_Tab, HotelFeatures_Tab, RoomType_Tab ,Room_Tab, HotelFAQs_Tab]
#     search_fields = ['user__username', 'name']
#     list_filter = ['featured', 'status']
#     list_editable = ['status']
#     list_display = ['thumbnail' ,'user',  'name', 'status', 'featured' ,'views']
#     list_per_page = 100
#     prepopulated_fields = {"slug": ("name", )}


# class RoomAdmin(ImportExportModelAdmin):
#     list_display = ['hotel' ,'room_number',  'room_type', 'price', 'number_of_beds' ,'is_available']
#     list_per_page = 100


# class BookingAdmin(ImportExportModelAdmin):
#     inlines = [ActivityLog_Tab, StaffOnDuty_Tab]
#     list_filter = [ 'hotel', 'room_type', 'check_in_date', 'check_out_date', 'is_active' , 'checked_in' ,'checked_out']
#     list_display = ['booking_id', 'user', 'hotel', 'room_type', 'rooms', 'total', 'total_days', 'num_adults', 'num_children', 'check_in_date', 'check_out_date', 'is_active' , 'checked_in' ,'checked_out']
#     search_fields = ['booking_id', 'user__username', 'user__email']
#     list_per_page = 100


# # class RoomServicesAdmin(ImportExportModelAdmin):
# #     list_display = ['booking' ,'room', 'date', 'price', 'service_type']
# #     list_per_page = 100

# class CouponAdmin(ImportExportModelAdmin):
#     inlines = [CouponUsers_Tab]
#     list_editable = ['valid_from', 'valid_to', 'active', 'type']
#     list_display = ['code', 'discount', 'type', 'redemption', 'valid_from', 'valid_to' , 'active', 'date']
        
# class NotificationAdmin(ImportExportModelAdmin):
#     list_editable = ['seen', 'type']
#     list_display = ['user', 'booking', 'type', 'seen', 'date']

# class BookmarkAdmin(ImportExportModelAdmin):
#     list_display = ['user', 'hotel']

# class ReviewAdmin(admin.ModelAdmin):
#     list_editable = ['active']
#     list_display = ['user', 'hotel', 'review', 'reply' ,'rating', 'active']



# admin.site.register(Hotel, HotelAdmin)
# admin.site.register(Room, RoomAdmin)
# admin.site.register(Booking, BookingAdmin)
# # admin.site.register(RoomServices, RoomServicesAdmin)
# admin.site.register(Coupon, CouponAdmin)
# admin.site.register(Notification, NotificationAdmin)
# admin.site.register(Bookmark, BookmarkAdmin)
# admin.site.register(Review, ReviewAdmin)

