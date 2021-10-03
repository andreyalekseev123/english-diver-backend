REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # Only session authentication enabled now as API for 3rd party
        # clients is out of scope now.
        # Note: do not use DRF"s default Auth token!
        # * It not supposed to work with multiple tokens per user
        # * It stored in DB as plain text
        "rest_framework.authentication.SessionAuthentication",
    ),
    "PAGE_SIZE": 100,
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",

    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "rest_framework.filters.SearchFilter",
    ),
    "DATE_FORMAT": "%b %-d, %Y",
    "TIME_FORMAT": "%I:%M %p",
}
