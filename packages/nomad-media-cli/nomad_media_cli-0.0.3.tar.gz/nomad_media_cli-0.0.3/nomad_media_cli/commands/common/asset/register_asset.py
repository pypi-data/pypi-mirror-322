import click
import json
import sys
from nomad_media_cli.helpers.get_id_from_url import get_id_from_url
from nomad_media_cli.helpers.utils import initialize_sdk
from nomad_media_cli.helpers.validate_json import validate_json

@click.command()
@click.option("--id", help="The ID of the asset to register.")
@click.option("--url", help="The Nomad URL of the Asset (file or folder) to register (bucket::object-key).")
@click.option("--parent-id", help="The ID of the parent.")
@click.option("--display-object-key", help="The display object key of the register.")
@click.option("--bucket-name", required=True, help="The bucket name of the register.")
@click.option("--object-key", required=True, help="The object key of the register.")
@click.option("--e-tag", help="The eTag of the register.")
@click.option("--tags", multiple=True, help="The tags of the register.")
@click.option("--collections", multiple=True, help="The collections of the register.")
@click.option("--related-contents", multiple=True, help="The related contents of the register.")
@click.option("--sequencer", help="The sequencer of the register.")
@click.option("--asset-status", help="The asset status of the register.")
@click.option("--storage-class", help="The storage class of the register.")
@click.option("--asset-type", help="The asset type of the register.")
@click.option("--content-length", type=click.INT, help="The content length of the register.")
@click.option("--storage-event-name", help="The storage event name of the register.")
@click.option("--created-date", help="The created date of the register.")
@click.option("--storage-source-ip-address", help="The storage source IP address of the register.")
@click.option("--start-media-processor", is_flag=True, help="The start media processor of the register.")
@click.option("--delete-missing-asset", is_flag=True, help="The delete missing asset of the register.")
@click.pass_context
def register_asset(ctx, id, url, parent_id, display_object_key, bucket_name, object_key, e_tag, tags, collections, 
                   related_contents, sequencer, asset_status, storage_class, asset_type, content_length, 
                   storage_event_name, created_date, storage_source_ip_address, start_media_processor, delete_missing_asset):
    """Register asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    if url:       
        id = get_id_from_url(ctx, url, None, nomad_sdk)

    try:
        result = nomad_sdk.register_asset(
            id,
            parent_id,
            display_object_key,
            bucket_name,
            object_key,
            e_tag,
            [validate_json(tag, "tags") for tag in tags] if tags else None,
            [validate_json(collection, "collections") for collection in collections] if collections else None,
            [validate_json(related_content, "related_contents") for related_content in related_contents] if related_contents else None,
            sequencer,
            asset_status,
            storage_class,
            asset_type,
            content_length,
            storage_event_name,
            created_date,
            storage_source_ip_address,
            start_media_processor,
            delete_missing_asset
        )
        
        if not result:
            click.echo(json.dumps({"error": f"Asset with id {id} not found."}))
            sys.exit(1)
            
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo(json.dumps({"error": f"Error registering asset: {e}"}))
        sys.exit(1)