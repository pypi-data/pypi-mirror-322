"""_____________________________________________________________________

:PROJECT: LARAsuite

*lara_django_people views *

:details: lara_django_people views module.
         - add app specific urls here
         - 
:authors: mark doerr <mark.doerr@uni-greifswald.de>

.. note:: -
.. todo:: -
________________________________________________________________________
"""


from dataclasses import dataclass, field
from typing import Any, List

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse, reverse_lazy

from django.utils.translation import gettext_lazy as _

from django.views.generic import DetailView
from django.views.generic import CreateView, UpdateView, DeleteView, RedirectView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.contrib.auth.forms import UserCreationForm
from django_filters.views import FilterView

from django.contrib import auth
from django_tables2 import MultiTableMixin, RequestConfig, SingleTableMixin, SingleTableView
from django_tables2.export.views import ExportMixin

from .models import Entity, Group, LaraUser
from .forms import EntityCreateForm, EntityUpdateForm #, LaraUserCreateForm, LaraUserUpdateForm
from .tables import EntityTable, LaraUserTable

from .filters import EntityFilterSet, GroupFilterSet

@dataclass
class PeopleMenu:
    menu_items:  List[dict] = field(default_factory=lambda: [
        {'name': 'Entities',
         'path': 'lara_django_people:entity-list'},
        {'name': 'Lara Users',
         'path': 'lara_django_people:lara-user-list'}
    ])


# class EntitiesListView(SingleTableView):
#     model = Entity
#     table_class = EntityTable

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['section_title'] = "Entities List"
#         return context

class EntitySingleTableView(SingleTableMixin, FilterView, ExportMixin):
    model = Entity
    #template_name = 'todos/todoitem_list.html'

    table_class = EntityTable
    filterset_class = EntityFilterSet

    template_name = 'lara_django_people/list.html'
    success_url = '/people'   # '/people/addresses/list'  # '/people'

    export_formats = ("csv",)

    def get_queryset(self):
        return super().get_queryset().select_related("entity_class")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_title'] = "Entity - List"
        context['create_link'] = 'lara_django_people:entity-create'
        context['delete_selected_link'] = 'lara_django_people:entity-delete-selected'
        context['menu_items'] = PeopleMenu().menu_items
        return context


class EntityDetailView(DetailView):
    model = Entity

    template_name = 'lara_django_people/entity_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        object = get_object_or_404(Entity, pk=self.kwargs['pk'])
        contact_dict = { "e-mail":  object.email, 
                         "Tel.(office)" : object.phone_number_office,
                         "Tel.(lab)" : object.phone_number_lab,
                         "Tel. (mobile)": object.phone_number_mobile } 

        context['section_title'] = "Entity - Details"
        context['update_link'] = 'lara_django_people:entity-update'
        context['menu_items'] = PeopleMenu().menu_items

        context['contact_dict'] = contact_dict
        return context


class EntityCreateView(CreateView):
    model = Entity
    template_name = 'lara_django_people/create_form.html'
    form_class = EntityCreateForm
    success_url = '/people'  # '/people'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_title'] = "Entity - Create"
        #context['update_link'] = 'lara_django_people:entity-create'
        #context['delete_link'] = 'lara_django_people:entity-delete'
        return context


class EntityUpdateView(UpdateView):
    model = Entity
    template_name = 'lara_django_people/update_form.html'
    form_class = EntityUpdateForm
    success_url = reverse_lazy('lara_django_people:entity-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_title'] = "Entity - Update"
        context['delete_link'] = 'lara_django_people:entity-delete'

        return context


class EntityDeleteView(DeleteView):
    model = Entity
    template_name = 'lara_django_people/delete_form.html'
    success_url = reverse_lazy('lara_django_people:entity-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_title'] = "Entity - Delete"
        context['delete_link'] = 'lara_django_people:entity-delete'
        return context
    
class EntityDeleteSelectedView(DeleteView):
    model = Entity
    template_name = 'lara_django_people/delete_selected_form.html'
    success_url = reverse_lazy('lara_django_people:entity-list')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        selected_rows = request.GET.getlist('selected_rows')

        print('---------------------- GET selected rows ---:\n', selected_rows)
    
        return super().get(request, *args, **kwargs)

    # def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:

    #     selected_rows = request.POST.getlist('selected_rows')

    #     print('---------------------- POST selected rows ---:\n', selected_rows)

    #     return super().post(request, *args, **kwargs)
        
        
    def get_object(self, queryset=None):
        if queryset is None:
            #queryset = self.get_queryset()

            # ask post for selected rows
            self.selected_rows = self.request.POST.getlist('selected_rows')

            print('---------------------- GET selected rows ---:\n', self.selected_rows)
    

            #Entity.objects.filter(pk__in=self.selected_rows).delete()
            queryset = Entity.objects.filter(pk__in=self.selected_rows)

            if queryset is None:
                raise Http404
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.selected_rows = self.request.POST.getlist('selected_rows')

        print('---------------------- POST selected rows ---:\n', self.selected_rows)

        context['section_title'] = "Entity - Delete selected 1a"
        context['delete_selected_link'] = 'lara_django_people:entity-delete-selected'
        context['selected_rows'] = self.selected_rows
        return context

