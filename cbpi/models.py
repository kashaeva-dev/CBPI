from django.conf import settings
from django.db import models

class Universe(models.Model):
    name = models.CharField("Название вселенной", max_length=255)

    class Meta:
        verbose_name = "Вселенная"
        verbose_name_plural = "Вселенные"


class Country(models.Model):
    name = models.CharField("Страна", max_length=255)

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"


class GlobalActorList(models.Model):
    nickname = models.CharField("Ник", max_length=255)
    date_of_registration = models.DateField("Дата регистрации")
    registered_by_user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, verbose_name="Зарегистрирован пользователем")

    class Meta:
        verbose_name = "Глобальный актор"
        verbose_name_plural = "Глобальные акторы"


class User(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    native_language = models.CharField("Родной язык", max_length=100)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, verbose_name="Страна")
    gla = models.ForeignKey(GlobalActorList, on_delete=models.SET_NULL, null=True, verbose_name="Глобальный актор")

    class Meta:
        verbose_name = "Пользователь (доп.)"
        verbose_name_plural = "Пользователи (доп.)"


class StampStatus(models.Model):
    name = models.CharField("Статус", max_length=100)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Статус отметки"
        verbose_name_plural = "Статусы отметок"


class UserStamp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    datetime = models.DateTimeField("Дата и время")
    status = models.ForeignKey(StampStatus, on_delete=models.SET_NULL, null=True, verbose_name="Статус")

    class Meta:
        verbose_name = "Отметка пользователя"
        verbose_name_plural = "Отметки пользователей"


class Author(models.Model):
    name = models.CharField("Имя автора", max_length=255)
    photo_file = models.ImageField("Фото", upload_to='authors/', null=True, blank=True)
    date_of_birth = models.DateField("Дата рождения", null=True, blank=True)
    wiki_link = models.URLField("Wiki ссылка", null=True, blank=True)
    country_of_birth = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, verbose_name="Страна рождения")
    gla = models.ForeignKey(GlobalActorList, on_delete=models.SET_NULL, null=True, verbose_name="Глобальный актор")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class CompositionType(models.Model):
    title = models.CharField("Название типа", max_length=255)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Тип произведения"
        verbose_name_plural = "Типы произведений"


class Saga(models.Model):
    name = models.CharField("Название саги", max_length=255)
    universe_of_events = models.ForeignKey(Universe, on_delete=models.SET_NULL, null=True, verbose_name="Вселенная событий")
    zero_event_abbreviature = models.CharField("Аббревиатура нулевого события", max_length=50, null=True, blank=True)
    date_first_published = models.DateField("Дата первой публикации", null=True, blank=True)
    country_first_published = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, verbose_name="Страна первой публикации", related_name='sagas')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, verbose_name="Автор")
    user_stamp = models.ForeignKey(UserStamp, on_delete=models.SET_NULL, null=True, verbose_name="Отметка пользователя")

    class Meta:
        verbose_name = "Сага"
        verbose_name_plural = "Саги"


class Place(models.Model):
    name = models.CharField("Название места", max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Родительское место")
    description = models.TextField("Описание", blank=True)
    wiki_link = models.URLField("Wiki ссылка", blank=True)
    real_flag = models.BooleanField("Реальное место?", default=False)

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"


class Composition(models.Model):
    saga = models.ForeignKey(Saga, on_delete=models.CASCADE, verbose_name="Сага")
    title = models.CharField("Название", max_length=255)
    date_published = models.DateField("Дата публикации", null=True, blank=True)
    composition_type = models.ForeignKey(CompositionType, on_delete=models.SET_NULL, null=True, verbose_name="Тип")
    file_source = models.FileField("Файл", upload_to='compositions/', null=True, blank=True)

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"


class Event(models.Model):
    title = models.CharField("Название события", max_length=255)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, verbose_name="Место")
    description = models.TextField("Описание", blank=True)
    zero_event_flag = models.BooleanField("Нулевое событие?", default=False)
    date_time_from_zero_event = models.CharField("Дата относительно нуля", max_length=255, null=True, blank=True)
    composition = models.ForeignKey(Composition, on_delete=models.SET_NULL, null=True, verbose_name="Произведение")
    cm_position = models.CharField("Позиция в произведении", max_length=255, null=True, blank=True)
    user_stamp = models.ForeignKey(UserStamp, on_delete=models.SET_NULL, null=True, verbose_name="Отметка")

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"


