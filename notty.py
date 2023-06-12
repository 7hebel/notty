""" A main entry point for notty. """
import os
import click

from core.repository import Repository
from core import todo as Todo
from core.path import Path
from core import visuals
from core import moment
from core import files

repository = Repository(os.getcwd())


def repo_status_validator(status: bool):
    """ Validate repo existence in current directory and compare it with given status.
    It works like a gate. If repo should exists but does not (or in reverse) it will
    display error message and prevent code from entering decorated function."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if repository.is_initialized != status:
                message = "No repository is initialized here." if status else "Already exists."
                visuals.display_error(message)
                return False
            return func(*args, **kwargs)
        return wrapper
    return decorator


# -- REPO -- #

@click.command("init")
@repo_status_validator(False)
def init():
    """ Initialize repository in current directory. """
    repository.create(Path(os.getcwd()))

@click.command("save")
@click.option("-c", "--comment", default="Not provided.", type=str, show_default=False,
              help="Comment changes made in this save.")
@click.option("-m", "--multiline", is_flag=True, help="Create multiline comment.")
@repo_status_validator(True)
def save_current_state(comment: str, multiline: bool):
    """ Save current work state. """
    if comment != "Not provided." and multiline:
        raise click.UsageError("Only one comment option can be used. Choose -c or -m.")

    if multiline:
        comment = visuals.get_multiline_input("Save's comment")

    repository.create_save(comment)

@click.command("list")
@repo_status_validator(True)
def list_saves():
    """ Display list of all saves located in ./.notty/saves/ directory. """
    bullets = [str(save_obj.hash) for save_obj in repository.get_all_saves()]
    visuals.display_bullet_list(f"Local saves: {len(bullets)}", bullets)

@click.command("desc")
@click.argument("save_hash", type=str)
@repo_status_validator(True)
def describe_save(save_hash):
    """ Display all known data about an save according to notty.save file. """
    save_obj = repository.find_save(save_hash)
    if save_obj is None:
        return

    if not save_obj.date_created:
        date_created = "Undefined."
    else:
        date_created = moment.read_timestamp(save_obj.date_created)

    data = {
        "Comment": "\n"+save_obj.comment.strip(),
        "Date created": date_created,
        "Short HASH": save_obj.hash.short,
        "Full HASH": save_obj.hash.full,
    }

    visuals.display_key_value(f"Description of {save_obj.hash.short}", data)

@click.command("rollback")
@click.argument("save_hash", type=str)
@click.option("-s", "--save", is_flag=True, help="Save current state before rolling back.")
@repo_status_validator(True)
def rollback_save(save_hash: str, save: bool):
    """ Revert changes, save current state if save param is set to True and remove
    all files located in working directory, copy back saved version. """

    save_obj = repository.find_save(save_hash)
    if save_obj is None:
        return

    with visuals.ProcessCallback(f"Rollback ({save_obj.hash.short}).", "Rolled back.") as callback:
        if save:
            repository.create_save("auto-generated: rollback")
            callback.success("saved current state")

        callback.info("removing current state")
        files.remove_current(Path(os.getcwd()))
        callback.success("removed current state")

        callback.info(f"rolling back save: ({save_obj.hash.short})")
        repository.rollback_save(save_obj)

@click.command("forget")
@click.argument("save_hash", type=str)
@repo_status_validator(True)
def forget(save_hash):
    """ Remove save from saves directory. """

    if save_hash.lower() == "all":
        visuals.display_warning("all saves will be removed!")
        if not visuals.get_boolean_response("Do You want to continue"):
            return

        with visuals.ProcessCallback("Remove all saves", "All saves has been removed") as callback:
            callback.info("starting...")
            all_saves = repository.get_all_saves()
            if not all_saves:
                callback.warn("no saves found...")
                return

            for save_obj in all_saves:
                callback.success(f"removing: {str(save_obj.hash)}")
                repository.remove_save(save_obj)
        return

    save_obj = repository.find_save(save_hash)
    if save_obj is None or not visuals.get_boolean_response("Are you sure"):
        return

    repository.remove_save(save_obj)
    visuals.display_success(f"Forgot save: {str(save_obj.hash)}")


# -- NOTES -- #

@click.command("clear")
@repo_status_validator(True)
def clear_notes():
    """ Clear notes file. """
    if not visuals.get_boolean_response("Are you sure"):
        return
    open(str(repository.repo_path / "notes.txt"), "w+").close()

@click.command("edit")
@repo_status_validator(True)
def edit_notes():
    """ Open an built in editor with notes file in it. """
    with open(str(repository.repo_path / "notes.txt"), "r") as file:
        content = file.read()

    with open(str(repository.repo_path / "notes.txt"), "w+") as file:
        new_content = click.edit(content)
        file.write(new_content)
    visuals.display_success("Notes saved.")

@click.command("show")
@repo_status_validator(True)
def show_notes():
    """ Print note's file content. """
    visuals.display_file_content(str(repository.repo_path / "notes.txt"))


