from django.shortcuts import render, redirect
from .models import City, VacancyRecord, EmployeeMovement, display_month_name, RecruitmentFunnel, FunnelStage, FunnelData, CallColumns, HhInsights_Rows, HhInsights_Columns
from django.http import JsonResponse
import pprint
from collections import defaultdict
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext as _


from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class CustomAdminLoginView(LoginView):
    template_name = 'admin/login.html'
    redirect_authenticated_user = True


from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def custom_admin_login(request):
    if request.method == 'POST':
        logger.debug(f"CSRF token received: {request.POST.get('csrfmiddlewaretoken')}")
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin:index')
        else:
            return render(request, 'admin/login.html', {'error': 'Invalid credentials'})
    logger.debug(f"CSRF token passed to template: {request.csrf_token}")
    return render(request, 'admin/login.html', {'csrf_token': request.csrf_token})

@csrf_exempt
def index(request):

    # recruitment_funnel_view(request=request) # Вызов второй таблицы 

    
    if request.method == "POST":
        city_id = request.POST.get('city')
        date = request.POST.get('date')
        vacancies = request.POST.get('vacancies')
        hired = request.POST.get('hired')
        fired = request.POST.get('fired')

        if city_id and date and vacancies:
            VacancyRecord.objects.create(
                city_id=city_id,
                date=date,
                vacancies=vacancies
            )

        if hired is not None and fired is not None:
            month = int(request.POST.get('month'))
            year = int(request.POST.get('year'))
            EmployeeMovement.objects.update_or_create(
                city_id=city_id,  # Добавьте city_id сюда
                month=month,
                year=year,
                defaults={'hired': hired, 'fired': fired}
            )
        
        return redirect('index')


    cities = City.objects.all()
    vacancy_records = VacancyRecord.objects.all()
    employee_movements = EmployeeMovement.objects.all()
    # funnel_data = FunnelData.objects.all()
    # movements = RecruitmentFunnel.objects.all()
    # funnel_stage = FunnelStage.objects.all()


    vacancy_records_by_date = defaultdict(list)
    for record in vacancy_records:
        vacancy_records_by_date[record.date.strftime('%d-%m')].append(record)
        # print(vacancy_records_by_date)

    # Создаем таблицу с объединенными записями
    table_data = []
    for city in cities:
        city_data = {'name': city.name}
        for date, records in vacancy_records_by_date.items():
            total_vacancies = sum([record.vacancies for record in records if record.city == city])
            city_data[date] = total_vacancies
        # Находим соответствующую запись в employee_movements
        movement = next(
            (m for m in employee_movements if m.city == city),
            None  # Возвращаем None, если запись не найдена
        )

        # Добавляем информацию о приеме и увольнении
        if movement:
            city_data['Принято'] = movement.hired
            city_data['Уволено'] = movement.fired

        table_data.append(city_data)
    
    monthYears = []
    seen_months = set()  # Используем множество для отслеживания уже добавленных месяцев

    for employee_movement in employee_movements:
        month = {}
        month_name = display_month_name(employee_movement.month)
        month['month_number'] = employee_movement.month
        month['month_name'] = month_name
        month['years'] = employee_movement.year

        # Проверяем, встречался ли этот месяц уже
        month_key = (month['month_number'], month['month_name'], month['years'])  # Ключ для проверки уникальности
        if month_key not in seen_months:
            monthYears.append(month)
            seen_months.add(month_key)

    # print(monthYears)
    # print(table_data)

    MONTH_CHOICES = {
        1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
        5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
        9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
    }
    

    # Создаем таблицы для движения сотрудников

    table_data2 = []

    # for movement in movements:
    #     funnel_data = []
    #     # print(f"{display_month_name(movement.month)} {movement.year}")
    #     data = {
    #         "reporting_period" : f"{display_month_name(movement.month)} {movement.year}",
    #         "rows": [],
    #         "columns": [],
    #         "date": [],
    #     }

    #     for item in FunnelData.objects.all():
    #         obj = {
    #             "rows": item.funnel_stage.name,
    #             item.date.strftime("%d-%m"): item.count,
    #         }
    #         data["rows"].append(item.funnel_stage.name)
    #         data["date"].append(item.date.strftime("%d-%m")) # Форматирование даты в строку
    #         data["columns"].append(item.count)
    #         print(obj)
    #         # print(item.count)
    #     data["date"] = list(set([str(d) for d in data["date"]])) # Удаление дубликатов и преобразование в строки
    #     data["rows"] = list(set([str(d) for d in data["rows"]])) # Удаление дубликатов и преобразование в строки
    #     # data["columns"] = list(set([str(d) for d in data["columns"]])) # Удаление дубликатов и преобразование в строки
    #     table_data2.append(data)

    movements = RecruitmentFunnel.objects.all()
    funnel_stages = FunnelStage.objects.all()
    funnel_data = FunnelData.objects.all()

    final_table_data = defaultdict(lambda: defaultdict(str))
    table_data2 = []


    funnel_data_by_date = defaultdict(list)
    for record in funnel_data:
        funnel_data_by_date[record.date.strftime('%d-%m')].append(record)
        # print(funnel_data_by_date.date)
    # print(funnel_data_by_date)
    
    
    # for el in funnel_data:
        # data = [el.date]
        # data["date"] = list(set([str(d) for d in data["date"]])) # Удаление дубликатов и преобразование в строки
        # print(el.date.item())

    for movement in movements:
        add_period = {}
        # Получаем данные только для текущего movement
        current_funnel_data = funnel_data.filter(movement=movement)
        add_period["reporting_period"] = f"{display_month_name(movement.month)} {movement.year}"
        table_data2.append(add_period)
        for stage in funnel_stages:
            for data_point in current_funnel_data.filter(funnel_stage=stage):
                # Форматируем дату в строку "YYYY-MM-DD"
                date_str = data_point.date.strftime("%Y-%m-%d")

                # Сохраняем данные в таблицу
                final_table_data[stage.name][date_str] = str(data_point.count)  # Преобразуем count в строку

    # Преобразуем словарь в список словарей для удобства отображения
    
    for stage_name, stage_data in final_table_data.items():
        row = {'rows': stage_name}
        row.update(stage_data)  # Объединяем данные о датах и значениях
        table_data2.append(row)






