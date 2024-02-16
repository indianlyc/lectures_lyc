from django.shortcuts import render
from django.views import View
from .models import Good, Category
from .forms import SearchForm
from django.shortcuts import redirect


class MainView(View):
    template_name =  "main/main.html"
    def get_base_context(self, request, *args, **kwargs):
        list_categories = Category.objects.all()
        context = {
            'list_goods': kwargs['list_goods'],
            "list_categories": list_categories,
            'form': kwargs['form'],
        }
        return context

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            if kwargs.get("good_id", None) is not None:
                return redirect(f"/?query={query}")


            if query == "":
                list_goods = self.get_goods(request, *args, **kwargs)
            else:
                list_goods = self.get_goods(request, *args, **kwargs)\
                                        .filter(title__icontains=query)
        else:
            list_goods = []

        kwargs["list_goods"] = list_goods
        kwargs["form"] = form
        context  = self.get_base_context(request, *args, **kwargs)
        return render(request, self.template_name, context)

    def get_goods(self, request, *args, **kwargs):
        return Good.objects.all()

    def get(self, request, *args, **kwargs):
        form = SearchForm()
        list_goods = self.get_goods(request, *args, **kwargs)
        kwargs["list_goods"] = list_goods
        kwargs["form"] = form
        context  = self.get_base_context(request, *args, **kwargs)
        return render(request, self.template_name, context)


# def main_view(request):
#     if request.method == "POST":
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#
#             if query == "":
#                 list_goods = Good.objects.all()
#             else:
#                 list_goods = Good.objects.filter(title__icontains=query)
#         else:
#             list_goods = []
#     else:
#         form = SearchForm()
#         list_goods = Good.objects.all()
#
#     list_categories = Category.objects.all()
#     context = {
#         'list_goods': list_goods,
#         "list_categories": list_categories,
#         'form': form
#     }
#     return render(request, 'main/main.html', context)

class CategoryView(MainView):
    template_name = 'main/category.html'

    def get_goods(self, request, *args, **kwargs):
        return Good.objects.filter(category=kwargs["category_id"])

    def get_base_context(self, request, *args, **kwargs):
        context = super().get_base_context(request, *args, **kwargs)
        context.update(
            {
                "category": Category.objects.get(id=kwargs["category_id"])
            }
        )
        return context

# def category_view(request, category_id):
#     form  = SearchForm()
#     list_goods = Good.objects.filter(category=category_id)
#     list_categories = Category.objects.all()
#     category = Category.objects.get(id=category_id)
#     context = {
#         'list_goods': list_goods,
#         "list_categories": list_categories,
#         "category": category,
#         'form': form,
#     }
#     return render(request, 'main/category.html', context)


class GoodView(MainView):
    template_name = "main/good.html"

    def get_base_context(self, request, *args, **kwargs):
        context = super().get_base_context(request, *args, **kwargs)
        good = Good.objects.get(id=kwargs["good_id"])
        context.update(
            {
                "good": good,
            }
        )
        return context


# def good_view(request, good_id):
#     form  = SearchForm()
#     good = Good.objects.get(id=good_id)
#     list_categories = Category.objects.all()
#     context = {
#         'good': good,
#         "list_categories": list_categories,
#         'form':  form,
#     }
#     return render(request, 'main/good.html', context)