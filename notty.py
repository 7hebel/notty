import click
import os

from core.repository import Repository
from core import visuals
from core import moment
from core import files

repository = Repository(os.getcwd())

def repo_status(status: bool):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if repository.is_initialized != status:
                message = "No repository is initialized here." if status else "Already exists."
                visuals.Message.error(message)
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator


@click.command("init")
@repo_status(False)
def init():
    repository.create(os.getcwd())

@click.command("save")
@click.option("-c", "--comment", default="Not provided.", type=str, show_default=False, help="Comment changes made in this save.")
@click.option("-m", "--multiline", is_flag=True, help="Create mutliline comment.")
@repo_status(True)
def save_work(comment: str, multiline: bool):   
    if comment != "Not provided." and multiline:
        raise click.UsageError("Only one comment option can be used. Choose -c or -m.")
    
    if multiline:
        comment = visuals.get_multiline_input("Save's comment")
        
    repository.create_save(comment)
    
@click.command("list")
@repo_status(True)
def list_saves():
    all_saves = repository.get_all_saves()
    bullets = []
    for save_obj in all_saves:
        bullets.append(str(save_obj.hash))

    visuals.Message.bullet_list(f"Local saves: {len(bullets)}", bullets)

@click.command("desc")
@click.argument("save_hash", type=str)
@repo_status(True)
def desc(save_hash):
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

    visuals.Message.key_value(f"Description of {save_obj.hash.short}", data)
    
@click.command("rollback")
@click.argument("save_hash", type=str)
@click.option("-s", "--save", is_flag=True, help="Save current state before rolling back.")
@repo_status(True)
def rollback(save_hash: str, save: bool):
    save_obj = repository.find_save(save_hash)
    if save_obj is None:
        return

    with visuals.ProcessCallback(f"Rollback ({save_obj.hash.short}).", "Rolled back.") as Callback:
        if save:
            repository.create_save("auto-generated: rollback")
            Callback.success("saved current state")

        Callback.info("removing current state")
        files.remove_current(os.getcwd())
        Callback.success("removed current state")

        Callback.info(f"rolling back save: ({save_obj.hash.short})")
        repository.rollback_save(save_obj)

@click.command("forget")
@click.argument("save_hash", type=str)
@repo_status(True)
def forget(save_hash):
    if save_hash.lower() == "all":
        visuals.Message.warning("all saves will be removed!")
        if not visuals.get_boolean_response("Do You want to continue"):
            return
        
        with visuals.ProcessCallback("Remove all saves", "All saves has been removed") as Callback:
            Callback.info("starting...")
            for save_obj in repository.get_all_saves():
                Callback.warn(f"removing: {str(save_obj.hash)}")
                repository.remove_save(save_obj)
        return

    save_obj = repository.find_save(save_hash)
    if save_obj is None or not visuals.get_boolean_response("Are you sure"):
        return

    repository.remove_save(save_obj)
    visuals.Message.success(f"Forgot save: {str(save_obj.hash)}")



@click.group()
def notty():
    """ Main command functions group. """
notty.add_command(init)
notty.add_command(save_work)
notty.add_command(list_saves)
notty.add_command(desc)
notty.add_command(rollback)
notty.add_command(forget)


if __name__ == "__main__":
    notty()
