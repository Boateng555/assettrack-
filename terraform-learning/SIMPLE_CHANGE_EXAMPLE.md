# 🎯 Simple Terraform Change Example

## 🚀 **Easy Change You Can Make: Add Tags**

### **What We'll Do:**
Add tags to your virtual machine to demonstrate how Terraform plan and apply work.

---

## 📝 **Step 1: Make a Small Change**

### **Edit your main.tf file:**
Find the virtual machine resource and add some tags:

```hcl
resource "azurerm_linux_virtual_machine" "main" {
  name                = "vm-terraform-learning"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  size                = "Standard_B2s"
  admin_username      = "azureuser"

  # Add these tags to your VM
  tags = {
    Environment = "Learning"
    Project     = "Terraform Automation"
    CreatedBy   = "Student"
    Status      = "Active"
    LastUpdated = "2024-01-15"
    Purpose     = "Assignment Demo"  # <-- Add this new tag
  }

  # ... rest of your configuration ...
}
```

---

## 🚀 **Step 2: Run Terraform Plan**

```powershell
terraform plan
```

**What you'll see:**
```
# azurerm_linux_virtual_machine.main will be updated in-place
  ~ resource "azurerm_linux_virtual_machine" "main" {
      ~ tags = {
          + Purpose     = "Assignment Demo"
            # ... other tags will show as unchanged
        }
    }

Plan: 0 to add, 1 to change, 0 to destroy.
```

**This shows:**
- ✅ **1 resource will be updated** (your VM)
- ✅ **Only the new tag will be added**
- ✅ **No resources will be destroyed**
- ✅ **No new resources will be created**

---

## 🚀 **Step 3: Apply the Change**

```powershell
terraform apply
```

**What will happen:**
1. Terraform will show the same plan
2. It will ask: "Do you want to perform these actions?"
3. Type `yes` and press Enter
4. Terraform will update your VM with the new tag

**Expected output:**
```
azurerm_linux_virtual_machine.main: Modifying... [id=/subscriptions/.../vm-terraform-learning]
azurerm_linux_virtual_machine.main: Modifications complete after 2s [id=/subscriptions/.../vm-terraform-learning]

Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
```

---

## 🎯 **Step 4: Verify the Change**

```powershell
# Check the current state
terraform show azurerm_linux_virtual_machine.main

# Or run plan again to see no changes
terraform plan
```

**You should see:**
- ✅ **No changes. Your infrastructure matches the configuration.**
- ✅ **The new tag is now in your VM**

---

## 🎓 **What This Demonstrates**

### **1. Infrastructure as Code:**
- **Code defines infrastructure**: You changed the code
- **Version control**: The change is tracked
- **Reproducibility**: Anyone can see what changed

### **2. Terraform Workflow:**
- **Plan**: See what will change before applying
- **Apply**: Make the changes to infrastructure
- **State**: Track what exists vs what should exist

### **3. System Administration:**
- **Change management**: Plan before applying
- **Infrastructure management**: Programmatic control
- **Documentation**: Code serves as documentation

---

## 🚀 **Other Simple Changes You Can Try**

### **Change 1: VM Size**
```hcl
# Change from Standard_B2s to Standard_B4s
size = "Standard_B4s"
```

### **Change 2: Add More Tags**
```hcl
tags = {
  Environment = "Learning"
  Project     = "Terraform Automation"
  CreatedBy   = "Student"
  Status      = "Active"
  LastUpdated = "2024-01-15"
  Purpose     = "Assignment Demo"
  Course      = "System Administration"  # <-- Add this
  Semester    = "Fall 2024"             # <-- Add this
}
```

### **Change 3: VM Name**
```hcl
# Change the VM name
name = "vm-terraform-learning-updated"
```

---

## 🎯 **Perfect for Your Assignment**

### **What You Can Demonstrate:**
1. **Show the problem**: Manual changes are time-consuming
2. **Show the solution**: Code-based changes are fast
3. **Demonstrate plan**: See what will change
4. **Demonstrate apply**: Make the changes
5. **Show benefits**: Time savings, consistency, documentation

### **Key Teaching Points:**
- *"I can modify infrastructure by editing code"*
- *"Plan shows exactly what will change"*
- *"Apply makes the changes to infrastructure"*
- *"Everything is tracked and documented"*

---

## 🎉 **Success Metrics**

### **Perfect Demonstration:**
- ✅ Show the change in code
- ✅ Run `terraform plan` to show what will change
- ✅ Run `terraform apply` to make the change
- ✅ Show that the change was applied
- ✅ Run `terraform plan` again to show no changes

### **Learning Outcomes:**
- ✅ Understand how Terraform works
- ✅ Demonstrate automation skills
- ✅ Show change management process
- ✅ Explain Infrastructure as Code benefits

---

**🎓 Remember: This simple example shows the power of Infrastructure as Code. You can make changes by editing code, see exactly what will change, and apply those changes programmatically!**