class Hero(models.Model):
    name = models.CharField("Имя героя", max_length=255)
    description = models.TextField("Описание", blank=True)
    photo_file = models.ImageField("Фото", upload_to='heroes/', null=True, blank=True)
    saga = models.ForeignKey(Saga, on_delete=models.SET_NULL, null=True, verbose_name="Сага")
    birth_event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, verbose_name="Событие рождения")
    user_stamp = models.ForeignKey(UserStamp, on_delete=models.SET_NULL, null=True, verbose_name="Отметка")
    gla = models.ForeignKey(GlobalActorList, on_delete=models.SET_NULL, null=True, verbose_name="Глобальный актор")

    class Meta:
        verbose_name = "Герой"
        verbose_name_plural = "Герои"


class Episode(models.Model):
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE, verbose_name="Произведение")
    title = models.CharField("Название эпизода", max_length=255)
    story_resume = models.TextField("Краткое описание")
    start_event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, verbose_name="Начальное событие")
    previous_episode = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Предыдущий эпизод")
    user_stamp = models.ForeignKey(UserStamp, on_delete=models.SET_NULL, null=True, verbose_name="Отметка")

    class Meta:
        verbose_name = "Эпизод"
        verbose_name_plural = "Эпизоды"


class RoleType(models.Model):
    name = models.CharField("Название роли", max_length=255)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Тип роли"
        verbose_name_plural = "Типы ролей"


class Participation(models.Model):
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE, verbose_name="Герой")
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, verbose_name="Эпизод")
    role_type = models.ForeignKey(RoleType, on_delete=models.SET_NULL, null=True, verbose_name="Роль")

    class Meta:
        verbose_name = "Участие героя"
        verbose_name_plural = "Участия героев"


class ValueDimension(models.Model):
    title = models.CharField("Название ценности", max_length=255)
    description = models.TextField("Описание", blank=True)
    utopiya_picture = models.TextField("Утопия (описание)", blank=True)
    user_stamp = models.ForeignKey(UserStamp, on_delete=models.SET_NULL, null=True, verbose_name="Отметка")

    class Meta:
        verbose_name = "Ценность"
        verbose_name_plural = "Ценности"


class FactType(models.Model):
    title = models.CharField("Тип факта", max_length=255)
    is_numerical = models.BooleanField("Числовой факт")
    measure = models.CharField("Единицы измерения", max_length=100, blank=True)

    class Meta:
        verbose_name = "Тип факта"
        verbose_name_plural = "Типы фактов"


class Fact(models.Model):
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE, verbose_name="Произведение")
    title = models.CharField("Заголовок", max_length=255)
    description = models.TextField("Описание", blank=True)
    fact_type = models.ForeignKey(FactType, on_delete=models.SET_NULL, null=True, verbose_name="Тип факта")
    numeric_value = models.FloatField("Числовое значение", null=True, blank=True)
    condition_for_effect = models.TextField("Условие действия", blank=True)
    result_of_event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, verbose_name="Результат события")

    class Meta:
        verbose_name = "Факт"
        verbose_name_plural = "Факты"


class AffectOnValue(models.Model):
    value_dimension = models.ForeignKey(ValueDimension, on_delete=models.CASCADE, verbose_name="Ценность")
    fact_type = models.ForeignKey(FactType, on_delete=models.CASCADE, verbose_name="Тип факта")
    weight = models.FloatField("Вес воздействия")

    class Meta:
        unique_together = ("value_dimension", "fact_type")
        verbose_name = "Влияние на ценность"
        verbose_name_plural = "Влияния на ценности"


