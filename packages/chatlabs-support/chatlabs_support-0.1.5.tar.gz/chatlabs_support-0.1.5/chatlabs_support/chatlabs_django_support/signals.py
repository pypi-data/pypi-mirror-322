from . import models
from .consumers import ChatConsumer
from asgiref.sync import async_to_sync


def post_save_ticket(sender, instance: models.Ticket, created: bool, **kwargs):  # noqa: ARG001
    if created:
        async_to_sync(ChatConsumer.get_channel_layer().group_send)(
            ChatConsumer.unassigned_tickets_group,
            {
                'type': 'ticket.created',
                'ticket': instance,
            },
        )


def post_save_message(
    sender,  # noqa: ARG001
    instance: models.Message,
    created: bool,
    **kwargs,  # noqa: ARG001
):
    if created:
        async_to_sync(ChatConsumer.get_channel_layer().group_send)(
            ChatConsumer.ticket_messages_group(instance.ticket.id),
            {
                'type': 'ticket.message.new',
                'message': instance,
            }
        )
