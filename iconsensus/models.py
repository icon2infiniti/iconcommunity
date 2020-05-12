from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify


# These are model schemas from pre-registration site
class CorePrep(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    introduction = models.CharField(max_length=2000, blank=True, null=True)
    server_location = models.CharField(max_length=100, blank=True, null=True)
    server_type = models.CharField(max_length=100, blank=True, null=True)
    server_spec = models.CharField(max_length=2000, blank=True, null=True)
    logo = models.CharField(max_length=100, blank=True, null=True)
    server_location_latlong = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField()
    display = models.BooleanField()
    updated_at = models.DateTimeField()
    proposal_rich = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    self_intro_video = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_prep'

    def get_team(self):
        return self.team.all()

    def get_social(self):
        return self.social.all()


class CorePrepsocial(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    social_select = models.CharField(max_length=20, blank=True, null=True)
    prep = models.ForeignKey(
        CorePrep,
        related_name='social', on_delete=models.SET_NULL,
        null=True)
    link = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_prepsocial'


class CorePrepteam(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    avatar = models.CharField(max_length=100, blank=True, null=True)
    background = models.CharField(max_length=2000, blank=True, null=True)
    prep = models.ForeignKey(
        CorePrep,
        related_name='team', on_delete=models.SET_NULL,
        null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_prepteam'


class PrepProject(models.Model):
    CATEGORIES = [
        (0, 'Marketing'),
        (1, 'Development'),
        (2, 'Education'),
        (3, 'Infrastructure'),  
        (4, 'Community'),
        (5, 'Design'),
        (6, 'Other'),
    ]

    PROGRESS = [(i, "{}0%".format(i)) for i in range(0, 11)]

    STATUS = [
        (0, 'Planning'),
        (1, 'In Progress'),
        (2, 'Complete'),       
    ]

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    prep_address = models.CharField(max_length=42)

    name = models.CharField(max_length=64)
    start_date = models.DateField()
    end_date = models.DateField()    
    description = models.CharField(max_length=256)
    category = models.IntegerField(default=6, choices=CATEGORIES)
    progress = models.IntegerField(default=0, choices=PROGRESS)    
    status = models.IntegerField(default=0, choices=STATUS)    
    details = RichTextField()
    updates = RichTextField(blank=True, null=True)
    final_update = RichTextField(blank=True, null=True)
    slug = models.SlugField(default='', editable=False, max_length=71)

    display = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = "{} {}".format(self.name, self.prep_address[-6:])
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
