from django.db import models
# Create your models here.


class InstituteModel(models.Model):
    """ Институт, пример - Инженерно-технический институт """

    name = models.CharField('Название', max_length=500, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Институт'
        verbose_name_plural = 'Институты'


class DirectionModel(models.Model):
    """ Направление, пример - 08.03.01 Строительство """

    name = models.CharField('Название', max_length=500, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'


class GroupModel(models.Model):
    """ Группа, пример - 03_стр_21_О_/(Общая) """

    name = models.CharField('Название', max_length=500, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class TeacherModel(models.Model):
    """ Учитель """

    name = models.CharField('Имя учителя', max_length=500, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'


class PairTimetableModel(models.Model):
    """ Расписание одной пары """

    institute = models.ForeignKey(InstituteModel, models.CASCADE, verbose_name='Институт')
    direction = models.ForeignKey(DirectionModel, models.CASCADE, verbose_name='Направление')
    group = models.ForeignKey(GroupModel, models.CASCADE, verbose_name='Группа')
    title = models.CharField('Название пары', max_length=500)
    type = models.CharField('Тип пары', max_length=500)
    start_time = models.TimeField('Время начала')
    end_time = models.TimeField('Время окончания')
    teacher = models.ForeignKey(TeacherModel, models.CASCADE, verbose_name='Учитель')
    place = models.CharField('Аудитория', max_length=500)
    date = models.DateField('Дата пары')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
