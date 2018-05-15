# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Author, Genre, Book, BookInstance


from django.contrib import admin

# Register your models here.

# admin.site.register(Book)
#
# admin.site.register(Genre)
# admin.site.register(BookInstance)

# Define the admin class
class BookAdminInLine(admin.TabularInline):
    model = Book
    extra = 0


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')  # Customize the tree display
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]  # Customize the form display
    inlines = [BookAdminInLine]

admin.site.register(Author, AuthorAdmin)


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0  # This is to stop creating the addtional book instance as tabular-in-line


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]  # This display the BookInstance view inside the Book detail page



@admin.register(BookInstance)
class BookInstance(admin.ModelAdmin):
    list_display = ('status', 'due_back', 'borrower')
    list_filter = ('status', 'due_back')  # Add filter in the tree view

    #Sectioning the model fields in the form view
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
