from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic, View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from .models import Recipe
from .forms import CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class RecipeList(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6


class RecipeDetails(View):

    def get(self, request, pk, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=pk)
        comments = recipe.comments.filter(
            approved=True).order_by("-created_on")
        comment_form = CommentForm()
        liked = False
        if recipe.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "recipe_detail.html",
            {
                "recipe": recipe,
                "comments": comments,
                "commented": False,
                "comment_form": comment_form,
                "liked": liked
            },
        )

    def post(self, request, pk, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=pk)
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.recipe = recipe
            new_comment.author = request.user
            new_comment.save()
            return redirect('recipe_detail', pk=pk)
        comments = recipe.comments.filter(approved=True)

        return render(
            request,
            "recipe_detail.html",
            {
                "recipe": recipe,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form
            },
        )


class LikeRecipe(View):

    def post(self, request, pk, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=pk)

        if recipe.likes.filter(id=request.user.id).exists():
            recipe.likes.remove(request.user)
        else:
            recipe.likes.add(request.user)

        return HttpResponseRedirect(reverse('recipe_detail', args=[pk]))


class AddRecipe(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = 'add_recipe.html'
    fields = ('title', 'featured_image',
              'content', 'ingredients', 'estimated_time')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('recipe_detail', args=[self.object.pk])


class EditRecipe(UpdateView):
    model = Recipe
    template_name = 'edit_recipe.html'
    fields = ['title', 'content', 'ingredients', 'estimated_time']

    def get_success_url(self):
        return reverse('recipe_detail', args=[self.object.pk])


class DeleteRecipe(DeleteView):
    model = Recipe
    template_name = 'delete_recipe.html'
    success_url = reverse_lazy('home')
