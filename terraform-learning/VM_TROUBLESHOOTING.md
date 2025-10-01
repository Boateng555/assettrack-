# 🚨 VM Connection Troubleshooting Guide

## 🔍 **Current Issue: SSH Connection Timeout**

### **Symptoms:**
```
ssh: connect to host 172.171.223.227 port 22: Connection timed out
```

### **Diagnosis:**
The VM is not responding to network connections, which typically means:
1. **VM is stopped/deallocated** (most likely)
2. **VM is still starting up**
3. **Network security group issues**
4. **Azure subscription issues**

---

## 🚀 **Solutions to Try**

### **Solution 1: Check VM Status in Azure Portal**
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Resource Groups**
3. Find **rg-terraform-learning**
4. Click on **vm-terraform-learning**
5. Check the **Status** - it should show "Running"
6. If it shows "Stopped" or "Deallocated", click **Start**

### **Solution 2: Start VM via Azure CLI**
```powershell
# Install Azure CLI if not installed
# Then start the VM
az vm start --resource-group rg-terraform-learning --name vm-terraform-learning

# Wait 2-3 minutes for VM to fully start
# Then try SSH again
```

### **Solution 3: Check VM Status via Terraform**
```powershell
# Check if VM exists in Terraform state
terraform state show azurerm_linux_virtual_machine.main

# If VM exists but is stopped, you can restart it
```

---

## 🎯 **For Your Teacher Demonstration**

### **If VM is Stopped (Most Likely Scenario):**

#### **Option 1: Show the Problem and Solution**
*"This demonstrates real-world troubleshooting. The VM has stopped, which is common in cloud environments. Let me show you how to diagnose and fix this."*

1. **Show the issue**: `ssh azureuser@172.171.223.227` (fails)
2. **Explain the problem**: "VM is stopped to save costs"
3. **Show the solution**: Start VM in Azure portal
4. **Test again**: SSH should work after VM starts

#### **Option 2: Demonstrate Infrastructure Management**
*"This shows the power of Infrastructure as Code. Even when resources are stopped, we can easily manage them."*

1. **Show Terraform state**: `terraform show`
2. **Explain**: "Infrastructure is defined in code"
3. **Show VM details**: `terraform state show azurerm_linux_virtual_machine.main`
4. **Explain**: "We can see the VM exists but is stopped"

### **If VM is Running but SSH Fails:**

#### **Check Network Security Group:**
```powershell
# Show security group rules
terraform show azurerm_network_security_group.main
```

#### **Check if VM is still starting:**
```powershell
# Wait 2-3 minutes and try again
ssh azureuser@172.171.223.227
```

---

## 🎓 **Teaching Moments from This Issue**

### **1. Cloud Cost Management:**
*"VMs can be stopped to save money, but we need to restart them when needed. This is a common practice in cloud computing."*

### **2. Infrastructure as Code Benefits:**
*"Even when resources are stopped, we can easily see what exists and manage them through code."*

### **3. Real-World Troubleshooting:**
*"In production environments, we need to monitor and maintain systems. This demonstrates real-world problem-solving skills."*

### **4. Automation Opportunities:**
*"We could automate VM startup based on schedules or triggers to avoid this issue."*

---

## 🚀 **Quick Fix Commands**

### **If VM is Stopped:**
```powershell
# Start VM via Azure CLI
az vm start --resource-group rg-terraform-learning --name vm-terraform-learning

# Wait 2 minutes, then test
ssh azureuser@172.171.223.227
```

### **If VM is Running but SSH Fails:**
```powershell
# Check if VM is fully started
az vm show --resource-group rg-terraform-learning --name vm-terraform-learning --query "provisioningState"

# Wait if still starting
# Then try SSH again
```

### **If Everything Fails:**
```powershell
# Show that infrastructure exists
terraform show

# Explain that this is a learning opportunity
# Show how to troubleshoot in real-world scenarios
```

---

## 🎯 **Demonstration Script with Troubleshooting**

### **Opening Statement:**
*"Today I'll demonstrate Infrastructure as Code with Terraform. I'll also show you how to troubleshoot common issues that occur in real-world deployments."*

### **Step 1: Show Infrastructure (This Will Work)**
```powershell
terraform show
terraform state list
terraform output
```

### **Step 2: Test Connectivity (May Fail)**
```powershell
ssh azureuser@172.171.223.227
```

### **Step 3: Demonstrate Troubleshooting (If SSH Fails)**
*"The SSH connection failed, which is common in cloud environments. Let me show you how to diagnose and fix this."*

1. **Check Azure Portal**: Show VM status
2. **Start VM if needed**: Demonstrate cloud management
3. **Test again**: Show problem-solving process

### **Step 4: Show Application (If VM is Running)**
```powershell
Invoke-WebRequest -Uri http://172.171.223.227 -TimeoutSec 10
```

---

## 🎉 **Success Scenarios**

### **Perfect Demo:**
- All commands work
- Web application accessible
- All features demonstrated

### **Good Demo (with troubleshooting):**
- Infrastructure working
- Some troubleshooting needed
- Shows real-world problem-solving

### **Learning Demo (with issues):**
- Infrastructure exists
- Troubleshooting demonstrated
- Shows debugging skills
- **This is actually valuable!**

---

## 🎓 **Key Points to Emphasize**

### **1. Infrastructure as Code:**
*"Even when things don't work perfectly, we can see exactly what exists and manage it through code."*

### **2. Cloud Computing:**
*"Cloud resources can be stopped to save money, but we need to restart them when needed."*

### **3. DevOps Practices:**
*"Real-world systems require troubleshooting skills. This is valuable experience."*

### **4. Cost Management:**
*"We can stop VMs to save money, but we need to monitor and restart them when needed."*

---

**🎉 Remember: Troubleshooting is a valuable skill! Use any issues as teaching moments to demonstrate real-world problem-solving.**


