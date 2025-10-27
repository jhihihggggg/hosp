import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

class QueueConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time queue updates"""
    
    async def connect(self):
        self.doctor_id = self.scope['url_route']['kwargs'].get('doctor_id', 'all')
        self.room_group_name = f'queue_{self.doctor_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send current queue status
        queue_data = await self.get_queue_data()
        await self.send(text_data=json.dumps({
            'type': 'queue_update',
            'queue': queue_data
        }))
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Receive message from WebSocket"""
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'call_next':
            # Call next patient
            appointment_id = data.get('appointment_id')
            await self.call_next_patient(appointment_id)
        
        elif message_type == 'refresh_queue':
            # Refresh queue data
            queue_data = await self.get_queue_data()
            await self.send(text_data=json.dumps({
                'type': 'queue_update',
                'queue': queue_data
            }))
    
    async def queue_update(self, event):
        """Receive queue update from room group"""
        await self.send(text_data=json.dumps({
            'type': 'queue_update',
            'queue': event['queue']
        }))
    
    async def patient_called(self, event):
        """Receive patient called event"""
        await self.send(text_data=json.dumps({
            'type': 'patient_called',
            'appointment': event['appointment'],
            'serial_number': event['serial_number'],
            'room_number': event['room_number']
        }))
    
    @database_sync_to_async
    def get_queue_data(self):
        """Get current queue data from database"""
        from appointments.models import Appointment
        from django.db.models import Q
        
        today = timezone.now().date()
        
        # Build query
        query = Q(appointment_date=today) & (
            Q(status='WAITING') | Q(status='CALLED') | Q(status='IN_PROGRESS')
        )
        
        if self.doctor_id != 'all':
            query &= Q(doctor_id=self.doctor_id)
        
        appointments = Appointment.objects.filter(query).select_related(
            'patient', 'doctor'
        ).order_by('serial_number')
        
        queue_list = []
        for apt in appointments:
            queue_list.append({
                'id': apt.id,
                'appointment_number': apt.appointment_number,
                'serial_number': apt.serial_number,
                'patient_name': apt.patient.get_full_name(),
                'patient_id': apt.patient.patient_id,
                'doctor_name': apt.doctor.get_full_name(),
                'status': apt.status,
                'check_in_time': apt.check_in_time.isoformat() if apt.check_in_time else None,
                'called_time': apt.called_time.isoformat() if apt.called_time else None,
                'room_number': apt.room_number,
            })
        
        return queue_list
    
    @database_sync_to_async
    def call_next_patient(self, appointment_id):
        """Call next patient and broadcast"""
        from appointments.models import Appointment
        
        try:
            appointment = Appointment.objects.select_related('patient', 'doctor').get(id=appointment_id)
            appointment.call_next()
            
            # Broadcast to all clients in this room
            return {
                'appointment_id': appointment.id,
                'appointment_number': appointment.appointment_number,
                'serial_number': appointment.serial_number,
                'patient_name': appointment.patient.get_full_name(),
                'room_number': appointment.room_number or 'Consultation Room',
            }
        except Appointment.DoesNotExist:
            return None


class DisplayMonitorConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for display monitors showing current patient"""
    
    async def connect(self):
        self.room_group_name = 'display_monitor'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        print(f"Display monitor connected: {self.channel_name}")
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"Display monitor disconnected: {self.channel_name}")
    
    async def patient_called(self, event):
        """Receive patient called event and display on monitor"""
        print(f"Broadcasting to display: {event}")
        await self.send(text_data=json.dumps({
            'type': 'patient_called',
            'patient_name': event.get('patient_name', ''),
            'queue_number': event.get('queue_number', ''),
            'serial_number': event.get('serial_number', ''),
            'doctor_name': event.get('doctor_name', ''),
            'room_number': event.get('room_number', 'Consultation Room'),
            'message': f"Patient {event.get('patient_name', '')} - Serial #{event.get('serial_number', '')}"
        }))
    
    async def queue_update(self, event):
        """Receive queue update notification"""
        await self.send(text_data=json.dumps({
            'type': 'queue_update',
            'message': 'Queue updated'
        }))
