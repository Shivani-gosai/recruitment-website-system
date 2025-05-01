from django.contrib import admin

# Register your models here.
from .models import Login
from .models import Agency
from .models import State
from .models import City
from .models import CompanyCategory
from .models import Positions
from .models import Organization
from .models import Member
from .models import Post
from .models import Job
from .models import Application
from .models import Comments
from .models import Message
from .models import Likes
from .models import Followers
# from .models import Employee

admin.site.register(Login)
#admin.site.register(Agency)
admin.site.register(State)
admin.site.register(City)
admin.site.register(CompanyCategory)
admin.site.register(Positions)
#admin.site.register(Post)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Comments)
admin.site.register(Message)
admin.site.register(Likes)
# admin.site.register(Employee)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('cmpname', 'stremail', 'strmobileno', 'website', 'state', 'city', 'intro', 'overview','mission','vision','values')
    search_fields = ('cmpname', 'stremail', 'strmobileno')

from django.contrib import admin
from myapp.models import (
    Member, MemberEducation, MemberSkills, 
    MemberExperience, MemberLanguage, MemberLink
)

# ✅ Inline for MemberEducation
class MemberEducationInline(admin.TabularInline):
    model = MemberEducation
    extra = 1  # Show an extra empty form for new entries

# ✅ Inline for MemberSkills
class MemberSkillsInline(admin.TabularInline):
    model = MemberSkills
    extra = 1

# ✅ Inline for MemberExperience
class MemberExperienceInline(admin.TabularInline):
    model = MemberExperience
    extra = 1

# ✅ Inline for MemberLanguage
class MemberLanguageInline(admin.TabularInline):
    model = MemberLanguage
    extra = 1

# ✅ Inline for MemberLink
class MemberLinkInline(admin.TabularInline):
    model = MemberLink
    extra = 1

# ✅ Modify MemberAdmin to show inlines
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'eemail', 'phoneno', 'status')
    search_fields = ('firstname', 'lastname', 'eemail')
    inlines = [MemberEducationInline, MemberSkillsInline, MemberExperienceInline, MemberLanguageInline, MemberLinkInline]


from django.contrib import admin
from myapp.models import Agency

@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('agency_name', 'contact_number', 'email_address', 'website', 'state', 'city', 'date_of_establishment')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        print(qs)  # Debugging: Check if all agencies are fetched
        return qs



@admin.register(MemberEducation)
class MemberEducationAdmin(admin.ModelAdmin):
    list_display = ('member', 'passingyear', 'institute', 'grade', 'remark')
    search_fields = ('member__eemail', 'institute', 'grade')

@admin.register(MemberSkills)
class MemberSkillsAdmin(admin.ModelAdmin):
    list_display = ('member', 'skills', 'details')
    search_fields = ('member__eemail', 'skills')

@admin.register(MemberExperience)
class MemberExperienceAdmin(admin.ModelAdmin):
    list_display = ('member', 'organizationname', 'worktitle', 'startdate', 'enddate', 'totalmonthexperience')
    search_fields = ('member__eemail', 'organizationname', 'worktitle')

@admin.register(MemberLanguage)
class MemberLanguageAdmin(admin.ModelAdmin):
    list_display = ('member', 'language', 'proficiency')
    search_fields = ('member__eemail', 'language')

@admin.register(MemberLink)
class MemberLinkAdmin(admin.ModelAdmin):
    list_display = ('member', 'link_name', 'link_url')
    search_fields = ('member__eemail', 'link_name')

from django.contrib import admin
from .models import Summary

@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ('member', 'summary')
    search_fields = ('member__eemail',)  # 🔹 Fix for searching by email

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('posttitle', 'postdesc', 'postdttime', 'get_stremail')
    search_fields = ('posttitle', 'postdesc', 'login__stremail')
    list_filter = ('postdttime',)
    ordering = ('-postdttime',)

    def get_stremail(self, obj):
        return obj.login.stremail
    get_stremail.short_description = 'Email'


class FollowersAdmin(admin.ModelAdmin):
    list_display = ('id', 'followid', 'login', 'followdate')  # Show followid directly

admin.site.register(Followers, FollowersAdmin)