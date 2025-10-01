# This is our main infrastructure file
# We'll build it step by step to understand automation

# Step 1: Create a Resource Group
# A Resource Group is like a container for all our Azure resources
resource "azurerm_resource_group" "main" {
  name     = "rg-terraform-learning"
  location = "East US"
  
  # Tags help us organize and identify resources
  tags = {
    Environment = "Learning"
    Project     = "Terraform Automation"
    CreatedBy   = "Student"
  }
}

# Step 2: Create a Virtual Network
# A Virtual Network is like a private network in the cloud
resource "azurerm_virtual_network" "main" {
  name                = "vnet-terraform-learning"
  address_space       = ["10.0.0.0/16"]  # This gives us 65,536 IP addresses
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  
  tags = {
    Environment = "Learning"
    Project     = "Terraform Automation"
    CreatedBy   = "Student"
  }
}

# Step 3: Create a Subnet within the Virtual Network
# A Subnet divides our network into smaller, manageable pieces
resource "azurerm_subnet" "main" {
  name                 = "subnet-terraform-learning"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]  # This gives us 254 usable IP addresses
}

# Step 4: Create a Public IP Address
# This gives our VM a public IP so we can access it from the internet
resource "azurerm_public_ip" "main" {
  name                = "pip-terraform-learning"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  allocation_method   = "Static"  # Static IP won't change
  sku                 = "Standard"
  
  tags = {
    Environment = "Learning"
    Project     = "Terraform Automation"
    CreatedBy   = "Student"
  }
}

# Step 5: Create a Network Security Group
# This acts like a firewall to control what traffic can reach our VM
resource "azurerm_network_security_group" "main" {
  name                = "nsg-terraform-learning"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  # Allow SSH access (port 22) from anywhere
  security_rule {
    name                       = "AllowSSH"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Allow HTTP access (port 80) from anywhere
  security_rule {
    name                       = "AllowHTTP"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
  
  tags = {
    Environment = "Learning"
    Project     = "Terraform Automation"
    CreatedBy   = "Student"
  }
}

# Step 6: Create a Network Interface
# This connects our VM to the network
resource "azurerm_network_interface" "main" {
  name                = "nic-terraform-learning"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.main.id
  }
  
  tags = {
    Environment = "Learning"
    Project     = "Terraform Automation"
    CreatedBy   = "Student"
  }
}

# Step 7: Associate Security Group with Subnet
# This applies our firewall rules to the network
resource "azurerm_subnet_network_security_group_association" "main" {
  subnet_id                 = azurerm_subnet.main.id
  network_security_group_id = azurerm_network_security_group.main.id
}

# Step 8: Create the Virtual Machine
# This is our actual server that will run our applications
resource "azurerm_linux_virtual_machine" "main" {
  name                = "vm-terraform-learning"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  size                = "Standard_B2s"  # 2 vCPUs, 4GB RAM
  admin_username      = "azureuser"

  # Disable password authentication for security
  disable_password_authentication = true

  # Use SSH key for authentication
  admin_ssh_key {
    username   = "azureuser"
    public_key = file("C:/Users/kwame.boateng/.ssh/id_rsa.pub")
  }

  # Connect to our network
  network_interface_ids = [azurerm_network_interface.main.id]

  # Configure the operating system disk
  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  # Use Ubuntu 22.04 LTS
  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }
  
  tags = {
    Environment = "Learning"
    Project     = "Terraform Automation"
    CreatedBy   = "Student"
    Status      = "Active"
    LastUpdated = "2024-01-15"
  }
}

# Step 9: Output the Public IP Address
# This shows us the IP address we can use to connect to our VM
output "vm_public_ip" {
  value = azurerm_public_ip.main.ip_address
  description = "The public IP address of the virtual machine"
}
