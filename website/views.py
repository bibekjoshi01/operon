from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from website.forms import TenantRegistrationForm
from tenants.models import Tenant, Domain


def home(request):
    """Homepage view for the SaaS app."""
    return render(request, "home.html")


def register_tenant(request):
    """Register a new tenant/organization."""
    if request.method == "POST":
        form = TenantRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Create the tenant
                tenant = Tenant.objects.create(
                    schema_name=form.cleaned_data["subdomain"],
                    name=form.cleaned_data["organization_name"],
                    subdomain=form.cleaned_data["subdomain"],
                    is_active=True,
                )

                # Create domain mapping
                domain = Domain.objects.create(
                    domain=f"{form.cleaned_data['subdomain']}.localhost",
                    tenant=tenant,
                    is_primary=True,
                )

                # Set tenant for creating user in tenant schema
                from django_tenants.utils import tenant_context

                # Create admin user for the tenant
                with tenant_context(tenant):
                    admin_user = User.objects.create_user(
                        username=form.cleaned_data["admin_username"],
                        email=form.cleaned_data["admin_email"],
                        password=form.cleaned_data["admin_password"],
                        is_staff=True,
                        is_superuser=True,
                    )

                # Store registration details to display confirmation
                request.session["registration_success"] = {
                    "organization": tenant.name,
                    "subdomain": tenant.subdomain,
                    "username": admin_user.username,
                    "email": admin_user.email,
                }

                return redirect("registration_success")

            except Exception as e:
                messages.error(request, f"Error creating tenant: {str(e)}")
    else:
        form = TenantRegistrationForm()

    return render(request, "register.html", {"form": form})


def registration_success(request):
    """Display registration success page with login credentials."""
    registration_data = request.session.get("registration_success")

    if not registration_data:
        return redirect("register_tenant")

    # Clear the session data after displaying
    del request.session["registration_success"]
    request.session.save()

    return render(
        request,
        "registration_success.html",
        {
            "organization": registration_data["organization"],
            "subdomain": registration_data["subdomain"],
            "username": registration_data["username"],
            "email": registration_data["email"],
        },
    )
