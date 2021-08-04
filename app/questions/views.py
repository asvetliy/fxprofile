from django.views import View
from django.views.defaults import page_not_found
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from mailer import Mailer

from .models import QuestionRequest, QuestionMessage
from .forms import *


class TicketsURLDispatcher(LoginRequiredMixin, View):
    def post(self, request, ticket, action):
        if action == 'add_comment':
            if not request.user.questionrequest_set.filter(pk=ticket).exists():
                return page_not_found(request, None)
            form = CreateTicketForm(request.POST)
            if form.is_valid():
                ticket_text = form.cleaned_data.get('ticket_text', '')
                question_request = request.user.questionrequest_set.get(id=ticket)
                question_messages = QuestionMessage.objects.filter(request=question_request).order_by('created_at').last()
                if question_messages.user.id != request.user.id and question_request.status_id <= 2:
                    question = QuestionMessage.objects.create(
                        user=request.user,
                        request_id=ticket,
                        text=ticket_text,
                        status_id=1,
                    )
                    Mailer.send_managers('question_message_created', 'New question message created', {
                        'user': request.user,
                        'question': question,
                    })
                else:
                    messages.add_message(request, messages.ERROR, _('QUESTION_COMMENT_ADD_DISABLED'))
                    return redirect('question-ticket-action', ticket, 'view')
                return redirect('question-ticket-action', ticket, 'view')
            messages.add_message(request, messages.ERROR, _('QUESTION_COMMENT_ADD_FAIL'))
            if len(form.errors):
                for k, e in form.errors.items():
                    messages.add_message(request, messages.ERROR, e)
            return redirect('question-ticket-action', ticket, 'view')
        return page_not_found(request, None)

    def get(self, request, ticket, action):
        if action == 'view':
            if not request.user.questionrequest_set.filter(pk=ticket).exists():
                return page_not_found(request, None)
            question_request = request.user.questionrequest_set.get(id=ticket)
            question_messages = QuestionMessage.objects.filter(request=question_request).order_by('created_at')
            is_comment_available = False
            if question_messages.reverse()[0].user.id != request.user.id and question_request.status_id <= 2:
                is_comment_available = True
            context = {
                'title_category': _('QUESTION_TICKET_VIEW_TITLE') + ' ' + ticket,
                'nav_question_view': 'active',
                'nav_ask_question_collapsed': 'show',
                'nav_ask_question': 'active',
                'question_request': question_request,
                'question_messages': question_messages,
                'is_comment_available': is_comment_available,
                'form': CreateTicketForm(),
            }
            return render(request, 'questions/view-ticket.html', context=context)
        return page_not_found(request, None)


class CreateTicketView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.questionrequest_set.filter(Q(status=1) | Q(status=2)).exists():
            messages.add_message(request, messages.WARNING, _('QUESTION_TICKET_ALREADY_EXIST'))
            return redirect('question-tickets')
        context = {
            'nav_question_create': 'active',
            'nav_ask_question_collapsed': 'show',
            'nav_ask_question': 'active',
            'title_category': _('QUESTION_TICKET_CREATE_TITLE'),
            'form': CreateTicketForm(),
        }
        return render(request, 'questions/create-ticket.html', context=context)

    def post(self, request):
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            ticket_text = form.cleaned_data.get('ticket_text', '')
            question_request = QuestionRequest.objects.create(
                user=request.user,
                status_id=1,
            )
            question = QuestionMessage.objects.create(
                user=request.user,
                request=question_request,
                text=ticket_text,
                status_id=1,
            )
            Mailer.send_managers('question_request_created', 'New question request created', {
                'user': request.user,
                'question': question,
            })
            messages.add_message(request, messages.SUCCESS, _('QUESTION_TICKET_CREATE_SUCCESS'))
            return redirect('question-tickets')
        messages.add_message(request, messages.ERROR, _('QUESTION_TICKET_CREATE_FAIL'))
        if len(form.errors):
            for k, e in form.errors.items():
                messages.add_message(request, messages.ERROR, e)
        return redirect('question-ticket-create')


class TicketsView(LoginRequiredMixin, View):
    def get(self, request):
        questions = QuestionRequest.objects.filter(user=request.user)
        context = {
            'title_category': _('QUESTION_TICKETS_VIEW_TITLE'),
            'nav_question_view': 'active',
            'nav_ask_question_collapsed': 'show',
            'nav_ask_question': 'active',
            'questions': questions,
            'colors': ['table-info', 'table-primary', 'table-success', 'table-warning'],
        }
        return render(request, 'questions/tickets.html', context=context)