def search_all(request):
    search_string = request.POST['search_query']

    try:
        entity_list = []
        entity = Entity.objects.filter(name_full__contains=search_string)
        entity_list.append(entity)

    except ValueError as err:
        print(f"ERROR: {err}")
        # ~ return render(request, 'polls/detail.html', {
        # ~ 'question': question,
        # ~ 'error_message': "You didn't select a choice.",
        # ~ })
    else:
        context = {'entity_list': entity_list}
        print('---------------------- POST search string ---:\n', search_string)
        print('---------------------- POST entity_list ---:\n', entity_list)
        #return render(request, 'lara_django_people/results.html', context)
        return HttpResponseRedirect(reverse('lara_django_people:entity-list', )) #args=(entity_list,)))



class LaraUserSingleTableView(SingleTableView):
    model = LaraUser
    #template_name = 'todos/todoitem_list.html'

    table_class = LaraUserTable

    template_name = 'lara_django_people/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_title'] = "LaraUser - List"
        context['create_link'] = 'lara_django_people:lara-user-create'
        context['menu_items'] = PeopleMenu().menu_items
        return context


class LaraUserDetailView(DetailView):
    model = LaraUser

    template_name = 'lara_django_people/larauser_detail.html'

    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_title'] = "LaraUser - Details"
        context['update_link'] = 'lara_django_people:lara-user-update'
        context['menu_items'] = PeopleMenu().menu_items
        return context

lara_user_detail_view = LaraUserDetailView.as_view()

class LaraUserCreateView(CreateView):
    model = LaraUser
    #template_name = 'lara_django_people/create_form.html'
    #form_class = LaraUserCreateForm
    #success_url = '/people'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_title'] = "LaraUser - Create"
        return context


class DisaLaraUserUpdateView(UpdateView, SuccessMessageMixin):
    model = LaraUser
    #template_name = 'lara_django_people/update_form.html'
    #form_class = LaraUserUpdateForm
    #success_url = '/people'

    success_message = _("Information successfully updated")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_title'] = "LaraUser - Update"
        context['delete_link'] = 'lara_django_people:lara-user-delete'

        return context
    
    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None = None) -> LaraUser:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user

class LaraUserUpdateView(SuccessMessageMixin, UpdateView):
    model = LaraUser
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_title'] = "LaraUser - Update"
        context['update_link'] = 'lara_django_people:lara-user-update'

        return context

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None = None) -> LaraUser:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user
    
lara_user_update_view = LaraUserUpdateView.as_view()

class LaraUserDeleteView(DeleteView):
    model = LaraUser
    #template_name = 'lara_django_people/delete_form.html'
    #success_url = '/people/entities/list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_title'] = "LaraUser - Delete"
        context['delete_link'] = 'lara_django_people:lara-user-delete'
        return context

class LaraUserRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.request.user.username})

lara_user_redirect_view = LaraUserRedirectView.as_view()

# class UserListView(ListView):
#     model = LaraUser

#     # retrieving super class context
#     def get_context_data(self, **kwargs):
#         context = super(UserListView, self).get_context_data(**kwargs)

#         context['table_caption'] = "List of all LARA users"
#         return context

# ~ def userGroups(request):
    # ~ lara_group_list = LaraGroup.objects.all()
    # ~ context = {'lara_group_list': lara_group_list}
    # ~ return render(request, 'lara_django_people/userGroups.html', context)


# def searchForm(request):
#     return render(request, 'lara_django_people/search.html', context={})


# def search(request):
#     search_string = request.POST['search']

#     try:
#         lara_user_list = []
#         lara_user = LaraUser.objects.get(user__first_name=search_string)
#         lara_user_list.append(lara_user)

#     except ValueError as err:
#         sys.stderr.write("ERROR: {}".format(err))
#         # ~ return render(request, 'polls/detail.html', {
#         # ~ 'question': question,
#         # ~ 'error_message': "You didn't select a choice.",
#         # ~ })
#     else:
#         context = {'lara_user_list': lara_user_list}
#         return render(request, 'lara_django_people/results.html', context)
#         # return HttpResponseRedirect(reverse('lara_django_people:results', args=(lara_user_list,)))


# def results(request, lara_user_list):
#     #question = get_object_or_404(Question, pk=question_id)
#     context = {'lara_user_list': lara_user_list}
#     return render(request, 'lara_django_people/results.html', context)


# def lara_user_detail(request, larauser_id):
#     lara_user = get_object_or_404(Lara_user, pk=larauser_id)
#     context = {'lara_user': lara_user}
#     return render(request, 'lara_django_people/users.html', context)
