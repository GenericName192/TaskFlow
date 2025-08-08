# TaskFlow
### By David Barton

live site - https://ci-david-barton-task-flow-85f82739c5b8.herokuapp.com/

project board -  https://github.com/users/GenericName192/projects/6/views/1

![Website landing page](/documentation/TaskFlow-landing-page.png)

## Index
1. [Overview](#overview)
2. [UX Design Process](#ux-design-process)
    - [User Stories](#user-stories)
    - [Wireframes](#wireframes)
    - [Color Scheme](#color-scheme)
    - [Fonts](#fonts)
3. [Features](#features)
4. [Improvements](#improvments-and-future-development)
5. [Deployment](#deployment)
6. [Testing and Validation](#testing-and-validation)
7. [AI implementation](#ai-implementation)
8. [Database](#database)
9. [References](#references)
10. [Tech used](#tech-used)
11. [Learning points](#learning-points)


## Overview
A to do website created using Django allowing you to track yours and your subordinates tasks with the additon of a chatbot to help you perform these tasks. If you would like to test it the password for all of the test users is Placeholder123 with a username of Testuser0 - testuser20 please do not change the passwords.

## UX Design Process
<details>

project board -  https://github.com/users/GenericName192/projects/6/views/1

### User stories
<details>
1. Authentication & Profiles

- As a user, I want to sign up and log in so that I can securely access my tasks.
- As a user, I want to edit my profile (name, email, boss) so that my information stays up to date.
- As a manager, I want to set who reports to me so that I can assign them tasks.

2. Task Management

- As a user, I want to create a task for myself so that I can track my personal work.
- As a manager, I want to create a task for my subordinates so that I can delegate work.
- As a manager, I want to assign a task to all users under my hierarchy so that I can broadcast important tasks (e.g., team meetings).
- As a user, I want to view all tasks assigned to me so that I know what I need to complete.
- As a user, I want to update the status of a task (e.g., Pending → Done) so that I can track progress.
- As a user, I want to delete my own tasks so that I can keep my task list clean.

3. Hierarchy & Permissions

- As a user, I want to see who my boss is so that I know my reporting line.
- As a manager, I want to view all my subordinates so that I know who I can assign tasks to.
- As a manager, I want to see tasks I’ve assigned to others so that I can track their progress.

4. Chatbot Integration

- As a user, I want to ask the chatbot to create a task for me so that I can save time.
- As a manager, I want to ask the chatbot to assign a task to all my subordinates so that I can quickly delegate work.
- As a user, I want the chatbot to list my pending tasks so that I can quickly review my workload.

All have been achived at this point but the last chatbot story of giving a list of pending tasks however this will be added if I have time.
</details>

### Wireframes

<details>
Task list page

![moblie wireframe](/documentation/capstone-moblie-main-page.png)

![tablet wireframe](/documentation/capstone-tablet-main-page.png)

![desktop wireframe](/documentation/capstone-pc-main-page.png)

![chatbot wireframe](/documentation/capstone-chat-bot-view.png)

These were the orginal wireframes I designed for the project, however the project ended up growing in scoop
and new wireframes were needed and some designers were changed, for example the desktop wireframe ended up
making the page feel too cluttered so I went with the tablet wireframe for all sizes above the tablet.
and the moblie wireframe for anything smaller.

here are the wireframes for the addiontal pages added:

![moblie wireframe landing page](/documentation/landing-page-wireframe-moblie.png)

![tablet and up wireframe landing page](/documentation/landing-page-wireframe-tablet-up.png)

![moblie wireframe profile page](/documentation/profile-moblie-view.png)

![tablet and up wireframe profile page](/documentation/profile-tablet-and-up-wireframe.png)
</details>

### Color schemes

<details>
The color scheme grew as the scoop of the project did, orginally I had the following planned with the help of chatGPT:

but in the end the scheme grew with the end result being:

![color scheme](/documentation/TaskFlow-color-scheme.png)

##### Primary Colors

Primary Purple: #3c2dcf (Main brand color - used for navigation, buttons)
Accent Purple: #7e2fcc (Lighter purple for gradients and hover states)
White: #ffffff (Clean backgrounds, button text)
##### Text Colors

Primary Text: #212529 (Dark gray for main content)
Secondary Text: #ffffff (White text on colored backgrounds)
##### Background Colors

Primary Background: #F9FAFB (Very light gray for page backgrounds)
Light Background: #f8f9fa (Slightly different light gray for cards)
Border Color: #e0e4e7 (Light gray for borders)
##### Status Colors

Success Green: #198754 (Completed tasks, success messages)
Success Light: #d4edda (Success background)
Success Text: #155724 (Success text)
Danger Red: #dc3545 (Delete buttons, error messages)
Warning Yellow: #fff3cd (Warning backgrounds)
Warning Text: #856404 (Warning text)
</details>

### Fonts

<details>
The fonts I went with were Roboto for the primary and Poppins for secondary, I wanted to go with a professional look and I felt these served that well. They were picked in collaboration with ChatGPT.
</details>
</details>

## Features

<details>
Main page
 - list of tasks
 - add task
 - chatbot 

Profile page
 - profile picture
 - user data with ability to update it
 - list of subordinates
 - managers name

These were the orginally planned features with an optional chatbot if I had time, however as I started to make the project I added an additional landing page

#### Landing page

![Landing page](/documentation/TaskFlow-landing-page.png)

As you can see the landing page shows some stats on your current tasks as well as a list of upcoming tasks. 
Also has a link to the main 2 pages profile and task list

#### Task list page

![task list page](/documentation/TaskFlow-tasks-one.png)

![task list page](/documentation/TaskFlow-tasks-two.png)

This is where you can perform your crud functionality on your tasks, can create at the top read update and delete below.

##### Task update

![task update page](/documentation/TaskFlow-update_task.png)

##### Task details

![task details page](/documentation/TaskFlow-task-details.png)

##### Task delete

![task details page](/documentation/TaskFlow-delete-task.png)

#### Profile page

![profile page](/documentation/TaskFlow-profile-one.png)

![profile page](/documentation/TaskFlow-profile-two.png)

This is where you can view your user account aswell as update infomation to it, you can also view a list of all direct and indirect subordinates. I in the end decided to remove the profile picture part as I was running low on the API key I had planned to use for this and felt it didnt really add anything

##### Change user details

![change user details](/documentation/TaskFlow-edit-profile.png)

##### Change password

![change password](/documentation/TaskFlow-change-password.png)

#### Chat bot

![chatbot](/documentation/capstone-chat-bot-view.png)

Is part of of the base.html therefore can be viewed on any page.

#### Custom error pages

##### 404 page not found

![404 page](/documentation/TaskFlow-404-error.png)

##### 403 access denied

![403 page](/documentation/TaskFlow-403-error.png)

##### 500 server issue

![500 page](/documentation/TaskFlow-500-error.png)
</details>

## Improvements and Future Developement

<details>
The AI could use with more tools atm its functionality is quite limited and to the point it hasnt manage to hit all the user stories yet. I also feel like there are some database optimizations that could be done to make the site run faster.
I also once again did not spend enough time planning and as such there were a lot of changes made during the development cycle that I should have decided on during the planning process I feel like I did better then I have done in the past the ERD I did helped but I still feel like this is an area of improvement for me.
</details>

## Testing and Validation

<details>
### HTML Validation

There was some feedback under info for each page but I decided to ignore this as it was an error introduced by prettier my formatter.

Users

![landing page](/documentation/landingpage-val.png)
![profile](/documentation/profile-val.png)
![edit profile](/documentation/profile-edit-val.png)
![change password](/documentation/change-password-val.png)

Tasks

![task list](/documentation/task-view-val.png)
![task details](/documentation/task-detail-val.png)
![task update](/documentation/task-update-val.png)
![bulk task creation](/documentation/bulk-create-val.png)

Errors

![404](/documentation/404val.png)
![403](/documentation/403-val.png)
![500](/documentation/500-val.png)

### CSS validation

![css validation](/documentation/css-validation.png)

### Python validation

authuser model
![authuser model](/documentation/authuser-model-val.png)

authuser views
![authuser views](/documentation/authuser-views-val.png)

chatbot tools
![chatbot tools](/documentation/chatbot-tools-val.png)

chatbot views
![chatbot views](/documentation/chatbot-views-val.png)

task models
![task models](/documentation/python-task-view-val.png)

task views
![task views](/documentation/task-view-val.png)

utils
![utils](/documentation/utils-val.png)

### JS validation

![js val](/documentation/js-val.png)


### Lighthouse

I have implimented some caching via whitenoise so performance is a bit hard to test on intial loading of the page so these are for the second loading of the page the one that lighthouse does during the testing.

![landing page](/documentation/landing-page-lighthouse.png)
![profile page](/documentation/profile-lighthouse.png)
![task page](/documentation/task-list-lighthouse.png)

### Wave

The only errors I had for wave were missing headings and redundant links but I decided to not fix these due to time restraints

![landing page](/documentation/Wave-landing-page.png)
![profile page](/documentation/profile-wave.png)
![task page](/documentation/task-list-wave.png)

### Testing

I have a series of 66 unit tests that were written in collaboration with copilot that can be found in the tests.py in each app. 

![unit tests](/documentation/unit-tests.png)

I also did a series of manual tests with me and a family member checking that each feature worked correctly.
There is currently no testing beyond manual testing for the chatbot as it is still a bit unperdictable. Some users have reported a bug with the AI saying unexpected token < I have been unable to reproduce this bug so I am unsure as to what it causing it. This is something I would like to spend more time on trying to fix. There is also a bug with the AI sometimes returning its thoughts as well as the answer to the prompt, I have tried to address this in the system prompt but it still sometimes happens.
I will however be adding a video of some testing of the chatbot incase the API key has been used up by the time of CIs testing.

# TaskFlow Application Testing Matrix

| Component | Functionality | Test Type | Status |
|-----------|--------------|-----------|---------|
| **USER AUTHENTICATION & MODELS** |
| User Model | User creation | Unit | ✅ Pass |
| User Model | Full name property | Unit | ✅ Pass |
| User Model | String representation | Unit | ✅ Pass |
| User Model | Email uniqueness constraint | Unit | ✅ Pass |
| User Model | Default field values | Unit | ✅ Pass |
| User Model | Direct subordinates query | Unit | ✅ Pass |
| User Model | All subordinates hierarchy | Unit | ✅ Pass |
| User Model | Boss-subordinate relationship | Unit | ✅ Pass |
| **AUTHENTICATION VIEWS** |
| Login View | Valid credentials login | Unit | ✅ Pass |
| Login View | Invalid credentials handling | Unit | ✅ Pass |
| Login View | Redirect after login | Unit | ✅ Pass |
| Registration View | Valid data registration | Unit | ✅ Pass |
| Registration View | Duplicate username prevention | Unit | ✅ Pass |
| Logout View | Logout functionality | Unit | ✅ Pass |
| Login View | Template rendering | Manual | ✅  Pass |
| Registration View | Form field validation display | Manual | ✅  Pass |
| **INDEX/LANDING PAGE** |
| Index View | Authenticated user display | Unit | ✅ Pass |
| Index View | Unauthenticated user display | Unit | ✅ Pass |
| Index View | Tip of the day functionality | Unit | ✅ Pass |
| Index View | Task statistics display | Manual | ✅  Pass |
| Index View | Quick action buttons | Manual | ✅  Pass |
| **PROFILE MANAGEMENT** |
| Profile View | Own profile edit buttons | Unit | ✅ Pass |
| Profile View | Other profile edit restrictions | Unit | ✅ Pass |
| Profile View | Subordinates display | Unit | ✅ Pass |
| Profile View | Boss information display | Unit | ✅ Pass |
| Profile View | 404 for non-existent user | Unit | ✅ Pass |
| Edit Profile | Owner access control | Unit | ✅ Pass |
| Edit Profile | Form pre-population | Unit | ✅ Pass |
| Edit Profile | Successful update | Unit | ✅ Pass |
| Edit Profile | Validation error display | Unit | ✅ Pass |
| Edit Profile | Permission denied for others | Unit | ✅ Pass |
| Change Password | Owner access control | Unit | ✅ Pass |
| Change Password | Successful password change | Unit | ✅ Pass |
| Change Password | Form validation | Unit | ✅ Pass |
| Change Password | User stays logged in | Unit | ✅ Pass |
| Change Password | Permission denied for others | Unit | ✅ Pass |
| **TASK MODELS & FORMS** |
| Task Model | Task creation | Unit | ✅ Pass |
| Task Model | String representation | Unit | ✅ Pass |
| Task Model | Task completion toggle | Unit | ✅ Pass |
| Task Form | Valid form submission | Unit | ✅ Pass |
| Task Form | Past due date validation | Unit | ✅ Pass |
| Task Form | Required fields validation | Unit | ✅ Pass |
| Task Form | Form save functionality | Unit | ✅ Pass |
| Task Form | Description max length (500 chars) | Unit | ✅ Pass |
| **TASK VIEWS & FUNCTIONALITY** |
| Task List | Authenticated user access | Unit | ✅ Pass |
| Task List | Login required | Unit | ✅ Pass |
| Task List | Task creation via POST | Unit | ✅ Pass |
| Task List | Pagination (4 per page) | Manual | ✅  Pass |
| Task Toggle | Completion toggle | Unit | ✅ Pass |
| Task Details | Task details view | Unit | ✅ Pass |
| Task Update | Permission control | Unit | ✅ Pass |
| Task Update | Form styling and layout | Manual | ✅  Pass |
| Task Delete | Permission control | Unit | ✅ Pass |
| Task Delete | Confirmation modal | Manual | ✅  Pass |
| Bulk Tasks | Mass task creation | Manual | ✅  Pass |
| **UTILITY FUNCTIONS** |
| Can Assign Task | Manager to subordinate | Unit | ✅ Pass |
| Can Assign Task | CEO to hierarchy | Unit | ✅ Pass |
| Can Assign Task | User to self | Unit | ✅ Pass |
| Can Assign Task | Non-subordinate restriction | Unit | ✅ Pass |
| Can Assign Task | Subordinate to manager restriction | Unit | ✅ Pass |
| Can Be Boss | Valid boss assignment | Unit | ✅ Pass |
| Can Be Boss | None boss validity | Unit | ✅ Pass |
| Can Be Boss | Circular hierarchy prevention | Unit | ✅ Pass |
| Can Be Boss | Self-boss prevention | Unit | ✅ Pass |
| Get Team Tasks | Manager team tasks | Unit | ✅ Pass |
| Get Team Tasks | Employee own tasks | Unit | ✅ Pass |
| Mass Create Tasks | Successful creation | Unit | ✅ Pass |
| Mass Create Tasks | Empty user list | Unit | ✅ Pass |
| Mass Create Tasks | Invalid form handling | Unit | ✅ Pass |
| Mass Create Tasks | Permission failure | Unit | ✅ Pass |
| Task Statistics | Basic statistics calculation | Unit | ✅ Pass |
| Task Statistics | User with no tasks | Unit | ✅ Pass |
| Task Statistics | User with completed tasks only | Unit | ✅ Pass |
| **CHATBOT FUNCTIONALITY** |
| Chatbot Controller | AI agent initialization | Manual | ✅  Pass |
| Chatbot Tools | Create task tool | Manual | ✅  Pass |
| Chatbot Tools | Find task tool | Manual | ✅  Pass |
| Chatbot Tools | Find user tool | Manual | ✅  Pass |
| Chatbot Tools | Delete task tool | Manual | ✅  Pass |
| Chatbot Tools | Update task tool | Manual | ✅  Pass |
| Chatbot Tools | Read task tool | Manual | ✅  Pass |
| Chatbot Tools | Create many tasks tool | Manual | ✅  Pass |
| Chatbot View | POST request handling | Manual | ✅  Pass |
| **FRONTEND JAVASCRIPT** |
| Chat Interface | Modal show/hide | Manual | ✅  Pass |
| Chat Interface | Message sending | Manual | ✅  Pass |
| Chat Interface | Message display | Manual | ✅  Pass |
| Chat Interface | Conversation persistence | Manual | ✅  Pass |
| Chat Interface | Enter key submission | Manual | ✅  Pass |
| Chat Interface | Loading indicators | Manual | ✅  Pass |
| Chat Interface | Error message display | Manual | ✅  Pass |
| Chat Interface | CSRF token handling | Manual | ✅  Pass |
| **SECURITY & PERMISSIONS** |
| Authentication | Login required decorators | Unit | ✅ Pass |
| Authentication | Redirect to login | Unit | ✅ Pass |
| Permissions | Edit own profile only | Unit | ✅ Pass |
| Permissions | Change own password only | Unit | ✅ Pass |
| Permissions | 403 for unauthorized access | Unit | ✅ Pass |
| Permissions | URL ID manipulation prevention | Unit | ✅ Pass |
| **ERROR HANDLING** |
| Error Pages | 404 page display | Manual | ✅  Pass |
| Error Pages | 403 page display | Manual | ✅  Pass |
| Error Pages | 500 page display | Manual | ✅  Pass |
| Form Validation | Client-side validation | Manual | ✅  Pass |
| Form Validation | Server-side validation | Unit | ✅ Pass |
| **RESPONSIVE DESIGN & UI** |
| Navigation | Mobile responsive menu | Manual | ✅  Pass |
| Layout | Bootstrap grid responsiveness | Manual | ✅  Pass |
| Styling | CSS custom properties | Manual | ✅  Pass |
| Styling | Task status styling | Manual | ✅  Pass |
| Styling | Pagination controls | Manual | ✅  Pass |
| **INTEGRATION TESTS** |
| Database | PostgreSQL integration | Manual | ✅  Pass |
| API | GitHub Models API integration | Manual | ✅  Pass |
| Static Files | CSS/JS loading | Manual | ✅  Pass |


</details>

## AI Implmentation

<details>
### Code Creation

Copilot did alot of the styling on this project I wired up the front end pages and then let Copilot take the lead on the visuals of it and then tweaked them as and when I felt it was needed. I think it did a smashing job as the website looks good and required fairly limited intervention beyond giving it things like the fonts to use and the general color schemee. Beyond that I didnt user code creation much opting to ask Copilot for hints rather then code generation, I know I want to work in the back end side of things and I felt because of this it was important I got as much practice as I could in this area.

### Debugging

I used Copilot again for debugging, helping me by giving me hints and pointing out likely areas to check when trying to find where a bug was occuring. It proved very helpful for the most part and spend up a lot of the small bug fixes that needed doing. That being said when I moved onto the chat bot and using smolagents Copilot actually slowed me down it sent me down many rabbit holes and massively over complicated problems, when I went to ChatGPT to seek addional support it largely did the same. In the end the problem was solved by me going through the documentation myself and I would have spent a lot less time on wiring up the chat bot if I had just done that from the start.

### Performance and Experience

Copilot was very useful in improving the performance while I do still have some database optimizations that could be done I at first had a lot of N + 1 issues and Copilot pointed me in the right direction telling me to reserach both bulkcreate and select_related to helping me improve performance. I also feel like as a developer have AI do some of the grunt work is also very helpful and improves your performance as a developer. That being said it did make some weird and sometimes unhelpful suggestions like moving all error messages to a singluar file and importing them all, I end up doing this for URLs and templates as I felt it had some value there but refused to implement the suggestion for error messages as it was a pointless abstraction.

### Development Process

Over all I feel like the use of AI massively helped speed up the development process and also pushed me to do things in a better way then I would have perhaps done otherwise, I frequently asked for feedback and it quite rightly criticized some of my initial ideas on how to solve problems.
</details>

## Database

<details>
The database is a Postgres database hosted by Code insitute

![ERD](/documentation/capstoneERD.png)

### User table
The user is a self referencing table were users can be bosses of other uses, I made my own custom user to do this inheriting from AbstractUser, it ended up with less fields then I had planned due to profile picture being cut because of my API key to Cloudinary being almost used up and I was worried it would run out during the developement of this project.

### Task table
The task table has 2 one to many relationships with the user table, one being created_by which would track which user created the task and another being assigned_to which would track which user the task belonged to.

</details>

## References

<details>
AI
chatgpt - helped me intial ideas for design such as the name Taskflow and what fonts to use.
Co-Pilot - I used copilot a lot as both a rubber duck and also for pair programming, I asked it to avoid giving code and to just talk through problems it found in my project.

Youtube videos

https://www.youtube.com/watch?v=mndLkCEiflg - helped me with making custom-users
https://www.youtube.com/@Codemycom - helped me with afew different things accross different videos
https://www.youtube.com/watch?v=1x0Zdukpjrs - helped with adding custom field validators
https://www.youtube.com/watch?v=3NDGnj19GiA - helped me understand prefetch and select related
https://www.youtube.com/watch?v=N_HLNV2UQjg - helped with writing my unit tests
https://www.youtube.com/watch?v=HBA6BSmBiT4 - helped me with the JS event listeners needed for the chatbot
https://www.youtube.com/watch?v=lc1sOvRaFpg - reminder on how to use data attributes and how to get JS and Django to talk
https://www.youtube.com/watch?v=RxUc6ZWwgfw - showed me how to use session storage allowing me to save the chatbots chat history.

Documentation

https://docs.djangoproject.com/en/5.2/ref/models/querysets/ - Django documentation was very useful for a few different sections.

W3schools

https://www.w3schools.com/python/python_lists_comprehension.asp - reminder on how list comprehension works

Old projects

https://github.com/GenericName192/CI-hackathon-chatbot - reminder of how to do some the JS.

hugging face course

https://huggingface.co/learn/agents-course/unit0/introduction - I started doing this during the course and referenced back to it during the project.
</details>

## Tech
<details>

- CSS
- HTML
- Django
- Bootstrap
- Copilot
- ChatGPT
- Postgres
- Smolagents
- Openai/gpt-4o-mini
</details>

## Learning Points

<details>
It's hard to sum up learning points as I feel like I've learnt an awful lot, I learnt a lot makeing a custom user, trying to do some database optimizations and an awful lot wireing up my first chatbot using agents. As for thing I would have done differently I think its the same learning points I've had before - be more ambitious and spend more time thinking and planning before building.
</details>