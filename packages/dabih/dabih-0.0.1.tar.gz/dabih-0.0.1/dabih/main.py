import click
import sys
from .config import *
from .helpers import *
from dabih.logger import setup_logger, dbg, error

@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.pass_context
def main(ctx, verbose):
    setup_logger(verbose)
    client, pem_files = get_client()
    if not healthy_func(client):
        error("Dabih server not healthy")
        dbg(f"client: {client}")
        sys.exit(0)
    else:
        dbg("Dabi server healthy")

    key_files, *_ = get_user_info(client)
    if pem_files:
        pem_files = get_user_key_files(key_files, pem_files)
    ctx.obj = {}
    ctx.obj["client"] = client
    ctx.obj["pem_files"] = pem_files


@click.command(
    short_help="Check if token is valid", help="This command will check if token is valid"
)
@click.pass_context
def token_val(ctx):
    client = ctx.obj["client"]
    answer = check_token_validity(client)
    if answer:
        print("Token is valid")
    else:
        print("Token is not valid")


@click.command(
    short_help="Get token scope info",
    help="This command will return user and role of the token",
)
@click.pass_context
def token_info(ctx):
    client = ctx.obj["client"]
    get_token_info(client)

@click.command(
    short_help="Check user credentials including token and available key files", help="Check token and existing key files"
)
@click.pass_context
def check(ctx):
    client = ctx.obj["client"]
    pem_files = ctx.obj["pem_files"]
    check_user_credentials(client, pem_files)


@click.command(
    short_help="List all files in user's home",
    help="see all files and folders in home",
)
@click.pass_context
def list_home(ctx):
    client = ctx.obj["client"]
    list_home_func(client)

@click.command(
    short_help="List files in a mnemonic",
    help="enter mnemonic e.g. dabih list-files rufus_shane to see file info or files under directory",
)
@click.pass_context
@click.argument("mnemonic")
def list_files(ctx, mnemonic):
    client = ctx.obj["client"]
    answer = list_files_func(mnemonic, client).content
    print_json(answer)


@click.command(
    short_help="Upload a file", help="This command will upload a file to dabih server"
)
@click.pass_context
@click.argument("file_path")
@click.argument("target_directory", required=False, default=None)
def upload(ctx, file_path, target_directory):  # potential namespace conflict?
    client = ctx.obj["client"]
    try:
        upload_func(file_path, client, target_directory)
    except FileNotFoundError as e:
        error(f"File at path: {file_path} not found. Please check the path.")
        dbg(f"Error: {e}")
        sys.exit(0)
    except Exception as e:
        error("Unexpected error")
        dbg(f"Error: {e}")

@click.command(
    short_help="Download a file",
    help="This command will download a file to dabih server",
)
@click.pass_context
@click.argument("mnemonic")
def download(ctx, mnemonic):
    client = ctx.obj["client"]
    if not ctx.obj["pem_files"]:
        print("No valid key files found; you need a private key to download files")
        return None
    download_func(mnemonic, client, ctx.obj["pem_files"])


@click.command(
    short_help="Search for file", help="This command will return all search results"
)
@click.pass_context
@click.argument("query")
def search(ctx, query):
    client = ctx.obj["client"]
    search_func(client, query)


main.add_command(token_info)
main.add_command(token_val)
main.add_command(check)
main.add_command(list_home)
main.add_command(list_files)
main.add_command(upload)
main.add_command(download)
main.add_command(search)


if __name__ == "__main__":
    main()

