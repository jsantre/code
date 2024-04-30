import os
import json

from pathlib import Path

import logging

logging.basicConfig(level=logging.DEBUG)

ROOT_DIR = Path.cwd()
TASK_DIR = os.path.join(ROOT_DIR, ".todo")
TASK_FILEPATH = os.path.join(TASK_DIR, "tasks.json")


def get_tasks():
    """found existing json task and return data
    :return: json data or empty dict
    :rtype: dict
    """
    if os.path.exists(TASK_FILEPATH):
        with open(TASK_FILEPATH, "r") as f:
            return json.load(f)
    return {}


def _write_task(tasks):
    """add task name to current tasks if not exist
    :param tasks: existing tasks with data
    :type tasks: dict
    """
    if not os.path.exists(TASK_DIR):
        os.makedirs(TASK_DIR)

    with open(TASK_FILEPATH, "w") as f:
        json.dump(tasks, f, indent=4)
        logging.info("Tasks updated")


def add_task(name):
    """add task name to current tasks if not exist
    :param name: task name
    :type name: str
    """
    tasks = get_tasks()
    if name in tasks.keys():
        logging.error("Task already exist")
        return

    tasks[name] = False
    _write_task(tasks)


def remove_task(name):
    """remove task name to current tasks if exist
    :param name: task name
    :type name: str
    """
    tasks = get_tasks()
    if name not in tasks.keys():
        logging.error("Task {} doesnt exist".format(name))
        return

    del tasks[name]
    _write_task(tasks)


def set_task_status(name, status=True):
    """change task status from given name
    :param name: task name
    :type name: str
    :param status: new status
    :type name: bool
    """
    tasks = get_tasks()
    if name not in tasks.keys():
        logging.error("Task {} doesnt exist".format(name))
        return

    tasks[name] = status
    _write_task(tasks)
