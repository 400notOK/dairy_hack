import random
from datacenter.models import Schoolkid, Mark, Lesson, Chastisement, Commendation

POSSIBLE_TEXT = ['Молодец!',
                 'Отлично!',
                 'Хорошо!',
                 'Гораздо лучше, чем я ожидал!',
                 'Ты меня приятно удивил!',
                 'Великолепно!',
                 'Прекрасно!',
                 'Ты меня очень обрадовал!',
                 'Именно этого я давно ждал от тебя!',
                 'Сказано здорово – просто и ясно!',
                 'Ты, как всегда, точен!',
                 'Очень хороший ответ!',
                 'Талантливо!',
                 'Ты сегодня прыгнул выше головы!',
                 'Я поражен!',
                 'Уже существенно лучше!',
                 'Потрясающе!',
                 'Замечательно!',
                 'Прекрасное начало!',
                 'Так держать!',
                 'Ты на верном пути!',
                 'Здорово!',
                 'Это как раз то, что нужно!',
                 'Я тобой горжусь!',
                 'С каждым разом у тебя получается всё лучше!',
                 'Мы с тобой не зря поработали!',
                 'Я вижу, как ты стараешься!',
                 'Ты растешь над собой!',
                 'Ты многое сделал, я это вижу!',
                 'Теперь у тебя точно все получится!']


def fix_marks(schoolkid, bad_marks=[2, 3], good_mark=5):
    Mark.objects.filter(points__in=bad_marks, schoolkid=schoolkid).update(points=good_mark)


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid, subject):
    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject
    ).order_by('date').last()

    Commendation.objects.create(
        text=random.choice(POSSIBLE_TEXT),
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher
    )


def start_correction(schoolkid_name,
                     enable_fix_marks=True,
                     enable_remove_chastisements=True,
                     subjects_for_correction=None):
    try:
        child = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.DoesNotExist:
        print('Не найдено ученика с указанным именем')
        return
    except Schoolkid.MultipleObjectsReturned:
        print('Нашлось несколько учеников, скорректируйте запрос')
        return

    if enable_fix_marks:
        print('Исправляем плохие оценки...')
        fix_marks(child)

    if enable_remove_chastisements:
        print('Удаляем замечания...')
        remove_chastisements(child)

    if subjects_for_correction:
        print('Добавляем в дневник хвалебные записи...')
        for subject in subjects_for_correction:
            create_commendation(child, subject)

    print('Выполнено!')
