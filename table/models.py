from django.db import models
from django.utils.translation import gettext_lazy as _


# Метод для отображения названия месяца
def display_month_name(month):
    MONTH_CHOICES = {
        1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
        5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
        9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
    }
    return MONTH_CHOICES.get(month, 'Неизвестно')

class City(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Город"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Город")
        verbose_name_plural = _("Города")

class VacancyRecord(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=_("Город"))
    date = models.DateField(verbose_name=_("Дата"))
    vacancies = models.PositiveIntegerField(verbose_name=_("Вакансии"))

    @property
    def month(self):
        return self.date.strftime("%m")

    @property
    def year(self):
        return self.date.year

    def __str__(self):
        return f"{self.city} - {self.date} - {self.vacancies} вакансий"

    class Meta:
        verbose_name = _("Запись вакансии")
        verbose_name_plural = _("Записи вакансий")
        ordering = ['date']

class EmployeeMovement(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=_("Город"))  # Добавлен город
    month = models.PositiveIntegerField(verbose_name=_("Месяц"))
    year = models.PositiveIntegerField(verbose_name=_("Год"))
    hired = models.PositiveIntegerField(default=0, verbose_name=_("Принято"))
    fired = models.PositiveIntegerField(default=0, verbose_name=_("Уволено"))

    def __str__(self):
        return f"{self.city} - {display_month_name(self.month)} {self.year}"


    class Meta:
        verbose_name = _("Движение сотрудников")
        verbose_name_plural = _("Движения сотрудников")
        unique_together = ('city', 'month', 'year')  # Уникальность по городу, месяцу и году


# Вторая таблица

# # Модель для хранения данных о движении сотрудников
# class RecruitmentFunnel(models.Model):
#     # Месяц, к которому относится запись
#     month = models.IntegerField(verbose_name="Месяц")  # Храним месяц как число
#     # Год, к которому относится запись
#     year = models.IntegerField(verbose_name="Год")
    
#     # Метод для получения всех данных для таблицы по заданному месяцу и году
#     def get_table_data(self):
#         # Получаем все записи из модели для данного месяца и года
#         data = self.objects.filter(month=self.month, year=self.year).values()
        
#         # Получаем список заголовков столбцов из базы данных
#         headers = list(data[0].keys())
        
#         # Создаем список для хранения данных таблицы
#         table_data = []
        
#         # Добавляем в список заголовки столбцов
#         table_data.append(headers)
        
#         # Добавляем в список данные из каждой записи в базе данных
#         for item in data:
#             row = list(item.values())
#             table_data.append(row)
        
#         return table_data
    
#     def __str__(self):
#         return f"{display_month_name(self.month)} - {self.year}"

#     class Meta:
#         verbose_name = _("Отчетный период")
#         verbose_name_plural = _("Отчетные периоды")

# # Модель для хранения данных о статусах
# class Status(models.Model):
#     # Название статуса
#     name = models.CharField(max_length=255)
#     # Связь с моделью RecruitmentFunnel (один ко многим)
#     movement = models.ForeignKey(RecruitmentFunnel, on_delete=models.CASCADE, related_name='statuses', verbose_name="Отчетный период")
#     # Значение для данного статуса
#     value = models.IntegerField()
#     class Meta:
#         verbose_name = _("Ячейка воронок")
#         verbose_name_plural = _("Ячейки воронок")

# # Модель для хранения данных о воронке подбора
# class Funnel(models.Model):
#     # Название этапа воронки
#     stage_name = models.CharField(max_length=255)
#     # Связь с моделью RecruitmentFunnel (один ко многим)
#     movement = models.ForeignKey(RecruitmentFunnel, on_delete=models.CASCADE, related_name='funnel_stages', verbose_name="Отчетный период")
#     # Значение для данного этапа
#     value = models.IntegerField()

#     class Meta:
#         verbose_name = _("Название этапа воронки")
#         verbose_name_plural = _("Название этапов воронок")

# # Модель для хранения данных о периодах
# class Period(models.Model):
#     # Начало периода
#     start_date = models.DateField(verbose_name="Дата начала")
#     # Конец периода
#     end_date = models.DateField(verbose_name="Дата окончания")
#     # Связь с моделью RecruitmentFunnel (один ко многим)
#     movement = models.ForeignKey(RecruitmentFunnel, on_delete=models.CASCADE, related_name='periods', verbose_name="Отчетный период")

#     class Meta:
#         verbose_name = _("Период")
#         verbose_name_plural = _("Периоды")



# Вторая таблица

