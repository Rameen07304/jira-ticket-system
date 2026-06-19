from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import CustomUser
from .models import tickets
from .forms import TicketForm
from django.db.models import Q
from account.views import register
from django.contrib import messages
from .signals import *

@login_required
@login_required
def home_view(request):
    if request.user.is_superuser:
        user_tickets_dict = {}
        for user in User.objects.all():
            user_tickets_dict[user.username] = {
                'To Do': list(tickets.objects.filter(user=user, status='To Do')),
                'In Progress': list(tickets.objects.filter(user=user, status='In Progress')),
                'Done': list(tickets.objects.filter(user=user, status='Done')),
            }

        all_tickets = tickets.objects.all()
        stats = {
            'total': all_tickets.count(),
            'todo': all_tickets.filter(status='To Do').count(),
            'in_progress': all_tickets.filter(status='In Progress').count(),
            'done': all_tickets.filter(status='Done').count(),
        }

        context = {
            'user_tickets_dict': user_tickets_dict,
            'is_admin': True,
            'stats': stats,
        }
    else:
        ticket_groups = {
            'To Do': tickets.objects.filter(user=request.user, status='To Do'),
            'In Progress': tickets.objects.filter(user=request.user, status='In Progress'),
            'Done': tickets.objects.filter(user=request.user, status='Done'),
        }

        user_tickets = tickets.objects.filter(user=request.user)
        stats = {
            'total': user_tickets.count(),
            'todo': user_tickets.filter(status='To Do').count(),
            'in_progress': user_tickets.filter(status='In Progress').count(),
            'done': user_tickets.filter(status='Done').count(),
        }

        context = {
            'ticket_groups': ticket_groups,
            'is_admin': False,
            'stats': stats,
        }
    return render(request, 'homepage.html', context)
@login_required
def home(request):
    query = request.GET.get('search', '')
    custom_users = CustomUser.objects.select_related('user').all()

    if query:
        custom_users = custom_users.filter(
            Q(user__first_name__icontains=query) | 
            Q(user__last_name__icontains=query)
        )

    paginator = Paginator(custom_users, 5)  # 5 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'page_obj': page_obj, 'query': query})
@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(tickets, id=ticket_id)
    if not (request.user == ticket.user or request.user.is_superuser):
        messages.error(request, 'Unauthorized deletion.')
        return redirect('ticket_list')

    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Ticket deleted.')
    
    return redirect('user_ticket_list' if request.user.is_superuser else 'ticket_list')
@login_required
def update_ticket_status(request, ticket_id):
    ticket = get_object_or_404(tickets, id=ticket_id)
    if not (request.user == ticket.user or request.user.is_superuser):
        messages.error(request, 'Unauthorized access.')
        return redirect('ticket_list')

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket.status = form.cleaned_data['status']
            ticket.save()
            messages.success(request, 'Status updated.')
    return redirect('user_ticket_list' if request.user.is_superuser else 'ticket_list')

@login_required
def update_ticket_priority(request, ticket_id):
    ticket = get_object_or_404(tickets, id=ticket_id)
    if not (request.user == ticket.user or request.user.is_superuser):
        messages.error(request, 'Unauthorized access.')
        return redirect('ticket_list')

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket.priority = form.cleaned_data['priority']
            ticket.save()
            messages.success(request, 'Priority updated.')

        next_url = request.POST.get('next')
        if next_url:
            return redirect(next_url)

    return redirect('user_ticket_list' if request.user.is_superuser else 'ticket_list')

@login_required
def user_ticket_list(request):
    if not request.user.is_superuser:
        return redirect('ticket_list')  
    username_filter = request.GET.get('username', '')
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')

    tickets_qs = tickets.objects.select_related('user').all()
    if username_filter:
        tickets_qs = tickets_qs.filter(user__username=username_filter)
    if status_filter:
        tickets_qs = tickets_qs.filter(status=status_filter)
    if priority_filter:
        tickets_qs = tickets_qs.filter(priority=priority_filter)
    form = TicketForm()
    if request.method == 'POST' and 'add_ticket' in request.POST:
        form = TicketForm(request.POST)
        username = request.POST.get('username')
        subject = request.POST.get('subject', '')
        description = request.POST.get('description', '')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, f"User '{username}' does not exist.")
        else:
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.user = user
                ticket.subject = subject
                ticket.description = description
                ticket.due_date = form.cleaned_data.get('due_date')
                ticket.save()
                messages.success(request, f"Ticket created for user '{user.username}'.")
                return redirect('user_ticket_list')
    context = {
        'tickets': tickets_qs,
        'form': form,
        'username_filter': username_filter,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'users': User.objects.all(),
    }

    return render(request, 'user_ticket_list.html', context)

@login_required
def ticket_list(request):
    user_tickets = tickets.objects.filter(user=request.user)
    if request.method == 'POST' and 'add_ticket' in request.POST:
        form = TicketForm(request.POST)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.subject = request.POST.get('subject', 'No Subject')
            new_ticket.description = request.POST.get('description', '')
            new_ticket.due_date = form.cleaned_data.get('due_date')  # ← add this
            new_ticket.save()
            messages.success(request, 'Ticket created successfully!')
            return redirect('ticket_list')
    else:
        form = TicketForm()
        
    return render(request, 'ticket_list.html', {
        'tickets': user_tickets,
        'form': form,
        'is_admin': request.user.is_superuser,
    })