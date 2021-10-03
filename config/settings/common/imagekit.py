"""Settings for django-imagekit app

Logic of thumbnail generation:
* Generate thumbnails on changing of source image (i.e. on post_save)
* Thumbnails generation using celery (separate task for each thumbnail)
* Locally generate thumbnails in same thread (if celery disabled)
* Do not generate thumbnails in tests

Used Optimistic strategy for thumbnails that does not check existence of each
thumbnail and simply believe that it exists. It may lead to case when thumbnail
is not generated, but it"s URL returned. But it is rare case. And without check
of each thumbnail existence we avoid a lot of requests to Redis during
representation of large (500+) sets of objects with thumbnails

"""
IMAGEKIT_DEFAULT_CACHEFILE_BACKEND = "imagekit.cachefiles.backends.Celery"

# cache of file existence
IMAGEKIT_CACHE_TIMEOUT = 60 * 60 * 24

# avatars thumbnails
AVATAR_THUMBNAILS_SIZE = (40, 40)

IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = "imagekit.cachefiles.strategies.Optimistic"
IMAGEKIT_CACHE_BACKEND = "default"
IMAGEKIT_CACHEFILE_DIR = "thumbnails"
