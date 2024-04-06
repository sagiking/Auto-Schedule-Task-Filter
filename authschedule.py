
import re
import os
import sys
import argparse
import subprocess

DEAFULT_TASKS_PATH = r"C:\Windows\System32\Tasks"
DESCRIPTION = "This tool is used to filter the schedules tasks in the PC"
READ = 'r'
WRITE = 'w'
SID = "S-"
TRUE = "true"
USER_REGEX = r'<UserId>(.*?)</UserId>'
NAME_REGEX = r'<URI>(.*?)</URI>'
ACTION_REGEX = r'<Exec>(.*?)</Exec>'
HIDDEN_REGEX = r'<Hidden>(.*?)</Hidden>'
DESCRIPTION_REGEX = r'<Description>(.*?)</Description>'
COMMAND_TAG = "Command"
ARGUMENT_TAG = "Arguments"
DASH = "---------------------------"

def sid_to_username(sid):
    
    powershell_command = (
        f'$securityIdentifier = New-Object System.Security.Principal.SecurityIdentifier(\'{sid}\');'
        '$user = $securityIdentifier.Translate([System.Security.Principal.NTAccount]);$user.value'
    )
    
    return subprocess.check_output(
        ["powershell", "-Command", powershell_command],
      
    ).decode()


def taskname_fun(file_data, task_name):
    file_data_str = ''.join(file_data)
    pattern = re.compile(NAME_REGEX, re.DOTALL)
    match = pattern.search(file_data_str)

    name = match.group(1).split("\\")

    # Checking if there is a match
    if match:

        # Comparing Task Names
        if task_name.lower() in name[-1].lower():
            return match.group(1)
        return
    else:
        return  # Return None if no match is found


def username_fun(file_data, username):
    file_data_str = ''.join(file_data)
    pattern = re.compile(USER_REGEX, re.DOTALL)
    match = pattern.search(file_data_str)

    # Checking if there is a match
    if match:

        # Removing Domain\Computer name
        if "\\" in match.group(1):
            temp_file_username = match.group(1).split("\\")
            file_username = temp_file_username[-1]

        # Checking if the username is in SID and translate it
        elif SID in match.group(1):
            file_username = sid_to_username(match.group(1))

            if "\\" in file_username:
                temp_file_username = file_username.split("\\")
                file_username = temp_file_username[-1]
            
        else:
            file_username = match.group(1)

        # Comparing Usernames
        if username.lower() in file_username.lower():    
            return True
        return
    else:
        return  # Return None if no match is found


def action_fun(file_data, task_action):
    file_data_str = ''.join(file_data)
    pattern = re.compile(ACTION_REGEX, re.DOTALL)
    match = pattern.search(file_data_str)
    # Checking if there is a match
    if match:
        
        action = match.group(1).replace(COMMAND_TAG, "")
        action = action.replace(ARGUMENT_TAG, "")
        
        # Comparing Task Names
        if task_action.lower() in action.lower():
            return True
        return
    else:
        return 

def hidden_fun(file_data):
    file_data_str = ''.join(file_data)
    pattern = re.compile(HIDDEN_REGEX, re.DOTALL)
    match = pattern.search(file_data_str)
    # Checking if there is a match
    if match:

        # Checking Hidden Flag
        if match.group(1).lower() == TRUE:
            return True
        return
    else:
        return

def description_fun(file_data, description):
    file_data_str = ''.join(file_data)
    pattern = re.compile(DESCRIPTION_REGEX, re.DOTALL)
    match = pattern.search(file_data_str)
    # Checking if there is a match
    if match:

        # Checking if the description match
        if description.lower() in match.group(1).lower():
            return True
        return
    else:
        return


def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("-u" ,"--username", type=str, help="Filter by Username")
    parser.add_argument("-a" ,"--action", type=str, help="Filter by the action the task create")
    parser.add_argument("-n" , "--name", type=str, help="Filter by the schedule task name")
    parser.add_argument("-d", "--description", type=str, help="Filter by the description")
    parser.add_argument("-o", "--output", type=str, help="Output the result to a file")
    parser.add_argument("-t", "--taskspath", type=str, default=DEAFULT_TASKS_PATH, help="Changing the deafult tasks file path")
    parser.add_argument("-H", "--hidden", default=False, action="store_true", help="Showing only hidden tasks")
    args = parser.parse_args()

    username = args.username
    action = args.action
    task_name = args.name
    description = args.description
    hidden = args.hidden
    output = args.output

    if args.taskspath:
        if os.path.exists(args.taskspath):
            taskspath = args.taskspath
        else:
            sys.exit("Invaild path")
    tasks_paths = []
    
    # Inserting all the schedule tasks files into a list
    for root, dirs, files in os.walk(taskspath):
        for file in files:
            file_path = root + '\\' + file

            # Tring to read the file
            try:
                with open(file_path, READ, encoding='utf-16') as schedule_file:
                    schedule_file_data = schedule_file.readlines()
            except PermissionError:
                print(f"\n{DASH*5}\nCan't read the file {file_path} due to a permission error\n{DASH*5}\n")

            if task_name:
                taskname_result = taskname_fun(schedule_file_data, task_name)
                if not taskname_result:
                    continue
            
            if hidden:
                hidden_result = hidden_fun(schedule_file_data)
                if not hidden_result:
                    continue

            if description:
                description_result = description_fun(schedule_file_data, description)
                if not description_result:
                    continue
            
            if action:
                action_result = action_fun(schedule_file_data, action)
                if not action_result:
                    continue
                
            if username:
                username_result = username_fun(schedule_file_data, username)
                if not username_result:
                    continue

            # Changing from file path to task schedule path
            tasks_paths.append(file_path)

    # Writing the paths to a file
    if output:
        with open(output, WRITE) as file:
            for task in tasks_paths:
                schedule_task_path = task.replace(taskspath, "")
                file.write(f'{schedule_task_path} - {task}\n')

    # Printing the paths to the screen
    for task in tasks_paths:
        schedule_task_path = task.replace(taskspath, "")
        print(schedule_task_path)


if __name__ == "__main__":
    main()
