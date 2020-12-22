from django.contrib import admin
from .models import User, listings, comments, WatchList, bidmodel, closedlistings

# Register your models here.
admin.site.register(User)
admin.site.register(listings)
admin.site.register(comments)
admin.site.register(WatchList)
admin.site.register(bidmodel)
admin.site.register(closedlistings)


