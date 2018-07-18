from djipsum.faker import FakerModel


def plan_faker(maximum=10):
    faker = FakerModel(
        app='test_plans',
        model='Plan'
    )
    object_list = []  # for print out after created the objects.

    for _ in range(maximum):
        fields = {
            'name': faker.fake.text(max_nb_chars=300),
            'description': ' '.join(faker.fake.paragraphs()),
            'create_at': str(faker.fake.date_time()),
            'create_by': faker.fake_relations(type='fk', field_name='create_by')
        }
        instance = faker.create(fields)
        object_list.append(instance)
    return object_list


def plancases_faker(maximum=10):
    faker = FakerModel(
        app='test_plans',
        model='PlanCases'
    )
    object_list = []  # for print out after created the objects.

    for _ in range(maximum):
        fields = {
            'plan': faker.fake_relations(type='fk', field_name='plan'),
            'case': faker.fake_relations(type='fk', field_name='case'),
        }
        instance = faker.create(fields)
        object_list.append(instance)
    return object_list
