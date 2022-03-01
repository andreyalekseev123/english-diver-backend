from django.contrib import admin

from django_admin_inline_paginator.admin import TabularInlinePaginated
from import_export.admin import ImportExportMixin

from . import models, resources


@admin.register(models.TrainingType)
class TrainingTypeAdmin(admin.ModelAdmin):
    """Admin class for ``TrainingType`` model."""
    search_fields = ("name",)
    list_display = ("id", "name", "cost")
    list_display_links = (
        "id",
        "name",
    )
    fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "id",
                "name",
                "image",
                "questions_count",
                "words_per_question_count",
                "cost",
                "words_can_be_chosen",
            ),
        }),
    )
    readonly_fields = ("id",)


class QuestionInline(admin.TabularInline):
    model = models.Question


@admin.register(models.Training)
class TrainingAdmin(admin.ModelAdmin):
    """Admin class for ``Training`` model."""
    autocomplete_fields = ("type", "user")
    list_display = (
        "id",
        "user",
        "type",
    )
    fieldsets = (
        ("Main info", {
            "classes": ("wide",),
            "fields": ("id", "user", "type"),
        }),
    )
    readonly_fields = ("id",)
    inlines = [
        QuestionInline,
    ]


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin class for ``Question`` model."""
    list_filter = (
        ('training', admin.RelatedOnlyFieldListFilter),
        ('user_word__word', admin.RelatedOnlyFieldListFilter),
    )
    list_display = (
        "id",
        "training",
        "user_word",
    )
    readonly_fields = ("id",)


@admin.register(models.UserWord)
class UserWordAdmin(admin.ModelAdmin):
    """Admin class for ``Question`` model."""
    search_fields = (
        "user__email",
        "word__english",
        "word__russian",
    )
    autocomplete_fields = ("user", "word")
    list_display = (
        "id",
        "user",
        "word",
        "rank",
    )
    fieldsets = (
        ("Main info", {
            "classes": ("wide",),
            "fields": ("id", "user", "word", "rank"),
        }),
    )
    readonly_fields = ("id",)


@admin.register(models.Word)
class WordAdmin(ImportExportMixin, admin.ModelAdmin):
    """Admin class for ``Word`` model."""
    resource_class = resources.WordResource

    search_fields = ("english", "russian")
    filter_horizontal = ("categories",)
    list_display = (
        "id",
        "english",
        "russian",
        "_categories",
    )
    fieldsets = (
        ("Main info", {
            "classes": ("wide",),
            "fields": ("id", "english", "russian", "categories"),
        }),
    )
    readonly_fields = ("id",)

    def _categories(self, instance):
        """Get all categories for word."""
        return ", ".join(
            [str(category) for category in instance.categories.all()]
        )


class WordInline(TabularInlinePaginated):
    model = models.Word.categories.through
    per_page = 10


@admin.register(models.Category)
class CategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    """Admin class for ``Category`` model."""
    resource_class = resources.CategoryResource
    search_fields = ("name",)
    list_display = (
        "id",
        "name",
    )
    fieldsets = (
        ("Main info", {
            "classes": ("wide",),
            "fields": ("name", "image"),
        }),
    )
    inlines = [
        WordInline,
    ]

    def get_queryset(self, request):
        """Prefetch words."""
        return super().get_queryset(request).prefetch_related("words")


@admin.register(models.TrainingTypeUserWord)
class TrainingTypeUserWordsAdmin(ImportExportMixin, admin.ModelAdmin):
    """Admin class for ``TrainingTypeUserWord`` model."""
    resource_class = resources.WordResource
    autocomplete_fields = (
        "training_type",
        "user_word",
    )
    search_fields = (
        "user_word__user__email",
        "user_word__word__english",
        "user_word__word__russian",
        "training_type__name",
    )
    list_filter = (
        "training_type",
    )
    list_display = (
        "id",
        "training_type",
        "user_word",
    )
    fieldsets = (
        ("Main info", {
            "classes": ("wide",),
            "fields": ("id", "training_type", "user_word"),
        }),
    )
    readonly_fields = ("id",)
