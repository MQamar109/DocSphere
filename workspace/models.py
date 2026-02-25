from django.db import models
from organization.models import Organization
from user.models import User


class Project(models.Model):
    """
    A project belonging to an organization. Contains documents and can have
    user permissions assigned via ProjectPermissions.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_active= models.BooleanField(default=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Document(models.Model):
    """
    A document within a project. Can have user-level permissions
    assigned via DocumentPermissions.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_active= models.BooleanField(default=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProjectPermissions(models.Model):
    """
    Through model for user–project access. Links a user to a project with
    a permission level: add, remove, or all.
    """

    PROJECT_PERMISSIONS_OPTIONS= [("add","Add"), ("remove","Remove"), ("all","All")]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    permissions = models.CharField(choices=PROJECT_PERMISSIONS_OPTIONS,max_length=6)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + " - " + self.project.name

class DocumentPermissions(models.Model):
    """
    Through model for user–document access. Links a user to a document with
    a permission level: read, write, or all.
    """

    DOCUMENT_PERMISSIONS_OPTIONS= [("read","Read"), ("write","Write"), ("all","All")]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    permissions = models.CharField(choices=DOCUMENT_PERMISSIONS_OPTIONS,max_length=5)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + " - " + self.document.name
    
    class Meta:
        ordering = ['-created_at']
        