# -- TODO -- #

@click.command("show")
@repo_status_validator(True)
def show_todo():
    """ Display all to do entries. """
    
    todo_list = Todo.TodoList(str(repository.repo_path / "todo.json"))
    todo_list.display_tasks()

@click.command("rm")
@click.argument("index", type=int)
@repo_status_validator(True)
def remove_task(index):
    """ Remove task from todo.json file. """
    
    todo_list = Todo.TodoList(str(repository.repo_path / "todo.json"))
    todo_list.remove_task(index)

@click.command("add")
@click.argument("content", type=str)
@click.argument("importance", type=str, required=False, default="low")
@repo_status_validator(True)
def add_task(content, importance):
    """ Add new task and save it. """
    
    todo_list = Todo.TodoList(str(repository.repo_path / "todo.json"))
    importance = importance.lower()

    if importance in ("l", "low", "1"):
        importance = Todo.Importance.LOW
    elif importance in ("m", "mid", "medium", "2"):
        importance = Todo.Importance.MEDIUM
    elif importance in ("h", "high", "!", "3"):
        importance = Todo.Importance.HIGH
    else:
        visuals.display_warning(f"Invalid importance level: {importance}. [L]ow/[M]edium/[H]igh")
        importance = Todo.Importance.LOW

    task = Todo.Task(content, Todo.State.PENDING, importance)
    todo_list.append_task(task)

@click.command("imp")
@click.argument("index", type=int)
@click.argument("level", type=str)
def update_importance(index, level):
    """ Change level of importance of a task. """
    
    todo_list = Todo.TodoList(str(repository.repo_path / "todo.json"))
    try:
        task: Todo.Task = todo_list.tasks[index]
        current_int = task.importance.value
    except IndexError:
        visuals.display_error(f"Invalid task index: {index}")

    level = level.lower()
    level_table = {
        ("l", "low", "1"): Todo.Importance.LOW,
        ("m", "mid", "medium", "2"): Todo.Importance.MEDIUM,
        ("h", "high", "!", "3"): Todo.Importance.HIGH,
    }

    if level == "+":
        try:
            task.importance = Todo.Importance(current_int+1)
            todo_list.save()
        except ValueError:
            visuals.display_error("Task's importance cannot go above HIGH level.")
        return
        
    elif level == "-":
        try:
            task.importance = Todo.Importance(current_int-1)
            todo_list.save()
        except ValueError:
            visuals.display_error("Task's importance cannot go below LOW level.")
        return
        
    for patterns, value in level_table.items():
        if level in patterns:
            task.importance = value
            todo_list.save()
            return

    visuals.display_error(f"Invalid importance level: {level}. [L]ow/[M]edium/[H]igh or +/-")
    return
    
@click.command("state")
@click.argument("index", type=int)
@click.argument("level", type=str)
def update_state(index, level):
    """ Update task's state. """
    
    todo_list = Todo.TodoList(str(repository.repo_path / "todo.json"))
    try:
        task: Todo.Task = todo_list.tasks[index]
        current_int = task.state.value
    except IndexError:
        visuals.display_error(f"Invalid task index: {index}")

    level = level.lower()
    level_table = {
        ("pending", "p", "1"): Todo.State.PENDING,
        ("in_progress", "i", "2"): Todo.State.IN_PROGRESS,
        ("done", "finished", "d", "f", "3"): Todo.State.FINISHED,
    }

    if level == "+":
        try:
            task.state = Todo.State(current_int+1)
            todo_list.save()
        except ValueError:
            visuals.display_error("Task's state cannot go above FINISHED level.")
        return
        
    elif level == "-":
        try:
            task.state = Todo.State(current_int-1)
            todo_list.save()
        except ValueError:
            visuals.display_error("Task's state cannot go below PENDING level.")
        return
        
    for patterns, value in level_table.items():
        if level in patterns:
            task.state = value
            todo_list.save()
            return

    visuals.display_error(f"Invalid state: {level} [P]ending,1/[I]n_progress,2/[F]inished,3 or +/-")
    return

# -- GROUPS -- #

@click.group()
def notes():
    """ Group of notes editing commands together. """
notes.add_command(clear_notes)
notes.add_command(edit_notes)
notes.add_command(show_notes)

@click.group()
def todo():
    """ Group of todo management commands. """
todo.add_command(show_todo)
todo.add_command(remove_task)
todo.add_command(add_task)
todo.add_command(update_importance)
todo.add_command(update_state)

@click.group()
def notty():
    """ Main command functions group. """
notty.add_command(init)
notty.add_command(save_current_state)
notty.add_command(list_saves)
notty.add_command(describe_save)
notty.add_command(rollback_save)
notty.add_command(forget)

notty.add_command(notes)
notty.add_command(todo)


if __name__ == "__main__":
    notty()
