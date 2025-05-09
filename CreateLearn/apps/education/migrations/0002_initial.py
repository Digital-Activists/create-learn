# Generated by Django 5.2 on 2025-04-30 13:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('education', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_courses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='enrolled_courses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='flashcard',
            name='deck',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='education.flashcarddeck', verbose_name='Набор'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='education.course', verbose_name='Курс'),
        ),
        migrations.AddField(
            model_name='flashcarddeck',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flashcard_decks', to='education.lesson', verbose_name='Урок'),
        ),
        migrations.AddField(
            model_name='lessonattachment',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='education.lesson', verbose_name='Урок'),
        ),
        migrations.AddField(
            model_name='matchingansweroption',
            name='left',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='left_options', to='education.matchingitem'),
        ),
        migrations.AddField(
            model_name='matchingansweroption',
            name='right',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='right_options', to='education.matchingitem'),
        ),
        migrations.AddField(
            model_name='matchingansweroption',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matching_options', to='education.question'),
        ),
        migrations.AddField(
            model_name='answeroption',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_options', to='education.question'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='lesson',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='education.lesson'),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='education.quiz'),
        ),
        migrations.AddField(
            model_name='useranswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.question'),
        ),
        migrations.AddField(
            model_name='useranswer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprogresscourse',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.course'),
        ),
        migrations.AddField(
            model_name='userprogresscourse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprogresslesson',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education.lesson'),
        ),
        migrations.AddField(
            model_name='userprogresslesson',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='lesson',
            constraint=models.UniqueConstraint(fields=('course', 'module', 'order'), name='unique_lesson_order_per_course'),
        ),
        migrations.AlterUniqueTogether(
            name='matchingansweroption',
            unique_together={('question', 'left')},
        ),
        migrations.AddIndex(
            model_name='useranswer',
            index=models.Index(fields=['user', 'question'], name='education_u_user_id_aa7618_idx'),
        ),
        migrations.AddIndex(
            model_name='useranswer',
            index=models.Index(fields=['is_correct'], name='education_u_is_corr_fa39a7_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='useranswer',
            unique_together={('user', 'question')},
        ),
    ]
