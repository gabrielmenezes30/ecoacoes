# users/views/profile.py (crie este arquivo)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from users.forms import ProfileUpdateForm
from django.contrib import messages

@login_required
def profile_update_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('profile_update')
        else:
            print(form.errors)  # Para verificar se há algum erro no formulário
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'users/profile_update.html', {'form': form})
