from django.contrib import admin
from .models import *


class ParticipationInline(admin.TabularInline):
    model = Participation
    extra = 1


class HeroValueInline(admin.TabularInline):
    model = HeroValue
    extra = 1


class HeroActionInline(admin.TabularInline):
    model = HeroAction
    extra = 1


class DecisionInline(admin.TabularInline):
    model = Decision
    extra = 1


class FactRelationInline(admin.TabularInline):
    model = FactRelation
    fk_name = "based_fact"
    extra = 1


@admin.register(Universe)
class UniverseAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(GlobalActorList)
class GlobalActorListAdmin(admin.ModelAdmin):
    list_display = ("id", "nickname", "date_of_registration", "registered_by_user")
    search_fields = ("nickname",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "country",)
    search_fields = ("id",)
    list_filter = ("country",)


@admin.register(StampStatus)
class StampStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(UserStamp)
class UserStampAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "datetime", "status")
    list_filter = ("status",)
    search_fields = ("user__name",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "date_of_birth", "country_of_birth")
    search_fields = ("name",)
    list_filter = ("country_of_birth",)


@admin.register(CompositionType)
class CompositionTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title",)


@admin.register(Saga)
class SagaAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "universe_of_events", "date_first_published")
    search_fields = ("name",)
    list_filter = ("universe_of_events", "country_first_published")


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent", "real_flag")
    search_fields = ("name",)
    list_filter = ("real_flag",)


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "saga", "date_published", "composition_type")
    search_fields = ("title",)
    list_filter = ("composition_type",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "composition", "place", "zero_event_flag")
    search_fields = ("title",)
    list_filter = ("zero_event_flag", "place")


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "saga", "birth_event")
    search_fields = ("name",)
    list_filter = ("saga",)
    inlines = [HeroValueInline, HeroActionInline, DecisionInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'photo_file')
        }),
        ("Привязка", {
            'fields': ('saga', 'birth_event', 'user_stamp', 'gla')
        })
    )


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "composition", "start_event")
    search_fields = ("title",)
    list_filter = ("composition",)
    inlines = [ParticipationInline]


@admin.register(RoleType)
class RoleTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ("id", "hero", "episode", "role_type")
    search_fields = ("hero__name", "episode__title")


@admin.register(ValueDimension)
class ValueDimensionAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title",)


@admin.register(FactType)
class FactTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_numerical")
    search_fields = ("title",)
    list_filter = ("is_numerical",)


@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "composition", "fact_type", "numeric_value")
    search_fields = ("title",)
    list_filter = ("fact_type",)
    inlines = [FactRelationInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'fact_type', 'numeric_value')
        }),
        ("Дополнительно", {
            'fields': ('composition', 'condition_for_effect', 'result_of_event')
        })
    )


@admin.register(AffectOnValue)
class AffectOnValueAdmin(admin.ModelAdmin):
    list_display = ("id", "value_dimension", "fact_type", "weight")
    list_filter = ("value_dimension",)


@admin.register(HeroValue)
class HeroValueAdmin(admin.ModelAdmin):
    list_display = ("id", "hero", "value_dimension", "weight", "event_after")


@admin.register(DecisionType)
class DecisionTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title",)


@admin.register(Decision)
class DecisionAdmin(admin.ModelAdmin):
    list_display = ("id", "hero", "decision_type", "event_after")


@admin.register(ActionType)
class ActionTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


@admin.register(HeroAction)
class HeroActionAdmin(admin.ModelAdmin):
    list_display = ("id", "hero", "action_type", "based_on_decision")


@admin.register(DecisionEvaluation)
class DecisionEvaluationAdmin(admin.ModelAdmin):
    list_display = ("id", "hero_was_evaluated", "eval_for_ha", "weight")


@admin.register(EventSequence)
class EventSequenceAdmin(admin.ModelAdmin):
    list_display = ("id", "event_before", "event_after", "straight")


@admin.register(FactRelation)
class FactRelationAdmin(admin.ModelAdmin):
    list_display = ("id", "based_fact", "followed_fact", "event_relation")
