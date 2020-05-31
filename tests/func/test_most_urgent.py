# -*- Coding: utf-8 -*-
import tasks
from tasks import Task


def test_most_urgent(tasks_db):
    tasks.add(Task('起きる', 'yattom'))
    tasks.add(Task('喰べる', 'yattom'))
    tasks.add(Task('寝る', 'yattom'))
    urgent_task = tasks.get_urgent_task()
    assert urgent_task.summary == '起きる'


def test_most_urgent_only_in_not_done(tasks_db):
    tasks.add(Task('起きる', 'yattom', True))
    tasks.add(Task('喰べる', 'yattom'))
    tasks.add(Task('寝る', 'yattom'))
    urgent_task = tasks.get_urgent_task()
    assert urgent_task.summary == '喰べる'


def test_most_urgent_when_none(tasks_db):
    urgent_task = tasks.get_urgent_task()
    assert urgent_task is None
