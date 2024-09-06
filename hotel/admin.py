from django.contrib import admin
from hotel.models import Hotel,Booking, Notification,ActivityLog, StaffOnDuty, Room, RoomType, HotelGallery, HotelFeatures, HotelFaqs, Coupon, Bookmark, Review

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


# class HotelGalleryAdmin(admin.ModelAdmin):
#   list_display = ('hotel', 'image')
#   readonly_fields = ('hgid',)

# admin.site.register(HotelGallery, HotelGalleryAdmin)


# class HotelFeaturesAdmin(admin.ModelAdmin):
#   list_display = ('hotel', 'icon_type', 'icon', 'name')
#   list_filter = ('hotel',)

# admin.site.register(HotelFeatures, HotelFeaturesAdmin)


# class HotelFaqsAdmin(admin.ModelAdmin):
#   list_display = ('hotel', 'question', 'date')
#   list_filter = ('hotel',)
#   readonly_fields = ('hfid',)

# admin.site.register(HotelFaqs, HotelFaqsAdmin)


# class RoomTypeAdmin(admin.ModelAdmin):
#   list_display = ('hotel', 'type', 'price', 'number_of_beds', 'room_capacity', 'date')
#   list_filter = ('hotel',)
#   readonly_fields = ('rtid',)

# admin.site.register(RoomType, RoomTypeAdmin)


# class RoomAdmin(admin.ModelAdmin):
#   list_display = ('hotel', 'room_type', 'room_number', 'is_available', 'date')
#   list_filter = ('hotel', 'room_type', 'is_available')
#   readonly_fields = ('rid',)

# admin.site.register(Room, RoomAdmin)


# class BookingAdmin(admin.ModelAdmin):
#   list_display = ('user', 'hotel', 'room_type', 'check_in_date', 'check_out_date', 'total', 'payment_status', 'is_active')
#   list_filter = ('hotel', 'room_type', 'payment_status', 'is_active')
#   readonly_fields = ('bid', 'booking_id')

# admin.site.register(Booking, BookingAdmin)


# class ActivityLogAdmin(admin.ModelAdmin):
#   list_display = ('booking', 'guest_in', 'guest_out', 'date')
#   list_filter = ('booking',)
#   readonly_fields = ('date',)

# admin.site.register(ActivityLog, ActivityLogAdmin)


# class StaffOnDutyAdmin(admin.ModelAdmin):
#   list_display = ('booking', 'staff_id', 'date')
#   list_filter = ('booking',)
#   readonly_fields = ('date',)

# admin.site.register(StaffOnDuty, StaffOnDutyAdmin)