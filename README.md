# Auto-Schedule-Task-Filter

## Description
Authschedule.py is a Python tool designed to filter scheduled tasks on a Windows PC based on various criteria such as username, action, task name, description, and hidden status. It provides a flexible way to manage and view scheduled tasks efficiently, While maintaining user input requests and displays the filtered results based on the specified criteria.


## Usage
The program can be executed via the command line with the following options:


## Arguments
- `-u`, `--username`: Filter tasks by username.
- `-a`, `--action`: Filter tasks by the action the task creates.
- `-n`, `--name`: Filter tasks by the scheduled task name.
- `-d`, `--description`: Filter tasks by the task description.
- `-o`, `--output`: Output the result to a file.
- `-t`, `--taskspath`: Change the default tasks file path.
- `-H`, `--hidden`: Show only hidden tasks.

## Defaults
- `DEFAULT_TASKS_PATH`: Default path for the scheduled tasks on Windows (C:\Windows\System32\Tasks).




