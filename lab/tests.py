"""
Comprehensive tests for Lab module views and endpoints
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from .models import LabTest, LabOrder, LabResult
from patients.models import Patient

User = get_user_model()


class LabViewsTestCase(TestCase):
    """Test lab views and endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='labtech',
            password='testpass123',
            email='lab@test.com'
        )
        
        # Create test patient
        self.patient = Patient.objects.create(
            patient_id='P001',
            first_name='John',
            last_name='Doe',
            date_of_birth='1990-01-01',
            gender='MALE',
            phone='1234567890',
            email='john@test.com'
        )
        
        # Create test lab test
        self.lab_test = LabTest.objects.create(
            test_code='CBC001',
            test_name='Complete Blood Count',
            category='HEMATOLOGY',
            price=500.00,
            turnaround_time=24,
            sample_type='Blood',
            is_active=True
        )
        
        # Create test lab order
        self.lab_order = LabOrder.objects.create(
            patient=self.patient,
            ordered_by=self.user,
            status='ORDERED',
            priority=False,
            total_amount=500.00
        )
        self.lab_order.tests.add(self.lab_test)
        
        # Login
        self.client.login(username='labtech', password='testpass123')
    
    def test_lab_dashboard_view(self):
        """Test lab dashboard loads"""
        response = self.client.get(reverse('lab:lab_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('pending_orders', response.context)
        self.assertIn('in_progress', response.context)
    
    def test_lab_order_list_view(self):
        """Test lab order list view"""
        response = self.client.get(reverse('lab:order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('order_list', response.context)
        self.assertEqual(len(response.context['order_list']), 1)
    
    def test_lab_order_detail_view(self):
        """Test lab order detail view"""
        response = self.client.get(
            reverse('lab:order_detail', kwargs={'pk': self.lab_order.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['order'], self.lab_order)
    
    def test_collect_sample_endpoint(self):
        """Test sample collection endpoint"""
        response = self.client.post(
            reverse('lab:collect_sample', kwargs={'pk': self.lab_order.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success'})
        
        # Verify order status updated
        self.lab_order.refresh_from_db()
        self.assertEqual(self.lab_order.status, 'SAMPLE_COLLECTED')
        self.assertIsNotNone(self.lab_order.sample_collected_at)
    
    def test_start_testing_endpoint(self):
        """Test start testing endpoint"""
        # First collect sample
        self.lab_order.status = 'SAMPLE_COLLECTED'
        self.lab_order.save()
        
        response = self.client.post(
            reverse('lab:start_testing', kwargs={'pk': self.lab_order.pk})
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify status updated
        self.lab_order.refresh_from_db()
        self.assertEqual(self.lab_order.status, 'IN_PROGRESS')
    
    def test_cancel_order_endpoint(self):
        """Test cancel order endpoint"""
        import json
        
        response = self.client.post(
            reverse('lab:cancel_order', kwargs={'pk': self.lab_order.pk}),
            data=json.dumps({'reason': 'Patient request'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify status updated
        self.lab_order.refresh_from_db()
        self.assertEqual(self.lab_order.status, 'CANCELLED')
    
    def test_enter_results_view_get(self):
        """Test result entry form loads"""
        response = self.client.get(
            reverse('lab:result_entry', kwargs={'pk': self.lab_order.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('order', response.context)
        self.assertIn('tests', response.context)
    
    def test_verify_result_endpoint(self):
        """Test result verification endpoint"""
        # Create a result first
        result = LabResult.objects.create(
            order=self.lab_order,
            test=self.lab_test,
            performed_by=self.user,
            result_data={'value': '150', 'unit': 'g/L'},
            is_verified=False
        )
        
        response = self.client.post(
            reverse('lab:verify_result', kwargs={'pk': self.lab_order.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success'})
        
        # Verify result is marked as verified
        result.refresh_from_db()
        self.assertTrue(result.is_verified)
    
    def test_view_report_not_complete(self):
        """Test viewing report when not complete shows warning"""
        response = self.client.get(
            reverse('lab:report_view', kwargs={'pk': self.lab_order.pk})
        )
        # Should redirect with warning
        self.assertEqual(response.status_code, 302)
    
    def test_view_report_complete(self):
        """Test viewing completed report"""
        # Mark order as complete
        self.lab_order.status = 'COMPLETED'
        self.lab_order.save()
        
        response = self.client.get(
            reverse('lab:report_view', kwargs={'pk': self.lab_order.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('order', response.context)
    
    def test_print_report_view(self):
        """Test print report view"""
        self.lab_order.status = 'COMPLETED'
        self.lab_order.save()
        
        response = self.client.get(
            reverse('lab:report_print', kwargs={'pk': self.lab_order.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('order', response.context)
    
    def test_sample_collection_view(self):
        """Test sample collection interface"""
        response = self.client.get(reverse('lab:sample_collection'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('pending_orders', response.context)
    
    def test_quality_control_view(self):
        """Test QC dashboard"""
        response = self.client.get(reverse('lab:quality_control'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('qc_runs_7d', response.context)
    
    def test_unauthorized_access(self):
        """Test that unauthorized users cannot access views"""
        self.client.logout()
        
        response = self.client.get(reverse('lab:lab_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_order_filtering(self):
        """Test order list filtering by status"""
        # Create additional orders with different statuses
        LabOrder.objects.create(
            patient=self.patient,
            ordered_by=self.user,
            status='COMPLETED',
            total_amount=300.00
        )
        
        response = self.client.get(reverse('lab:order_list') + '?status=COMPLETED')
        self.assertEqual(response.status_code, 200)
        orders = response.context['order_list']
        for order in orders:
            self.assertEqual(order.status, 'COMPLETED')


class LabOrderWorkflowTestCase(TestCase):
    """Test complete lab order workflow"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='labtech',
            password='testpass123'
        )
        self.patient = Patient.objects.create(
            patient_id='P001',
            first_name='Jane',
            last_name='Smith',
            date_of_birth='1985-05-15',
            gender='FEMALE',
            phone='9876543210',
            email='jane@test.com'
        )
        self.lab_test = LabTest.objects.create(
            test_code='LFT001',
            test_name='Liver Function Test',
            category='BIOCHEMISTRY',
            price=800.00,
            is_active=True
        )
        self.client.login(username='labtech', password='testpass123')
    
    def test_complete_order_workflow(self):
        """Test complete workflow from order to report"""
        # 1. Create order
        order = LabOrder.objects.create(
            patient=self.patient,
            ordered_by=self.user,
            status='ORDERED',
            total_amount=800.00
        )
        order.tests.add(self.lab_test)
        
        # 2. Collect sample
        response = self.client.post(
            reverse('lab:collect_sample', kwargs={'pk': order.pk})
        )
        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.status, 'SAMPLE_COLLECTED')
        
        # 3. Start testing
        response = self.client.post(
            reverse('lab:start_testing', kwargs={'pk': order.pk})
        )
        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.status, 'IN_PROGRESS')
        
        # 4. Enter results (mark as completed)
        response = self.client.post(
            reverse('lab:result_entry', kwargs={'pk': order.pk})
        )
        order.refresh_from_db()
        self.assertEqual(order.status, 'COMPLETED')
        
        # 5. View report
        response = self.client.get(
            reverse('lab:report_view', kwargs={'pk': order.pk})
        )
        self.assertEqual(response.status_code, 200)

