"""
Test views with complete standalone HTML - NO dependencies
"""
from django.http import HttpResponse

def test_admin(request):
    """Admin dashboard with full UI"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Dashboard - Nazipuruhs Hospital</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
        <style>
            body { background: #f8f9fa; }
            .stat-card { border-left: 4px solid; }
            .stat-card.primary { border-left-color: #0d6efd; }
            .stat-card.success { border-left-color: #198754; }
            .stat-card.warning { border-left-color: #ffc107; }
            .stat-card.danger { border-left-color: #dc3545; }
            .sidebar { min-height: 100vh; background: #343a40; color: white; }
            .sidebar a { color: #adb5bd; text-decoration: none; }
            .sidebar a:hover { color: white; }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row">
                <!-- Sidebar -->
                <div class="col-md-2 sidebar p-3">
                    <h4 class="text-white mb-4"><i class="bi bi-hospital"></i> Nazipuruhs</h4>
                    <nav class="nav flex-column">
                        <a class="nav-link active" href="/test-admin/"><i class="bi bi-speedometer2"></i> Dashboard</a>
                        <a class="nav-link" href="/test-doctor/"><i class="bi bi-person-heart"></i> Doctors</a>
                        <a class="nav-link" href="/test-reception/"><i class="bi bi-person-badge"></i> Reception</a>
                        <a class="nav-link" href="/test-display/"><i class="bi bi-tv"></i> Display Monitor</a>
                    </nav>
                </div>
                
                <!-- Main Content -->
                <div class="col-md-10 p-4">
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <h2><i class="bi bi-speedometer2"></i> Admin Dashboard</h2>
                        <div>
                            <span class="badge bg-success"><i class="bi bi-circle-fill"></i> Online</span>
                        </div>
                    </div>
                    
                    <!-- Stats Cards -->
                    <div class="row mb-4">
                        <div class="col-md-3 mb-3">
                            <div class="card stat-card primary">
                                <div class="card-body">
                                    <h6 class="text-muted">Total Income</h6>
                                    <h3 class="mb-0">৳ 125,000</h3>
                                    <small class="text-success"><i class="bi bi-arrow-up"></i> +15% from yesterday</small>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3">
                            <div class="card stat-card success">
                                <div class="card-body">
                                    <h6 class="text-muted">Total Profit</h6>
                                    <h3 class="mb-0">৳ 80,000</h3>
                                    <small class="text-success"><i class="bi bi-arrow-up"></i> 64% margin</small>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3">
                            <div class="card stat-card warning">
                                <div class="card-body">
                                    <h6 class="text-muted">Appointments</h6>
                                    <h3 class="mb-0">28</h3>
                                    <small class="text-info">24 completed today</small>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 mb-3">
                            <div class="card stat-card danger">
                                <div class="card-body">
                                    <h6 class="text-muted">Total Patients</h6>
                                    <h3 class="mb-0">450</h3>
                                    <small class="text-success"><i class="bi bi-person-plus"></i> 12 new today</small>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Department Revenue -->
                    <div class="row mb-4">
                        <div class="col-md-6">
                            <div class="card">
                                <div class="card-header bg-primary text-white">
                                    <h5 class="mb-0"><i class="bi bi-graph-up"></i> Department Revenue</h5>
                                </div>
                                <div class="card-body">
                                    <div class="mb-3">
                                        <div class="d-flex justify-content-between mb-1">
                                            <span><i class="bi bi-heart-pulse"></i> Lab Services</span>
                                            <strong>৳ 45,000</strong>
                                        </div>
                                        <div class="progress">
                                            <div class="progress-bar bg-success" style="width: 36%"></div>
                                        </div>
                                    </div>
                                    <div class="mb-3">
                                        <div class="d-flex justify-content-between mb-1">
                                            <span><i class="bi bi-calendar-check"></i> Appointments</span>
                                            <strong>৳ 35,000</strong>
                                        </div>
                                        <div class="progress">
                                            <div class="progress-bar bg-primary" style="width: 28%"></div>
                                        </div>
                                    </div>
                                    <div class="mb-3">
                                        <div class="d-flex justify-content-between mb-1">
                                            <span><i class="bi bi-capsule"></i> Pharmacy</span>
                                            <strong>৳ 30,000</strong>
                                        </div>
                                        <div class="progress">
                                            <div class="progress-bar bg-warning" style="width: 24%"></div>
                                        </div>
                                    </div>
                                    <div>
                                        <div class="d-flex justify-content-between mb-1">
                                            <span><i class="bi bi-cup-hot"></i> Canteen</span>
                                            <strong>৳ 15,000</strong>
                                        </div>
                                        <div class="progress">
                                            <div class="progress-bar bg-info" style="width: 12%"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-6">
                            <div class="card">
                                <div class="card-header bg-success text-white">
                                    <h5 class="mb-0"><i class="bi bi-people"></i> Staff Overview</h5>
                                </div>
                                <div class="card-body">
                                    <div class="row text-center">
                                        <div class="col-4">
                                            <div class="p-3 bg-light rounded">
                                                <h3 class="text-primary">8</h3>
                                                <small>Doctors</small>
                                            </div>
                                        </div>
                                        <div class="col-4">
                                            <div class="p-3 bg-light rounded">
                                                <h3 class="text-success">12</h3>
                                                <small>Nurses</small>
                                            </div>
                                        </div>
                                        <div class="col-4">
                                            <div class="p-3 bg-light rounded">
                                                <h3 class="text-info">15</h3>
                                                <small>Other Staff</small>
                                            </div>
                                        </div>
                                    </div>
                                    <hr>
                                    <div class="d-flex justify-content-between">
                                        <span><i class="bi bi-cash-stack"></i> Total Investment</span>
                                        <strong>৳ 50,00,000</strong>
                                    </div>
                                    <div class="d-flex justify-content-between mt-2">
                                        <span><i class="bi bi-people-fill"></i> Active Investors</span>
                                        <strong>5</strong>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Alerts -->
                    <div class="card">
                        <div class="card-header bg-warning">
                            <h5 class="mb-0"><i class="bi bi-exclamation-triangle"></i> System Alerts</h5>
                        </div>
                        <div class="card-body">
                            <div class="alert alert-warning">
                                <i class="bi bi-box"></i> 3 drugs are running low on stock
                            </div>
                            <div class="alert alert-info">
                                <i class="bi bi-clipboard-check"></i> 6 lab orders are pending
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    return HttpResponse(html)

def test_doctor(request):
    """Doctor dashboard with full UI"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Doctor Dashboard - Nazipuruhs Hospital</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
        <style>
            body { background: #f8f9fa; }
            .sidebar { min-height: 100vh; background: #198754; color: white; }
            .sidebar a { color: #d1f2e6; text-decoration: none; }
            .sidebar a:hover { color: white; }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-2 sidebar p-3">
                    <h4 class="text-white mb-4"><i class="bi bi-hospital"></i> Nazipuruhs</h4>
                    <nav class="nav flex-column">
                        <a class="nav-link" href="/test-admin/"><i class="bi bi-speedometer2"></i> Admin</a>
                        <a class="nav-link active" href="/test-doctor/"><i class="bi bi-person-heart"></i> Doctors</a>
                        <a class="nav-link" href="/test-reception/"><i class="bi bi-person-badge"></i> Reception</a>
                        <a class="nav-link" href="/test-display/"><i class="bi bi-tv"></i> Display</a>
                    </nav>
                </div>
                
                <div class="col-md-10 p-4">
                    <h2><i class="bi bi-person-heart"></i> Doctor Dashboard</h2>
                    <p class="text-muted">Dr. ডাঃ শাকেব সুলতানা - ক্যান্সার বিশেষজ্ঞ</p>
                    
                    <div class="row mb-4">
                        <div class="col-md-3">
                            <div class="card border-success">
                                <div class="card-body text-center">
                                    <h2 class="text-success">8</h2>
                                    <p>Today's Appointments</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="card border-warning">
                                <div class="card-body text-center">
                                    <h2 class="text-warning">3</h2>
                                    <p>Pending</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="card border-primary">
                                <div class="card-body text-center">
                                    <h2 class="text-primary">5</h2>
                                    <p>Completed</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="card border-info">
                                <div class="card-body text-center">
                                    <h2 class="text-info">120</h2>
                                    <p>Total Patients</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header bg-success text-white">
                            <h5 class="mb-0">Today's Schedule</h5>
                        </div>
                        <div class="card-body">
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th>Time</th>
                                        <th>Patient</th>
                                        <th>Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>10:00 AM</td>
                                        <td>Patient #001</td>
                                        <td><span class="badge bg-success">Completed</span></td>
                                    </tr>
                                    <tr>
                                        <td>11:00 AM</td>
                                        <td>Patient #002</td>
                                        <td><span class="badge bg-warning">In Progress</span></td>
                                    </tr>
                                    <tr>
                                        <td>12:00 PM</td>
                                        <td>Patient #003</td>
                                        <td><span class="badge bg-secondary">Waiting</span></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

def test_reception(request):
    """Reception dashboard with full UI"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reception Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
        <style>
            body { background: #f8f9fa; }
            .sidebar { min-height: 100vh; background: #0dcaf0; color: white; }
            .sidebar a { color: #e6f7fb; text-decoration: none; }
            .sidebar a:hover { color: white; }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-2 sidebar p-3">
                    <h4 class="text-white mb-4"><i class="bi bi-hospital"></i> Nazipuruhs</h4>
                    <nav class="nav flex-column">
                        <a class="nav-link" href="/test-admin/"><i class="bi bi-speedometer2"></i> Admin</a>
                        <a class="nav-link" href="/test-doctor/"><i class="bi bi-person-heart"></i> Doctors</a>
                        <a class="nav-link active" href="/test-reception/"><i class="bi bi-person-badge"></i> Reception</a>
                        <a class="nav-link" href="/test-display/"><i class="bi bi-tv"></i> Display</a>
                    </nav>
                </div>
                
                <div class="col-md-10 p-4">
                    <h2><i class="bi bi-person-badge"></i> Reception Dashboard</h2>
                    
                    <div class="row mb-4">
                        <div class="col-md-4">
                            <div class="card border-info">
                                <div class="card-body text-center">
                                    <h2 class="text-info">15</h2>
                                    <p>Today's Appointments</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card border-warning">
                                <div class="card-body text-center">
                                    <h2 class="text-warning">5</h2>
                                    <p>Waiting</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card border-success">
                                <div class="card-body text-center">
                                    <h2 class="text-success">3</h2>
                                    <p>Walk-ins</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="card-header bg-info text-white">
                            <h5 class="mb-0">Quick Actions</h5>
                        </div>
                        <div class="card-body">
                            <button class="btn btn-primary me-2"><i class="bi bi-person-plus"></i> New Patient</button>
                            <button class="btn btn-success me-2"><i class="bi bi-calendar-plus"></i> Book Appointment</button>
                            <button class="btn btn-warning"><i class="bi bi-printer"></i> Print Queue</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

def test_display(request):
    """Display monitor with full UI"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Display Monitor</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background: #000; color: #0f0; font-family: 'Courier New', monospace; }
            .display-box { border: 3px solid #0f0; padding: 20px; margin: 20px; }
            .serial-number { font-size: 8rem; font-weight: bold; text-align: center; }
            .blink { animation: blink 1s infinite; }
            @keyframes blink { 50% { opacity: 0.5; } }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <h1 class="text-center mt-3 blink">নাজিরপুর হাসপাতাল - Nazipuruhs Hospital</h1>
            
            <div class="display-box mt-5">
                <h2 class="text-center">বর্তমান সিরিয়াল / Current Serial</h2>
                <div class="serial-number blink">015</div>
            </div>
            
            <div class="row mt-4">
                <div class="col-md-6">
                    <div class="display-box">
                        <h3>অপেক্ষমাণ / Waiting: 8</h3>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="display-box">
                        <h3>ডাক্তার উপলব্ধ / Doctors Available: 4</h3>
                    </div>
                </div>
            </div>
            
            <div class="display-box mt-4">
                <h3 class="text-center">Welcome to Nazipuruhs Hospital</h3>
                <p class="text-center">আপনার সিরিয়াল নম্বর মনিটর দেখুন</p>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)
