import uuid
from django.conf import settings

from django.db import models
from django.utils import timezone


class TeamRole(models.TextChoices):
    OWNER = "owner", "owner"
    MEMBER = "member", "member"


class MembershipStatus(models.TextChoices):
    INACTIVE = "inactive", "inactive"
    INVITED = "invited", "invited"
    ACTIVE = "active", "active"


class TeamSlotsStatus(models.TextChoices):
    """Статус слотов в команду"""
    FULL = "full", "full"
    REC = "rec", "rec"  # rec - open for recruitment/набор открыт


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
