from colorfield.fields import ColorField
from django.contrib.auth.models import AbstractUser
from django.db import models
from guardian.shortcuts import assign_perm, get_perms, remove_perm


class CustomUser(AbstractUser):
     # For task list and task detail we need user to have a list of tasks as its own model to be able to display all of them on a page task list easily and that model will require "def get_absolute_url(self): return reverse('task-detail', args=[str(self.id)])".
     # That will allow task_detail.html to have a link back to the list of all tasks for the user.
     # Make email required and has to be unique in the database
     email = models.EmailField(unique=True, blank=False)
     
class User(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

# For use with Tasks
class Category(models.Model):
    name = models.CharField(max_length=20)
    color = ColorField(default='#0d6efd')
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
    '''class Meta:
        permissions = (
            ('change_category', 'Edit Category'),
            ('delete_category', 'Delete Category'),
            ('view_category', 'View Category'),
        )'''

    def save(self,*args,**kwargs):
        #assign permissions to owner
        if (not self.pk):
            super(Category,self).save(*args,**kwargs)
            assign_perm('view_category',self.user,self)
            assign_perm('change_category',self.user,self)
            assign_perm('delete_category',self.user,self)
        else:
            super(Category,self).save(*args,**kwargs)

class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    deadlineDay = models.DateField()
    deadlineTime = models.TimeField()

    category = models.ForeignKey(Category,blank=True,null=True,on_delete=models.SET_NULL)
    duration = models.DurationField()
    status = models.BooleanField()
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE) # Changed to use CustomUser instead of User
    def __str__(self):
        return self.name
    
    """ class Meta:
        permissions = (
            ('change_task', 'Edit Task'),
            ('delete_task', 'Delete Task'),
            ('view_task', 'View Task'),
        ) """

    def save(self,*args,**kwargs):
        if self.category:
            if not self.category.user == self.user:
                raise ValueError("Category user must be the same as the task user")
            #assign permissions to owner
        if (not self.pk):
            super(Task,self).save(*args,**kwargs)
            assign_perm('view_task',self.user,self)
            assign_perm('change_task',self.user,self)
            assign_perm('delete_task',self.user,self)
        else:
            super(Task,self).save(*args,**kwargs)