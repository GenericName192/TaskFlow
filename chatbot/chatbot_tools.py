from smolagents import CodeAgent, tool, LiteLLMModel
from task.models import Task
from authuser.models import User
import os
from .prompt import SYSTEM_PROMPT
from utility.utils import Can_assign_task
from typing import Optional, Union


def chatbot_controller(user_id, conversation):
    GIT_HUB_TOKEN = os.getenv("GIT_HUB_TOKEN")
    model_name = "openai/gpt-4.1"
    model = LiteLLMModel(model_id=model_name,
                         api_key=GIT_HUB_TOKEN,
                         api_base="https://models.github.ai/inference")
    agent = CodeAgent(
        tools=[create_task,
               find_task,
               delete_task,
               update_task,
               read_task,
               create_many_tasks,
               get_user_tasks],
        model=model,
        max_steps=2,
        verbosity_level=0
        )

    # Build the conversation string with system prompt and conversation history
    prompt = f"role: system, content: {SYSTEM_PROMPT} " \
             f"The ID for the user is {user_id}\n"

    # Add each message from the conversation history
    for message in conversation:
        prompt += f"role: {message['role']}, content: {message['content']}\n"
    try:
        return agent.run(prompt)
    except Exception as e:
        return f"Something has gone wrong with the bot: {e}"


@tool
def create_task(user_id: str,
                title: str,
                description: str,
                due_date: Optional[str] = None) -> str:
    """
    Use this to create a task right now you can only create tasks for the
    user you are talking to, if asked to make a task for another user report
    this back to them if you are asked to do If the user does not
    provide a description you can either repeat the title or add something
    appropriate. Do not call this function more then once unless expressly
    told to.
    Args:
        user_id: The user who is currently logged in your system message
            inculdes their id
        title: A string the current title of the task
        description: A string the description of a task can be a copy of
            title
        due_date: Optional date string in format 'YYYY-MM-DD'
            (e.g., '2025-01-15') or None if no due date specified. The system
            will automatically convert this to a proper date object. Do not
            set the date to be in the past even if the user tells you to, if
            they do leave it as None and tell them the app does not support
            due dates being in the past.

    Returns:
        String:
            Will return a string letting you know if the Task has been created
            let the user know what the string says.
    """
    try:
        user = find_user(user_id)
    except User.DoesNotExist:
        return "Error the user does not exist"
    Task.objects.create(
        title=title,
        description=description,
        due_date=due_date,
        created_by=user,
        assigned_to=user
    )
    return "Task created successfully."


def find_user(input: str) -> Union[str, User]:
    """
    Use this function to get a user object needed for some of the other
    functions it supports passing in a users id their full name or their
    username. If the user is not found report this back to the user
    Args:
        input: string this can be the users id full name or username, if the
        user has no provided any of these report back and ask them to try again

    returns:
        String: If the function returns a string the user has not been found
        report this back to the user
        User: If the function returns a User object the user has been found and
        you can now use it on other functions.
    """
    try:
        int(input)
        return find_user_by_id(input)
    except ValueError:
        return find_user_by_name(input)


