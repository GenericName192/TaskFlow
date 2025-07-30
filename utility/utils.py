from task.models import Task


def Can_assign_task(task_user, assigning_user):
    """Returns true if the user can assign false if they cant"""
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


def can_be_boss(user, new_boss):
    """Check to see if new boss can be assigned as the users boss"""
    if new_boss is None:
        return True
    users_subordinates = user.get_all_subordinates()
    # if the boss is in user_subordinates then it will cause
    # a circular hierarchy so this returns true if they're not
    # and false if they are.
    return new_boss not in users_subordinates


def get_all_team_tasks(user):
    user_subordinates = user.get_all_subordinates()
    team_members_and_tasks = {user.full_name: user.tasks.all()}
    for subordinate in user_subordinates:
        team_members_and_tasks[subordinate.full_name] = subordinate.tasks.all()
    return team_members_and_tasks


def mass_create_tasks(user_list, form, active_user):
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
