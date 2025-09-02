from django.contrib import admin
from .models import Profile, AcademicDetail, Degree, Contact, Email, Phone, Address, SocialMediaPlatform, \
    SocialMediaLink, ProfessionalDetail, Skills, SkillCategory, Event, EventTag, Certification, Project, ProjectTag

# Register your models here.

admin.site.register(Profile)
admin.site.register(AcademicDetail)
admin.site.register(Degree)
admin.site.register(Contact)
admin.site.register(Email)
admin.site.register(Phone)
admin.site.register(Address)
admin.site.register(SocialMediaPlatform)
admin.site.register(SocialMediaLink)
admin.site.register(ProfessionalDetail)
admin.site.register(Skills)
admin.site.register(SkillCategory)
admin.site.register(Event)
admin.site.register(EventTag)
admin.site.register(Certification)
admin.site.register(Project)
admin.site.register(ProjectTag)
