from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.urls import reverse

User = get_user_model()

class Group(models.Model):
    ROLES = [
        ('admin', 'Administrador'),
        ('mod', 'Moderador'),
        ('member', 'Membro'),
    ]
    
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='groups/avatars/', null=True, blank=True)
    total_points = models.IntegerField(default=0)
    invite_code = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_groups')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = get_random_string(8)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('grupos:group_detail', kwargs={'pk': self.pk})

    def get_invite_url(self, request):
        return request.build_absolute_uri(
            reverse('grupos:join_group', kwargs={'invite_code': self.invite_code})
        )

class GroupMembership(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('mod', 'Moderador'),
        ('member', 'Membro'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'group')
    
    def __str__(self):
        return f"{self.user.username} in {self.group.name} as {self.role}"

class GroupPointsHistory(models.Model):
    POINT_TYPES = [
        ('event', 'Evento'),
        ('challenge', 'Desafio'),
        ('admin', 'Administrativo'),
        ('other', 'Outro'),
    ]
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='points_history')
    points = models.IntegerField()
    type = models.CharField(max_length=10, choices=POINT_TYPES)
    description = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.group.total_points += self.points
        self.group.save()
    
    def __str__(self):
        return f"{self.points} pts for {self.group.name}"