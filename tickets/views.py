from django.views import View
from django.shortcuts import render
from .utils import *


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/welcome.html')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html')


class GetTicketView(View):
    line = LineOfCars()

    def get(self, request, *args, **kwargs):
        if kwargs and kwargs['service'] in SERVICES_PROVIDED:
            t = Ticket(kwargs['service'])
            self.line.add_ticket_to_line(t)
            return render(request, 'tickets/ticket.html', context={
                'ticket': t
            })
        return render(request, 'tickets/menu.html')


class ProcessingView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/processing.html', context={
            'que': GetTicketView.line.current_line
        })

    def post(self, request, *args, **kwargs):
        GetTicketView.line.pop_first_ticket_from_que()
        return render(request, 'tickets/processing.html', context={
            'que': GetTicketView.line.current_line
        })


class NextView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/next_ticket.html', context={
            'ticket': GetTicketView.line.get_current_ticket()
        })
