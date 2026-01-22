from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Command, EditRequest
from .forms import CommandForm, EditRequestForm

def command_list(request):
    query = request.GET.get('q')
    if query:
        commands = Command.objects.filter(
            Q(title__icontains=query) | Q(command_string__icontains=query)
        )
    else:
        commands = Command.objects.all().order_by('-created_at')
    return render(request, 'commands/command_list.html', {'commands': commands})

def command_detail(request, pk):
    command = get_object_or_404(Command, pk=pk)
    pending_edits = command.edit_requests.filter(status='PENDING')
    
    # If a user is viewing their own command, they see pending edits.
    # If a user is viewing someone else's command, they might see a button to suggest functionality.
    
    # distinct() might vary by DB, but for sqlite/postgres this is standard for getting unique users
    contributors = command.edit_requests.filter(status='APPROVED').select_related('user').order_by('user__username').distinct('user__username')
    # Note: distinct on field is Postgres only. For SQLite/Generic compatibility:
    # We'll fetch all and deduplicate in python or use a different query.
    # Simple approach for now:
    approved_edits = command.edit_requests.filter(status='APPROVED').select_related('user')
    contributors = {edit.user for edit in approved_edits}

    return render(request, 'commands/command_detail.html', {
        'command': command,
        'pending_edits': pending_edits,
        'contributors': contributors
    })

@login_required
def add_command(request):
    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            command = form.save(commit=False)
            command.author = request.user
            command.save()
            return redirect('command_detail', pk=command.pk)
    else:
        form = CommandForm()
    return render(request, 'commands/add_command.html', {'form': form})

@login_required
def edit_command(request, pk):
    command = get_object_or_404(Command, pk=pk)
    # Ensure only the author can edit
    if request.user != command.author:
        return redirect('command_detail', pk=pk)
    
    if request.method == 'POST':
        form = CommandForm(request.POST, instance=command)
        if form.is_valid():
            form.save()
            return redirect('command_detail', pk=pk)
    else:
        form = CommandForm(instance=command)
    
    return render(request, 'commands/edit_command.html', {'form': form, 'command': command})

@login_required
def suggest_edit(request, pk):
    command = get_object_or_404(Command, pk=pk)
    if request.method == 'POST':
        form = EditRequestForm(request.POST)
        if form.is_valid():
            edit_request = form.save(commit=False)
            edit_request.original_command = command
            edit_request.user = request.user
            edit_request.save()
            return redirect('command_detail', pk=pk)
    else:
        # Pre-fill with current data
        form = EditRequestForm(initial={
            'suggested_command_string': command.command_string,
            'suggested_explanation': command.explanation
        })
    return render(request, 'commands/suggest_edit.html', {'form': form, 'command': command})

@login_required
def dashboard(request):
    my_commands = Command.objects.filter(author=request.user)
    # Suggestions made by me
    my_suggestions = EditRequest.objects.filter(user=request.user)
    # Suggestions on my commands that are pending
    pending_reviews = EditRequest.objects.filter(original_command__author=request.user, status='PENDING')
    
    return render(request, 'commands/dashboard.html', {
        'my_commands': my_commands,
        'my_suggestions': my_suggestions,
        'pending_reviews': pending_reviews
    })

@login_required
def review_edit(request, pk):
    edit_request = get_object_or_404(EditRequest, pk=pk)
    # Only the author of the original command can review
    if request.user != edit_request.original_command.author:
        return redirect('command_list')
        
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            # Update the original command
            command = edit_request.original_command
            command.command_string = edit_request.suggested_command_string
            command.explanation = edit_request.suggested_explanation
            command.save()
            
            edit_request.status = 'APPROVED'
            edit_request.save()
        elif action == 'reject':
            edit_request.status = 'REJECTED'
            edit_request.save()
            
        return redirect('dashboard')
        
    return render(request, 'commands/review_edit.html', {'edit_request': edit_request})

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('command_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
