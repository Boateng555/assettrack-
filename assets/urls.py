from django.urls import path
from . import views

app_name = 'assets'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Admin Dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # User Profile
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    
    # Employee management
    path('employees/', views.employees, name='employees'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/<uuid:employee_id>/', views.employees_detail, name='employees_detail'),
    path('employees/<uuid:employee_id>/edit/', views.edit_employee, name='edit_employee'),
    path('employees/<uuid:employee_id>/delete/', views.delete_employee, name='delete_employee'),
    path('employees/<uuid:employee_id>/handovers/', views.employee_handovers, name='employee_handovers'),
    
    # Asset management
    path('assets/', views.assets, name='assets'),
    path('assets/unassigned/', views.unassigned_assets, name='unassigned_assets'),
    path('assets/assigned/', views.assigned_assets, name='assigned_assets'),
    path('assets/maintenance/', views.maintenance_assets, name='maintenance_assets'),
    path('assets/lost/', views.lost_assets, name='lost_assets'),
    path('assets/retired/', views.retired_assets, name='retired_assets'),
    path('assets/old/', views.old_assets, name='old_assets'),
    
    # Dashboard card views
    path('assets/healthy/', views.healthy_assets, name='healthy_assets'),
    path('assets/new/', views.new_assets_view, name='new_assets'),
    path('assets/attention/', views.attention_assets, name='attention_assets'),
    path('assets/department/<path:department>/', views.department_assets, name='department_assets'),
    
    # Asset search and mark as lost
    path('assets/search-for-missing/', views.search_assets_for_missing, name='search_assets_for_missing'),
    path('assets/<uuid:asset_id>/mark-as-lost/', views.mark_asset_as_lost, name='mark_asset_as_lost'),
    path('assets/add/', views.add_asset, name='add_asset'),
    path('assets/<uuid:asset_id>/', views.assets_detail, name='assets_detail'),
    path('assets/<uuid:asset_id>/edit/', views.edit_asset, name='edit_asset'),
    path('assets/<uuid:asset_id>/delete/', views.delete_asset, name='delete_asset'),

    path('api/barcode-lookup/', views.barcode_lookup, name='barcode_lookup'),
    path('api/ai-recognition/', views.ai_product_recognition, name='ai_product_recognition'),
    
    # Handover management
    path('handovers/', views.handovers, name='handovers'),
    path('handovers/new/', views.new_handover, name='new_handover'),
    path('handovers/<uuid:handover_id>/', views.handover_detail, name='handover_detail'),
    path('handovers/<uuid:handover_id>/edit/', views.edit_handover, name='edit_handover'),
    path('handovers/<uuid:handover_id>/send-email/', views.send_handover_email, name='send_handover_email'),
    path('handovers/<uuid:handover_id>/pdf/', views.handover_pdf, name='handover_pdf'),
    path('handovers/<uuid:handover_id>/approve/', views.approve_handover, name='approve_handover'),
    
    # Welcome pack management
    path('welcome-packs/', views.welcome_packs, name='welcome_packs'),
    path('welcome-packs/add/', views.add_welcome_pack, name='add_welcome_pack'),
    path('welcome-packs/new/', views.new_welcome_pack, name='new_welcome_pack'),
    path('welcome-packs/<uuid:pack_id>/', views.welcome_pack_detail, name='welcome_pack_detail'),
    path('welcome-packs/<uuid:pack_id>/edit/', views.edit_welcome_pack, name='edit_welcome_pack'),
    path('welcome-packs/<uuid:pack_id>/delete/', views.delete_welcome_pack, name='delete_welcome_pack'),
    path('welcome-packs/<uuid:pack_id>/send-email/', views.send_welcome_pack_email, name='send_welcome_pack_email'),
    
    # Azure AD Integration
    path('azure-sync/', views.azure_ad_sync, name='azure_ad_sync'),
    path('azure-status/', views.azure_ad_status_api, name='azure_ad_status_api'),
    
    # API endpoints
    path('api/save-signature/', views.save_signature, name='save_signature'),
    
    # Employee photos
    path('employees/<uuid:employee_id>/photo/', views.employee_photo, name='employee_photo'),
    
    # Privacy Policy
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]
