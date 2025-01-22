from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import LimitOffsetPagination

from . import filters, models, serializers


class Support(LoginRequiredMixin, TemplateView):
    template_name = 'support/support_manager.html'

    def get_context_data(self, **kwargs):
        kwargs['my_tickets'] = serializers.Ticket(
            models.Ticket.objects.filter(
                support_manager=self.request.user,
            ),
            many=True,
        ).data
        kwargs['unassigned_tickets'] = serializers.Ticket(
            models.Ticket.objects.filter(
                support_manager__isnull=True,
            ),
            many=True,
        ).data
        return super().get_context_data(**kwargs)


class TicketList(ListCreateAPIView):
    queryset = models.Ticket.objects.all()
    serializer_class = serializers.Ticket
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = filters.Ticket


class Ticket(RetrieveUpdateAPIView):
    queryset = models.Ticket.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'ticket_id'
    serializer_class = serializers.Ticket


class MessageList(ListCreateAPIView):
    serializer_class = serializers.Message
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return models.Message.objects.filter(
            ticket__id=self.kwargs['ticket_id']
        ).order_by('-created_at')

    def perform_create(self, serializer: serializer_class):
        serializer.save(
            ticket=models.Ticket.objects.get(id=self.kwargs['ticket_id']),
        )
