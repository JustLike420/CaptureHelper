import uuid
from django.conf import settings

from django.db import models
from django.utils import timezone


class TeamRole(models.TextChoices):
    OWNER = "owner", "owner"
    EDITOR = "editor", "editor"
    VIEWER = "viewer", "viewer"


class MembershipStatus(models.TextChoices):
    INACTIVE = "inactive", "inactive"
    INVITED = "invited", "invited"
    ACTIVE = "active", "active"


class TeamMembership(models.Model):
    ROLE = TeamRole
    MEMBERSHIP_STATUS = MembershipStatus
    ROLES_DICT = dict(TeamRole.choices)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE
    )
    # email = models.CharField(max_length=255, blank=True)
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=TeamRole.choices)
    status = models.CharField(max_length=30, choices=MembershipStatus.choices)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "team"],
                condition=models.Q(user__isnull=False),
                name="unique_user_team",
            )
        ]

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
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through=TeamMembership)
    logo = models.ImageField(upload_to=clan_directory_path, default='default/default_logo.png')

    def __str__(self):
        return self.name
