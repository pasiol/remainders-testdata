import random
import datetime
import time
import pytz
import json
from faker import Faker
import lipsum
from lipsum.generator import generate_paragraphs
from pprint import pprint


fake = Faker(["fi_FI"])

documents = 100000
persons = 500
message_types = 50


def generate_message_types(count):
    types = list()
    for n in range(count):
        types.append(
            {
                "title": fake.sentence(
                    nb_words=random.randint(4, 12),
                ),
                "type": fake.sentence(nb_words=random.randint(1, 3))[:-1],
                "message": fake.paragraph(nb_sentences=random.randint(1, 6)),
            }
        )
    return types


def generate_emails(count):
    emails = list()
    for n in range(count):
        emails.append(fake.email())
    return emails


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return str(z)
        else:
            return super().default(z)


class DateTimeEncoder2(json.JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


def main():

    fake_message_types = generate_message_types(message_types)
    fake_persons = generate_emails(persons)

    test_data = []
    for i in range(documents):
        random_message = fake_message_types[random.randint(1, message_types - 1)]
        test_document = {
            "to": fake_persons[random.randint(1, persons - 1)],
            "title": random_message["title"],
            "message": random_message["message"],
            "type": random_message["type"],
            # "updated_at": "date({})".format(
            #    time.mktime(
            #        fake.date_time_this_year(
            #            before_now=True, tzinfo=pytz.utc
            #        ).timetuple()
            #    )
            # ),"""
            "updated_at": fake.date_time_this_year(before_now=True, tzinfo=pytz.utc),
        }
        test_data.append(test_document)

    with open("test_data.json", "w") as output_file:
        json.dump(test_data, output_file, cls=DateTimeEncoder2)
        # json.dump(test_data, output_file)


if __name__ == "__main__":
    main()
