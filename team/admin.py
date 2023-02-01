from django.contrib import admin

# Register your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Team, TeamMembership, TeamRole


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):

    def owners(self, obj):
        display_text = ", ".join([
            "<a href={}>{}</a>".format(
                reverse('admin:auth_user_change',
                        args=(member.pk,)),
                member.user.username)

            for member in TeamMembership.objects.filter(team=obj, role=dict(TeamRole.choices)['owner'])
        ])
        print(display_text)
        if display_text:
            return mark_safe(display_text)
        return "0"

    def members(self, obj):
        display_text = ", ".join([
            "<a href={}>{}</a>".format(
                reverse('admin:auth_user_change',
                        args=(member.pk,)),
                member.user.username)

            for member in TeamMembership.objects.filter(team=obj, role=dict(TeamRole.choices)['member'])
        ])
        print(display_text)
        if display_text:
            return mark_safe(display_text)
        return "0"

    def logo_img(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.logo.url,
            width=150,
            height=150,
        )
        )

    readonly_fields = ('owners', 'members', 'logo_img')
    list_display = ('name', 'wins')


admin.site.register(TeamMembership)
