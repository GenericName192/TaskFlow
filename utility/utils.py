from task.models import Task
from authuser.models import User
from django.forms import ModelForm


def Can_assign_task(task_user: User, assigning_user: User) -> bool:
    """Checks to see if a user is able to assign a task to the task_user.

    Args:
        task_user: A User that the task will be assigned to.
        assigning_user: A User that the task will be assigned by.

    Returns:
        bool: True if the user can assign, False if they cannot.
    """
    can_assign = [task_user.id]
    boss = task_user.boss
    # creates loops that collects the boss until the value is null
    while boss:
        # if the user is already in bosses then its stuck in a loop
        if boss in can_assign:
            break
        else:
            can_assign.append(boss.id)
            boss = boss.boss
    return assigning_user.id in can_assign


def can_be_boss(user: User, new_boss: User) -> bool:
    """Check to see if a circular hierarchy would be formed by the
    user being assigned new_boss as a boss.

    Args:
        user: The User whose boss may be reassigned.
        new_boss: The User who it will be reassigned to.

    Returns:
        bool: True if the user can be assigned without issue, False if it would
              create a circular hierarchy.
    """
    if new_boss is None:
        return True
    users_subordinates = user.get_all_subordinates()
    # if the boss is in user_subordinates then it will cause
    # a circular hierarchy so this returns true if they're not
    # and false if they are.
    return new_boss not in users_subordinates


def get_all_team_tasks(user: User) -> dict:
    """Gets a dict of all of the user's team members and their tasks.

    Args:
        user: The user whose team you want to view.

    Returns:
        dict: A dict with each team member's full_name as the key
              and a list of all of their tasks as the value.
    """
    user_subordinates = (user.get_all_subordinates()
                         .prefetch_related('tasks'))
    team_members_and_tasks = {user.full_name: user.tasks.all()}
    for subordinate in user_subordinates:
        team_members_and_tasks[subordinate.full_name] = subordinate.tasks.all()
    return team_members_and_tasks


def mass_create_tasks(user_list: list, form: ModelForm, active_user: User):
    """ Creates the same task for each user in a user_list

    Validates the form and checks that each user can be assigned a task by the
    active_user. Uses an all-or-nothing approach - if any user cannot be
    assigned a task, no tasks are created. On success, uses bulk_create
    for efficiency. returns a success message.

    Args:
        user_list: a list of users for whom the tasks should be assigned.
        form: The form submitted with all the information about the task.
        active_user: The user who has submitted the form.

    Returns:
        Tuple:
            (success_bool, message_string) - Bool to say if it was successful
            or not and string with the error/success message.
    """
    if not user_list:
        return False, "empty list detected, please try again"
    if form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        due_date = form.cleaned_data["due_date"]
        created_by = active_user
        tasks = []
        success_user_list = []
        failed_user_list = []
        for user in user_list:
            if Can_assign_task(user, active_user):
                success_user_list.append(user.full_name)
                tasks.append(Task(
                    title=title,
                    description=description,
                    due_date=due_date,
                    created_by=created_by,
                    assigned_to=user))
            else:
                failed_user_list.append(user.full_name)
        if failed_user_list:
            return False, ", ".join(failed_user_list) + "failed"
        else:
            try:
                Task.objects.bulk_create(tasks)
            except Exception as e:
                return False, str(e)
            return True, ", ".join(success_user_list)


def calculate_user_task_statistics(user: User) -> dict:
    """Takes a user and provides useful statics to be displayed on the
    index page e.g: upcoming tasks and completed/going counts
    args:
        user - The user who is viewing the index page who the stats will
        be about
    returns:
        dict - A dict with all of the stats that will be passed to
        the index page.
        - total_tasks_count: total number of tasks the user has.
        - completed_tasks_count: number of completed tasks the user has.
        - total_ongoing_tasks: number of ongoing tasks the user has.
        - up_coming_tasks: QuerySet of upcoming tasks."""
    tasks = user.tasks.all().select_related("assigned_to", "created_by")
    total_tasks_count = len(tasks)
    completed_tasks_count = len([x for x in tasks if x.completed is True])
    total_ongoing_tasks = total_tasks_count - completed_tasks_count
    up_coming_tasks = tasks.filter(completed=False).order_by("due_date")

    content = {
                "total_tasks_count": total_tasks_count,
                "completed_tasks_count": completed_tasks_count,
                "total_ongoing_tasks": total_ongoing_tasks,
                "up_coming_tasks": up_coming_tasks
                }
    return content
