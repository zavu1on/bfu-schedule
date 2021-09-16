from json import loads, load
from datetime import datetime, timedelta, time
from dateutil.relativedelta import relativedelta
from copy import deepcopy
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.shortcuts import render, redirect
from Schedule.settings import KEY_PASSWORD
from .forms import GroupForm, TeacherForm, ChooseGroupForm
from .models import InstituteModel, DirectionModel, GroupModel, TeacherModel, PairTimetableModel
from .service import get_week, get_button, get_month, get_pair_times
# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class AddTimetableView(View):

    def post(self, request: WSGIRequest):
        body = loads(request.body.decode('utf8'))

        if body['key_pass'] != KEY_PASSWORD:
            return HttpResponseForbidden('KeyPass is wrong!'.encode('utf8'))

        InstituteModel.objects.all().delete()
        DirectionModel.objects.all().delete()
        GroupModel.objects.all().delete()
        TeacherModel.objects.all().delete()
        PairTimetableModel.objects.all().delete()

        for _institute, institute in body['data'].items():
            i = InstituteModel.objects.get_or_create(name=_institute)
            if type(i) == tuple:
                i = i[0]

            for _direction, direction in institute.items():
                d = DirectionModel.objects.get_or_create(name=_direction)
                if type(d) == tuple:
                    d = d[0]

                for _group, group in direction.items():
                    _group, subgroup = _group.replace('/', '|').split('(')
                    subgroup = subgroup.replace(')', '')
                    g = GroupModel.objects.get_or_create(name=_group)
                    if type(g) == tuple:
                        g = g[0]

                    for timetable in group:

                        t = TeacherModel.objects.get_or_create(name=timetable['teacher'])
                        if type(t) == tuple:
                            t = t[0]

                        PairTimetableModel.objects.create(
                            institute=i,
                            direction=d,
                            group=g,
                            subgroup=subgroup,
                            teacher=t,
                            title=timetable['title'],
                            type=timetable['type'],
                            start_time=timetable['startTime'],
                            end_time=timetable['endTime'],
                            place=timetable['place'],
                            date=timetable['date'].split('T')[0]
                        )

        return JsonResponse({'success': True})


def get_timetable_view(request: WSGIRequest):
    start = request.GET['start']

    with open('./static/timetable.json', 'r', encoding='utf8') as file:
        json = load(file)
        resp = deepcopy(json)
        _start = datetime(*map(int, start.split('T')[0].split('-')))

        for _el, el in resp.items():
            for _institute, institute in el.items():
                for _directions, directions in institute.items():
                    directions.clear()

        for _el, el in json.items():
            for _institute, institute in el.items():
                for _directions, directions in institute.items():
                    for item in directions:
                        date = datetime.fromisoformat(item['date'])

                        if _start <= date <= _start + timedelta(7):
                            resp[_el][_institute][_directions].append(item)

        return JsonResponse(resp)


class AbitsTimetableView(View):
    def get(self, request: WSGIRequest):

        return render(request, 'abits.html', {
            'form': GroupForm
        })

    def post(self, request: WSGIRequest):

        form = GroupForm(request.POST)
        button = get_button(request)

        if form.is_valid():
            cd = form.cleaned_data

            if button == 'default':
                try:
                    cd['date'] = datetime.strptime(cd['date'], '%b %d, %Y')
                except ValueError:
                    return redirect('/')

                return redirect(reverse('timetable:find_timetable', kwargs={
                    'group_or_teacher': cd['group'].name,
                    'date': str(cd['date'])
                }))
            else:
                return redirect(reverse('timetable:find_timetable', kwargs={
                    'group_or_teacher': cd['group'].name,
                    'date': button
                }))

        return redirect('/')


