from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Employee(models.Model):
    DEPARTMENTS = [
        ('Engineering', 'Engineering'),
        ('Marketing', 'Marketing'),
        ('Sales', 'Sales'),
        ('HR', 'Human Resources'),
        ('Finance', 'Finance'),
        ('IT', 'Information Technology'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('deleted', 'Deleted'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=50, choices=DEPARTMENTS)
    avatar_url = models.URLField(max_length=500, blank=True, default='https://randomuser.me/api/portraits/men/1.jpg')
    phone = models.CharField(max_length=20, blank=True)
    start_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', help_text="Employee status from Azure AD sync")
    
    # Azure AD Integration Fields
    azure_ad_id = models.CharField(max_length=100, blank=True, null=True, unique=True, help_text="Azure AD User ID")
    azure_ad_username = models.CharField(max_length=200, blank=True, null=True, help_text="Azure AD User Principal Name")
    job_title = models.CharField(max_length=200, blank=True, null=True, help_text="Job title from Azure AD")
    employee_id = models.CharField(max_length=50, blank=True, null=True, help_text="Employee ID from Azure AD")
    last_azure_sync = models.DateTimeField(null=True, blank=True, help_text="Last time data was synced from Azure AD")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.department}"
    
    class Meta:
        ordering = ['name']

class Asset(models.Model):
    ASSET_TYPES = [
        # Hardware Assets
        ('laptop', 'Laptop'),
        ('desktop', 'Desktop'),
        ('tablet', 'Tablet'),
        ('phone', 'Phone'),
        ('monitor', 'Monitor'),
        ('keyboard', 'Keyboard'),
        ('mouse', 'Mouse'),
        ('headphones', 'Headphones'),
        ('printer', 'Printer'),
        ('scanner', 'Scanner'),
        ('server', 'Server'),
        ('network_device', 'Network Device'),
        ('peripheral', 'Peripheral'),
        
        # Software Assets
        ('software_license', 'Software License'),
        ('subscription', 'Software Subscription'),
        ('saas', 'SaaS Application'),
        ('mobile_app', 'Mobile Application'),
        ('cloud_service', 'Cloud Service'),
        ('digital_asset', 'Digital Asset'),
        
        # Other
        ('other', 'Other'),
        ('all', 'All Assets'),  # For filtering purposes
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
        ('lost', 'Lost/Stolen'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    serial_number = models.CharField(max_length=100, unique=True)
    model = models.CharField(max_length=200, blank=True, null=True)
    manufacturer = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_assets')
    purchase_date = models.DateField(null=True, blank=True)
    warranty_expiry = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    # Azure AD Integration Fields
    azure_ad_id = models.CharField(max_length=100, blank=True, null=True, unique=True, help_text="Azure AD Device ID")
    operating_system = models.CharField(max_length=50, blank=True, null=True, help_text="Operating system from Azure AD")
    os_version = models.CharField(max_length=50, blank=True, null=True, help_text="OS version from Azure AD")
    last_azure_sync = models.DateTimeField(null=True, blank=True, help_text="Last time data was synced from Azure AD")
    azure_last_signin = models.DateTimeField(null=True, blank=True, help_text="Last sign-in date from Azure AD")
    
    # Health Score Field
    health_score = models.IntegerField(null=True, blank=True, help_text="Asset health score (0-100)")
    
    # Software Asset Fields
    license_key = models.CharField(max_length=200, blank=True, null=True, help_text="Software license key")
    license_type = models.CharField(max_length=50, blank=True, null=True, help_text="License type (perpetual, subscription, etc.)")
    version = models.CharField(max_length=50, blank=True, null=True, help_text="Software version")
    vendor = models.CharField(max_length=200, blank=True, null=True, help_text="Software vendor/developer")
    subscription_end = models.DateField(null=True, blank=True, help_text="Subscription expiry date")
    seats = models.IntegerField(null=True, blank=True, help_text="Number of seats/licenses")
    used_seats = models.IntegerField(null=True, blank=True, help_text="Number of seats currently in use")
    
    # Permission Fields
    can_delete = models.BooleanField(default=False, help_text="Whether this asset can be deleted by non-admin users")
    deletion_restricted = models.BooleanField(default=True, help_text="Whether deletion is restricted to admin users only")
    
    # Maintenance Fields
    maintenance_start_date = models.DateField(null=True, blank=True, help_text="Date when maintenance started")
    maintenance_expected_end = models.DateField(null=True, blank=True, help_text="Expected date when maintenance will be completed")
    maintenance_notes = models.TextField(blank=True, help_text="Notes about the maintenance work being performed")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.serial_number}"
    
    class Meta:
        ordering = ['name']

class Handover(models.Model):
    MODE_CHOICES = [
        ('Screen Sign', 'Screen Sign'),
        ('Paper & Scan', 'Paper & Scan'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Approved', 'Approved'),
        ('Pending Scan', 'Pending Scan'),
        ('Cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    handover_id = models.CharField(max_length=20, unique=True, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='handovers')
    assets = models.ManyToManyField(Asset, through='HandoverAsset')
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='Screen Sign')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    employee_signature = models.TextField(blank=True)  # Store signature data as JSON
    it_signature = models.TextField(blank=True)  # Store signature data as JSON
    employee_acknowledgment = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_handovers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Email tracking
    email_sent = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.handover_id:
            # Generate handover ID like HOV-2023-0065
            year = timezone.now().year
            last_handover = Handover.objects.filter(handover_id__startswith=f'HOV-{year}').order_by('-handover_id').first()
            if last_handover:
                last_number = int(last_handover.handover_id.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            self.handover_id = f'HOV-{year}-{new_number:04d}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.handover_id} - {self.employee.name}"
    
    @property
    def asset_count(self):
        return self.assets.count()
    
    @property
    def asset_list(self):
        return ', '.join([asset.name for asset in self.assets.all()[:3]])
    
    class Meta:
        ordering = ['-created_at']

class HandoverAsset(models.Model):
    handover = models.ForeignKey(Handover, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    condition_before = models.TextField(blank=True)
    condition_after = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['handover', 'asset']

class WelcomePack(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='welcome_packs')
    
    # Employee Information
    employee_password = models.CharField(max_length=200, blank=True, help_text="Temporary password for the employee")
    employee_email = models.EmailField(blank=True, help_text="Employee's email address")
    
    # IT Contact Information
    it_contact_person = models.CharField(max_length=200, blank=True, help_text="Primary IT contact person")
    it_helpdesk_email = models.EmailField(blank=True, help_text="IT Helpdesk email address")
    it_phone_number = models.CharField(max_length=50, blank=True, help_text="IT phone number")
    
    # Teams Information
    teams_username = models.CharField(max_length=200, blank=True, help_text="Employee's Teams username")
    teams_email = models.EmailField(blank=True, help_text="Employee's Teams email")
    
    # Additional Information
    department_info = models.TextField(blank=True, help_text="Department-specific information")
    office_location = models.CharField(max_length=200, blank=True, help_text="Employee's office location")
    start_date = models.DateField(null=True, blank=True, help_text="Employee's start date")
    
    # Email Settings
    email_sent_to_employee = models.BooleanField(default=False)
    email_sent_to_it = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Whether this welcome pack is active")
    notes = models.TextField(blank=True, help_text="Additional notes")
    
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_welcome_packs')
    
    def __str__(self):
        return f"Welcome Pack for {self.employee.name}"
    
    def save(self, *args, **kwargs):
        # Auto-populate employee email if not provided
        if not self.employee_email and self.employee.email:
            self.employee_email = self.employee.email
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-generated_at']