# таблица 3


    call_columns = CallColumns.objects.all()
    # print(call_columns.dates)

    final_table_data3 = defaultdict(lambda: defaultdict(str))
    table_data3 = []

    call_data_by_date = defaultdict(list)
    for record in call_columns:
        call_data_by_date[record.date.strftime('%d-%m')].append(record)

    # print(call_data_by_date)

    for movement in movements:
        add_period = {}
        # Получаем данные только для текущего movement
        current_call_columns = call_columns.filter(movement=movement)
        add_period["reporting_period"] = f"{display_month_name(movement.month)} {movement.year}"
        table_data3.append(add_period)
        for call in call_columns:
            for data_point in current_call_columns.filter(rows=call.rows):
                # Форматируем дату в строку "YYYY-MM-DD"
                date_str = data_point.date.strftime("%Y-%m-%d")

                # Сохраняем данные в таблицу
                final_table_data3[call.rows][date_str] = str(data_point.columns)  # Преобразуем count в строку

    # Преобразуем словарь в список словарей для удобства отображения
    for rows, stage_data in final_table_data3.items():
        row = {'rows': rows}  # Используем call.rows
        row.update(stage_data)  # Объединяем данные о датах и значениях
        table_data3.append(row)



# Четвертая таблица 


    hh_insights_columns = HhInsights_Columns.objects.all()
    # print(call_columns.dates)

    final_table_data4 = defaultdict(lambda: defaultdict(str))
    table_data4 = []

    hh_insights_columns_by_date = defaultdict(list)
    for record in hh_insights_columns:
        hh_insights_columns_by_date[record.date.strftime('%d-%m')].append(record)

    # print(call_data_by_date)

    for movement in movements:
        add_period = {}
        # Получаем данные только для текущего movement
        current_hh_insights_columns = hh_insights_columns.filter(movement=movement)
        add_period["reporting_period"] = f"{display_month_name(movement.month)} {movement.year}"
        table_data4.append(add_period)
        for call in hh_insights_columns:
            for data_point in current_hh_insights_columns.filter(rows=call.rows):
                # Форматируем дату в строку "YYYY-MM-DD"
                date_str = data_point.date.strftime("%Y-%m-%d")

                # Сохраняем данные в таблицу
                final_table_data4[call.rows][date_str] = str(data_point.columns)  # Преобразуем count в строку

    # Преобразуем словарь в список словарей для удобства отображения
    for rows, stage_data in final_table_data4.items():
        row = {'rows': rows}  # Используем call.rows
        row.update(stage_data)  # Объединяем данные о датах и значениях
        table_data4.append(row)


    
    # print(table_data3)

            # print(stage_data)
        #     stage_data = {}
        #     for date in dates:
        #         count = current_funnel_data.filter(funnel_stage=stage, date=date).values_list('count', flat=True).first() or 0
        #         stage_data[date.strftime("%d-%m")] = count
        #         stage_data = {'name': stage.name, **stage_data}
        #         movement_data.update(stage_data)

        # table_data2.append(movement_data)

    # print(table_data2)


        
    # print(table_data2)
    #     # Цикл по данным воронки
    #     for item in FunnelData.objects.all():
    #         # Создаем словарь для каждой стадии воронки
    #         funnel_stage_data = {
    #             "rows": item.funnel_stage,
    #             "date": item.date,
    #             "columns": item.count,
    #         }
    #         # Добавляем данные воронки к данным движения    
    #         print("funnel_stage_data ", funnel_stage_data)
    #         data.update(funnel_stage_data)

    #     funnel_data.append(data)
    #     print("funnel_data", funnel_data)

    #     # print(data)
    # print("table_data2 ", table_data2)

    # for item in funnel_data:
    #     # date_str = item['date']
    #     # count_str = item['count']

    #     data = {
    #         "reporting_period" : f"{display_month_name(item.movement.month)} {item.movement.year}",
    #         "rows": item.funnel_stage.name,
    #         "date": item.date,
    #         "columns": item.count,
    #     }
    #     # print("---_---")
    #     # print(data)
    #     table_data2.append(data)
    # print(table_data)
    # print(table_data2)

    # for el in table_data2:
    #     # print(el.items())
    #     for date, count in el.items():
    #         print(count)

    # for city in table_data:
        # print(city.items())
        # for date, vacancies in city.items():
        #     print(vacancies)

            #         {% for date, vacancies in city.items %}
            #   {% if date != 'name' %}
            #     <td>{{ vacancies }}</td>
            #   {% endif %}
            # {% endfor %}

    context = {
        'cities': cities,
        'vacancy_records': vacancy_records_by_date,
        'employee_movements': employee_movements,
        'table_data': table_data,
        'monthYears': monthYears[0], 
        'MONTH_CHOICES': MONTH_CHOICES.items(),
        'table_data2': table_data2,
        'funnel_stages': funnel_stages,
        'funnel_data': funnel_data_by_date,
        'table_data3': table_data3,
        'call_date': call_data_by_date,
        'table_data4': table_data4,
        'hh_insights_by_date': hh_insights_columns_by_date
    }

    return render(request, 'index.html', context)












