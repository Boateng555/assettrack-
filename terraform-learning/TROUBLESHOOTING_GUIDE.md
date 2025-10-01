# 🔧 Troubleshooting Guide for Teacher Demonstration

## 🚨 **Common Issues and Solutions**

### **Issue 1: SSH Connection Timeout**
**Symptoms:**
```
ssh: connect to host 172.171.223.227 port 22: Connection timed out
```

**Possible Causes:**
1. VM is stopped/deallocated
2. Network Security Group blocking SSH
3. VM is still starting up

**Solutions:**
```powershell
# Check VM status in Azure portal
# Or restart VM using Azure CLI
az vm start --resource-group rg-terraform-learning --name vm-terraform-learning

# Wait 2-3 minutes for VM to fully start
# Then try SSH again
```

### **Issue 2: Web Application Not Responding**
**Symptoms:**
```
Invoke-WebRequest : The operation has timed out.
```

**Possible Causes:**
1. Django server not running
2. VM stopped
3. Application crashed

**Solutions:**
```bash
# SSH into VM first
ssh azureuser@172.171.223.227

# Check if Django is running
ps aux | grep python

# If not running, start Django
cd assettrack-
sudo python3 manage.py runserver 0.0.0.0:80 --noreload --insecure --settings=assettrack_django.settings_override &

# Exit SSH
exit
```

### **Issue 3: Terraform State Issues**
**Symptoms:**
```
Error: No state file found
```

**Solutions:**
```powershell
# Reinitialize Terraform
terraform init

# If state is lost, re-import resources
terraform import azurerm_resource_group.main /subscriptions/2c99f8c4-d28c-467b-8b03-15255b312d55/resourceGroups/rg-terraform-learning
```

---

## 🎯 **Quick Health Check Commands**

### **1. Infrastructure Status**
```powershell
# Check Terraform state
terraform show

# Check all resources
terraform state list

# Check public IP
terraform output
```

### **2. VM Status**
```powershell
# Test SSH (if this works, VM is running)
ssh azureuser@172.171.223.227

# Test web application
Invoke-WebRequest -Uri http://172.171.223.227 -TimeoutSec 5
```

### **3. Application Status**
```bash
# SSH into VM and check Django
ssh azureuser@172.171.223.227
ps aux | grep python
netstat -tlnp | grep :80
```

---

## 🚀 **Emergency Recovery Steps**

### **If Everything is Broken:**

#### **Step 1: Check Azure Portal**
1. Go to Azure Portal
2. Navigate to Resource Groups
3. Find `rg-terraform-learning`
4. Check if VM is running
5. Start VM if stopped

#### **Step 2: Restart Application**
```bash
# SSH into VM
ssh azureuser@172.171.223.227

# Kill any existing Django processes
sudo pkill -f python

# Restart Django
cd assettrack-
sudo python3 manage.py runserver 0.0.0.0:80 --noreload --insecure --settings=assettrack_django.settings_override &

# Exit SSH
exit
```

#### **Step 3: Test Application**
```powershell
# Test web application
Invoke-WebRequest -Uri http://172.171.223.227 -TimeoutSec 10

# Open browser
# Navigate to http://172.171.223.227
```

---

## 📋 **Pre-Demonstration Checklist**

### **Before Starting Demo:**
- [ ] Check internet connection
- [ ] Verify Azure subscription is active
- [ ] Test SSH connection to VM
- [ ] Test web application access
- [ ] Have backup plan ready

### **If Issues Occur During Demo:**
1. **Stay Calm**: Explain that troubleshooting is part of DevOps
2. **Show Problem-Solving**: Demonstrate how to diagnose issues
3. **Use Azure Portal**: Show how to check VM status
4. **Explain Recovery**: Show how to restart services

---

## 🎓 **Teaching Moments from Issues**

### **1. Infrastructure as Code Benefits:**
*"Even when things break, we can quickly diagnose and fix because everything is defined in code."*

### **2. Cloud Management:**
*"Cloud resources can be stopped/started, which is why we need monitoring and automation."*

### **3. DevOps Practices:**
*"Real-world systems require troubleshooting skills - this is valuable experience."*

### **4. Cost Management:**
*"VMs can be stopped to save money, but we need to restart them when needed."*

---

## 🔍 **Advanced Troubleshooting**

### **Check VM Status via Azure CLI:**
```powershell
# Install Azure CLI if not installed
# Then check VM status
az vm show --resource-group rg-terraform-learning --name vm-terraform-learning --show-details
```

### **Check Network Security Groups:**
```powershell
# Verify security group rules
terraform show azurerm_network_security_group.main
```

### **Check Application Logs:**
```bash
# SSH into VM and check Django logs
ssh azureuser@172.171.223.227
cd assettrack-
tail -f logs/django.log  # if logging is configured
```

---

## 🎯 **Demonstration Recovery Script**

### **If Demo Fails, Use This Script:**
```powershell
# 1. Check infrastructure
terraform show

# 2. Check VM status
az vm show --resource-group rg-terraform-learning --name vm-terraform-learning --query "provisioningState"

# 3. Start VM if needed
az vm start --resource-group rg-terraform-learning --name vm-terraform-learning

# 4. Wait 2 minutes, then test
ssh azureuser@172.171.223.227 "echo 'VM is running'"

# 5. Restart Django if needed
ssh azureuser@172.171.223.227 "cd assettrack- && sudo python3 manage.py runserver 0.0.0.0:80 --noreload --insecure --settings=assettrack_django.settings_override &"

# 6. Test application
Invoke-WebRequest -Uri http://172.171.223.227 -TimeoutSec 10
```

---

## 🎉 **Success Indicators**

### **Everything Working:**
- ✅ `terraform show` shows all resources
- ✅ SSH connection successful
- ✅ Web application responds
- ✅ Browser shows login page
- ✅ Admin login works

### **Partial Success (Still Demonstratable):**
- ✅ Infrastructure exists (terraform show works)
- ✅ VM is running (SSH works)
- ❌ Web app not responding (can explain troubleshooting)

### **Complete Failure (Learning Opportunity):**
- ❌ Infrastructure issues (can show terraform destroy/apply)
- ❌ VM not accessible (can show Azure portal)
- ❌ Application not working (can show debugging process)

---

**🎓 Remember: Troubleshooting is a valuable skill in DevOps! Use any issues as teaching moments to demonstrate real-world problem-solving.**


