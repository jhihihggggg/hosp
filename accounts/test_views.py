"""
Test views with complete standalone HTML - NO dependencies
"""
from django.http import HttpResponse

def test_admin(request):
    """Admin dashboard with full UI + Investor Management"""
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
            .sidebar a { color: #adb5bd; text-decoration: none; padding: 10px; display: block; }
            .sidebar a:hover, .sidebar a.active { color: white; background: #495057; }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row">
                <!-- Sidebar -->
                <div class="col-md-2 sidebar p-3">
                    <h4 class="text-white mb-4"><i class="bi bi-hospital"></i> Nazipuruhs</h4>
                    <nav class="nav flex-column">
                        <a class="nav-link active" href="#dashboard" onclick="showSection('dashboard')"><i class="bi bi-speedometer2"></i> Dashboard</a>
                        <a class="nav-link" href="#investors" onclick="showSection('investors')"><i class="bi bi-cash-stack"></i> Investors</a>
                        <a class="nav-link" href="/test-doctor/"><i class="bi bi-person-heart"></i> Doctors</a>
                        <a class="nav-link" href="/test-reception/"><i class="bi bi-person-badge"></i> Reception</a>
                        <a class="nav-link" href="/test-display/"><i class="bi bi-tv"></i> Display Monitor</a>
                    </nav>
                </div>
                
                <!-- Main Content -->
                <div class="col-md-10 p-4">
                    <!-- Dashboard Section -->
                    <div id="dashboard-section">
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
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Investors Section -->
                    <div id="investors-section" style="display:none;">
                        <div class="d-flex justify-content-between align-items-center mb-4">
                            <h2><i class="bi bi-cash-stack"></i> Investor Management</h2>
                            <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addInvestorModal">
                                <i class="bi bi-plus-circle"></i> Add New Investor
                            </button>
                        </div>
                        
                        <div class="card">
                            <div class="card-body">
                                <table class="table table-hover">
                                    <thead class="table-dark">
                                        <tr>
                                            <th>#</th>
                                            <th>Name</th>
                                            <th>Investment Amount</th>
                                            <th>Share %</th>
                                            <th>Contact</th>
                                            <th>Status</th>
                                            <th>Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody id="investorTableBody">
                                        <tr>
                                            <td>1</td>
                                            <td>মোঃ আব্দুল করিম</td>
                                            <td>৳ 15,00,000</td>
                                            <td>30%</td>
                                            <td>01712-345678</td>
                                            <td><span class="badge bg-success">Active</span></td>
                                            <td>
                                                <button class="btn btn-sm btn-info"><i class="bi bi-eye"></i></button>
                                                <button class="btn btn-sm btn-warning"><i class="bi bi-pencil"></i></button>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>2</td>
                                            <td>মিসেস ফাতিমা বেগম</td>
                                            <td>৳ 10,00,000</td>
                                            <td>20%</td>
                                            <td>01812-987654</td>
                                            <td><span class="badge bg-success">Active</span></td>
                                            <td>
                                                <button class="btn btn-sm btn-info"><i class="bi bi-eye"></i></button>
                                                <button class="btn btn-sm btn-warning"><i class="bi bi-pencil"></i></button>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>3</td>
                                            <td>ডাঃ রহমান</td>
                                            <td>৳ 12,50,000</td>
                                            <td>25%</td>
                                            <td>01912-456789</td>
                                            <td><span class="badge bg-success">Active</span></td>
                                            <td>
                                                <button class="btn btn-sm btn-info"><i class="bi bi-eye"></i></button>
                                                <button class="btn btn-sm btn-warning"><i class="bi bi-pencil"></i></button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                                
                                <div class="mt-3 p-3 bg-light rounded">
                                    <div class="row">
                                        <div class="col-md-6">
                                            <strong>Total Investment:</strong> ৳ 50,00,000
                                        </div>
                                        <div class="col-md-6">
                                            <strong>Active Investors:</strong> 5
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Add Investor Modal -->
        <div class="modal fade" id="addInvestorModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title"><i class="bi bi-person-plus"></i> Add New Investor</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="addInvestorForm">
                            <div class="mb-3">
                                <label class="form-label">Name</label>
                                <input type="text" class="form-control" placeholder="Investor name" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Investment Amount (৳)</label>
                                <input type="number" class="form-control" placeholder="Amount" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Share Percentage</label>
                                <input type="number" class="form-control" placeholder="%" max="100" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Contact Number</label>
                                <input type="tel" class="form-control" placeholder="01XXXXXXXXX" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Email (optional)</label>
                                <input type="email" class="form-control" placeholder="email@example.com">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Address</label>
                                <textarea class="form-control" rows="2"></textarea>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" onclick="addInvestor()">
                            <i class="bi bi-save"></i> Save Investor
                        </button>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            function showSection(section) {
                document.getElementById('dashboard-section').style.display = 'none';
                document.getElementById('investors-section').style.display = 'none';
                
                if(section === 'dashboard') {
                    document.getElementById('dashboard-section').style.display = 'block';
                } else if(section === 'investors') {
                    document.getElementById('investors-section').style.display = 'block';
                }
                
                // Update active nav link
                document.querySelectorAll('.sidebar a').forEach(a => a.classList.remove('active'));
                event.target.closest('a').classList.add('active');
            }
            
            function addInvestor() {
                alert('Investor added successfully!');
                bootstrap.Modal.getInstance(document.getElementById('addInvestorModal')).hide();
            }
        </script>
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

def test_pharmacy(request):
    """Pharmacy dashboard with sales, stock management"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pharmacy Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
        <style>
            body { background: #f8f9fa; }
            .sidebar { min-height: 100vh; background: #6f42c1; color: white; }
            .sidebar a { color: #e0cffc; text-decoration: none; padding: 10px; display: block; }
            .sidebar a:hover, .sidebar a.active { color: white; background: #5936a0; }
            .low-stock { background: #fff3cd; }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-2 sidebar p-3">
                    <h4 class="text-white mb-4"><i class="bi bi-hospital"></i> Nazipuruhs</h4>
                    <nav class="nav flex-column">
                        <a class="nav-link" href="/test-admin/"><i class="bi bi-speedometer2"></i> Admin</a>
                        <a class="nav-link active" href="#sales" onclick="showPharmacySection('sales')"><i class="bi bi-cart-check"></i> Sales</a>
                        <a class="nav-link" href="#stock" onclick="showPharmacySection('stock')"><i class="bi bi-box-seam"></i> Stock</a>
                        <a class="nav-link" href="#patients" onclick="showPharmacySection('patients')"><i class="bi bi-people"></i> Patient Data</a>
                        <a class="nav-link" href="/test-canteen/"><i class="bi bi-cup-hot"></i> Canteen</a>
                    </nav>
                </div>
                
                <div class="col-md-10 p-4">
                    <!-- Sales Section -->
                    <div id="sales-section">
                        <div class="d-flex justify-content-between align-items-center mb-4">
                            <h2><i class="bi bi-cart-check"></i> Pharmacy Sales</h2>
                            <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#newSaleModal">
                                <i class="bi bi-plus-circle"></i> New Sale
                            </button>
                        </div>
                        
                        <div class="row mb-4">
                            <div class="col-md-3">
                                <div class="card border-primary">
                                    <div class="card-body text-center">
                                        <h3 class="text-primary">৳ 30,000</h3>
                                        <p>Today's Sales</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="card border-success">
                                    <div class="card-body text-center">
                                        <h3 class="text-success">45</h3>
                                        <p>Transactions</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="card border-warning">
                                    <div class="card-body text-center">
                                        <h3 class="text-warning">8</h3>
                                        <p>Low Stock Items</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="card border-info">
                                    <div class="card-body text-center">
                                        <h3 class="text-info">350</h3>
                                        <p>Total Items</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="card">
                            <div class="card-header bg-primary text-white">
                                <h5 class="mb-0">Recent Sales</h5>
                            </div>
                            <div class="card-body">
                                <table class="table table-hover">
                                    <thead>
                                        <tr>
                                            <th>Invoice</th>
                                            <th>Patient</th>
                                            <th>Items</th>
                                            <th>Amount</th>
                                            <th>Time</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>#PHR001</td>
                                            <td>রহিম উদ্দিন</td>
                                            <td>3</td>
                                            <td>৳ 850</td>
                                            <td>10:30 AM</td>
                                            <td><button class="btn btn-sm btn-info"><i class="bi bi-printer"></i> Print</button></td>
                                        </tr>
                                        <tr>
                                            <td>#PHR002</td>
                                            <td>সালমা খাতুন</td>
                                            <td>5</td>
                                            <td>৳ 1,250</td>
                                            <td>11:15 AM</td>
                                            <td><button class="btn btn-sm btn-info"><i class="bi bi-printer"></i> Print</button></td>
                                        </tr>
                                        <tr>
                                            <td>#PHR003</td>
                                            <td>করিম মিয়া</td>
                                            <td>2</td>
                                            <td>৳ 650</td>
                                            <td>12:00 PM</td>
                                            <td><button class="btn btn-sm btn-info"><i class="bi bi-printer"></i> Print</button></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Stock Section -->
                    <div id="stock-section" style="display:none;">
                        <div class="d-flex justify-content-between align-items-center mb-4">
                            <h2><i class="bi bi-box-seam"></i> Medicine Stock Management</h2>
                            <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addStockModal">
                                <i class="bi bi-plus-circle"></i> Add Stock
                            </button>
                        </div>
                        
                        <div class="card">
                            <div class="card-body">
                                <table class="table table-hover">
                                    <thead class="table-dark">
                                        <tr>
                                            <th>Medicine Name</th>
                                            <th>Type</th>
                                            <th>Stock Qty</th>
                                            <th>Unit Price</th>
                                            <th>Expiry Date</th>
                                            <th>Status</th>
                                            <th>Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr class="low-stock">
                                            <td>Napa (Paracetamol)</td>
                                            <td>Tablet</td>
                                            <td><strong class="text-danger">15</strong></td>
                                            <td>৳ 2.50</td>
                                            <td>Dec 2025</td>
                                            <td><span class="badge bg-warning">Low Stock</span></td>
                                            <td>
                                                <button class="btn btn-sm btn-primary"><i class="bi bi-plus"></i> Add</button>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>Ace (Paracetamol)</td>
                                            <td>Tablet</td>
                                            <td>250</td>
                                            <td>৳ 2.00</td>
                                            <td>Jan 2026</td>
                                            <td><span class="badge bg-success">In Stock</span></td>
                                            <td>
                                                <button class="btn btn-sm btn-primary"><i class="bi bi-plus"></i> Add</button>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>Maxpro (Omeprazole)</td>
                                            <td>Capsule</td>
                                            <td>180</td>
                                            <td>৳ 8.00</td>
                                            <td>Mar 2026</td>
                                            <td><span class="badge bg-success">In Stock</span></td>
                                            <td>
                                                <button class="btn btn-sm btn-primary"><i class="bi bi-plus"></i> Add</button>
                                            </td>
                                        </tr>
                                        <tr class="low-stock">
                                            <td>Seclo (Omeprazole)</td>
                                            <td>Capsule</td>
                                            <td><strong class="text-danger">20</strong></td>
                                            <td>৳ 7.50</td>
                                            <td>Feb 2026</td>
                                            <td><span class="badge bg-warning">Low Stock</span></td>
                                            <td>
                                                <button class="btn btn-sm btn-primary"><i class="bi bi-plus"></i> Add</button>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>Flexi (Naproxen)</td>
                                            <td>Tablet</td>
                                            <td>120</td>
                                            <td>৳ 5.00</td>
                                            <td>Apr 2026</td>
                                            <td><span class="badge bg-success">In Stock</span></td>
                                            <td>
                                                <button class="btn btn-sm btn-primary"><i class="bi bi-plus"></i> Add</button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Patient Data Section -->
                    <div id="patients-section" style="display:none;">
                        <h2 class="mb-4"><i class="bi bi-people"></i> Patient Purchase Data</h2>
                        
                        <div class="card">
                            <div class="card-header bg-info text-white">
                                <h5 class="mb-0">Patient Medicine History</h5>
                            </div>
                            <div class="card-body">
                                <div class="mb-3">
                                    <input type="text" class="form-control" placeholder="Search patient by name or phone...">
                                </div>
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th>Patient Name</th>
                                            <th>Phone</th>
                                            <th>Last Purchase</th>
                                            <th>Total Spent</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>রহিম উদ্দিন</td>
                                            <td>01712-345678</td>
                                            <td>Today</td>
                                            <td>৳ 2,500</td>
                                            <td><button class="btn btn-sm btn-info"><i class="bi bi-eye"></i> View History</button></td>
                                        </tr>
                                        <tr>
                                            <td>সালমা খাতুন</td>
                                            <td>01812-987654</td>
                                            <td>Yesterday</td>
                                            <td>৳ 3,200</td>
                                            <td><button class="btn btn-sm btn-info"><i class="bi bi-eye"></i> View History</button></td>
                                        </tr>
                                        <tr>
                                            <td>করিম মিয়া</td>
                                            <td>01912-456789</td>
                                            <td>2 days ago</td>
                                            <td>৳ 1,800</td>
                                            <td><button class="btn btn-sm btn-info"><i class="bi bi-eye"></i> View History</button></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- New Sale Modal -->
        <div class="modal fade" id="newSaleModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title"><i class="bi bi-cart-plus"></i> New Sale</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row mb-3">
                            <div class="col-md-6">
                                <label class="form-label">Patient Name</label>
                                <input type="text" class="form-control" placeholder="Enter patient name">
                            </div>
                            <div class="col-md-6">
                                <label class="form-label">Phone</label>
                                <input type="tel" class="form-control" placeholder="01XXXXXXXXX">
                            </div>
                        </div>
                        <hr>
                        <h6>Add Medicines</h6>
                        <div class="row mb-2">
                            <div class="col-md-6">
                                <select class="form-select">
                                    <option>Select Medicine</option>
                                    <option>Napa (Paracetamol)</option>
                                    <option>Ace (Paracetamol)</option>
                                    <option>Maxpro (Omeprazole)</option>
                                </select>
                            </div>
                            <div class="col-md-3">
                                <input type="number" class="form-control" placeholder="Qty" value="1">
                            </div>
                            <div class="col-md-3">
                                <button class="btn btn-success w-100"><i class="bi bi-plus"></i> Add</button>
                            </div>
                        </div>
                        <div class="mt-3 p-3 bg-light">
                            <strong>Total: ৳ 0</strong>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary"><i class="bi bi-printer"></i> Print Invoice</button>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            function showPharmacySection(section) {
                document.getElementById('sales-section').style.display = 'none';
                document.getElementById('stock-section').style.display = 'none';
                document.getElementById('patients-section').style.display = 'none';
                document.getElementById(section + '-section').style.display = 'block';
                
                document.querySelectorAll('.sidebar a').forEach(a => a.classList.remove('active'));
                event.target.closest('a').classList.add('active');
            }
        </script>
    </body>
    </html>
    """
    return HttpResponse(html)

def test_canteen(request):
    """Canteen dashboard with sales and stock management"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Canteen Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
        <style>
            body { background: #f8f9fa; }
            .sidebar { min-height: 100vh; background: #fd7e14; color: white; }
            .sidebar a { color: #ffe5d0; text-decoration: none; padding: 10px; display: block; }
            .sidebar a:hover, .sidebar a.active { color: white; background: #dc6a00; }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-2 sidebar p-3">
                    <h4 class="text-white mb-4"><i class="bi bi-hospital"></i> Nazipuruhs</h4>
                    <nav class="nav flex-column">
                        <a class="nav-link" href="/test-admin/"><i class="bi bi-speedometer2"></i> Admin</a>
                        <a class="nav-link active" href="#sales" onclick="showCanteenSection('sales')"><i class="bi bi-cart-check"></i> Sales</a>
                        <a class="nav-link" href="#menu" onclick="showCanteenSection('menu')"><i class="bi bi-book"></i> Menu</a>
                        <a class="nav-link" href="#stock" onclick="showCanteenSection('stock')"><i class="bi bi-box-seam"></i> Stock</a>
                        <a class="nav-link" href="/test-pharmacy/"><i class="bi bi-capsule"></i> Pharmacy</a>
                    </nav>
                </div>
                
                <div class="col-md-10 p-4">
                    <!-- Sales Section -->
                    <div id="sales-section">
                        <div class="d-flex justify-content-between align-items-center mb-4">
                            <h2><i class="bi bi-cup-hot"></i> Canteen Sales</h2>
                            <button class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#newOrderModal">
                                <i class="bi bi-plus-circle"></i> New Order
                            </button>
                        </div>
                        
                        <div class="row mb-4">
                            <div class="col-md-3">
                                <div class="card border-warning">
                                    <div class="card-body text-center">
                                        <h3 class="text-warning">৳ 15,000</h3>
                                        <p>Today's Sales</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="card border-success">
                                    <div class="card-body text-center">
                                        <h3 class="text-success">85</h3>
                                        <p>Orders</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="card border-primary">
                                    <div class="card-body text-center">
                                        <h3 class="text-primary">12</h3>
                                        <p>Pending</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="card border-info">
                                    <div class="card-body text-center">
                                        <h3 class="text-info">45</h3>
                                        <p>Menu Items</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="card">
                            <div class="card-header bg-warning">
                                <h5 class="mb-0">Recent Orders</h5>
                            </div>
                            <div class="card-body">
                                <table class="table table-hover">
                                    <thead>
                                        <tr>
                                            <th>Order #</th>
                                            <th>Customer</th>
                                            <th>Items</th>
                                            <th>Amount</th>
                                            <th>Time</th>
                                            <th>Status</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>#CNT001</td>
                                            <td>Staff Room 1</td>
                                            <td>Tea x3, Samosa x5</td>
                                            <td>৳ 180</td>
                                            <td>10:30 AM</td>
                                            <td><span class="badge bg-success">Served</span></td>
                                        </tr>
                                        <tr>
                                            <td>#CNT002</td>
                                            <td>Doctor Chamber</td>
                                            <td>Coffee x2, Cake x1</td>
                                            <td>৳ 250</td>
                                            <td>11:00 AM</td>
                                            <td><span class="badge bg-warning">Preparing</span></td>
                                        </tr>
                                        <tr>
                                            <td>#CNT003</td>
                                            <td>Reception</td>
                                            <td>Lunch x4</td>
                                            <td>৳ 600</td>
                                            <td>12:30 PM</td>
                                            <td><span class="badge bg-primary">Pending</span></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Menu Section -->
                    <div id="menu-section" style="display:none;">
                        <div class="d-flex justify-content-between align-items-center mb-4">
                            <h2><i class="bi bi-book"></i> Menu Management</h2>
                            <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addMenuItem">
                                <i class="bi bi-plus-circle"></i> Add Item
                            </button>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-4 mb-3">
                                <div class="card">
                                    <div class="card-body">
                                        <h5>চা / Tea</h5>
                                        <p class="text-muted">Hot beverage</p>
                                        <h4 class="text-warning">৳ 15</h4>
                                        <button class="btn btn-sm btn-warning"><i class="bi bi-pencil"></i> Edit</button>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4 mb-3">
                                <div class="card">
                                    <div class="card-body">
                                        <h5>কফি / Coffee</h5>
                                        <p class="text-muted">Hot beverage</p>
                                        <h4 class="text-warning">৳ 25</h4>
                                        <button class="btn btn-sm btn-warning"><i class="bi bi-pencil"></i> Edit</button>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4 mb-3">
                                <div class="card">
                                    <div class="card-body">
                                        <h5>সমুচা / Samosa</h5>
                                        <p class="text-muted">Snack</p>
                                        <h4 class="text-warning">৳ 20</h4>
                                        <button class="btn btn-sm btn-warning"><i class="bi bi-pencil"></i> Edit</button>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4 mb-3">
                                <div class="card">
                                    <div class="card-body">
                                        <h5>ভাত / Rice</h5>
                                        <p class="text-muted">Main course</p>
                                        <h4 class="text-warning">৳ 80</h4>
                                        <button class="btn btn-sm btn-warning"><i class="bi bi-pencil"></i> Edit</button>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4 mb-3">
                                <div class="card">
                                    <div class="card-body">
                                        <h5>রুটি / Roti</h5>
                                        <p class="text-muted">Main course</p>
                                        <h4 class="text-warning">৳ 10</h4>
                                        <button class="btn btn-sm btn-warning"><i class="bi bi-pencil"></i> Edit</button>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4 mb-3">
                                <div class="card">
                                    <div class="card-body">
                                        <h5>বিরিয়ানি / Biryani</h5>
                                        <p class="text-muted">Special</p>
                                        <h4 class="text-warning">৳ 150</h4>
                                        <button class="btn btn-sm btn-warning"><i class="bi bi-pencil"></i> Edit</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Stock Section -->
                    <div id="stock-section" style="display:none;">
                        <h2 class="mb-4"><i class="bi bi-box-seam"></i> Inventory Stock</h2>
                        
                        <div class="card">
                            <div class="card-body">
                                <table class="table">
                                    <thead class="table-dark">
                                        <tr>
                                            <th>Item</th>
                                            <th>Unit</th>
                                            <th>Stock Qty</th>
                                            <th>Status</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>চা পাতা / Tea Leaves</td>
                                            <td>KG</td>
                                            <td>5 kg</td>
                                            <td><span class="badge bg-success">Good</span></td>
                                            <td><button class="btn btn-sm btn-primary"><i class="bi bi-plus"></i> Add</button></td>
                                        </tr>
                                        <tr>
                                            <td>চিনি / Sugar</td>
                                            <td>KG</td>
                                            <td>15 kg</td>
                                            <td><span class="badge bg-success">Good</span></td>
                                            <td><button class="btn btn-sm btn-primary"><i class="bi bi-plus"></i> Add</button></td>
                                        </tr>
                                        <tr class="table-warning">
                                            <td>চাল / Rice</td>
                                            <td>KG</td>
                                            <td>8 kg</td>
                                            <td><span class="badge bg-warning">Low</span></td>
                                            <td><button class="btn btn-sm btn-primary"><i class="bi bi-plus"></i> Add</button></td>
                                        </tr>
                                        <tr>
                                            <td>আটা / Flour</td>
                                            <td>KG</td>
                                            <td>20 kg</td>
                                            <td><span class="badge bg-success">Good</span></td>
                                            <td><button class="btn btn-sm btn-primary"><i class="bi bi-plus"></i> Add</button></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- New Order Modal -->
        <div class="modal fade" id="newOrderModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header bg-warning">
                        <h5 class="modal-title"><i class="bi bi-cart-plus"></i> New Order</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label">Customer/Location</label>
                            <input type="text" class="form-control" placeholder="Enter location">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Select Item</label>
                            <select class="form-select">
                                <option>Tea - ৳15</option>
                                <option>Coffee - ৳25</option>
                                <option>Samosa - ৳20</option>
                                <option>Rice - ৳80</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Quantity</label>
                            <input type="number" class="form-control" value="1">
                        </div>
                        <div class="p-3 bg-light">
                            <strong>Total: ৳ 0</strong>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-warning">Place Order</button>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            function showCanteenSection(section) {
                document.getElementById('sales-section').style.display = 'none';
                document.getElementById('menu-section').style.display = 'none';
                document.getElementById('stock-section').style.display = 'none';
                document.getElementById(section + '-section').style.display = 'block';
                
                document.querySelectorAll('.sidebar a').forEach(a => a.classList.remove('active'));
                event.target.closest('a').classList.add('active');
            }
        </script>
    </body>
    </html>
    """
    return HttpResponse(html)
