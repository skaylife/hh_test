from django.contrib import admin
from .models import City, VacancyRecord, EmployeeMovement, RecruitmentFunnel, FunnelData, FunnelStage, CallRows, CallColumns, HhInsights_Rows, HhInsights_Columns, display_month_name

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(VacancyRecord)
class VacancyRecordAdmin(admin.ModelAdmin):
    list_display = ('city', 'date', 'vacancies')

@admin.register(EmployeeMovement)
class EmployeeMovementAdmin(admin.ModelAdmin):
    list_display = ('city', 'display_month_name', 'year', 'hired', 'fired')
    # Если вы хотите, чтобы поле 'display_month_name' было отформатировано в списке, используйте следующий метод:
    def display_month_name(self, obj):
        return display_month_name(obj.month)
    display_month_name.short_description = 'Месяц'


@admin.register(RecruitmentFunnel)
class RecruitmentFunnelAdmin(admin.ModelAdmin):
    list_display = ('display_month_name', 'year')
    def display_month_name(self, obj):
        return display_month_name(obj.month)
    display_month_name.short_description = 'Месяц'

@admin.register(FunnelData)
class FunnelDataAdmin(admin.ModelAdmin):
    list_display = ('movement', 'funnel_stage', 'date', 'count')
    
    # Метод для отображения названия стадии
    def funnel_stage(self, obj):
        return obj.funnel_stage.name
    funnel_stage.short_description = 'Стадия'

    # Метод для отображения названия отчетного периода
    def movement(self, obj):
        return obj.movement.display_month_name
    movement.short_description = 'Отчетный период'

@admin.register(FunnelStage)
class FunnelStageAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(CallRows)
class CallRowsAdmin(admin.ModelAdmin):
    list_display = ('movement', 'get_rows')  # Use 'get_rows' instead of 'rows'
    
    def get_rows(self, obj):
        return obj.rows

    get_rows.short_description = 'Причина отказа' 
@admin.register(CallColumns)
class CallColumnsAdmin(admin.ModelAdmin):
    list_display = ('movement', 'date', 'rows', 'columns')


# Четвертая таблица 
@admin.register(HhInsights_Rows)
class HhInsights_RowsAdmin(admin.ModelAdmin):
    list_display = ('movement', 'get_rows')  
    
    def get_rows(self, obj):
        return obj.rows

    get_rows.short_description = 'Работодатели и резюме на HH' 

@admin.register(HhInsights_Columns)
class HhInsights_ColumnsAdmin(admin.ModelAdmin):
    list_display = ('movement', 'get_date', 'rows', 'columns')

    def get_date(self, obj):
        return obj.date
    get_date.short_description = 'Дата'

    def columns(self, obj):
        return obj.columns
    columns.short_description = 'Значение'



# @admin.register(Status)
# class StatusAdmin(admin.ModelAdmin):
#     list_display = ('name', 'movement', 'value')

# @admin.register(Funnel)
# class FunnelAdmin(admin.ModelAdmin):
#     list_display = ('stage_name', 'movement', 'value')

# @admin.register(Period)
# class PeriodAdmin(admin.ModelAdmin):
#     list_display = ('start_date', 'end_date', 'movement')
