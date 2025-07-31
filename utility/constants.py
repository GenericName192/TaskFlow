# utility/constants.py
"""
Project-wide constants for URLs, and, templates.
Centralizes all hardcoded strings to improve maintainability.
"""

# URL NAMES
LOGIN_URL_NAME = 'login_view'
INDEX_URL_NAME = 'index'
PROFILE_URL_NAME = 'profile'
TASK_LIST_URL_NAME = 'task_list'
EDIT_PROFILE_URL_NAME = 'edit_profile'
CHANGE_PASSWORD_URL_NAME = 'change_password'
BULK_TASK_CREATION_URL_NAME = 'bulk_task_creation'
REGISTER_URL_NAME = 'register'
LOGOUT_URL_NAME = 'logout_view'
TOGGLE_COMPLETE_URL_NAME = 'toggle_complete'
TASK_DETAILS_URL_NAME = 'task_details'
UPDATE_TASK_URL_NAME = 'update_task'
DELETE_TASK_URL_NAME = 'delete_task'

# TEMPLATE NAMES
INDEX_TEMPLATE = 'authuser/index.html'
PROFILE_TEMPLATE = 'authuser/profile.html'
EDIT_PROFILE_TEMPLATE = 'authuser/edit_profile.html'
LOGIN_TEMPLATE = 'authuser/login.html'
REGISTER_TEMPLATE = 'authuser/register.html'
TASK_LIST_TEMPLATE = 'task/task_list.html'
BULK_TASK_TEMPLATE = 'task/bulk_task_creation.html'
UPDATE_PASSWORD_TEMPLATE = 'authuser/update_password.html'
TASK_DETAILS_TEMPLATE = 'task/task_details.html'
TASK_UPDATE_TEMPLATE = 'task/task_update.html'
