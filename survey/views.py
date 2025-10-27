from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from django.http import JsonResponse
from django.views.generic import ListView, CreateView
from datetime import timedelta
import json

from .models import (
    CanteenItem, CanteenSale, CanteenSaleItem,
    FeedbackSurvey, Announcement
)
from patients.models import Patient


# ========== CANTEEN VIEWS ==========

@login_required
def canteen_dashboard(request):
    """Canteen dashboard with today's statistics"""
    today = timezone.now().date()
    
    # Today's sales statistics
    today_sales = CanteenSale.objects.filter(sale_date__date=today)
    today_revenue = today_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    today_transactions = today_sales.count()
    
    # This week's sales
    week_start = today - timedelta(days=today.weekday())
    week_sales = CanteenSale.objects.filter(sale_date__date__gte=week_start)
    week_revenue = week_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # This month's sales
    month_start = today.replace(day=1)
    month_sales = CanteenSale.objects.filter(sale_date__date__gte=month_start)
    month_revenue = month_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Popular items today
    popular_items = CanteenSaleItem.objects.filter(
        sale__sale_date__date=today
    ).values(
        'item__name', 'item__category'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum('total_price')
    ).order_by('-total_quantity')[:5]
    
    # Available menu items count
    available_items = CanteenItem.objects.filter(is_available=True).count()
    
    # Chart data - Last 7 days revenue
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    daily_revenue = []
    daily_labels = []
    
    for day in last_7_days:
        day_sales = CanteenSale.objects.filter(sale_date__date=day)
        revenue = day_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        daily_revenue.append(float(revenue))
        daily_labels.append(day.strftime('%a'))
    
    # Category breakdown
    category_sales = CanteenSaleItem.objects.filter(
        sale__sale_date__date__gte=month_start
    ).values('item__category').annotate(
        total=Sum('total_price')
    ).order_by('-total')
    
    category_labels = [item['item__category'] for item in category_sales]
    category_data = [float(item['total']) for item in category_sales]
    
    context = {
        'today_revenue': today_revenue,
        'today_transactions': today_transactions,
        'week_revenue': week_revenue,
        'month_revenue': month_revenue,
        'popular_items': popular_items,
        'available_items': available_items,
        'daily_labels': json.dumps(daily_labels),
        'daily_revenue': json.dumps(daily_revenue),
        'category_labels': json.dumps(category_labels),
        'category_data': json.dumps(category_data),
        'today': today,
    }
    
    return render(request, 'accounts/canteen_dashboard.html', context)


@login_required
def canteen_menu(request):
    """Display canteen menu"""
    # Get all available items
    items = CanteenItem.objects.filter(is_available=True).order_by('category', 'name')
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        items = items.filter(category=category)
    
    # Search
    search = request.GET.get('search')
    if search:
        items = items.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Group by category
    categories = {}
    for item in items:
        if item.category not in categories:
            categories[item.category] = []
        categories[item.category].append(item)
    
    context = {
        'items': items,
        'categories': categories,
        'all_categories': CanteenItem.CATEGORY_CHOICES,
    }
    
    return render(request, 'survey/canteen_menu.html', context)


@login_required
def canteen_order_create(request):
    """Create new canteen order (AJAX)"""
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Create sale
        sale = CanteenSale.objects.create(
            customer_name=data.get('customer_name', ''),
            payment_method=data.get('payment_method', 'CASH'),
            served_by=request.user,
            notes=data.get('notes', '')
        )
        
        # Create sale items
        total_amount = 0
        items = data.get('items', [])
        
        for item_data in items:
            canteen_item = CanteenItem.objects.get(pk=item_data['item_id'])
            quantity = int(item_data['quantity'])
            
            sale_item = CanteenSaleItem.objects.create(
                sale=sale,
                item=canteen_item,
                quantity=quantity,
                unit_price=canteen_item.price,
                total_price=canteen_item.price * quantity
            )
            total_amount += sale_item.total_price
        
        # Update sale total
        sale.total_amount = total_amount
        sale.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Order placed successfully!',
            'sale_number': sale.sale_number,
            'total_amount': float(total_amount)
        })
    
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def canteen_order_list(request):
    """List canteen orders/sales"""
    # Get filter parameters
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    payment_method = request.GET.get('payment_method')
    
    sales = CanteenSale.objects.select_related('patient', 'served_by').prefetch_related('items')
    
    # Apply filters
    if date_from:
        sales = sales.filter(sale_date__date__gte=date_from)
    if date_to:
        sales = sales.filter(sale_date__date__lte=date_to)
    if payment_method:
        sales = sales.filter(payment_method=payment_method)
    
    sales = sales.order_by('-sale_date')[:100]
    
    # Calculate totals
    total_sales = sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_transactions = sales.count()
    
    context = {
        'sales': sales,
        'total_sales': total_sales,
        'total_transactions': total_transactions,
    }
    
    return render(request, 'survey/canteen_order_list.html', context)


@login_required
def canteen_item_detail(request, pk):
    """Get canteen item details (AJAX)"""
    item = get_object_or_404(CanteenItem, pk=pk)
    
    data = {
        'id': item.id,
        'name': item.name,
        'category': item.category,
        'price': float(item.price),
        'description': item.description,
        'is_available': item.is_available,
    }
    
    return JsonResponse(data)


# ========== FEEDBACK/SURVEY VIEWS ==========

