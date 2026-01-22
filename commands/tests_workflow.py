from django.test import TestCase, Client
from django.contrib.auth.models import User
from commands.models import Command, EditRequest

class WorkflowTest(TestCase):
    def setUp(self):
        # Create users
        self.owner = User.objects.create_user(username='owner', password='password123')
        self.contributor = User.objects.create_user(username='contributor', password='password123')
        
        # Create a command
        self.command = Command.objects.create(
            title="Convert MP4 to GIF",
            command_string="ffmpeg -i input.mp4 output.gif",
            explanation="Basic conversion",
            author=self.owner
        )
        
        self.client = Client()

    def test_suggest_and_approve_edit(self):
        # 1. Contributor logs in
        self.client.login(username='contributor', password='password123')
        
        # 2. Contributor suggests an edit
        response = self.client.post(f'/command/{self.command.pk}/suggest/', {
            'suggested_command_string': 'ffmpeg -i input.mp4 -vf scale=320:-1 output.gif',
            'suggested_explanation': 'Added scaling for optimization'
        })
        self.assertEqual(response.status_code, 302) # Redirects to detail
        
        # Verify EditRequest created
        edit_request = EditRequest.objects.get(original_command=self.command)
        self.assertEqual(edit_request.status, 'PENDING')
        
        # 3. Owner logs in
        self.client.logout()
        self.client.login(username='owner', password='password123')
        
        # 4. Owner approves edit
        response = self.client.post(f'/review/{edit_request.pk}/', {
            'action': 'approve'
        })
        self.assertEqual(response.status_code, 302) # Redirects to dashboard
        
        # 5. Verify Command updated
        self.command.refresh_from_db()
        self.assertEqual(self.command.command_string, 'ffmpeg -i input.mp4 -vf scale=320:-1 output.gif')
        
        # Verify EditRequest status
        edit_request.refresh_from_db()
        self.assertEqual(edit_request.status, 'APPROVED')
        
        print("\n\nSUCCESS: Workflow verified - Edit suggestion was made by contributor and approved by owner.")