class TeacherTimetableView(View):

    def get(self, request: WSGIRequest):
        return render(request, 'teacher.html', {
            'form': TeacherForm
        })

    def post(self, request: WSGIRequest):

        form = TeacherForm(request.POST)
        button = get_button(request)

        if form.is_valid():
            cd = form.cleaned_data

            if button == 'default':
                try:
                    cd['date'] = datetime.strptime(cd['date'], '%b %d, %Y')
                except ValueError:
                    return redirect('/')

                return redirect(reverse('timetable:find_timetable', kwargs={
                    'group_or_teacher': cd['teacher'].name,
                    'date': str(cd['date'])
                }))
            else:
                return redirect(reverse('timetable:find_timetable', kwargs={
                    'group_or_teacher': cd['teacher'].name,
                    'date': button
                }))

        return redirect('teachers/')


class FindTimetableView(View):

    def get(self, request: WSGIRequest, group_or_teacher: str, date: str):
        # timetable = None

        try:
            date = datetime(*map(int, date.split()[0].split('-')))
        except (TypeError, ValueError):

            if date == 'today':
                date = datetime.now()
            elif date == 'tomorrow':
                date = datetime.now() + timedelta(1)
            elif date == 'this_week':
                date = list(get_week(datetime.now().date()))
                timetable = PairTimetableModel.objects.filter(group__name=group_or_teacher,
                                                              date__in=date) or PairTimetableModel.objects.filter(
                    teacher__name=group_or_teacher, date__in=date)

                if not len(timetable):
                    return render(request, '404.html')

                timetable = timetable.order_by('start_time').order_by('date')
                return render(request, 'timetable.html', {
                    'title': group_or_teacher,
                    'timetable': timetable,
                    'date': 'текущую неделю'
                })
            elif date == 'next_week':
                date = list(get_week((datetime.now() + timedelta(7)).date()))
                timetable = PairTimetableModel.objects.filter(group__name=group_or_teacher,
                                                              date__in=date) or PairTimetableModel.objects.filter(
                    teacher__name=group_or_teacher, date__in=date)

                if not len(timetable):
                    return render(request, '404.html')

                timetable = timetable.order_by('start_time').order_by('date')
                return render(request, 'timetable.html', {
                    'title': group_or_teacher,
                    'timetable': timetable,
                    'date': 'следующую неделю'
                })
            else:
                return render(request, '404.html')

        timetable = PairTimetableModel.objects.filter(group__name=group_or_teacher,
                                                      date=date) or PairTimetableModel.objects.filter(
            teacher__name=group_or_teacher, date=date)

        if not len(timetable):
            return render(request, '404.html')

        timetable = timetable.order_by('start_time')
        return render(request, 'timetable.html', {
            'title': group_or_teacher,
            'timetable': timetable.order_by('start_time'),
            'date': date.date()
        })


class ChooseGroupForMonthTableView(View):

    def get(self, request: WSGIRequest):

        return render(request, 'choose_group.html', {
            'form': ChooseGroupForm
        })

    def post(self, request: WSGIRequest):
        form = ChooseGroupForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            return redirect(reverse('timetable:month_timetable', kwargs={
                'group': cd['group']
            }))

        return redirect('choose_group_for_table')


class MonthTableView(View):

    def get(self, request: WSGIRequest, group: str):
        now = datetime.now()
        this_month = datetime(now.year, now.month, 1)
        next_month = this_month + relativedelta(months=1)
        qs = PairTimetableModel.objects.filter(group__name=group, date__range=[this_month, next_month])
        times = {i: [] for i in map(lambda el: ' - '.join(el), get_pair_times())}

        for date in get_month(this_month, next_month - timedelta(1)):
            qs_for_date = qs.filter(date=date)

            for start, end in get_pair_times():
                db_resp = qs_for_date.filter(start_time=time(*map(int, start.split('.'))))

                if len(db_resp):
                    times[f'{start} - {end}'].append(db_resp)
                else:
                    times[f'{start} - {end}'].append(None)

        return render(request, 'month_table.html', {
            'group': group,
            'times': times,
            'dates': get_month(this_month, next_month - timedelta(1))
        })
