from django.db import migrations, models


def split_tech_stack_strings(apps, schema_editor):
    """Turn each project's old "Python, Django" string into shared TechStack rows."""
    Project = apps.get_model('punsalang_q2', 'Project')
    TechStack = apps.get_model('punsalang_q2', 'TechStack')

    for project in Project.objects.all():
        for raw_name in project.tech_stack.split(','):
            name = raw_name.strip()
            if not name:
                continue
            stack = TechStack.objects.filter(name__iexact=name).first()
            if stack is None:
                stack = TechStack.objects.create(name=name)
            project.tech_stacks.add(stack)


def join_tech_stacks(apps, schema_editor):
    Project = apps.get_model('punsalang_q2', 'Project')

    for project in Project.objects.all():
        project.tech_stack = ', '.join(stack.name for stack in project.tech_stacks.all())
        project.save(update_fields=['tech_stack'])


class Migration(migrations.Migration):

    dependencies = [
        ('punsalang_q2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TechStack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='project',
            name='tech_stacks',
            field=models.ManyToManyField(related_name='projects', to='punsalang_q2.techstack'),
        ),
        migrations.RunPython(split_tech_stack_strings, join_tech_stacks),
        migrations.RemoveField(
            model_name='project',
            name='tech_stack',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='tech_stacks',
            new_name='tech_stack',
        ),
    ]
