import click
import json
import sys
from nomad_media_cli.helpers.get_id_from_url import get_id_from_url
from nomad_media_cli.helpers.utils import initialize_sdk
from nomad_media_cli.helpers.validate_json import validate_json

@click.command()
@click.option("--id", help="The ID of the asset to be clipped.")
@click.option("--url", help="The Nomad URL of the Asset to be clipped (bucket::object-key).")
@click.option("--object-key", help="Object-key of the Asset to be clipped. This option assumes the default bucket that was previously set with the `set-bucket` command.")
@click.option("--start-time-code", required=True, help="The start time code of the asset. Format: hh:mm:ss;ff.")
@click.option("--end-time-code", required=True, help="The end time code of the asset. Format: hh:mm:ss;ff.")
@click.option("--title", required=True, help="The title of the asset.")
@click.option("--output-folder-id", required=True, help="The output folder ID of the asset.")
@click.option("--tags", multiple=True, help="The tags of the asset in JSON list format.")
@click.option("--collections", multiple=True, help="The collections of the asset in JSON list format.")
@click.option("--related-contents", multiple=True, help="The related contents of the asset in JSON list format.")
@click.option("--video-bitrate", type=click.INT, help="The video bitrate of the asset.")
@click.option("--audio-tracks", help="The audio tracks of the asset in JSON list format.")
@click.pass_context
def clip_asset(ctx, id, url, object_key, start_time_code, end_time_code, title, output_folder_id, tags, 
    collections, related_contents, video_bitrate, audio_tracks):
    """Clip asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]
    
    if not id and not url and not object_key:
        click.echo(json.dumps({"error": "Please provide an id, url, or object-key."}))
        sys.exit(1)
        
    if url or object_key:
        id = get_id_from_url(ctx, url, object_key, nomad_sdk)

    try:
        result = nomad_sdk.clip_asset(
            id,
            start_time_code,
            end_time_code,
            title,
            output_folder_id,
            [validate_json(tag, "tags") for tag in tags] if tags else None,
            [validate_json(collection, "collections") for collection in collections] if collections else None,
            [validate_json(related_content, "related_contents") for related_content in related_contents] if related_contents else None,
            video_bitrate,
            [validate_json(audio_track, "audio_tracks") for audio_track in audio_tracks] if audio_tracks else None
        )

        if not result:          
            click.echo(json.dumps({"error": f"Asset with id {id} not found."}))
            sys.exit(1)        

        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo(json.dumps({"error": f"Error clipping asset: {e}"}))
        sys.exit(1)