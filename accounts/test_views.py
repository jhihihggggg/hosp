"""
Simple test views without authentication
"""
from django.shortcuts import render
from django.http import HttpResponse

def test_admin(request):
    """Test admin dashboard"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Dashboard - Test</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h1>✅ Admin Dashboard Working!</h1>
            <p class="lead">You can see the admin dashboard.</p>
            <hr>
            <h3>Quick Links:</h3>
            <a href="/test-doctor/" class="btn btn-success">Go to Doctor Dashboard</a>
            <a href="/test-reception/" class="btn btn-info">Go to Reception Dashboard</a>
            <a href="/test-display/" class="btn btn-warning">Go to Display Monitor</a>
            <a href="/accounts/admin-dashboard/" class="btn btn-primary mt-3">Go to Real Admin Dashboard</a>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

def test_doctor(request):
    """Test doctor dashboard"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Doctor Dashboard - Test</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h1>✅ Doctor Dashboard Working!</h1>
            <p class="lead">You can see the doctor dashboard.</p>
            <hr>
            <h3>Quick Links:</h3>
            <a href="/test-admin/" class="btn btn-primary">Go to Admin Dashboard</a>
            <a href="/test-reception/" class="btn btn-info">Go to Reception Dashboard</a>
            <a href="/test-display/" class="btn btn-warning">Go to Display Monitor</a>
            <a href="/accounts/doctor-dashboard/" class="btn btn-success mt-3">Go to Real Doctor Dashboard</a>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

def test_reception(request):
    """Test reception dashboard"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Reception Dashboard - Test</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h1>✅ Reception Dashboard Working!</h1>
            <p class="lead">You can see the reception dashboard.</p>
            <hr>
            <h3>Quick Links:</h3>
            <a href="/test-admin/" class="btn btn-primary">Go to Admin Dashboard</a>
            <a href="/test-doctor/" class="btn btn-success">Go to Doctor Dashboard</a>
            <a href="/test-display/" class="btn btn-warning">Go to Display Monitor</a>
            <a href="/accounts/receptionist-dashboard/" class="btn btn-info mt-3">Go to Real Reception Dashboard</a>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

def test_display(request):
    """Test display monitor"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Display Monitor - Test</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h1>✅ Display Monitor Working!</h1>
            <p class="lead">You can see the display monitor.</p>
            <hr>
            <h3>Quick Links:</h3>
            <a href="/test-admin/" class="btn btn-primary">Go to Admin Dashboard</a>
            <a href="/test-doctor/" class="btn btn-success">Go to Doctor Dashboard</a>
            <a href="/test-reception/" class="btn btn-info">Go to Reception Dashboard</a>
            <a href="/accounts/display-monitor/" class="btn btn-warning mt-3">Go to Real Display Monitor</a>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)
