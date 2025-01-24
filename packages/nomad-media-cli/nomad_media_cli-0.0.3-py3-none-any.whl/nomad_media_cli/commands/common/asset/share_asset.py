import click
import json
import sys
from nomad_media_cli.helpers.get_id_from_url import get_id_from_url
from nomad_media_cli.helpers.utils import initialize_sdk
from nomad_media_cli.helpers.validate_json import validate_json

@click.command()
@click.option("--id", help="The ID of the asset to share.")
@click.option("--url", help="The Nomad URL of the Asset (file or folder) to share (bucket::object-key).")
@click.option("--object-key", help="Object-key of the Asset (file or folder) to share. This option assumes the default bucket that was previously set with the `set-bucket` command.")
@click.option("--nomad-users", multiple=True, help="The nomad users of the share in JSON list format.")
@click.option("--external-users", multiple=True, help="The external users of the share in JSON list format.")
@click.option("--shared-duration-in-hours", type=click.INT, help="The share duration in hours of the share.")
@click.pass_context
def share_asset(ctx, id, url, object_key, nomad_users, external_users, shared_duration_in_hours):
    """Share asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    if not id and not url and not object_key:
        click.echo(json.dumps({"error": "Please provide an id, url, or object-key."}))
        sys.exit(1)

    if url or object_key:       
        id = get_id_from_url(ctx, url, object_key, nomad_sdk)

    try:
        result = nomad_sdk.share_asset(
            id,
            [validate_json(nomad_user, "nomad_users") for nomad_user in nomad_users] if nomad_users else None,
            [validate_json(external_user, "external_users") for external_user in external_users] if external_users else None,
            shared_duration_in_hours
        )
        
        if result is None:
            click.echo(json.dumps({"error": f"Asset with id {id} not found."}))
            sys.exit(1)
            
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo(json.dumps({"error": f"Error sharing asset: {e}"}))
        sys.exit(1)