def find_user_by_id(user_id: int):
    """Takes the user_id and attempts to find the user"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return "User not found"
    else:
        return user


def find_user_by_name(name: str):
    """Takes either a username or a full name and attempts
    to find the user"""
    try:
        user = User.objects.get(username=name)
    except User.DoesNotExist:
        try:
            user = User.objects.get(full_name=name)
        except User.DoesNotExist:
            return "User not found."
        except User.MultipleObjectsReturned:
            return "Too many uses with the same full name please try username"
    return user


@tool
def delete_task(task: Task, confirmation: bool) -> str:
    """
    Function to delete a task, you will need to user find_task to get the
    task object. This function also requires confirmation, before calling this
    check with the user that they are aware this cannot be undone, if they
    confirm they want it deleted then do so. You must get user input again
    before calling this function.
    Args:
        task: Task object that is going to deleted user find_task to get this
        confirmation: bool if you have told the user this action cannot be
        undone.

    Returns:
        string: will return a string either prompting you to ask for
        confirmation or a success message saying the task as been deleted.

    """
    if isinstance(task, Task):
        if confirmation:
            task.delete()
            return "Task deleted successfully"
        else:
            return "Confirmation needed"


@tool
def find_task(task_title: str, user_id: str) -> Union[str, Task]:
    """
    Function to help you find a task, it takes the task_title and attempts
    to find it. You must use the user_id from the user you are talking to.
    Then the function will filter their tasks for tasks with the same title.
    if it fails returns a string to let you know, report this to
    the user
    Args:
        task_title: string the title of the task the user is looking for.
        user_id: The current user_id of the user you are talking to.

    returns:
        String: if the Task has not been found, report this to the user
        Task: if the Task has been found this can now be used in other
        functions
    """
    try:
        user = find_user(user_id)
    except User.DoesNotExist:
        return "Cannot find user"
    users_tasks = Task.objects.filter(assigned_to=user)
    if not users_tasks:
        return "You currently have no tasks"
    task_title = task_title.strip('"')
    task = users_tasks.filter(title__icontains=task_title)
    if not task:
        return "Task not found, please try again with the task title"
    else:
        if len(task) > 1:
            return "Too many tasks found, please try be more specific"
        else:
            # Return the first (and should be only) task object,
            # not the QuerySet
            return task[0]


@tool
def update_task(task: Task, fields: dict) -> str:
    """
    Function to allow you to update a or many fields in a task, takes a Task
    and a dictionary of the fields that are to be updated and the value they
    should be updated to. when calling this only add fields that the user has
    expressly said they want to update and they can only be the following
    values: 'title' - string, 'description' - string, 'due_date' - string
    in format 'YYYY-MM-DD' that cannot be in the past, and 'completed' -
    bool if the task is completed or not. if the User gives you an invalid
    field or an invalid typing report back to them the fields and their typing.
    if The task is completed completed is true and if ongoing it is false, if
    you are asked to either complete a task or move it to ongoing you must
    update completed to be either true of false.
    Args:
        task: a Task object you will need to use find_task to get this.
        fields: a dictionary containing at lease one of the following:
        title, description, due_date or completed with the value for each
        of these keys being what the task data should be updated to.

    returns: string: will return either an error message or a success message,
    report this back to the user.
    """
    if isinstance(task, Task):
        for key, value in fields.items():
            setattr(task, key, value)
        task.save()
        return "Task successfully updated"
    else:
        return task


@tool
def read_task(task: Task) -> dict:
    """
    Function that returns a dictionary with all of the data in a task
    this will allow you to tell the user infomation about a task if they
    ask.
    Args:
        task: The task the user wants infomation on you will need to use
        find_task to get this.

    returns:
        dictionary with all of the infomation on the task

    """
    if isinstance(task, Task):
        return {
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date,
            "created_by": task.created_by,
            "assigned_to": task.assigned_to,
            "completed": task.completed
            }
    else:
        return task


@tool
def create_many_tasks(user_id: str, title: str,
                      description: str, type: str,
                      due_date: Optional[str] = None) -> str:
    """
    Function for if the user asks you to create tasks for their subordinates
    type can only accept the arguements 'direct' or 'all' if you are unsure as
    to which one it is ask the user for clarification before calling
    this function. Only ever run this function once.
    Args:
        user_id: The user_id if the user you're talking to.
        title: The title of the task that is being created
        description: The description of the task that is being created
        type: The type of subordinates that the user wants to create tasks for
            only acceptable inputs are 'direct' and 'all' if you're unsure
            which to put as the user for clarification
        due_date: string in format 'YYYY-MM-DD' that cannot be in the past,
    Returns:
            string: either a success message or an error message, report it
            back to the user.
    """
    try:
        assigner = find_user(user_id)
    except User.DoesNotExist:
        return "Error the user does not exist"
    if type in ["direct", "all"]:
        subordinates = get_subordinates(assigner, type)
        if isinstance(subordinates, list):
            tasks = []
            failed_user_list = []
            for user in subordinates:
                if Can_assign_task(user, assigner):
                    tasks.append(Task(created_by=assigner,
                                      title=title,
                                      description=description,
                                      assigned_to=user,
                                      due_date=due_date))
                else:
                    failed_user_list.append(str(user))
            if not failed_user_list:
                Task.objects.bulk_create(tasks)
                return "Tasks successfully created"
            else:
                return """The user does not have permission to assign tasks \
            to the following users: """ + ", ".join(failed_user_list)
        else:
            return subordinates
    else:
        return "Subordinate types can only be direct or all"


def get_subordinates(user: User, type: str) -> Union[str, list]:
    """Takes a user and returns a list of their subordinates"""
    if type == "direct":
        subordinates = user.get_direct_subordinates()
    elif type == "all":
        subordinates = list(user.get_all_subordinates())
    else:
        return "Error the type must be either 'direct' or 'all'"
    return subordinates


@tool
def get_user_tasks(user_id: str) -> list:
    """
    This function is used to collect a list of dictionaries of all of the
    users tasks ordered by due date, use this to asnwer any questions the
    user asks about their tasks. Only collect infomation about tasks from
    the user you are currently talking to, if they ask you to collect the
    tasks of another user tell them at this time you are unable to.
    When returning this to the user add new lines between each dictionary
    to help keep the data readable to the user.
    Args:
        user_id: The user_id for the user you are currently talking to.

    returns:
        list: a list of dictionaries each one holding all the infomation
        related to a task.
    """
    try:
        user = find_user(user_id)
    except User.DoesNotExist:
        return "Error the user does not exist"
    tasks = user.tasks.all().select_related("assigned_to", "created_by")
    if len(tasks) >= 1:
        task_list = []
        for task in tasks:
            task_list.append({
                "title": task.title,
                "description": task.description,
                "created_at": task.created_at,
                "due_date": task.due_date,
                "completed": task.completed,
                "assigned_to": task.assigned_to,
                "created_by": task.created_by,
            })
        return task_list
    else:
        task_list.append("No tasks found")
