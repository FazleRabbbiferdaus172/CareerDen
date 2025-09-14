from django.contrib import admin
from .models import Profile, AcademicDetail, Degree, Contact, Email, Phone, Address, SocialMediaPlatform, \
    SocialMediaLink, ProfessionalDetail, Skills, SkillCategory, Event, EventTag, Certification, Project, ProjectTag


# Register your models here.

class SocialMediaLinkInline(admin.TabularInline):
    model = SocialMediaLink
    extra = 0

class SocialMediaPlatformAdmin(admin.ModelAdmin):
    fields = ['name', 'get_link']
    readonly_fields = ['get_link']
    inlines = [SocialMediaLinkInline]

class SocialMediaPlatformInline(admin.TabularInline):
    fields = ['name', 'get_link']
    readonly_fields = ['get_link']
    model = SocialMediaPlatform
    extra = 0

class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 0

class EmailInline(admin.TabularInline):
    model = Email
    extra = 0

class AddressInline(admin.TabularInline):
    model = Contact.addresses.through
    extra = 0

class ContactAdmin(admin.ModelAdmin):
    inlines = [AddressInline, EmailInline, PhoneInline, SocialMediaPlatformInline]
    exclude = ['addresses']

class DegreeAdmin(admin.ModelAdmin):
    fields = ['institution', 'start_date', 'end_date', 'is_graduated', 'education_type', 'address', 'gpa']


class DegreeInline(admin.TabularInline):
    model = AcademicDetail.degrees.through
    extra = 0


class AcademicDetailAdmin(admin.ModelAdmin):
    inlines = [DegreeInline]
    exclude = ['degrees']


class AcademicDetailInline(admin.TabularInline):
    model = Profile.academic_details.through
    extra = 0


class ProfessionalDetailInline(admin.StackedInline):
    model = Profile.professional_details.through
    extra = 0


class ContactDetailInline(admin.StackedInline):
    model = Profile.contact_details.through
    extra = 0


class ProfileAdmin(admin.ModelAdmin):
    inlines = [
        AcademicDetailInline,
        ProfessionalDetailInline,
        ContactDetailInline,
    ]
    exclude = ['contact_details', 'academic_details', 'professional_details']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(AcademicDetail, AcademicDetailAdmin)
admin.site.register(Degree, DegreeAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Email)
admin.site.register(Phone)
admin.site.register(Address)
admin.site.register(SocialMediaPlatform, SocialMediaPlatformAdmin)
admin.site.register(SocialMediaLink)
admin.site.register(ProfessionalDetail)
admin.site.register(Skills)
admin.site.register(SkillCategory)
admin.site.register(Event)
admin.site.register(EventTag)
admin.site.register(Certification)
admin.site.register(Project)
admin.site.register(ProjectTag)
