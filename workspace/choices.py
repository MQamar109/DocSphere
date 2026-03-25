class ProjectPermissions(models.TextChoices):
    ADD = "add", "Add"
    REMOVE = "remove", "Remove"
    ALL = "all", "All"


class DocumentPermissions(models.TextChoices):
    READ = "read", "Read"
    WRITE = "write", "Write"
    ALL = "all", "All"