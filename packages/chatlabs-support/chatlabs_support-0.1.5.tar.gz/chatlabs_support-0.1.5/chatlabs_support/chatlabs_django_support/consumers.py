from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import BaseChannelLayer, get_channel_layer
from django.contrib.auth.models import User

from . import models, serializers


class BaseChatConsumer(AsyncJsonWebsocketConsumer):
    unassigned_tickets_group = 'unassigned_tickets'

    @staticmethod
    def ticket_messages_group(ticket_id: int) -> str:
        return f'ticket_{ticket_id}_messages'

    @classmethod
    def get_channel_layer(cls) -> BaseChannelLayer:
        return get_channel_layer(cls.channel_layer_alias)

    @property
    def _channel_layer(self) -> BaseChannelLayer:
        return self.channel_layer

    async def connect(self):
        self.manager: User = self.scope['user']
        await self._channel_layer.group_add(
            self.unassigned_tickets_group,
            self.channel_name,
        )
        async for ticket in models.Ticket.objects.filter(
            support_manager=self.manager
        ):
            await self._channel_layer.group_add(
                self.ticket_messages_group(ticket.id),
                self.channel_name,
            )
        await self.accept()

    async def disconnect(self, code):  # noqa: ARG002
        await self._channel_layer.group_discard(
            self.unassigned_tickets_group,
            self.channel_name,
        )
        async for ticket in models.Ticket.objects.filter(
            support_manager=self.manager
        ):
            await self._channel_layer.group_discard(
                self.ticket_messages_group(ticket.id),
                self.channel_name,
            )


class ChatConsumerSerializerMixin:
    def serialize_message(self, message: models.Message) -> dict:
        return serializers.Message(message).data

    def serialize_messages(self, ticket_id: int) -> list[dict]:
        return serializers.Message(
            models.Message.objects.filter(
                ticket__id=ticket_id,
            ).order_by('-created_at'),
            many=True,
        ).data


class ChatConsumerSender(ChatConsumerSerializerMixin, BaseChatConsumer):
    async def ticket_created(self, event: dict):
        event['ticket'] = serializers.Ticket(event['ticket']).data
        await self.send_json(event)

    async def ticket_assigned(self, event: dict):
        await self.send_json(event)

    async def ticket_message_viewed(self, event: dict):
        event['message'] = await sync_to_async(self.serialize_message)(
            event['message']
        )
        await self.send_json(event)

    async def ticket_message_new(self, event: dict):
        event['message'] = await sync_to_async(self.serialize_message)(
            event['message']
        )
        await self.send_json(event)

    async def ticket_message_list(self, event: dict):
        event['messages'] = await sync_to_async(self.serialize_messages)(
            event['ticket_id']
        )
        await self.send_json(event)


class ChatConsumerReceiver(BaseChatConsumer):
    async def _receive_ticket_assign(self, *, ticket_id: int):
        ticket = await models.Ticket.objects.aget(
            id=ticket_id,
        )
        ticket.support_manager = self.manager
        await ticket.asave()
        await self._channel_layer.group_add(
            self.ticket_messages_group(ticket.id),
            self.channel_name,
        )
        return (
            self.unassigned_tickets_group,
            {
                'type': 'ticket.assigned',
                'id': ticket.id,
                'support_manager': self.manager.pk,
            }
        )

    async def _receive_ticket_message_viewed(
        self,
        *,
        ticket_id: int,
        message_id: int,
    ):
        message = await models.Message.objects.aget(
            ticket__id=ticket_id,
            id=message_id,
        )
        message.viewed = True
        await message.asave()
        return (
            self.ticket_messages_group(ticket_id),
            {
                'type': 'ticket.message.viewed',
                'message': message,
            }
        )

    async def _receive_ticket_message_new(self, *, ticket_id: int, text: str):
        ticket=await models.Ticket.objects.aget(
            id=ticket_id,
        )
        message = await models.Message.objects.acreate(
            ticket=ticket,
            sender=models.Message.Sender.SUPPORT_MANAGER,
            text=text,
            viewed=True,
        )
        return (
            self.ticket_messages_group(ticket.id),
            {
                'type': 'ticket.message.new',
                'message': message,
            }
        )

    async def _receive_ticket_message_list(self, *, ticket_id: int):
        return (
            self.ticket_messages_group(ticket_id),
            {
                'type': 'ticket.message.list',
                'ticket_id': ticket_id,
            }
        )


class ChatConsumer(ChatConsumerReceiver, ChatConsumerSender):
    async def get_group_and_message(self, content: dict) -> tuple[str, dict]:
        match content['type']:
            case 'ticket.assign':
                return await self._receive_ticket_assign(
                    ticket_id=content['id'],
                )
            case 'ticket.message.viewed':
                return await self._receive_ticket_message_viewed(
                    ticket_id=content['ticket_id'],
                    message_id=content['message_id'],
                )
            case 'ticket.message.new':
                return await self._receive_ticket_message_new(
                    ticket_id=content['ticket_id'],
                    text=content['text'],
                )
            case 'ticket.message.list':
                return await self._receive_ticket_message_list(
                    ticket_id=content['ticket_id'],
                )
            case _:
                return None, None

    async def receive_json(self, content: dict, **_):
        try:
            group, message = await self.get_group_and_message(content)
        except KeyError:
            group, message = None, None
        if all([group, message]):
            await self._channel_layer.group_send(
                group,
                message,
            )
