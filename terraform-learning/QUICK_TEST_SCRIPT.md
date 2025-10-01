# 🧪 Quick Test Script for Teacher Demonstration

## 🚀 **Copy-Paste Commands for Live Demo**

### **Step 1: Verify Infrastructure**
```powershell
# Navigate to project directory
cd C:\sal hardwear\terraform-learning

# Show current infrastructure state
terraform show

# Show all resources
terraform state list

# Show public IP
terraform output
```

### **Step 2: Test VM Connectivity**
```powershell
# Test SSH connection (will prompt for password)
ssh azureuser@172.171.223.227

# If successful, type 'exit' to return
# If SSH fails, the VM might be stopped - check Azure portal
# Alternative: Test network connectivity
Test-NetConnection -ComputerName 172.171.223.227 -Port 22
```

### **Step 3: Test Web Application**
```powershell
# Test main application
Invoke-WebRequest -Uri http://172.171.223.227 -TimeoutSec 10

# Test admin panel
Invoke-WebRequest -Uri http://172.171.223.227/admin/ -TimeoutSec 10

# If web app fails, Django server might not be running
# SSH into VM and restart Django: sudo python3 manage.py runserver 0.0.0.0:80 --noreload &
```

### **Step 4: Browser Testing**
1. **Open Browser**: Go to `http://172.171.223.227`
2. **Login**: Username: `admin`, Password: `admin123`
3. **Test Features**: Navigate through the application

---

## 📋 **Expected Results**

### **Terraform Commands:**
- ✅ `terraform show`: Shows all infrastructure details
- ✅ `terraform state list`: Lists all 7 resources
- ✅ `terraform output`: Shows IP address `172.171.223.227`

### **Connectivity Tests:**
- ✅ SSH: Successful connection to VM
- ✅ Web App: HTTP 200 OK response
- ✅ Admin Panel: Django admin interface loads

### **Application Features:**
- ✅ Login page loads correctly
- ✅ Admin login works
- ✅ Dashboard displays
- ✅ Asset management features work

---

## 🎯 **Key Points to Explain**

### **1. Infrastructure as Code:**
*"We defined our entire cloud infrastructure using code, not manual clicks in the Azure portal."*

### **2. Automation Benefits:**
*"This infrastructure can be recreated anywhere in minutes, not hours."*

### **3. Version Control:**
*"All infrastructure changes are tracked and can be rolled back."*

### **4. Cost Efficiency:**
*"We can destroy this infrastructure when not needed to save money."*

### **5. Troubleshooting (If Issues Occur):**
*"This demonstrates real-world problem-solving skills. In production, we need to troubleshoot issues like VMs being stopped to save costs."*

---

## 🎓 **Learning Outcomes Demonstrated**

1. **Infrastructure as Code (IaC)**: Automated infrastructure provisioning
2. **Cloud Computing**: Azure platform integration
3. **DevOps Practices**: Automation and deployment
4. **Web Development**: Django application deployment
5. **Network Security**: Firewall and access control
6. **Database Management**: Django migrations and setup

---

**🎉 Ready for your teacher demonstration!**

cd C:\sal hardwear\terraform-learning