class FeedbackListView(LoginRequiredMixin, ListView):
    """List all feedback surveys"""
    model = FeedbackSurvey
    template_name = 'survey/feedback_list.html'
    context_object_name = 'feedbacks'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = FeedbackSurvey.objects.select_related('patient')
        
        # Filter by rating
        min_rating = self.request.GET.get('min_rating')
        if min_rating:
            queryset = queryset.filter(overall_experience__gte=int(min_rating))
        
        # Filter by date
        date_from = self.request.GET.get('date_from')
        if date_from:
            queryset = queryset.filter(submitted_at__date__gte=date_from)
        
        return queryset.order_by('-submitted_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calculate statistics
        all_feedback = FeedbackSurvey.objects.all()
        context['total_feedback'] = all_feedback.count()
        context['average_overall'] = all_feedback.aggregate(
            Avg('overall_experience')
        )['overall_experience__avg'] or 0
        context['would_recommend_percent'] = (
            all_feedback.filter(would_recommend=True).count() / all_feedback.count() * 100
            if all_feedback.count() > 0 else 0
        )
        
        return context


@login_required
def feedback_create(request):
    """Create feedback survey"""
    if request.method == 'POST':
        # Get form data
        patient_id = request.POST.get('patient_id')
        patient = get_object_or_404(Patient, pk=patient_id) if patient_id else None
        
        # Create feedback
        feedback = FeedbackSurvey.objects.create(
            patient=patient,
            overall_experience=int(request.POST.get('overall_experience')),
            staff_behavior=int(request.POST.get('staff_behavior')),
            cleanliness=int(request.POST.get('cleanliness')),
            waiting_time=int(request.POST.get('waiting_time')),
            facility_quality=int(request.POST.get('facility_quality')),
            positive_feedback=request.POST.get('positive_feedback', ''),
            negative_feedback=request.POST.get('negative_feedback', ''),
            suggestions=request.POST.get('suggestions', ''),
            would_recommend=request.POST.get('would_recommend') == 'yes'
        )
        
        messages.success(request, 'Thank you for your feedback!')
        return redirect('survey:feedback_list')
    
    # GET request - show form
    patients = Patient.objects.filter(is_active=True).order_by('-created_at')[:50]
    
    context = {
        'patients': patients,
        'rating_choices': FeedbackSurvey.RATING_CHOICES,
    }
    
    return render(request, 'survey/feedback_form.html', context)


@login_required
def feedback_report(request):
    """Feedback analysis report"""
    feedbacks = FeedbackSurvey.objects.all()
    
    # Overall statistics
    total_feedback = feedbacks.count()
    
    if total_feedback > 0:
        avg_overall = feedbacks.aggregate(Avg('overall_experience'))['overall_experience__avg']
        avg_staff = feedbacks.aggregate(Avg('staff_behavior'))['staff_behavior__avg']
        avg_cleanliness = feedbacks.aggregate(Avg('cleanliness'))['cleanliness__avg']
        avg_waiting = feedbacks.aggregate(Avg('waiting_time'))['waiting_time__avg']
        avg_facility = feedbacks.aggregate(Avg('facility_quality'))['facility_quality__avg']
        
        recommend_count = feedbacks.filter(would_recommend=True).count()
        recommend_percent = (recommend_count / total_feedback) * 100
    else:
        avg_overall = avg_staff = avg_cleanliness = avg_waiting = avg_facility = 0
        recommend_percent = 0
    
    # Rating distribution
    rating_distribution = {i: feedbacks.filter(overall_experience=i).count() for i in range(1, 6)}
    
    # Chart data
    category_labels = ['Overall', 'Staff', 'Cleanliness', 'Waiting Time', 'Facility']
    category_averages = [avg_overall, avg_staff, avg_cleanliness, avg_waiting, avg_facility]
    
    context = {
        'total_feedback': total_feedback,
        'avg_overall': avg_overall,
        'avg_staff': avg_staff,
        'avg_cleanliness': avg_cleanliness,
        'avg_waiting': avg_waiting,
        'avg_facility': avg_facility,
        'recommend_percent': recommend_percent,
        'rating_distribution': rating_distribution,
        'category_labels': json.dumps(category_labels),
        'category_averages': json.dumps(category_averages),
    }
    
    return render(request, 'survey/feedback_report.html', context)


# ========== ANNOUNCEMENT VIEWS ==========

@login_required
def announcement_list(request):
    """List active announcements"""
    announcements = Announcement.objects.filter(
        is_active=True
    ).select_related('created_by').order_by('-priority', '-created_at')
    
    # Filter out expired announcements
    valid_announcements = [a for a in announcements if not a.is_expired]
    
    context = {
        'announcements': valid_announcements,
    }
    
    return render(request, 'survey/announcement_list.html', context)


# ========== SURVEY DASHBOARD ==========

@login_required
def survey_dashboard(request):
    """Survey module dashboard"""
    today = timezone.now().date()
    
    # Canteen stats
    today_canteen_sales = CanteenSale.objects.filter(sale_date__date=today)
    canteen_revenue = today_canteen_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Feedback stats
    total_feedback = FeedbackSurvey.objects.count()
    avg_rating = FeedbackSurvey.objects.aggregate(Avg('overall_experience'))['overall_experience__avg'] or 0
    
    # Recent feedback
    recent_feedback = FeedbackSurvey.objects.select_related('patient').order_by('-submitted_at')[:5]
    
    context = {
        'canteen_revenue': canteen_revenue,
        'canteen_transactions': today_canteen_sales.count(),
        'total_feedback': total_feedback,
        'avg_rating': avg_rating,
        'recent_feedback': recent_feedback,
    }
    
    return render(request, 'survey/survey_dashboard.html', context)

