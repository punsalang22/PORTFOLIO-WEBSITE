from django.db import models

class PersonalInformation(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    summary = models.TextField()
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TechStack(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Project(models.Model):
    project_name = models.CharField(max_length=100)
    description = models.TextField()
    # One TechStack (e.g. "Python") can be shared by many projects.
    tech_stack = models.ManyToManyField(TechStack, related_name='projects')
    link = models.URLField()

    def __str__(self):
        return self.project_name

    @property
    def tech_stack_names(self):
        return ', '.join(stack.name for stack in self.tech_stack.all())
