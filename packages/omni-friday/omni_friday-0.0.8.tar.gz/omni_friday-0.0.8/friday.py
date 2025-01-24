import click
from click_help_colors import HelpColorsGroup
from app.commands.project import info as project_info_command
from dotenv import load_dotenv

load_dotenv()

@click.group(
    cls=HelpColorsGroup,
    help_headers_color='yellow',
    help_options_color='green',
)
@click.version_option()
def cli():
    pass


cli.add_command(project_info_command.run, name='project:info')
