from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils.html import format_html


class BaseAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "created_by")
    list_display_links = None

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)

        try:
            cl = response.context_data["cl"]

            # inject serial numbers directly into result_list
            for index, obj in enumerate(cl.result_list, start=1):
                obj.serial_number = index

        except Exception:
            pass

        return response

    def serial_number(self, obj):
        return getattr(obj, "serial_number", "-")

    serial_number.short_description = "S.N"

    def edit_action(self, obj):
        url = reverse(f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change", args=[obj.pk])
        return format_html('<a href="{}" title="Edit"><i class="fas fa-edit"></i></a>', url)

    edit_action.short_description = "Edit"

    def save_model(self, request, obj, form, change):
        # Auto assign creator
        if not obj.pk:
            obj.created_by = request.user

        # Permission check
        if not request.user.is_superuser and not request.user.has_perm(
            f"{obj._meta.app_label}.add_{obj._meta.model_name}"
        ):
            raise PermissionDenied("You do not have permission to create this object.")

        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Superuser sees all
        if request.user.is_superuser:
            return qs

        # Normal users → only their data
        return qs.filter(created_by=request.user)

    def has_delete_permission(self, request, obj=...):
        return False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)

        model = db_field.remote_field.model

        if hasattr(model, "is_active"):
            qs = formfield.queryset.filter(is_active=True)

            # 👇 IMPORTANT: include currently selected object
            if request.resolver_match and request.resolver_match.kwargs.get("object_id"):
                obj_id = request.resolver_match.kwargs["object_id"]
                try:
                    current_obj = model.objects.get(pk=obj_id)

                    # include inactive selected value
                    qs = (qs | model.objects.filter(pk=current_obj.pk)).distinct()
                except model.DoesNotExist:
                    pass

            formfield.queryset = qs

        return formfield
