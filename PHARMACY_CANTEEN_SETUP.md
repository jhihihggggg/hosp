# Pharmacy & Canteen Dashboard Setup

## ✅ New Features Added

### 1. **Pharmacy Dashboard** (`/test-pharmacy/`)

#### Features:
- **Sales Management**
  - Today's sales: ৳30,000
  - Transaction count: 45 today
  - Recent sales list with invoice numbers
  - Print invoice functionality
  - New Sale modal with patient info collection

- **Medicine Stock Management**
  - Full medicine inventory with stock levels
  - Low stock alerts (highlighted in yellow)
  - Medicine details: name, type, quantity, price, expiry date
  - Stock status indicators (In Stock / Low Stock)
  - Add stock functionality

- **Patient Data Collection**
  - Patient purchase history
  - Track total spending per patient
  - Search by name or phone
  - View detailed medicine history

#### Sample Data:
- **Medicines**: Napa, Ace, Maxpro, Seclo, Flexi
- **Patients**: রহিম উদ্দিন, সালমা খাতুন, করিম মিয়া

---

### 2. **Canteen Dashboard** (`/test-canteen/`)

#### Features:
- **Sales Management**
  - Today's sales: ৳15,000
  - Order tracking: 85 orders today, 12 pending
  - Recent orders list with status
  - New Order modal

- **Menu Management**
  - Display all menu items with prices
  - Bengali & English names
  - Category tags (Hot beverage, Snack, Main course, Special)
  - Edit menu items

- **Inventory Stock**
  - Raw material tracking
  - Stock levels with units (KG)
  - Status indicators (Good / Low)
  - Add stock functionality

#### Sample Menu Items:
- **Beverages**: চা/Tea (৳15), কফি/Coffee (৳25)
- **Snacks**: সমুচা/Samosa (৳20)
- **Main Course**: ভাত/Rice (৳80), রুটি/Roti (৳10)
- **Special**: বিরিয়ানি/Biryani (৳150)

#### Sample Stock Items:
- চা পাতা/Tea Leaves: 5 kg
- চিনি/Sugar: 15 kg
- চাল/Rice: 8 kg (Low)
- আটা/Flour: 20 kg

---

## 🚀 Access URLs

After deployment, access these dashboards at:

- **Admin Dashboard**: https://nazipuruhs.com:8005/test-admin/
- **Doctor Dashboard**: https://nazipuruhs.com:8005/test-doctor/
- **Reception Dashboard**: https://nazipuruhs.com:8005/test-reception/
- **Display Monitor**: https://nazipuruhs.com:8005/test-display/
- **Pharmacy Dashboard**: https://nazipuruhs.com:8005/test-pharmacy/
- **Canteen Dashboard**: https://nazipuruhs.com:8005/test-canteen/

---

## 📦 Deployment on VPS

### Quick Deploy (One Command):

```bash
ssh root@vmi2823196.contaboserver.net "cd /var/www/hosp && sudo -u www-data git pull origin main && sudo systemctl restart nazipuruhs.service"
```

### Step-by-Step:

1. **SSH to VPS**:
   ```bash
   ssh root@vmi2823196.contaboserver.net
   ```

2. **Pull Latest Code**:
   ```bash
   cd /var/www/hosp
   sudo -u www-data git pull origin main
   ```

3. **Restart Service**:
   ```bash
   sudo systemctl restart nazipuruhs.service
   ```

4. **Check Status**:
   ```bash
   sudo systemctl status nazipuruhs.service
   ```

5. **Test URLs** (from browser):
   - Pharmacy: https://nazipuruhs.com:8005/test-pharmacy/
   - Canteen: https://nazipuruhs.com:8005/test-canteen/

---

## 🎨 UI Features

### Color Schemes:
- **Pharmacy**: Purple theme (#6f42c1)
- **Canteen**: Orange theme (#fd7e14)
- **Admin**: Blue theme (#0d6efd)
- **Doctor**: Success green theme (#198754)
- **Reception**: Info cyan theme (#0dcaf0)

### Common Features:
- Bootstrap 5.3.0 responsive design
- Bootstrap Icons for visual elements
- Bengali & English bilingual support
- Modal forms for data entry
- Section navigation (sidebar)
- Print functionality
- Status badges (color-coded)
- Low stock alerts

---

## 📊 Data Structure

### Pharmacy Sales:
- Invoice number
- Patient name & phone
- Items sold & quantities
- Total amount
- Transaction time
- Print invoice

### Medicine Stock:
- Medicine name (generic)
- Type (Tablet/Capsule/Syrup)
- Current stock quantity
- Unit price (৳)
- Expiry date
- Status (In Stock/Low Stock/Expired)

### Patient Data:
- Patient name
- Contact phone
- Last purchase date
- Total amount spent
- Purchase history

### Canteen Orders:
- Order number
- Customer/Location
- Items ordered
- Order amount
- Order time
- Status (Pending/Preparing/Served)

### Menu Items:
- Item name (Bengali & English)
- Category
- Price (৳)
- Availability

### Canteen Stock:
- Ingredient name
- Unit (KG/L/PCS)
- Current quantity
- Status (Good/Low)

---

## 🔗 Integration Points

### Navigation Links:
All dashboards have quick navigation to:
- Admin Dashboard
- Pharmacy Dashboard
- Canteen Dashboard

### Future Integration:
- Connect to real database models
- Real-time stock updates
- Actual invoice generation
- Patient data synchronization
- Financial reporting integration

---

## ✅ What Works Now:
- ✅ Full UI for Pharmacy & Canteen dashboards
- ✅ Sample data for testing
- ✅ Section navigation
- ✅ Modal forms for data entry
- ✅ Responsive design
- ✅ Print buttons
- ✅ Status indicators
- ✅ Low stock alerts
- ✅ No authentication required (test mode)

## 🔄 Next Steps:
1. Deploy to VPS using command above
2. Test all URLs in browser
3. Add real database integration later
4. Create proper authentication for production
5. Connect to actual patient/appointment systems
