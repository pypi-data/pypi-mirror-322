from django.contrib.auth import logout, login
from django.db.models import IntegerChoices, Model
from django.forms import Form
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View as DjangoView, generic
from django.contrib.auth import views as auth_views
from typing import Union, Optional, Any
from dataclasses import dataclass

sn = Optional[str]


class Category:
    def __init__(self, name: str, slug: str):
        self.name = name
        self.slug = slug

    def __str__(self):
        return f'name={self.name}, slug={self.slug}'


class HrenpackDjangoError(Exception):
    pass


class MenuElement:
    """Элемент меню"""
    def __init__(self, title: str, href: str = '/'):
        self.href = href
        self.title = title

    def __str__(self):
        return self.title


def view_dict(app_name: str, title: str, **kwargs) -> dict:
    kwargs['media_url'] = '/media/'
    kwargs['title'] = title
    kwargs['style'] = f'{app_name}/css/{app_name}.css'
    return kwargs


def boolean_choices(arg: IntegerChoices):
    return tuple(map(lambda x: (bool(x[0]), x[1]), arg.choices))


def semicolon_plus(model, del_id: bool = True):
    output = dict()
    for field in model._meta.fields:
        verbose_name = field.verbose_name + ':'
        name = field.name
        output[name] = verbose_name
    if del_id:
        del output['id']
    return output


class DataMixin:
    """Использовать в случае несовместимости с классами View и TemplateView"""
    title: str
    app_name: Optional[str] = None

    def get_mixin(self, context: dict, **kwargs):
        if not self.app_name:
            self.app_name = self.__module__.split('.')[0]
        context['style'] = f'{self.app_name}/css/{self.app_name}.css'
        context['title'] = self.title
        context.update(kwargs)
        return context


class View(DjangoView):
    title: str
    template_name: str
    app_name: sn = None
    style: sn = None

    def get_context_data(self, **kwargs):
        app_name = self.app_name if self.app_name else self.__module__.split('.')[0]
        try:
            kwargs = super().get_context_data(**kwargs)
        except AttributeError:
            pass
        kwargs['style'] = f'{app_name}/css/{app_name}.css' if not self.style else self.style
        kwargs['title'] = self.title
        return kwargs

    def _get(self, *args, **kwargs):
        """То, что выполняется до метода get"""

    def get_(self, *args, **kwargs):
        """То, что выполняется после метода get"""

    def _post(self, *args, **kwargs):
        """То, что выполняется до метода post"""

    def post_(self, *args, **kwargs):
        """То, что выполняется после метода post"""

    def get_decor(self, func):
        def wrapper(*args, **kwargs):
            self._get(*args, **kwargs)
            func(*args, **kwargs)
            self.get_(*args, **kwargs)
        return wrapper

    def post_decor(self, func):
        def wrapper(*args, **kwargs):
            self._post(*args, **kwargs)
            func(*args, **kwargs)
            self.post_(*args, **kwargs)
        return wrapper


class TemplateView(View, generic.TemplateView):
    pass


class ListView(TemplateView):
    model: Model
    context_name: str = 'db'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs[self.context_name] = self.get_queryset()
        return kwargs

    def get_queryset(self):
        return self.model.objects.all()

    # def get_model_dk(self, field: str):
    #     """Возвращает элементы из определенного поля модели"""
    #     if field in self.model._meta.fields:
    #         output = list()
    #         for el in self.get_queryset():
    #             output.append(el.__dict__[field])
    #         return output
    #     else:
    #         raise AttributeError("Указанного поля модели не существует")
    #
    # def get_object_or_404(self, field: str, value) -> Model:
    #     """Возвращает объект модели. Если нет, то возвращает исключение 404"""
    #     elements = self.get_queryset()
    #     values = self.get_model_dk(field)
    #     if not value in values:
    #         raise Http404
    #     return elements.get(**{field: value})


class DetailView(View, generic.DetailView):
    pass


class FormView(View, generic.FormView):
    pass


class CreateView(View, generic.CreateView):
    pass


class UpdateView(View, generic.UpdateView):
    pass


class RegistrationView(View):
    """Класс представления для регистрации пользователей"""
    form: Form
    success_url: sn = None
    success_template: sn = None
    title_success: sn = None
    username: str = 'username'
    password: str = 'password'
    first_name: str = 'first_name'
    last_name: str = 'last_name'
    email: str = 'email'
    enter_password: str = 'enter_password'
    authorize: str = 'authorize'

    def get(self, request):
        form = self.form()
        app_name = self.__module__.split('.')[0]
        return render(request, self, view_dict(**self.get_context_data(), form=form, app_name=app_name))

    def post(self, request):
        @self.post_decor
        def wrapper():
            form = self.form(request.POST)
            if request.user.is_authenticated:
                logout(request)
            if form.is_valid():
                user = form.save(False)
                user.set_password(form.cleaned_data[self.password])
                user.save()
                if form.cleaned_data[self.password]:
                    login(request, user)
        return wrapper()

    def post_(self, request, **kwargs):
        if self.success_url:
            return redirect(self.success_url)
        elif self.success_template and self.title_success:
            return render(request, self.success_template, kwargs)
        else:
            raise AttributeError("Нужные атрибуты не заданы")


class PasswordChangeView(View, auth_views.PasswordChangeView):
    pass


class PasswordChangeDoneView(View, auth_views.PasswordChangeDoneView):
    pass


class PasswordResetView(View, auth_views.PasswordResetView):
    pass


class PasswordResetDoneView(View, auth_views.PasswordResetDoneView):
    pass


class PasswordResetConfirmView(View, auth_views.PasswordResetConfirmView):
    pass


class PasswordResetCompleteView(View, auth_views.PasswordResetCompleteView):
    pass
