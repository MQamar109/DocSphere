from django.db import models

from core.models import BaseModel
from .choices import PROJECT_PERMISSIONS_OPTIONS, DOCUMENT_PERMISSIONS_OPTIONS


class ProjectDocumentBase(BaseModel):
    """
    Abstract base model for project and document models. Contains name and description.
    """

    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
    
class Project(ProjectDocumentBase):
    """
    A project belonging to an organization. Contains documents and can have
    user permissions assigned via ProjectPermissions.
    """

    organization = models.ForeignKey("organization.Organization", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Document(ProjectDocumentBase):
    """
    A document within a project. Can have user-level permissions
    assigned via DocumentPermissions.
    """

    project = models.ForeignKey("Project", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ProjectPermissions(BaseModel):
    """
    Through model for user–project access. Links a user to a project with
    a permission level: add, remove, or all.
    """
    
    permissions = models.CharField(choices=PROJECT_PERMISSIONS_OPTIONS, max_length=6)

    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.project.name}"
    
    class Meta:
        ordering = ['-created']

class DocumentPermissions(BaseModel):
    """
    Through model for user–document access. Links a user to a document with
    a permission level: read, write, or all.
    """
    
    permissions = models.CharField(choices=DOCUMENT_PERMISSIONS_OPTIONS, max_length=5)

    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    document = models.ForeignKey("Document", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.document.name}"
    
    class Meta:
        ordering = ['-created']
