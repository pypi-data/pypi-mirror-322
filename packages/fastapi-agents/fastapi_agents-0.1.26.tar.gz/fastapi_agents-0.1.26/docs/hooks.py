import os
import re
import logging
from urllib.parse import unquote_plus
from mkdocs.plugins import get_plugin_logger

log = get_plugin_logger(__name__)

def transform_name(name):
    """
    Transform folder and file names to lowercase and hyphenated format.
    Decodes URL-encoded characters first.
    """
    name = unquote_plus(name)
    name = re.sub(r'[^a-zA-Z0-9-]', '-', name.lower().replace('.ipynb', ''))
    return name.strip('-').strip('/')

def on_files(files, config, **kwargs):
    """
    Modify file URIs before MkDocs processes them to lowercase and hyphenated format.
    """
    log.info("Running on_files hook to update page URIs...")
    
    for file in files:
        if file.src_uri.endswith('.ipynb'):
            new_uri = transform_name(file.dest_uri)
            if file.dest_uri != new_uri:
                log.info(f"Updating page URI: {file.dest_uri} -> {new_uri}")
                file.dest_uri = new_uri

    return files

def on_post_build(config, **kwargs):
    """
    Rename notebook output folders to lowercase and replace spaces with hyphens.
    """
    log.info("Running on_post_build hook to rename output folders...")

    site_dir = config['site_dir']
    rename_map = {}

    for root, dirs, _ in os.walk(site_dir, topdown=False):
        for dirname in dirs:
            new_name = transform_name(dirname)
            if dirname != new_name:
                original_path = os.path.join(root, dirname)
                temp_path = os.path.join(root, f"{new_name}_temp")
                final_path = os.path.join(root, new_name)

                try:
                    os.rename(original_path, temp_path)
                    os.rename(temp_path, final_path)
                    rename_map[f"/{dirname}/"] = f"/{new_name}/"
                except Exception as e:
                    log.error(f"Failed to rename {original_path}: {e}")
                else:
                    log.info(f"Successfully renamed: {original_path} -> {final_path}")

    log.info("Updating links in HTML files...")

    for root, _, files in os.walk(site_dir):
        for filename in files:
            if filename.endswith('.html'):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                updated_content = content
                for old, new in rename_map.items():
                    updated_content = re.sub(
                        rf'href="{re.escape(old)}"', f'href="{new}"', updated_content
                    )

                if content != updated_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    log.info(f"Updated links in: {file_path}")

def on_nav(nav, config, files, **kwargs):
    """
    Update navigation links to reflect lowercase and hyphenated notebook names.
    """
    log.info("Running on_nav hook to update navigation links...")
    
    def update_nav_item(item):
        if isinstance(item, list):
            for subitem in item:
                update_nav_item(subitem)
        elif isinstance(item, dict):  # Handle dictionaries (nested nav entries)
            for key, value in item.items():
                update_nav_item(value)
        elif hasattr(item, 'url') and item.url:
            original_url = unquote_plus(item.url)
            cleaned_url = transform_name(original_url)
            if original_url != cleaned_url:
                log.info(f"Updating navigation link: {original_url} -> {cleaned_url}")
                item.url = cleaned_url

    for nav_item in nav.items:
        update_nav_item(nav_item)
    
    log.info("Navigation link updates complete.")
    return nav