def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

from .models import HhInsights_Columns, HhInsights_Rows

def serialize_rows(rows):
    """
    Convert HhInsights_Rows objects to a list of dictionaries.
    """
    return [
        {
            'id': row.id,  # Извлекаем идентификатор строки
            'rows': row.rows,  # Извлекаем значение строки (предполагается, что 'rows' является полем в HhInsights_Rows)
        }
        for row in rows  # Для каждой строки в переданном списке строк
    ]

def data_api(request):
    # Получаем все объекты HhInsights_Columns, отсортированные по дате
    data_points = HhInsights_Columns.objects.all().order_by('date')  # Сортировка по дате
    
    # Удаляем дубликаты из имен
    unique_names = []  # Список для уникальных имен
    seen = set()  # Множество для отслеживания уже встреченных имен
    for dp in data_points:  # Для каждого объекта HhInsights_Columns
        if dp.rows.rows not in seen:  # Если имя еще не встречалось
            seen.add(dp.rows.rows)  # Добавляем имя в множество
            unique_names.append({
                'id': dp.rows.id,  # Извлекаем идентификатор строки
                'rows': dp.rows.rows  # Извлекаем значение строки
            })
    
    # Группируем данные по дате и имени
    grouped_data = defaultdict(lambda: defaultdict(list))  # Создаем вложенный словарь для группировки данных
    for dp in data_points:  # Для каждого объекта HhInsights_Columns
        grouped_data[dp.date.isoformat()][dp.rows.rows].append(dp.columns)  # Группируем значения по дате и имени
    
    # Подготавливаем данные для Chart.js
    dates = sorted(grouped_data.keys())  # Получаем и сортируем ключи (даты)
    values = []  # Список для значений
    
    # Формируем значения в нужном порядке
    for name in unique_names:  # Для каждого уникального имени
        for date in dates:  # Для каждой даты
            values.append(sum(grouped_data[date].get(name['rows'], [0])))  # Суммируем значения для дубликатов и добавляем в список значений
    
    # Формируем данные для ответа
    data = {
        'names': unique_names,  # Уникальные имена
        'dates': dates,  # Отсортированные даты
        'values': values  # Суммированные значения
    }
    
    # Возвращаем данные в формате JSON
    return JsonResponse(data)

