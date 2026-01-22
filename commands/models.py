from django.db import models
from django.contrib.auth.models import User

class Command(models.Model):
    title = models.CharField(max_length=255)
    command_string = models.TextField(help_text="The actual FFmpeg command.")
    explanation = models.TextField(help_text="Detailed breakdown of what the command does.")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commands')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class EditRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    original_command = models.ForeignKey(Command, on_delete=models.CASCADE, related_name='edit_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='edit_suggestions')
    suggested_command_string = models.TextField()
    suggested_explanation = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    admin_comment = models.TextField(blank=True, null=True, help_text="Reason for rejection or feedback.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Edit for {self.original_command.title} by {self.user.username}"
