import os
import gdown
import click

def download_folder_from_drive(folder_id, save_path):
    """
    Downloads an entire folder from Google Drive using its folder ID.

    Args:
        folder_id (str): The Google Drive folder ID.
        save_path (str): The local path to save the folder contents.
    """
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)
        print("Downloading folder from Google Drive...")
        gdown.download_folder(
            url=f"https://drive.google.com/drive/folders/{folder_id}",
            output=save_path,
            quiet=False,
        )
        print(f"Folder downloaded to {save_path}")
    else:
        print("Folder already exists. Skipping download.")


@click.group()
def cli():
    """Command-line interface for OpenFace."""
    pass

@cli.command()
@click.option("--folder-id", default="1aBEol-zG_blHSavKFVBH9dzc9U9eJ92p", help="Google Drive folder ID")
@click.option("--output", default="./weights", help="Path to save the folder contents")
def download(folder_id, output):
    """Download an entire folder from Google Drive."""
    save_path = os.path.abspath(output)
    download_folder_from_drive(folder_id, save_path)

if __name__ == "__main__":
    cli()
