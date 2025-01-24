import click
import json
import sys
from nomad_media_cli.helpers.get_id_from_url import get_id_from_url
from nomad_media_cli.helpers.utils import initialize_sdk
from nomad_media_cli.helpers.validate_json import validate_json

@click.command()
@click.option("--source-ids", multiple=True, help="The source ids of the media in JSON list format.")
@click.option("--source-urls", multiple=True, help="The source urls of the media in JSON list format.")
@click.option("--source-object-keys", multiple=True, help="The source object keys of the media in JSON list format.")
@click.option("--title", help="The title of the media.")
@click.option("--tags", multiple=True, help="The tags of the media in JSON list format.")
@click.option("--collections", multiple=True, help="The collections of the media in JSON list format.")
@click.option("--related-contents", multiple=True, help="The related contents of the media in JSON list format.")
@click.option("--destination-folder-id", required=True, help="The destination folder ID of the media.")
@click.option("--video-bitrate", type=click.INT, help="The video bitrate of the media.")
@click.option("--audio-tracks", multiple=True, help="The audio tracks of the media in JSON list format.")
@click.pass_context
def build_media(ctx, source_ids, source_urls, source_object_keys, title, tags, collections, related_contents, destination_folder_id, video_bitrate, audio_tracks):
    """Build media"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]
    
    if not source_ids and not source_urls and not source_object_keys:
        click.echo(json.dumps({"error": "Please provide source-ids, source-urls, or source-object-keys."}))
        sys.exit(1)
        
    if not source_ids:
        source_ids = []

    if source_urls:
        for source in source_urls:
            source_dict = json.loads(source)
            url = source_dict.get("url")
            start_time_code = source_dict.get("start_time_code")
            end_time_code = source_dict.get("end_time_code")
            asset_id = get_id_from_url(ctx, url, None, nomad_sdk)
            source_ids.append({
                "sourceAssetId": asset_id,
                "start_time_code": start_time_code,
                "end_time_code": end_time_code
            })

    if source_object_keys:
        for source in source_object_keys:
            source_dict = json.loads(source)
            object_key = source_dict.get("object_key")
            start_time_code = source_dict.get("start_time_code")
            end_time_code = source_dict.get("end_time_code")
            asset_id = get_id_from_url(ctx, None, object_key, nomad_sdk)
            source_ids.append({
                "sourceAssetId": asset_id,
                "start_time_code": start_time_code,
                "end_time_code": end_time_code
            })

    try:
        nomad_sdk.build_media(
            source_ids,
            title,
            [validate_json(tag, "tags") for tag in tags] if tags else None,
            [validate_json(collection, "collections") for collection in collections] if collections else None,
            [validate_json(related_content, "related_contents") for related_content in related_contents] if related_contents else None,
            destination_folder_id,
            video_bitrate,
            [validate_json(audio_track, "audio_tracks") for audio_track in audio_tracks] if audio_tracks else None
        )
        click.echo("Media built successfully.")

    except Exception as e:
        click.echo(json.dumps({"error": f"Error building media: {e}"}))
        sys.exit(1)