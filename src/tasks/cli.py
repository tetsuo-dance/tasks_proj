# -*- Coding: utf-8 -*-
"""Command Line Interface (CLI) for tasks project."""

from __future__ import print_function
import click
import tasks.config
from contextlib import contextmanager
from tasks.api import Task


# The main entry point for tasks.
@click.group(context_settings={'help_option_names': ['-h', '--help']})
#クリックにコマンドラインを登録する。addとかdeleteとかサブコマンドを登録していく。
@click.version_option(version='0.1.1')
def tasks_cli():
    """Run the tasks application.(cahgened)"""
    pass


@tasks_cli.command(help="add a task")
@click.argument('summary')
@click.option('-o', '--owner', default=None,
              help='set the task owner')
@click.option('-dl', '--deadline', default=None,
              help='set the deadline')
def add(summary, owner, deadline):
    """Add a task to db."""
    with _tasks_db():

        tasks.add(Task(summary, owner, deadline))

@tasks_cli.command(help="delete a task")
@click.argument('task_id', type=int)
def delete(task_id):
    """Remove task in db with given id."""
    with _tasks_db():
        tasks.delete(task_id)

@tasks_cli.command(help="deletedone a task")
def deletedone():
    """Remove done task."""
    with _tasks_db():
        tasks.deletedone()


@tasks_cli.command(name="list", help="list tasks")
#　name=list で呼べる
@click.option('-o', '--owner', default=None,
              help='list tasks with this owner')
def list_tasks(owner):
    """
    List tasks in db.

    If owner given, only list tasks with that owner.
    """
    formatstr = "{: >4} {: >10} {: >10} {: >5} {}"
    print(formatstr.format('ID', 'owner', 'deadline', 'done', 'summary'))
    print(formatstr.format('--', '-----', '--------', '----', '-------'))
    with _tasks_db():
        for t in tasks.list_tasks(owner):
            done = 'True' if t.done else 'False'
            owner = '' if t.owner is None else t.owner
            deadline = '' if t.deadline is None else t.deadline
            print(formatstr.format(
                  t.id, owner, deadline, done, t.summary))


@tasks_cli.command(help="update task")
@click.argument('task_id', type=int)
@click.option('-o', '--owner', default=None,
              help='change the task owner')
@click.option('-s', '--summary', default=None,
              help='change the task summary')
@click.option('-d', '--done', default=None,
              type=bool,
              help='change the task done state (True or False)')
@click.option('-dl', '--deadline', default=None,
              help='change the deadline')
def update(task_id, owner, summary, done, deadline):
    """Modify a task in db with given id with new info."""
    with _tasks_db():
        tasks.update(task_id, Task(summary, owner, done, deadline))


@tasks_cli.command(help="list count")
def count():
    """Return number of tasks in db."""
    with _tasks_db():
        c = tasks.count()
        print(c)



@contextmanager
def _tasks_db():
    config = tasks.config.get_config()
    #設定をひっぱってる→DBの場所、
    #定義ジャンプする
    tasks.start_tasks_db(config.db_path, config.db_type)
    #
    yield
    #tasks_dbを呼び出した元に、呼び出し元に処理を戻す
    tasks.stop_tasks_db()



if __name__ == '__main__':
    tasks_cli()
