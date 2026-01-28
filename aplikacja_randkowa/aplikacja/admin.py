from django.contrib import admin
from .models import Pet, UserProfile, Match, Message


class PetAdmin(admin.ModelAdmin):
    list_display = ["name", "pet_type", "breed", "age", "is_friendly"]
    list_filter = ["pet_type", "is_friendly"]
    search_fields = ["name", "breed", "description"]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["first_name", "city", "get_age_display", "created_at"]
    list_filter = ["city", "gender", "preferred_pet_type", "created_at"]
    search_fields = ["first_name", "city", "bio", ]

    def get_age_display(self, obj):
        return obj.get_age()
    get_age_display.short_description = "Wiek"


class MatchAdmin(admin.ModelAdmin):
    list_display = ["swiper", "target", "is_match", "timestamp"]
    list_filter = ["is_match", "timestamp"]
    search_fields = ["swiper__first_name", "target__first_name"]


class MessageAdmin(admin.ModelAdmin):
    list_display = ["match", "sender", "recipient", "timestamp", "content"]
    list_filter = ["timestamp", "match__is_match"]
    search_fields = ["content", "sender__first_name", "recipient__first_name"]

admin.site.register(Pet, PetAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Message, MessageAdmin)

