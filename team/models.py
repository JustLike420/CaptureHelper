import uuid
from django.conf import settings

from django.db import models
from django.utils import timezone


class TeamRole(models.TextChoices):
    OWNER = "Owner", "Владелец"
    MEMBER = "Member", "Участник"


class MembershipStatus(models.TextChoices):
    INACTIVE = "Inactive", "Неактивный"
    INVITED = "Invited", "Приглашенный"
    ACTIVE = "Active", "Активный"


class TeamSlotsStatus(models.TextChoices):
    """Статус слотов в команду"""
    FULL = "Full", "Набор закрыт"
    REC = "Rec", "Есть слоты"  # rec - open for recruitment/набор открыт


class InvitationStatus(models.TextChoices):
    WAITING = 'Waiting', 'В ожидании'
    APPROVED = 'Approved', 'Одобрено'
    REJECTED = 'Rejected', 'Отклонено'


class TeamMembership(models.Model):
    ROLE = TeamRole
    MEMBERSHIP_STATUS = MembershipStatus
    ROLES_DICT = dict(TeamRole.choices)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE,
        related_name='team_members'
    )
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=TeamRole.choices)
    status = models.CharField(max_length=30, choices=MembershipStatus.choices)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s in %s" % (self.user, self.team)

    def is_active(self):
        return self.status == self.MEMBERSHIP_STATUS.ACTIVE

    def is_invited(self):
        return self.status == self.MEMBERSHIP_STATUS.INVITED

    def is_owner(self):
        return self.role == self.ROLE.OWNER

    def send_invite_mail(self):
        pass


def clan_directory_path(instance: 'Team', filename: str) -> str:
    """Generate path to file in upload"""
    return f'clans/logos/clan_{instance.name}/{str(uuid.uuid4())}.{filename.split(".")[-1]}'


class Team(models.Model):
    name = models.CharField(max_length=250)
    logo = models.ImageField(upload_to=clan_directory_path, default='default/default_logo.png')
    slots = models.CharField(max_length=30, choices=TeamSlotsStatus.choices, default=TeamSlotsStatus.FULL)
    wins = models.IntegerField(default=0)  # кол-во соток
    site = models.URLField(max_length=50, null=True, blank=True)  # discord server

    def __str__(self):
        return self.name


class Invitation(models.Model):

    team = models.ForeignKey(Team, related_name="invitations", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invitations')
    invite_status = models.CharField(max_length=100, choices=InvitationStatus.choices, default=InvitationStatus.WAITING)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User {self.user} - team {self.team}'
