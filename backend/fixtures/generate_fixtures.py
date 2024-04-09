#!/usr/bin/env python
import argparse
from datetime import datetime, timedelta
import json
import random

from django.contrib.auth.hashers import PBKDF2PasswordHasher
import faker

hasher = PBKDF2PasswordHasher()
faker = faker.Faker()

fixture = []
user_count = 20
event_count = 60
post_count = 40
comment_count = 80
event_count = 20
location_count = 40


def generate_time(future_end=False):
    start = datetime.now()
    end = ((datetime.now() + timedelta(days=365)) if future_end
           else (datetime.now() - timedelta(days=365)))
    return not_naive(start + (end - start) * random.random())


def not_naive(time):
    return str(time).replace(" ", "T")[:-3] + "Z"


def pseudorandom(M, N, max):
    tups = set()
    while (len(tups) <= max):
        tup = (random.randrange(1, M), random.randrange(1, N))
        tups.add(tup)
    return list(tups)


# users app
def generate_user(test: bool):
    for i in range(1, user_count + 1):
        fixture.append(
            {
                'model': 'users.ConcertifyUser',
                'pk': i,
                'fields': {
                    'username': f'test{i}',
                    'email': f'test{i}@email.com',
                    'password': hasher.encode(f'TestTest{i}', str(i)),
                    'first_name': f'Test{i}',
                    'last_name': f'Test{i}',
                    'picture': None
                } if test else {
                    'username': faker.user_name(),
                    'email': faker.email(),
                    'password': hasher.encode(faker.password(), str(i)),
                    'first_name': faker.first_name(),
                    'last_name': faker.last_name(),
                    'picture': None
                }
            }
        )


def generate_paymentinfo(test: bool):
    for i in range(1, user_count + 1):
        fixture.append(
            {
                'model': 'users.PaymentInfo',
                'pk': i,
                'fields': {
                    'line1': f'test {i}',
                    'line2': f'test {i}',
                    'city': f'Test{i}',
                    'postal_code': i,
                    'country': f'Test{i}',
                    'telephone': faker.phone_number(),
                    'mobile': faker.phone_number(),
                    'user': i,
                } if test else {
                    'line1': faker.address(),
                    'line2': faker.address(),
                    'city': faker.city(),
                    'postal_code': faker.postalcode(),
                    'country': faker.country_code(),
                    'telephone': faker.phone_number(),
                    'mobile': faker.phone_number(),
                    'user': i,
                }
            }
        )


def generate_notification(test):
    for i in range(1, event_count + 1):
        fixture.append(
            {
                'model': 'users.Notification',
                'pk': i,
                'fields': {
                    'title': f'test{i}',
                    'desc': f'test{i}',
                    'notification_type': 'TEST',
                    'user': i + 1
                } if test else {
                    'title': faker.word(),
                    'desc': faker.text(max_nb_chars=100),
                    'notification_type': faker.word().upper(),
                    'user': i//2 + 1
                }
            }
        )


def generate_eventreport(test):
    for i in range(1, user_count*2 + 1):
        fixture.append(
            {
                'model': 'users.EventReport',
                'pk': i,
                'fields': {
                    'title': f'test{i}',
                    'desc': f'test{i}',
                    'report_type': 'TEST',
                    'created_at': generate_time(),
                    'user': random.randrange(1, user_count + 1),
                    'event': random.randrange(1, event_count + 1)
                } if test else {
                    'title': faker.word(),
                    'desc': faker.text(max_nb_chars=100),
                    'report_type': faker.word().upper(),
                    'created_at': generate_time(),
                    'user': random.randrange(1, user_count + 1),
                    'event': random.randrange(1, event_count + 1)
                }
            }
        )


# posts_comments app
def generate_post(test):
    for i in range(1, post_count + 1):
        fixture.append(
            {
                'model': 'posts_comments.Post',
                'pk': i,
                'fields': {
                    'title': f'test{i}',
                    'desc': f'test{i}',
                    'created_at': generate_time(),
                    'picture': None,
                    'event': random.randrange(1, event_count + 1)
                } if test else {
                    'title': faker.word(),
                    'desc': faker.text(max_nb_chars=100),
                    'created_at': generate_time(),
                    'picture': None,
                    'event': random.randrange(1, event_count + 1)
                }
            }
        )


def generate_comment(test):
    for i in range(1, comment_count + 1):
        fixture.append(
            {
                'model': 'posts_comments.Comment',
                'pk': i,
                'fields': {
                    'title': f'test{i}',
                    'desc': f'test{i}',
                    'created_at': generate_time(),
                    'post': random.randrange(1, post_count + 1),
                    'user': random.randrange(1, user_count + 1)
                } if test else {
                    'title': faker.word(),
                    'desc': faker.text(max_nb_chars=100),
                    'created_at': generate_time(),
                    'post': random.randrange(1, post_count + 1),
                    'user': random.randrange(1, user_count + 1)
                }
            }
        )


def generate_postvote(test):
    rand_id = pseudorandom(user_count, post_count, post_count*3)
    for i in range(1, post_count*3 + 1):
        user_id, post_id = rand_id[i-1]
        fixture.append(
            {
                'model': 'posts_comments.PostVote',
                'pk': i,
                'fields': {
                    'post': post_id,
                    'user': user_id
                } if test else {
                    'post': post_id,
                    'user': user_id
                }
            }
        )


