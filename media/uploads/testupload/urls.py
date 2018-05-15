from django.conf.urls import url
from django.views.generic import RedirectView
from . import views
from django.contrib.auth import views as auth_views
# Overrides the default 404 handler django.views.defaults.page_not_found
handler404 = 'catalog.views.page_not_found'

urlpatterns = [
    # url('', RedirectView.as_view(url='/catalog/')),
    url('^$', views.index, name="index"),
    url('^books/$', views.BookListView.as_view(), name='books'),
    url('^book/(?P<pk>[0-9]+)/$', views.BookDetailView.as_view(), name='book-detail'),
    url('^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='borrowed-books'),
    url('^borrowed/$', views.AllBorrowedBooks.as_view(), name='borrowed'),
    url('book/(?P<pk>[a-zA-Z0-9-]+)/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    url('author/create/', views.AuthorCreate.as_view(), name='author_create'),


]
