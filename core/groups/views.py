from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Group, GroupMembership, GroupPointsHistory
from .forms import GroupForm, InviteForm
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            
            # Adiciona o criador como admin
            GroupMembership.objects.create(
                user=request.user,
                group=group,
                role='admin'
            )
            
            messages.success(request, 'Grupo criado com sucesso!')
            return redirect('grupos:group_detail', pk=group.pk)
    else:
        form = GroupForm()
    
    return render(request, 'groups/create_group.html', {'form': form})

@login_required
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    is_member = GroupMembership.objects.filter(
        user=request.user,
        group=group
    ).exists()
    
    return render(request, 'groups/detail.html', {
        'group': group,
        'is_member': is_member,
        'members': group.memberships.all(),
        'points_history': group.points_history.all().order_by('-created_at')[:10]
    })

@login_required
def join_group(request, invite_code):
    group = get_object_or_404(Group, invite_code=invite_code)
    
    if GroupMembership.objects.filter(user=request.user, group=group).exists():
        messages.warning(request, 'Você já é membro deste grupo!')
    else:
        GroupMembership.objects.create(
            user=request.user,
            group=group,
            role='member'
        )
        messages.success(request, f'Você entrou no grupo {group.name}!')
    
    return redirect('grupos:group_detail', pk=group.pk)

@login_required
def generate_invite(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if not GroupMembership.objects.filter(
        user=request.user,
        group=group,
        role__in=['admin', 'mod']
    ).exists():
        messages.error(request, 'Você não tem permissão para convidar membros!')
        return redirect('grupos:group_detail', pk=group.pk)
    
    invite_url = group.get_invite_url(request)
    return render(request, 'groups/invite.html', {
        'group': group,
        'invite_url': invite_url
    })

@login_required
def add_points(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if not GroupMembership.objects.filter(
        user=request.user,
        group=group,
        role__in=['admin', 'mod']
    ).exists():
        messages.error(request, 'Permissão negada!')
        return redirect('grupos:group_detail', pk=group.pk)
    
    if request.method == 'POST':
        points = int(request.POST.get('points', 0))
        description = request.POST.get('description', '')
        point_type = request.POST.get('type', 'other')
        
        GroupPointsHistory.objects.create(
            group=group,
            points=points,
            type=point_type,
            description=description,
            added_by=request.user
        )
        messages.success(request, f'{points} pontos adicionados!')
        return redirect('grupos:group_detail', pk=group.pk)
    
    return render(request, 'groups/add_points.html', {'group': group})