from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from config.settings import addable_model


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    professional_details = models.ManyToManyField('core.ProfessionalDetail',
                                                  related_name='profiles', blank=True)
    academic_details = models.ManyToManyField('core.AcademicDetail', related_name='profiles', blank=True)
    Contact_details = models.ManyToManyField('core.Contact', related_name='profiles', blank=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class AcademicDetail(models.Model):
    degrees = models.ManyToManyField('core.Degree', related_name='academic_details')

    def __str__(self):
        return self.degrees.all()[0].__str__() if self.degrees.all() else 'N/A'


class Degree(models.Model):
    institution = models.CharField(max_length=100)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_graduated = models.BooleanField(default=True)
    education_type = models.CharField(max_length=100)
    address = models.OneToOneField('core.Address', null=True, on_delete=models.CASCADE)
    gpa = models.FloatField()

    def __str__(self):
        return "{} - {} - {}".format(self.institution, self.address, self.education_type)


class Contact(models.Model):
    addresses = models.ManyToManyField('core.Address', related_name='contacts')
    def __str__(self):
        return self.addresses.all()[0].__str__() if self.addresses.all() else 'N/A'


class Email(models.Model):
    class UsageType(models.TextChoices):
        PRIMARY = 'primary', 'Primary'
        SECONDARY = 'secondary', 'Secondary'

    address = models.EmailField()
    usage_type = models.CharField(choices=UsageType.choices, max_length=100)
    is_professional = models.BooleanField(default=False)
    contact = models.ForeignKey(Contact, related_name='emails', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['usage_type'],
                condition=Q(usage_type='primary'),
                name='unique_primary_type_constraint'
            )
        ]

    def __str__(self):
        return self.address.__str__()


class Phone(models.Model):
    value = models.CharField(max_length=100)
    contact = models.ForeignKey(Contact, related_name='phones', on_delete=models.CASCADE)

    def __str__(self):
        return self.value


class Address(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        if self.state == self.city:
            return self.state + ", " + self.country
        return self.city + ", " + self.state+ ", " + self.country


class SocialMediaPlatform(models.Model):
    name = models.CharField(max_length=100)
    contact = models.ForeignKey(Contact, related_name='social_medias', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SocialMediaLink(models.Model):
    link = models.URLField()
    media = models.ForeignKey(SocialMediaPlatform, related_name='links', on_delete=models.CASCADE)

    def __str__(self):
        return self.link


class ProfessionalDetail(models.Model):
    company_name = models.CharField(max_length=100)
    company_address = models.ForeignKey(Address, related_name='professional_details', on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    events = models.ManyToManyField('core.Event', related_name='professional_details', blank=True)

    def __str__(self):
        return self.company_name + " " + self.position


class Skills(models.Model):
    name = models.CharField(max_length=100)
    category = models.ManyToManyField('core.SkillCategory', related_name='skills')

    def __str__(self):
        return self.name


class SkillCategory(models.Model):
    '''
    default
        Languages: Python, JavaScript, TypeScript, SQL, Bash

        Frameworks & Libraries: Odoo, React.js, Node.js, Django, Flask

        Databases: PostgreSQL, MySQL, MongoDB, Redis

        Tools & DevOps: Git, Docker, GitHub
        Actions, Jenkins, AWS, Nginx
    '''
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    sequence = models.IntegerField()
    tags = models.ManyToManyField('core.EventTag', related_name='events')
    reference_link = models.URLField()

    def __str__(self):
        return self.title


class EventTag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Certification(models.Model):
    name = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    link = models.URLField()
    date_start = models.DateField()
    date_end = models.DateField()
    is_lifetime = models.BooleanField(default=False)

    def __str__(self):
        return self.name + " " + self.institution


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField()
    tags = models.ManyToManyField('core.ProjectTag', related_name='projects')
    events = models.ManyToManyField('core.Event', related_name='projects')

    def __str__(self):
        return self.title


class ProjectTag(models.Model):
    '''
    default
        professional
        personal
        opensource
    '''
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Todo: make it a model?
addable_model.add(Profile)
