import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from django.contrib import admin
from django.db import models
from django.http import HttpResponse
from django.urls import path
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import CampusChapter, Member


def generate_members_excel_response(queryset, filename_prefix="NABAS_Members"):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Registered Members"
    ws.views.sheetView[0].showGridLines = True

    headers = [
        "Member ID", "Full Name", "First Name", "Last Name", "Middle Name",
        "Gender", "Email", "Phone", "Institution", "Campus Chapter",
        "Faculty", "Department", "Matric Number", "Level", "Blood Group",
        "Date of Birth", "State of Origin", "LGA", "Hometown Division",
        "Verified Status", "Registration Date"
    ]

    header_fill = PatternFill(start_color="0B1A30", end_color="0B1A30", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    border_thin = Border(
        left=Side(style='thin', color='E2E8F0'),
        right=Side(style='thin', color='E2E8F0'),
        top=Side(style='thin', color='E2E8F0'),
        bottom=Side(style='thin', color='E2E8F0')
    )

    ws.append(headers)
    ws.row_dimensions[1].height = 28

    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment
        cell.border = border_thin

    zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    regular_font = Font(name="Calibri", size=10)

    for row_idx, member in enumerate(queryset, start=2):
        reg_date_str = member.registered_at.strftime("%Y-%m-%d %H:%M") if member.registered_at else ""
        dob_str = member.date_of_birth.strftime("%Y-%m-%d") if member.date_of_birth else ""
        chapter_str = str(member.chapter) if member.chapter else ""
        verified_str = "Verified" if member.is_verified else "Pending"

        row_data = [
            member.id_number,
            member.full_name,
            member.first_name,
            member.last_name,
            member.middle_name,
            member.get_gender_display() if hasattr(member, 'get_gender_display') else member.gender,
            member.email,
            member.phone,
            member.institution,
            chapter_str,
            member.faculty,
            member.department,
            member.matric_number,
            member.get_level_display() if hasattr(member, 'get_level_display') else member.level,
            member.blood_group,
            dob_str,
            member.state_of_origin,
            member.lga,
            member.hometown_division,
            verified_str,
            reg_date_str
        ]
        ws.append(row_data)
        ws.row_dimensions[row_idx].height = 20

        is_even = (row_idx % 2 == 0)
        for col_idx in range(1, len(row_data) + 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.font = regular_font
            cell.border = border_thin
            if is_even:
                cell.fill = zebra_fill
            if col_idx in [1, 6, 13, 14, 15, 16, 20, 21]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")

    for col in ws.columns:
        col_letter = col[0].column_letter
        max_len = 0
        for cell in col:
            val_str = str(cell.value or '')
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = f'attachment; filename="{filename_prefix}_{timestamp}.xlsx"'
    wb.save(response)
    return response


@admin.register(CampusChapter)
class CampusChapterAdmin(admin.ModelAdmin):
    list_display = ('institution_code', 'institution_name', 'president_name', 'members_count', 'is_active')
    list_filter = ('is_active', 'state')
    search_fields = ('institution_name', 'institution_code', 'president_name')
    prepopulated_fields = {'slug': ('institution_code',)}
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')},
    }


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    change_list_template = "admin/members/member/change_list.html"
    list_display = ('id_number', 'full_name', 'institution', 'department', 'level', 'phone', 'is_verified', 'registered_at')
    list_filter = ('is_verified', 'institution', 'level', 'gender')
    search_fields = ('id_number', 'first_name', 'last_name', 'email', 'phone', 'matric_number')
    readonly_fields = ('id_number', 'registered_at')
    actions = ['export_selected_members_to_excel']

    @admin.action(description="Export Selected Members to Excel (.xlsx)")
    def export_selected_members_to_excel(self, request, queryset):
        return generate_members_excel_response(queryset, filename_prefix="NABAS_Selected_Members")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-all-excel/', self.admin_site.admin_view(self.export_all_members_view), name='members_member_export_all_excel'),
        ]
        return custom_urls + urls

    def export_all_members_view(self, request):
        queryset = self.get_queryset(request)
        return generate_members_excel_response(queryset, filename_prefix="NABAS_All_Registered_Members")

