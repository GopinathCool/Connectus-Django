# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Custom import
from .models import Book, Author, BookInstance, Genre
from forms import RenewBookModelForm

# Django builtins import
from django.shortcuts import render
from django.views import generic
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin  # class based login check
from django.shortcuts import get_object_or_404
from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

# Python builtins import
import datetime

from django.contrib.contenttypes.models import ContentType
#Sample usage of contenttype objects
#ContentType.objects.get(app_label="auth", model="user").model_class().objects.all()
from django.contrib.auth.backends import ModelBackend


@login_required
def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    messages.success(request, 'Your password was updated successfully!', extra_tags='alert')
    # print messages.get_messages(request)
    print 'index'
    num_books=Book.objects.all().count()
    genre = Book.objects.all()[0]
    num_instances=BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # The 'all()' is implied by default.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    request.session['name'] = 'gopi'
    # print 'middle data', request.sessioln['middleware_data']


    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'catalog/index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors, 'num_visits': num_visits},
    )

class BookListView(LoginRequiredMixin, generic.ListView):
    # If template name is not given, then the default
    # template name will be application_name/model_name_list.html

    model = Book
    paginate_by = 1
    # context_object_name = 'my_book_list'
    #
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='harry')[:5]  # Get 5 books containing the title war
    def get_context_data(self, **kwargs):
        from django.core.paginator import Paginator
        from django.core.paginator import EmptyPage
        from django.core.paginator import PageNotAnInteger
        context = super(BookListView, self).get_context_data(**kwargs)
        list_exam = Book.objects.all()
        page = self.request.GET.get('page')
        paginator = Paginator(list_exam, self.paginate_by)

        try:
            file_exams = paginator.page(1)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context['list_exams'] = file_exams
        return context

class BookDetailView(generic.DetailView):
    model = Book
    # template_name = 'catalog/results.html'

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):

    model = BookInstance

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user)

    # def get_context_data(self, **kwargs):
    #     context = super(LoanedBooksByUserListView, self).get_context_data(**kwargs)
    #     booksbyUser = BookInstance.objects.filter(borrower=self.request.user)
    #     context['bookinstance_list'] = booksbyUser
    #     return context


class AllBorrowedBooks(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = ('catalog.can_view_all_borrowed')
    raise_exception = True  # Enable this to show 403 FORBIDDEN message


def renew_book_librarian(request, pk):
    print request.session['name']
    # print BookInstance.objects.filter(id=pk)
    book_inst = get_object_or_404(BookInstance, id=pk)
    # book_inst = get_object_or_404(BookInstance, book__title__contains = 'gfre')
    print book_inst
    if request.method == 'POST':
        form = RenewBookModelForm(request.POST)
        if form.is_valid():
            book_inst.due_back = form.cleaned_data['due_back']
            book_inst.save()
            return HttpResponseRedirect(reverse('borrowed'))
    else:
        proposal_date = datetime.datetime.today()
        form = RenewBookModelForm(initial={'due_back': proposal_date + datetime.timedelta(weeks=4)})
        print form
    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'book_inst': book_inst})


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'05/01/2018'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

def page_not_found(request):
    # Dict to pass to template, data could come from DB query
    values_for_template = {}
    return render(request,'404.html',values_for_template,status=404)