import requests
import telebot
import config
from bs4 import BeautifulSoup
from telebot import apihelper
from datetime import datetime


bot = telebot.TeleBot(config.CONFIG.get("access_token"))

apihelper.proxy = {'https': 'socks5://185.43.110.132:9999'}


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.CONFIG.get("domain"),
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_a_monday(web_page):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": "1day"})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    day, week, group = message.text.split()
    day = day[1:]
    web_page = get_page(group, week)
    soup = BeautifulSoup(web_page, "html5lib")
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    for day_id in range(len(days)):
        if days[day_id] == day:
            # Получаем таблицу с расписанием на конкретный день
            schedule_table = soup.find("table", attrs={"id": str(day_id + 1) + "day"})
            break
    if schedule_table is not None:
        # Время проведения занятий
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        times_list = [time.span.text for time in times_list]

        # Место проведения занятий
        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text for room in locations_list]

        # Название дисциплин и имена преподавателей
        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
        lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

        resp = ''
        for time, location, lession in zip(times_list, locations_list, lessons_list):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, "У данной группы нет занятий в этот день", parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    _, group = message.text.split()
    this_day = datetime.now()
    print(this_day.isocalendar()[1])

    times_list = []
    locations_list = []
    lessons_list = []

    for n_week in range(0, 2):
        web_page = get_page(group, (this_day.isocalendar()[1] + n_week) % 2)
        soup = BeautifulSoup(web_page, "html5lib")
        for i in range(0, 7):
            schedule_table = soup.find("table", attrs={"id": str(i + 1) + "day"})
            if schedule_table is not None:
                times = schedule_table.find_all("td", attrs={"class": "time"})
                times_list.append([datetime.strptime(time.span.text[:5], '%H:%M') for time in times if time.span.text != "День"])

                locations = schedule_table.find_all("td", attrs={"class": "room"})
                locations_list.append([room.span.text for room in locations])

                lessons = schedule_table.find_all("td", attrs={"class": "lesson"})
                lessons = [lesson.text.split('\n\n') for lesson in lessons]
                lessons_list.append([', '.join([info for info in lesson_info if info]) for lesson_info in lessons])

    for n_lesson in range(len(times_list[this_day.weekday()])):
        if times_list[this_day.weekday()][n_lesson].time() >= this_day.time():
            resp = '<b>{}</b>, {}, {}\n'.format(times_list[this_day.weekday()][n_lesson].time(), locations_list[this_day.weekday()][n_lesson], lessons_list[this_day.weekday()][n_lesson])
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
            break
    else:
        resp = '<b>{}</b>, {}, {}\n'.format(times_list[this_day.weekday() + 1][0].time(), locations_list[this_day.weekday() + 1][0], lessons_list[this_day.weekday() + 1][0])
        bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    _, group = message.text.split()
    this_day = datetime.now()
    print(this_day.weekday())
    if this_day.weekday() != 6:
        web_page = get_page(group, this_day.isocalendar()[1])
        soup = BeautifulSoup(web_page, "html5lib")
        schedule_table = soup.find("table", attrs={"id": str(this_day.weekday() + 2) + "day"})
    else:
        web_page = get_page(group, (this_day.isocalendar()[1] + 1) % 2)
        soup = BeautifulSoup(web_page, "html5lib")
        schedule_table = soup.find("table", attrs={"id": str(1) + "day"})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    resp = ''
    for time, location, lession in zip(times_list, locations_list, lessons_list):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    _, week, group = message.text.split()
    web_page = get_page(group, week)
    soup = BeautifulSoup(web_page, "html5lib")
    for day in range(1, 7):
        schedule_table = soup.find("table", attrs={"id": str(day) + "day"})
        # Время проведения занятий
        if schedule_table is not None:
            times_list = schedule_table.find_all("td", attrs={"class": "time"})
            times_list = [time.span.text for time in times_list]

            # Место проведения занятий
            locations_list = schedule_table.find_all("td", attrs={"class": "room"})
            locations_list = [room.span.text for room in locations_list]

            # Название дисциплин и имена преподавателей
            lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
            lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
            lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

            resp = ''
            for time, location, lession in zip(times_list, locations_list, lessons_list):
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
            bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
