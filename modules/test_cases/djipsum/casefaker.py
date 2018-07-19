from djipsum.faker import FakerModel


def case_faker(maximum=10):
    faker = FakerModel(
        app='test_cases',
        model='Case'
    )
    object_list = []  # for print out after created the objects.

    for _ in range(maximum):
        fields = {
            'name': faker.fake.text(max_nb_chars=100),
            'description': ' '.join(faker.fake.paragraphs()),
            'precondition': ' '.join(faker.fake.paragraphs()),
            'excepted_result': ' '.join(faker.fake.paragraphs()),
            # 'create_at': str(faker.fake.date_time()),
            'create_by': faker.fake_relations(type='fk', field_name='create_by')
        }
        instance = faker.create(fields)
        object_list.append(instance)
    return object_list