def data_api2(request):
    # Получаем все объекты FunnelData, отсортированные по дате
    data_points = FunnelData.objects.all().order_by('date')  # Сортировка по дате
    
    # Удаляем дубликаты из имен
    unique_names = []  # Список для уникальных имен
    seen = set()  # Множество для отслеживания уже встреченных имен
    for dp in data_points:  # Для каждого объекта FunnelData
        if dp.funnel_stage.name not in seen:  # Если имя еще не встречалось
            seen.add(dp.funnel_stage.name)  # Добавляем имя в множество
            unique_names.append({
                'id': dp.funnel_stage.id,  # Извлекаем идентификатор строки
                'rows': dp.funnel_stage.name  # Извлекаем значение строки
            })
    
    # Группируем данные по дате и имени
    grouped_data = defaultdict(lambda: defaultdict(list))  # Создаем вложенный словарь для группировки данных
    for dp in data_points:  # Для каждого объекта FunnelData
        grouped_data[dp.date.isoformat()][dp.funnel_stage.name].append(dp.count)  # Группируем значения по дате и имени
    
    # Подготавливаем данные для Chart.js
    dates = sorted(grouped_data.keys())  # Получаем и сортируем ключи (даты)
    values = []  # Список для значений
    
    # Формируем значения в нужном порядке
    for name in unique_names:  # Для каждого уникального имени
        for date in dates:  # Для каждой даты
            values.append(sum(grouped_data[date].get(name['rows'], [0])))  # Суммируем значения для дубликатов и добавляем в список значений
    
    # Формируем данные для ответа
    data = {
        'names': unique_names,  # Уникальные имена
        'dates': dates,  # Отсортированные даты
        'values': values  # Суммированные значения
    }
    
    # Возвращаем данные в формате JSON
    return JsonResponse(data)







