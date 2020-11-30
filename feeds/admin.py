from django.contrib import admin

from feeds.models import Feed, FeedItem, FollowingFeed


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "url",
        "title",
        "subtitle",
        "rights",
        "info",
        "language",
        "guid",
        "icon_url",
        "image_url",
        "last_modified",
        "last_updated",
        "is_active",
    ]
    raw_id_fields = ["user"]


@admin.register(FeedItem)
class FeedItemAdmin(admin.ModelAdmin):
    list_display = [
        "feed",
        "title",
        "url",
        "guid",
        "content",
        "comments_url",
        "date_modified",
        "created_at",
    ]
    raw_id_fields = ["feed"]


@admin.register(FollowingFeed)
class FollowingFeedAdmin(admin.ModelAdmin):
    list_display = ["user", "feed"]
    raw_id_fields = ["user", "feed"]
