import click
import json
import sys
from nomad_media_cli.helpers.get_id_from_url import get_id_from_url
from nomad_media_cli.helpers.utils import initialize_sdk
from nomad_media_cli.helpers.validate_json import validate_json

@click.command()
@click.option("--id", help="The ID of the asset to update the ad break for.")
@click.option("--url", help="The Nomad URL of the Asset (file or folder) to update the ad break for (bucket::object-key).")
@click.option("--object-key", help="Object-key of the Asset (file or folder) to update the ad break for. This option assumes the default bucket that was previously set with the `set-bucket` command.")
@click.option("--ad-break-id", required=True, help="The ID of the ad break.")
@click.option("--time-code", help="The time code of the asset ad break. Format: hh:mm:ss;ff.")
@click.option("--tags", multiple=True, help="The tags of the asset ad break in JSON list format.")
@click.option("--labels", multiple=True, help="The labels of the asset ad break in JSON list format.")
@click.pass_context
def update_asset_ad_break(ctx, id, url, object_key, ad_break_id, time_code, tags, labels):
    """Update asset ad break"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    if not id and not url and not object_key:
        click.echo(json.dumps({"error": "Please provide an id, url, or object-key."}))
        sys.exit(1)

    if url or object_key:       
        id = get_id_from_url(ctx, url, object_key, nomad_sdk)
        
    try:
        result = nomad_sdk.update_asset_ad_break(
            id,
            ad_break_id,
            time_code,
            [validate_json(tag, "tags") for tag in tags] if tags else None,
            [validate_json(label, "labels") for label in labels] if labels else None
        )
        
        if not result:
            click.echo(json.dumps({"error": f"Asset ad break with id {ad_break_id} not found."}))
            sys.exit(1)
            
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo(json.dumps({"error": f"Error updating asset ad break: {e}"}))
        sys.exit(1)