# def display_month_name(month):
#     month_names = {
#         1: _("Январь"),
#         2: _("Февраль"),
#         3: _("Март"),
#         4: _("Апрель"),
#         5: _("Май"),
#         6: _("Июнь"),
#         7: _("Июль"),
#         8: _("Август"),
#         9: _("Сентябрь"),
#         10: _("Октябрь"),
#         11: _("Ноябрь"),
#         12: _("Декабрь"),
#     }
#     return month_names.get(month, _("Неизвестный месяц"))




# def recruitment_funnel_view(request):
#     """
#     Представление для отображения данных о движении сотрудников.
#     """
#     movements = RecruitmentFunnel.objects.all()
#     funnel_stage = FunnelStage.objects.all()
#     funnel_data = FunnelData.objects.all()

#     # Получаем все отчетные периоды
#     periods = RecruitmentFunnel.objects.all().values('month', 'year').distinct()
    
#     table_data2 = []
#     # for period in periods:
#     #     # Получаем данные для каждого отчетного периода
#     #     funnel_data_for_period = FunnelData.objects.filter(
#     #         movement__month=period['month'], movement__year=period['year']
#     #     )
        
#     #     # Создаем структуру данных для текущего периода
#     #     period_data = {
#     #         'name': f"{display_month_name(period['month'])} - {period['year']}", 
#     #     }

#     #     # Добавляем данные по столбцам
#     #     for stage in funnel_stage:
#     #         stage_name = stage.name
#     #         stage_data = funnel_data_for_period.filter(funnel_stage=stage).values('date', 'count')
#     #         for item in stage_data:
#     #             period_data["rows"] = stage.name
#     #             # print(period_data)


#     #     # Добавляем данные "Принято" и "Уволено"
#     #     # ... (Здесь вам нужно добавить логику для получения этих данных)
#     #     # ...

#     #     table_data.append(period_data)

#     for item in funnel_data:
#         # date_str = item['date']
#         # count_str = item['count']

#         data = {
#             "reporting_period" : f"{display_month_name(item.movement.month)} {item.movement.year}",
#             "rows": item.funnel_stage.name,
#             "date": item.date,
#             "columns": item.count,
#         }
#         # print("---_---")
#         # print(data)
#         table_data2.append(data)
#         # period_data[date_str] = item['count']

#     # print(table_data2)
#     # Передача данных в контекст
#     context = {
#         'table_data2': table_data2,
#     }
#     # # Форма для добавления данных
#     # if request.method == 'POST':
#     #     selected_movement_id = request.POST.get('movement_id')
#     #     funnel_stage_id = request.POST.get('funnel_stage')
#     #     date = request.POST.get('date')
#     #     count = request.POST.get('count')

#     #     if all([selected_movement_id, funnel_stage_id, date, count]):
#     #         try:
#     #             selected_movement = RecruitmentFunnel.objects.get(pk=selected_movement_id)
#     #             funnel_stage = FunnelStage.objects.get(pk=funnel_stage_id)
                
#     #             # Проверка, не существует ли уже записи с такими данными
#     #             if not FunnelData.objects.filter(movement=selected_movement, funnel_stage=funnel_stage, date=date).exists():
#     #                 FunnelData.objects.create(
#     #                     movement=selected_movement,
#     #                     funnel_stage=funnel_stage,
#     #                     date=date,
#     #                     count=count
#     #                 )
#     #                 messages.success(request, _("Данные успешно добавлены."))
#     #             else:
#     #                 messages.error(request, _("Данные с такими параметрами уже существуют."))
#     #         except (RecruitmentFunnel.DoesNotExist, FunnelStage.DoesNotExist):
#     #             messages.error(request, _("Неверные данные."))
#     #         return redirect(reverse('recruitment_funnel') + f'?movement_id={selected_movement_id}')

#     return render(request, 'table2.html', context)