def generate_commentvote(test):
    rand_id = pseudorandom(user_count, comment_count, comment_count*3)
    for i in range(1, comment_count*3 + 1):
        user_id, comment_id = rand_id[i-1]
        fixture.append(
            {
                'model': 'posts_comments.CommentVote',
                'pk': i,
                'fields': {
                    'comment': comment_id,
                    'user': user_id
                } if test else {
                    'comment': comment_id,
                    'user': user_id
                }
            }
        )


# events app
def generate_location(test):
    for i in range(1, location_count + 1):
        fixture.append(
            {
                'model': 'events.Location',
                'pk': i,
                'fields': {
                    'name': f'test{i}',
                    'address_line': f'test {i}',
                    'city': 'Test',
                    'postal_code': f'T{i}-{i}',
                    'country': 'TST'
                } if test else {
                    'name': faker.word(),
                    'address_line': faker.address(),
                    'city': faker.city(),
                    'postal_code': faker.postalcode(),
                    'country': faker.country_code()
                }
            }
        )


def generate_event(test):
    for i in range(1, event_count + 1):
        fixture.append(
            {
                'model': 'events.Event',
                'pk': i,
                'fields': {
                    'title': f'test{i}',
                    'desc': f'test{i}',
                    'picture': None,
                    'start': generate_time(),
                    'end': generate_time(True),
                    'location': random.randrange(1, location_count + 1)
                } if test else {
                    'title': faker.word(),
                    'desc': faker.text(max_nb_chars=100),
                    'picture': None,
                    'start': generate_time(),
                    'end': generate_time(True),
                    'location': random.randrange(1, location_count + 1)
                }
            }
        )


def generate_role(test):
    rand_id = pseudorandom(user_count, event_count, event_count*3)
    for i in range(1, event_count*3 + 1):
        user_id, event_id = rand_id[i-1]
        fixture.append(
            {
                'model': 'events.Role',
                'pk': i,
                'fields': {
                    'event': event_id,
                    'user': user_id,
                    'name': random.choice(range(0, 4))
                } if test else {
                    'event': event_id,
                    'user': user_id,
                    'name': random.choice(range(0, 4))
                }
            }
        )


def generate_eventcontact(test):
    for i in range(1, event_count*3 + 1):
        fixture.append(
            {
                'model': 'events.EventContact',
                'pk': i,
                'fields': {
                    'name': 'test',
                    'phone': '123456789',
                    'event': random.randrange(1, event_count + 1)
                } if test else {
                    'name': faker.name(),
                    'phone': faker.phone_number(),
                    'event': random.randrange(1, event_count + 1)
                }
            }
        )


def generate_socialmedia(test):
    for i in range(1, event_count*2 + 1):
        fixture.append(
            {
                'model': 'events.SocialMedia',
                'pk': i,
                'fields': {
                    'link': f'www.test{i}.com',
                    'platform': random.choice(['X', 'INSTAGRAM', 'FACEBOOK']),
                    'event': random.randrange(1, event_count + 1)
                } if test else {
                    'link': faker.url(),
                    'platform': random.choice(['X', 'INSTAGRAM', 'FACEBOOK']),
                    'event': random.randrange(1, event_count + 1)
                }
            }
        )


def generate_scheduleitem(test):
    for i in range(1, event_count*2 + 1):
        fixture.append(
            {
                'model': 'events.ScheduleItem',
                'pk': i,
                'fields': {
                    'title': f'test{i}',
                    'desc': f'test{i}',
                    'place': f'test{i}',
                    'when': generate_time(),
                    'event': random.randrange(1, event_count + 1)
                } if test else {
                    'title': faker.word(),
                    'desc': faker.text(max_nb_chars=100),
                    'place': faker.word(),
                    'when': generate_time(),
                    'event': random.randrange(1, event_count + 1)
                }
            }
        )


def generate_ticket(test):
    for i in range(1, event_count*2 + 1):
        fixture.append(
            {
                'model': 'events.Ticket',
                'pk': i,
                'fields': {
                    'title': f'test{i}',
                    'desc': f'test{i}',
                    'quantity': i,
                    'amount': round(random.uniform(0, 100), 2),
                    'event': random.randrange(1, event_count + 1)
                } if test else {
                    'title': faker.word(),
                    'desc': faker.text(max_nb_chars=100),
                    'quantity': i,
                    'amount': round(random.uniform(0, 100), 2),
                    'event': random.randrange(1, event_count + 1)
                }
            }
        )


def run_generate(test: bool = False):
    path = ('./backend/fixtures/test_fixture.json' if test
            else './backend/fixtures/fixture.json')

    generate_user(test)
    generate_paymentinfo(test)
    generate_notification(test)
    generate_eventreport(test)

    generate_post(test)
    generate_comment(test)
    generate_postvote(test)
    generate_commentvote(test)

    generate_location(test)
    generate_event(test)
    generate_role(test)
    generate_eventcontact(test)
    generate_socialmedia(test)
    generate_scheduleitem(test)
    generate_ticket(test)

    with open(path, 'w') as outfile:
        json.dump(fixture, outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate fixtures')
    parser.add_argument('--test', '-t', dest='test',
                        action='store_true', default=False)
    args = parser.parse_args()

    run_generate(args.test)
