from smolagents import CodeAgent, InferenceClientModel, tool
from task.models import Task
from authuser.models import User
import os
from .prompt import SYSTEM_PROMPT
from utility.utils import Can_assign_task
from typing import Optional, Union


def chatbot_controller(user_id, message):
    HF_TOKEN = os.getenv("HF_TOKEN")
    print(f"DEBUG: HF_TOKEN exists: {HF_TOKEN is not None}")
    # Try a known working model first
    model_name = "Qwen/Qwen2.5-Coder-32B-Instruct"
    print(f"DEBUG: Using model: {model_name}")
    model_test = InferenceClientModel(model_id=model_name,
                                      api_key=HF_TOKEN,)
    agent = CodeAgent(
        tools=[create_task,
               find_task,
               find_user,
               delete_task,
               update_task,
               read_task,
               create_many_tasks],
        model=model_test,
        max_steps=5,
        verbosity_level=2
        )
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
            {SYSTEM_PROMPT} The ID for the user is {user_id}
            <|eot_id|><|start_header_id|>user<|end_header_id|>
            {message}
            <|eot_id|><|start_header_id|>assistant<|end_header_id|>
            """
    return agent.run(prompt)


@tool
def create_task(assigner: User,
                title: str,
                description: str,
                target_user: User,
                due_date: Optional[str] = None) -> str:
    """
    Use this to create a task You will need to use the find_user tool
    first to get both the assigner and the target_user. If the user does not
    provide a description you can either repeat the title or add something
    appropriate.
    Args:
        assigner: The user who is currently logged in your system message
            inculdes their ID, use find_user to get the User object.
        title: A string the current title of the task
        description: A string the description of a task can be a copy of
            title
        target_user: The User the task is for, The user will give
            you a ID a username or a full name, use find_user to find them.
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
    if Can_assign_task(target_user, assigner):
        Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            created_by=assigner,
            assigned_to=target_user
        )
        return "Task created successfully."
    else:
        return "The user does no have permission to update this user."


@tool
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
    confirm they want it deleted then do so.
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
def find_task(task_title: str) -> Union[str, Task]:
    """
    Function to help you find a task, it takes the task_title and attempts
    to find it. if it fails returns a string to let you know, report this to
    the user
    Args:
        task_title: string the title of the task the user is looking for.

    returns:
        String: if the Task has not been found, report this to the user
        Task: if the Task has been found this can now be used in other
        functions
    """
    try:
        task = Task.objects.filter(title__icontains=task_title)
    except Task.DoesNotExist:
        return "Task not found, please try again with the task title"
    else:
        if len(task) > 1:
            return "Too many tasks found, please try be more specific"
        else:
            return task


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
def create_many_tasks(assigner: User, title: str,
                      description: str, type: str,
                      due_date: Optional[str] = None) -> str:
    """
    Function for if the user asks you to create tasks for their subordinates
    type can only accept the arguements 'direct' or 'all' if you are unsure as
    to which one it is ask the user for clarification before calling
    this function.
    Args:
        assigner: User object for the user that you are talking to must
        find_user to get.
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
    if type in ["direct", "all"]:
        subordinates = get_subordinates(assigner, type)
        if subordinates:
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
            return "That user has no subordinates"
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
