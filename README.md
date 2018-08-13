Загрузка фикстур
```bash
./manage.py loaddata initial_data
```

Генерация кейсов  и планов
```bash
./manage.py djipsum --auto_gen --custom_generation=modules.test_cases.djipsum.casefaker.case_faker
./manage.py djipsum --auto_gen --custom_generation=modules.test_plans.djipsum.planfaker.plan_faker
./manage.py djipsum --auto_gen --custom_generation=modules.test_plans.djipsum.planfaker.plancases_faker
```