class HeroValue(models.Model):
    hero = models.ForeignKey('Hero', on_delete=models.CASCADE, verbose_name="Герой")
    value_dimension = models.ForeignKey('ValueDimension', on_delete=models.CASCADE, verbose_name="Ценность")
    weight = models.FloatField("Вес")
    event_after = models.ForeignKey('Event', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="После события")

    class Meta:
        verbose_name = "Убеждение героя"
        verbose_name_plural = "Убеждения героев"


class DecisionType(models.Model):
    title = models.CharField("Тип решения", max_length=255)
    example = models.TextField("Пример", blank=True)
    user_stamp = models.ForeignKey('UserStamp', on_delete=models.SET_NULL, null=True, verbose_name="Отметка")

    class Meta:
        verbose_name = "Тип решения"
        verbose_name_plural = "Типы решений"


class Decision(models.Model):
    decision_type = models.ForeignKey(DecisionType, on_delete=models.SET_NULL, null=True, verbose_name="Тип")
    hero = models.ForeignKey('Hero', on_delete=models.CASCADE, verbose_name="Герой")
    event_after = models.ForeignKey('Event', on_delete=models.SET_NULL, null=True, verbose_name="После события")

    class Meta:
        verbose_name = "Решение"
        verbose_name_plural = "Решения"


class ActionType(models.Model):
    title = models.CharField("Тип действия", max_length=255)
    description = models.TextField("Описание", blank=True)
    user_stamp = models.ForeignKey('UserStamp', on_delete=models.SET_NULL, null=True, verbose_name="Отметка")

    class Meta:
        verbose_name = "Тип действия"
        verbose_name_plural = "Типы действий"


class HeroAction(models.Model):
    hero = models.ForeignKey('Hero', on_delete=models.CASCADE, verbose_name="Герой")
    action_type = models.ForeignKey(ActionType, on_delete=models.SET_NULL, null=True, verbose_name="Тип действия")
    based_on_decision = models.ForeignKey(Decision, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Основано на решении")
    cause_event = models.ForeignKey('Event', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Причинное событие")
    in_role = models.ForeignKey('Participation', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Роль в эпизоде")

    class Meta:
        verbose_name = "Действие героя"
        verbose_name_plural = "Действия героев"


class DecisionEvaluation(models.Model):
    hero_was_evaluated = models.ForeignKey('Hero', on_delete=models.CASCADE, related_name='оцененный_герой', verbose_name="Оцениваемый герой")
    eval_for_ha = models.ForeignKey(HeroAction, on_delete=models.CASCADE, verbose_name="Оцениваемое действие")
    gla_evaluator = models.ForeignKey('GlobalActorList', on_delete=models.SET_NULL, null=True, verbose_name="Оценивающий актор")
    event_after = models.ForeignKey('Event', on_delete=models.SET_NULL, null=True, verbose_name="После события")
    affects_on_vd = models.ForeignKey(ValueDimension, on_delete=models.SET_NULL, null=True, verbose_name="Затрагиваемая ценность")
    weight = models.FloatField("Влияние от -1 до 1")

    class Meta:
        verbose_name = "Оценка действия"
        verbose_name_plural = "Оценки действий"


class EventSequence(models.Model):
    event_before = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='событие_до', verbose_name="Предыдущее событие")
    event_after = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='событие_после', verbose_name="Следующее событие")
    straight = models.BooleanField("Сразу после?", default=False)

    class Meta:
        verbose_name = "Последовательность событий"
        verbose_name_plural = "Последовательности событий"
        unique_together = ("event_before", "event_after")


class FactRelation(models.Model):
    based_fact = models.ForeignKey(Fact, on_delete=models.CASCADE, related_name='основанный_факт', verbose_name="Базовый факт")
    followed_fact = models.ForeignKey(Fact, on_delete=models.CASCADE, related_name='следующий_факт', verbose_name="Следующий факт")
    group_id = models.CharField("ID группы", max_length=100, blank=True)
    event_relation = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Связанное событие")

    class Meta:
        verbose_name = "Связь фактов"
        verbose_name_plural = "Связи фактов"
        unique_together = ("based_fact", "followed_fact")
