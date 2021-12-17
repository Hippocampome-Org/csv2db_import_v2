from django.contrib import admin
from csv2db.models import Article
from csv2db.models import Author

admin.site.register(Article)
admin.site.register(Author)
