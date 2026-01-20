# from django.shortcuts import render
# from django.http import HttpResponse
# from rolepermissions.decorators import has_permission_decorator

# @has_permission_decorator('view_users')
# def create_users(request):
#     # return HttpResponse("Create Users Page")
#     return render(request, 'create_users.html')


from django.shortcuts import render
from .forms import UserCreationForm, UserChangeForm, CustomAuthenticationForm, CustomPasswordResetForm
from .models import Users
from rolepermissions.decorators import has_role_decorator, has_permission_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.views import LoginView, PasswordResetView

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/password_reset_form.html'


@has_role_decorator('Full')
def create_user_view(request):
    form = UserCreationForm()
    if request.method == 'GET':
        if request.user.perfil != 'full':
            messages.error(request, "Você não tem permissão para criar usuários.")
            return redirect("list_users")
        form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Usuário criado com sucesso!")
                return redirect("list_users")
            except IntegrityError:
                messages.error(request, "Este e-mail já está cadastrado.")
        else:
            messages.error(request, "Erro ao criar usuário. Verifique os dados.")


    return render(request, 'users/create_users.html', {'form': form})

@has_permission_decorator('view_content')
def list_users_view(request):
    users = Users.objects.all()
    return render(request, "users/list_users.html", {"usuarios": users})

@has_permission_decorator('edit_content')
def edit_user_view(request, user_id):
    user = get_object_or_404(Users, id=user_id)

    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=user, request_user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário atualizado com sucesso!")
            return redirect("list_users")
        else:
            messages.error(request, "Erro ao atualizar usuário. Verifique os dados.")
    else:
        form = UserChangeForm(instance=user, request_user=request.user)

    return render(request, "users/edit_user.html", {"form": form, "user": user})

@has_permission_decorator('delete_content')
def delete_user_view(request, user_id):
    user = get_object_or_404(Users, id=user_id)

    if request.method == "POST":
        user.delete()
        messages.success(request, "Usuário removido!")
        return redirect("list_users")

    return render(request, "users/delete_user.html", {"user": user})