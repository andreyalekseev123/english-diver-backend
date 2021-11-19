import datetime
from random import sample

from apps.training.factories import WordFactory
from apps.users.factories import UserFactory

WORDS_COUNT = 100
USERS_COUNT = 4
USERS_WORDS_COUNT = 50

YEAR = datetime.datetime.now().year

print("Creating users...")
users = UserFactory.create_batch(USERS_COUNT)

print("Creating words...")
words = WordFactory.create_batch(WORDS_COUNT)

print("Creating user words...")
for user in users:
    user.words.add(*sample(words, USERS_WORDS_COUNT))


# For manage.py runscript, so that it counts as a script
def run():
    pass
