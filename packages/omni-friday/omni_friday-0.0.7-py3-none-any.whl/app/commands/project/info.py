import click
from click_help_colors import HelpColorsCommand
from app.common.config import get_project_settings
from app.common.composer import read_composer_file, extract_magento_info
from app.common.aws import sqs_deliver_message


@click.command(
    cls=HelpColorsCommand,
    help_headers_color='yellow',
    help_options_color='green',
)
def run():
    click.secho("Initializing project config...", fg='blue')
    try:
        settings = get_project_settings()
        click.secho(f"Settings loaded: {settings}", fg='green')

        click.secho("Reading composer file...", fg='blue')
        composeer_info = read_composer_file()
        click.secho(f"Composer info loaded", fg='green')

        click.secho("Extracting Magento info...", fg='blue')
        magento_info = extract_magento_info(composeer_info)
        click.secho(f"Magento info loaded: {magento_info}", fg='green')

        message = {
          'project': settings,
          'platform': magento_info
        }

        message = {
            "entidad": "proyectos",
            "objeto": {
                "id": settings['project'],
                "nombre": settings['project'],
                "magento_id": magento_info['version'],
                # "cloud_name": "CloudDynamic",
                # "cloud_code": "DynamicCode",
                # "correo_soporte_adobe": "correo@dinamico.com",
                "estado": "1"
            }
        }

        response = sqs_deliver_message(message)

        click.secho(f"Message sent to SQS: {response['MessageId']}", fg='green')
        

        
    except FileNotFoundError as e:
        click.secho(str(e), fg='red')
    except Exception as e:
        click.secho(f"An error occurred: {str(e)}", fg='red')
       