# Модель для хранения данных о движении сотрудников
class RecruitmentFunnel(models.Model):
    # Месяц, к которому относится запись
    month = models.IntegerField(verbose_name="Месяц")  # Храним месяц как число
    # Год, к которому относится запись
    year = models.IntegerField(verbose_name="Год")
    
    # Метод для получения всех данных для таблицы по заданному месяцу и году
    def get_table_data(self):
        # Получаем все записи из модели для данного месяца и года
        data = self.objects.filter(month=self.month, year=self.year).values()
        
        # Получаем список заголовков столбцов из базы данных
        headers = list(data[0].keys())
        
        # Создаем список для хранения данных таблицы
        table_data = []
        
        # Добавляем в список заголовки столбцов
        table_data.append(headers)
        
        # Добавляем в список данные из каждой записи в базе данных
        for item in data:
            row = list(item.values())
            table_data.append(row)
        
        return table_data
    
    def __str__(self):
        return f"{display_month_name(self.month)} - {self.year}"

    class Meta:
        verbose_name = _("Отчетный период")
        verbose_name_plural = _("Отчетные периоды")


class FunnelStage(models.Model):
    """
    Модель для хранения данных о каждой стадии воронки подбора.
    """
    movement = models.ForeignKey(RecruitmentFunnel, on_delete=models.CASCADE, related_name='funnel_stage', verbose_name="Отчетный период")
    name = models.CharField(max_length=100, unique=True, verbose_name="Название строки")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Модель строк")
        verbose_name_plural = _("Строки")

class FunnelData(models.Model):
    """
    Модель для хранения данных о количестве кандидатов на каждой стадии
    воронки подбора для каждой даты.
    """
    movement = models.ForeignKey(RecruitmentFunnel, on_delete=models.CASCADE, related_name='funnel_data', verbose_name="Отчетный период")
    funnel_stage = models.ForeignKey(FunnelStage, on_delete=models.CASCADE, verbose_name="Название столбца")
    date = models.DateField( verbose_name="Дата")
    count = models.IntegerField(default=0, verbose_name="Значение")

    class Meta:
        unique_together = ('funnel_stage', 'date')
        verbose_name = _("Модель столбцов")
        verbose_name_plural = _("Столбцы")

    def __str__(self):
        return f"{self.funnel_stage} - {self.date}: {self.count}"




# Третья таблица. 


class CallRows(models.Model):
    """
    Модель для хранения причин отказа при первичном звонке.
    """
    movement = models.ForeignKey(RecruitmentFunnel, on_delete=models.CASCADE, related_name='call_rows', verbose_name="Отчетный период")
    rows = models.CharField(max_length=100, unique=True, verbose_name="Строка описание причины")

    def __str__(self):
        return self.rows

    class Meta:
        verbose_name = "Модель строк при первом зконке"
        verbose_name_plural = "Строки при первых звонках"


class CallColumns(models.Model):
    """
    Модель для хранения данных о результатах первичных звонков.
    """
    movement = models.ForeignKey(RecruitmentFunnel, on_delete=models.CASCADE, related_name='recruitment_funnel', verbose_name="Отчетный период")
    rows = models.ForeignKey(CallRows, on_delete=models.CASCADE, verbose_name="Название столбца")
    date = models.DateField( verbose_name="Дата")
    columns = models.IntegerField(default=0, verbose_name="Значение")

    class Meta:
        verbose_name = _("Модель столбцов")
        verbose_name_plural = _("Столбцы результатов первичных звонков")

    def __str__(self):
        return f"{self.rows} - {self.date}: {self.columns}"


# Четвертая таблица
# HH Insights - "Справочно: база размещенных вакансий от работодателей и резюме на HH, с охватом всех регионов РФ"


class HhInsights_Rows(models.Model):
    """
    Модель для хранения причин отказа при первичном звонке.
    """
    movement = models.ForeignKey(RecruitmentFunnel, on_delete=models.CASCADE, related_name='HhInsights_rows', verbose_name="Отчетный период")
    rows = models.CharField(max_length=100, unique=True, verbose_name="Строка работодателей и резюме")

    def __str__(self):
        return self.rows

    class Meta:
        verbose_name = "Строка работодателей и резюме на HH"
        verbose_name_plural = "Строки работодателей и резюме на HH"


class HhInsights_Columns(models.Model):
    """
    Модель для хранения данных о результатах первичных звонков.
    """
    movement = models.ForeignKey(RecruitmentFunnel, on_delete=models.CASCADE, related_name='HhInsights_Columns', verbose_name="Отчетный период")
    rows = models.ForeignKey(HhInsights_Rows, on_delete=models.CASCADE, verbose_name="Столбец работодателей и резюме")
    date = models.DateField( verbose_name="Дата")
    columns = models.IntegerField(default=0, verbose_name="Значение")

    class Meta:
        verbose_name = _("Модель столбцов работодателей и резюме на HH")
        verbose_name_plural = _("Столбцы работодателей и резюме на HH")

    def __str__(self):
        return f"{self.rows} - {self.date}: {self.columns}"



