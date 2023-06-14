  
![Logo](https://github.com/gental-py/notty/blob/main/assets/notty.png?raw=true)  
  
 
# 📂 notty  
  
**LVCS** - Local Version Control System. Easily manage versions of **Your work**. Works like GiT, but easier and with different features like *todo* or *notes* for each projects.  
  
## ⬇️ Installation  
Downlaod notty using `git clone`:  
  
```bash  
git clone [https://github.com/gental-py/notty](https://github.com/gental-py/notty)  
cd notty  
```  
Install notty:
```bash
pip install .
//// or ////
py setup.py install
``` 
  
## 💻 Usage  
Navigate to Your project's directory and initalize repository here.
```bash
cd your/projects/directory
notty init
```
Save current work state.
```bash
notty save -c "Initial save"
```
### List of commands:
| **Command**   | **Arguments**                        | **Description**                                                                                           |
| ------------- | ------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| `--help`      |                                      | Display help message.                                                                                     |
| `init`        |                                      | Initalize REPO in current directory.                                                                      |
| `save`        | [-c, --comment] OR [-m, --multiline] | Save current work state. Add comment if option selected                                                   |
| `desc`        | <save_hash>                          | Describe save.                                                                                            |
| `forget`      | <save_hash>                          | Remove save.                                                                                              |
| `rollback`    | <save_hash> [-s, --save]             | Roll back to save's state and save current state if save option enabled                                   |
| `list`        |                                      | Display list of all saves.                                                                                |
| `ignore`      |                                      | Open editable version of ignore file.                                                                     |
| **NOTES**     | ---                                  | ---                                                                                                       |
| `notes clear` |                                      | Clear project's notes.                                                                                    |
| `notes edit`  |                                      | Open editable version of project's notes.                                                                 |
| `notes show`  |                                      | Display all notes in terminal.                                                                            |
| **TODO**      | ---                                  | ---                                                                                                       |
| `todo add`    | <content> [importance]               | Add new todo entry. Check todo section for legal importance levels.                                       |
| `todo rm`     | <index>                              | Remove todo entry. Use `todo show` for indexes.                                                           |
| `todo show`   |                                      | Show table of all todo entries with their: content, index, importance level and state                     |
| `todo imp`    | <index> <level>                      | Change importance level of an todo entry. You can use `+` or `-` as a level or name (check todo section). |
| `todo state`  | <index> <level>                      | Change current state of an todo entry. Use `+` or `-` or any of state names described in todo section.    |

Syntax: `notty COMMAND ARGUMENTS`

## 📁 Saves
Each save has it's HASH which is SHA256 hash. Some commands requires `save_hash` as argument to get into interaction with an save. Full hash has `64` characters but you can use short version of hash which are **first 5 characters** of full hash. When You use `notty list` command and you have some saves saved, you will see a list with hashes in: `(SHORT) FULL` format. You can also type `notty desc <save_hash>` to it's short and full form.
  
## 🎯 Todo
Every repository has it's own todo list. Each entry has it's own: 
- `content`: You provide it when todo entry is created.
- `state`: It describes current state of task. Possible values are:
	*  `pending`/`p`/`1`: You have not started this task yet.
	* `in_progress`/`i`/`2`: You are currently working on it.
	* `done`/`finished`/`d`/`f`/`3`: You have done this task.
- `importance`: How important is this task. Possible values are:
	* `low`/`l`/`1`: This task is not important.
	* `medium`/`mid`/`m`/`2`: You should finish this task in short future.
	* `high`/`h`/`!`/`3`: This task is very important and you should finish it ASAP.
- `index`: Dynamically changed discriminator of each task.

## 🌳REPO structure
```bash
(inside project's directory)

/.notty/
|-bin/
|-saves/
| |-<save_hash>/
| | |-[project files]
| | |-notty.save
| |-<save_hash>/
| |...
|-notes.txt
|-notty.ignore
|-notty.meta
|-todo.json
```
