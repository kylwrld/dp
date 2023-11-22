from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="user")
    title = models.CharField(max_length=200)
    task_content = models.TextField()
    state = models.CharField(max_length=100, default="pendente")
    worklist = models.BooleanField(default=False)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(null=True)
    date = models.DateTimeField('date', default=None, null=True, blank=True)
    worklist_date = models.DateTimeField('worklist_date', default=None, null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Task, self).save(*args, **kwargs)
    
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50, default='')

    def __str__(self) -> str:
        return self.user.get_username()