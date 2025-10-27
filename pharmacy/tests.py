"""
Comprehensive tests for Pharmacy module views and endpoints
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
import json

from .models import Drug, DrugCategory, PharmacySale, SaleItem, StockAdjustment
from patients.models import Patient

User = get_user_model()


class PharmacyViewsTestCase(TestCase):
    """Test pharmacy views and endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='pharmacist',
            password='testpass123',
            email='pharma@test.com'
        )
        
        # Create drug category
        self.category = DrugCategory.objects.create(
            name='Antibiotics',
            description='Antibiotic medicines'
        )
        
        # Create test drug
        self.drug = Drug.objects.create(
            drug_code='DRG001',
            generic_name='Amoxicillin',
            brand_name='Amoxil',
            category=self.category,
            form='CAPSULE',
            strength='500mg',
            manufacturer='Pharma Inc',
            quantity_in_stock=100,
            reorder_level=20,
            unit_price=Decimal('5.00'),
            selling_price=Decimal('8.00'),
            is_active=True
        )
        
        # Login
        self.client.login(username='pharmacist', password='testpass123')
    
    def test_pharmacy_dashboard_view(self):
        """Test pharmacy dashboard loads"""
        response = self.client.get(reverse('pharmacy:pharmacy_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_drugs', response.context)
    
    def test_drug_list_view(self):
        """Test drug list view"""
        response = self.client.get(reverse('pharmacy:drug_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('drugs', response.context)
        self.assertTrue(len(response.context['drugs']) >= 1)
    
    def test_drug_create_view_get(self):
        """Test drug create form loads"""
        response = self.client.get(reverse('pharmacy:drug_create'))
        self.assertEqual(response.status_code, 200)
    
    def test_drug_create_view_post(self):
        """Test drug creation"""
        data = {
            'drug_code': 'DRG002',
            'generic_name': 'Paracetamol',
            'brand_name': 'Panadol',
            'category': self.category.id,
            'form': 'TABLET',
            'strength': '500mg',
            'manufacturer': 'GSK',
            'quantity_in_stock': 200,
            'reorder_level': 50,
            'unit_price': '2.00',
            'selling_price': '3.50',
        }
        response = self.client.post(reverse('pharmacy:drug_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Drug.objects.filter(drug_code='DRG002').exists())
    
    def test_drug_detail_ajax(self):
        """Test drug detail AJAX endpoint"""
        response = self.client.get(
            reverse('pharmacy:drug_detail', kwargs={'pk': self.drug.pk})
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['name'], 'Amoxil')
        self.assertEqual(data['quantity'], 100)
    
    def test_drug_update_view(self):
        """Test drug update"""
        data = {
            'drug_code': 'DRG001',
            'generic_name': 'Amoxicillin',
            'brand_name': 'Amoxil Updated',
            'category': self.category.id,
            'form': 'CAPSULE',
            'strength': '500mg',
            'manufacturer': 'Pharma Inc',
            'quantity_in_stock': 150,
            'reorder_level': 20,
            'unit_price': '5.00',
            'selling_price': '8.50',
        }
        response = self.client.post(
            reverse('pharmacy:drug_update', kwargs={'pk': self.drug.pk}),
            data
        )
        self.assertEqual(response.status_code, 302)
        self.drug.refresh_from_db()
        self.assertEqual(self.drug.brand_name, 'Amoxil Updated')
    
    def test_drug_adjust_stock_endpoint(self):
        """Test stock adjustment AJAX endpoint"""
        data = {
            'adjust_type': 'add',
            'quantity': 50,
            'reason': 'New stock received'
        }
        response = self.client.post(
            reverse('pharmacy:drug_adjust_stock', kwargs={'pk': self.drug.pk}),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['new_quantity'], 150)
    
    def test_stock_report_view(self):
        """Test stock report view"""
        response = self.client.get(reverse('pharmacy:stock_report'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('drugs', response.context)
        self.assertIn('total_drugs', response.context)
    
    def test_stock_report_filtering(self):
        """Test stock report filtering by category"""
        response = self.client.get(
            reverse('pharmacy:stock_report') + f'?category={self.category.name}'
        )
        self.assertEqual(response.status_code, 200)
        drugs = response.context['drugs']
        for drug in drugs:
            self.assertEqual(drug.category, self.category)
    
    def test_stock_adjust_form_view(self):
        """Test stock adjustment form"""
        response = self.client.get(reverse('pharmacy:stock_adjust'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('drugs', response.context)
    
    def test_stock_adjust_post(self):
        """Test stock adjustment submission"""
        data = {
            'drug_id': self.drug.id,
            'adjust_type': 'PURCHASE',
            'quantity': 100,
            'reason': 'New purchase order'
        }
        response = self.client.post(reverse('pharmacy:stock_adjust'), data)
        self.assertEqual(response.status_code, 302)
        
        # Verify adjustment created and stock updated
        self.drug.refresh_from_db()
        self.assertEqual(self.drug.quantity_in_stock, 200)
        self.assertTrue(StockAdjustment.objects.filter(drug=self.drug).exists())
    
    def test_stock_adjust_history_view(self):
        """Test stock adjustment history view"""
        # Create adjustment
        StockAdjustment.objects.create(
            drug=self.drug,
            adjustment_type='PURCHASE',
            quantity=50,
            reason='Test adjustment',
            adjusted_by=self.user
        )
        
        response = self.client.get(reverse('pharmacy:stock_adjust_history'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('adjustments', response.context)
        self.assertTrue(len(response.context['adjustments']) >= 1)
    
    def test_quick_adjust_modal_endpoint(self):
        """Test quick adjust modal AJAX endpoint"""
        data = {
            'adjust_type': 'CORRECTION',
            'quantity': 10,
            'reason': 'Quick correction'
        }
        response = self.client.post(
            reverse('pharmacy:quick_adjust', kwargs={'pk': self.drug.pk}),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertEqual(result['status'], 'success')
    
    def test_prescription_list_view(self):
        """Test prescription list view"""
        response = self.client.get(reverse('pharmacy:prescription_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('prescriptions', response.context)
    
    def test_prescription_process_view(self):
        """Test prescription processing view"""
        # This requires Prescription model setup
        # Skip if prescription doesn't exist yet
        try:
            from appointments.models import Prescription
            # Test implementation when prescription model is available
        except:
            self.skipTest("Prescription model not available")
    
    def test_supplier_list_view(self):
        """Test supplier list view"""
        response = self.client.get(reverse('pharmacy:supplier_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('suppliers', response.context)
    
    def test_unauthorized_access(self):
        """Test that unauthorized users cannot access views"""
        self.client.logout()
        
        response = self.client.get(reverse('pharmacy:pharmacy_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_low_stock_detection(self):
        """Test low stock property"""
        self.drug.quantity_in_stock = 15
        self.drug.save()
        
        self.assertTrue(self.drug.is_low_stock)
        
        self.drug.quantity_in_stock = 30
        self.drug.save()
        self.assertFalse(self.drug.is_low_stock)


class PharmacyInventoryTestCase(TestCase):
    """Test pharmacy inventory management"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='pharmacist',
            password='testpass123'
        )
        self.category = DrugCategory.objects.create(name='Test Category')
        self.drug = Drug.objects.create(
            drug_code='TEST001',
            generic_name='Test Generic',
            brand_name='Test Brand',
            category=self.category,
            form='TABLET',
            strength='100mg',
            manufacturer='Test Pharma',
            quantity_in_stock=50,
            reorder_level=10,
            unit_price=Decimal('10.00'),
            selling_price=Decimal('15.00'),
            is_active=True
        )
        self.client.login(username='pharmacist', password='testpass123')
    
    def test_stock_depletion_workflow(self):
        """Test complete stock depletion and replenishment"""
        initial_stock = self.drug.quantity_in_stock
        
        # 1. Reduce stock (simulate sale)
        data = {
            'adjust_type': 'reduce',
            'quantity': 30,
            'reason': 'Sale'
        }
        response = self.client.post(
            reverse('pharmacy:drug_adjust_stock', kwargs={'pk': self.drug.pk}),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.drug.refresh_from_db()
        self.assertEqual(self.drug.quantity_in_stock, 20)
        
        # 2. Check if low stock
        self.assertTrue(self.drug.is_low_stock)
        
        # 3. Replenish stock
        adjustment_data = {
            'drug_id': self.drug.id,
            'adjust_type': 'PURCHASE',
            'quantity': 100,
            'reason': 'Replenishment order'
        }
        response = self.client.post(
            reverse('pharmacy:stock_adjust'),
            adjustment_data
        )
        self.drug.refresh_from_db()
        self.assertEqual(self.drug.quantity_in_stock, 120)
        self.assertFalse(self.drug.is_low_stock)
    
    def test_expired_drug_removal(self):
        """Test removing expired drugs"""
        # Set expired date
        self.drug.expiry_date = timezone.now().date() - timezone.timedelta(days=30)
        self.drug.save()
        
        self.assertTrue(self.drug.is_expired)
        
        # Remove expired stock
        data = {
            'drug_id': self.drug.id,
            'adjust_type': 'EXPIRED',
            'quantity': self.drug.quantity_in_stock,
            'reason': 'Expired items removal'
        }
        response = self.client.post(reverse('pharmacy:stock_adjust'), data)
        self.drug.refresh_from_db()
        self.assertEqual(self.drug.quantity_in_stock, 0)

