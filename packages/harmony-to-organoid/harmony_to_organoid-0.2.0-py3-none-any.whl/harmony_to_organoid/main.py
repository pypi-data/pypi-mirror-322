import json
import math
import os
import re
import time
import xml.etree.ElementTree as ET
from typing import List, Tuple

import markdown
import matplotlib.image as mpimg
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import tifffile
import typer
from matplotlib import colormaps, colors as mpl_colors
from matplotlib.colors import to_hex

app = typer.Typer(pretty_exceptions_show_locals=False)

fig_size = (10, 20)
colors = ["red", "blue", "green", "orange", "purple", "cyan", "magenta", "yellow", "black", "brown"]


def ensure_dirs(paths: List[str]):
    for path in paths:
        os.makedirs(path, exist_ok=True)


# Function to extract namespace
def get_namespace(tag):
    if tag.startswith('{'):
        return tag.split('}')[0] + '}'
    return ''


def boxes_overlap(a: Tuple[float, float, float, float], b: Tuple[float, float, float, float]) -> bool:
    if len(a) != 4 or len(b) != 4:
        typer.echo(f"Error: Each bounding box must have exactly four elements. Received: a={a}, b={b}", err=True)
        raise ValueError("Each bounding box must have exactly four elements.")

    leftA, topA, rightA, bottomA = a
    leftB, topB, rightB, bottomB = b
    no_overlap = (rightA < leftB) or (rightB < leftA) or (bottomA < topB) or (bottomB < topA)
    return not no_overlap


def build_adjacency(bboxes: List[Tuple[float, float, float, float]]) -> List[List[int]]:
    n = len(bboxes)
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if boxes_overlap(bboxes[i], bboxes[j]):
                adj[i].append(j)
                adj[j].append(i)
    return adj


def find_connected_components(adj: List[List[int]]) -> List[List[int]]:
    visited = set()
    components = []

    def dfs(start: int):
        stack = [start]
        comp = []
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                comp.append(node)
                for neigh in adj[node]:
                    if neigh not in visited:
                        stack.append(neigh)
        return comp

    for i in range(len(adj)):
        if i not in visited:
            comp = dfs(i)
            components.append(comp)
    return components


@app.command()
def preprocess_groups(
        index_file: str = typer.Option(..., help="Harmony XML index file from export."),
        output_dir: str = typer.Option(..., help="Directory to store all outputs."),
):
    """
    Parse the XML, plot field rectangles, identify and plot grouped overlapping rectangles.
    """
    projections_dir = get_projections_dir(output_dir)
    plots_dir = get_plots_dir(output_dir)
    intermediate_dir = get_intermediate_dir(output_dir)
    ensure_dirs([output_dir, projections_dir, plots_dir, intermediate_dir])

    tree = ET.parse(index_file)
    root = tree.getroot()

    namespace = get_namespace(root.tag)

    # ns = {"pehh": "http://www.perkinelmer.com/PEHH/HarmonyV5"}
    images_elems = root.findall(f".//{namespace}Images/{namespace}Image")
    typer.echo(f"Found {len(images_elems)} <Image> elements.")

    # xml_string = ET.tostring(root, encoding='unicode')
    # print(xml_string)

    channel_resolution = get_channel_metadata(namespace, root)

    # Collect field_rects
    field_rects = {}
    for idx, img_elem in enumerate(images_elems):
        channel_id = img_elem.find(f"{namespace}ChannelID").text
        field_str = img_elem.findtext(f"{namespace}FieldID")
        pos_x_m = img_elem.findtext(f"{namespace}PositionX")
        pos_y_m = img_elem.findtext(f"{namespace}PositionY")
        res_x_m = channel_resolution[channel_id]["ImageResolutionX"]
        res_y_m = channel_resolution[channel_id]["ImageResolutionY"]
        size_x_px = channel_resolution[channel_id]["ImageSizeX"]
        size_y_px = channel_resolution[channel_id]["ImageSizeY"]

        if not (field_str and pos_x_m and pos_y_m and res_x_m and res_y_m and size_x_px and size_y_px):
            continue

        fieldID = int(field_str)
        x_m = float(pos_x_m)
        y_m = float(pos_y_m)
        rX_m = float(res_x_m)
        rY_m = float(res_y_m)
        w_px = float(size_x_px)
        h_px = float(size_y_px)

        x_center_px = x_m / rX_m
        y_center_px = y_m / rY_m

        left_x = x_center_px - w_px / 2
        right_x = x_center_px + w_px / 2
        top_y = y_center_px - h_px / 2
        bottom_y = y_center_px + h_px / 2

        if fieldID in field_rects:
            if field_rects[fieldID] != (left_x, top_y, right_x, bottom_y):
                typer.echo(f"Warning: FieldID {fieldID} has inconsistent bounding boxes.", err=True)
        else:
            field_rects[fieldID] = (left_x, top_y, right_x, bottom_y)

    typer.echo(f"Processed field_rects. Total fields before removal: {len(field_rects)}")

    # Save field_rects to intermediate JSON
    with open(os.path.join(intermediate_dir, "field_rects.json"), 'w') as f:
        json.dump(field_rects, f)

    # Group overlapping fields
    fieldIDs = list(field_rects.keys())
    bounding_boxes = [tuple(v) for v in field_rects.values()]

    adj = build_adjacency(bounding_boxes)
    components = find_connected_components(adj)
    typer.echo(f"Found {len(components)} groups of overlapping fields.")

    # Assign fields to groups
    field_to_group = {}
    for group_idx, comp in enumerate(components):
        for idx in comp:
            fieldID = fieldIDs[idx]
            field_to_group[fieldID] = group_idx

    typer.echo(f"Assigned fields to groups.")

    # Save field_to_group to intermediate JSON
    with open(os.path.join(intermediate_dir, "field_to_group.json"), 'w') as f:
        json.dump(field_to_group, f)

    plot_grouped_fields(bounding_boxes, components, fieldIDs, plots_dir)


def plot_grouped_fields(bounding_boxes, components, fieldIDs, plots_dir):
    # Plot grouped rectangles
    fig, ax = plt.subplots(figsize=fig_size)
    for group_index, comp in enumerate(components):
        color = colors[group_index % len(colors)]

        min_left = None
        max_right = None
        max_top = None

        for idx in comp:
            left, top, right, bottom = bounding_boxes[idx]
            w = right - left
            h = bottom - top

            max_top = max(max_top, bottom) if max_top else bottom
            min_left = min(min_left, left) if min_left else left
            max_right = max(max_right, right) if max_right else right

            # Draw the bounding box
            rect = patches.Rectangle(
                (left, top),
                w, h,
                linewidth=1.5,
                edgecolor=color,
                facecolor='none'
            )
            ax.add_patch(rect)

            ax.text(left + w / 2, top + h / 2, f"{fieldIDs[idx]}", color=color, fontsize=8, ha='center', va='center')

        ax.text((min_left + max_right)*0.5, max_top + 40, f"Group {group_index}", color=color, fontsize=10, ha='center', va='bottom')

    ax.set_aspect("equal", "box")
    ax.relim()
    ax.autoscale_view()
    plt.title("Grouped Fields")
    plt.xlabel("X (pixels)")
    plt.ylabel("Y (pixels)")
    fig.tight_layout()
    grouped_plot_path = os.path.join(plots_dir, "plot_grouped_fields.png")
    plt.savefig(grouped_plot_path)
    plt.close()
    typer.echo(f"Saved grouped fields plot at '{grouped_plot_path}'.")


def get_channel_metadata(namespace, root):
    # Parse the <Map> section
    map_entries = root.findall(f".//{namespace}Maps/{namespace}Map/{namespace}Entry")
    channel_meta = {}
    for entry in map_entries:
        channel_id = entry.attrib.get("ChannelID")
        if not channel_id:
            continue
        res_x_tag = entry.find(f"{namespace}ImageResolutionX")
        if res_x_tag is not None:
            channel_meta[channel_id] = {
                "ImageResolutionX": float(res_x_tag.text),
                "ImageResolutionY": float(entry.find(f"{namespace}ImageResolutionY").text),
                "ImageSizeX": float(entry.find(f"{namespace}ImageSizeX").text),
                "ImageSizeY": float(entry.find(f"{namespace}ImageSizeY").text),
                "ChannelName": str(entry.find(f"{namespace}ChannelName").text)
            }
    typer.echo(f"Channel metadata: {channel_meta}")
    return channel_meta


def get_projections_dir(output_dir):
    projections_dir = os.path.join(output_dir, "projections")
    return projections_dir


def get_plots_dir(output_dir):
    plots_dir = os.path.join(output_dir, "plots")
    return plots_dir


def get_intermediate_dir(output_dir):
    intermediate_dir = os.path.join(output_dir)
    return intermediate_dir


def plot_projections_in_rectangles(field_rects, field_to_group, projections_dir, plots_dir):
    fig, ax = plt.subplots(figsize=fig_size)

    # Aggregate bounding boxes per group
    group_bboxes = {}
    for fieldID, group_idx in field_to_group.items():
        bbox = field_rects[str(fieldID)]
        if group_idx in group_bboxes:
            # Expand the group's bounding box to include the current field's bbox
            group_bboxes[group_idx][0] = min(group_bboxes[group_idx][0], bbox[0])  # left
            group_bboxes[group_idx][1] = min(group_bboxes[group_idx][1], bbox[1])  # top
            group_bboxes[group_idx][2] = max(group_bboxes[group_idx][2], bbox[2])  # right
            group_bboxes[group_idx][3] = max(group_bboxes[group_idx][3], bbox[3])  # bottom
        else:
            group_bboxes[group_idx] = list(bbox)

    # Plot each group's max projection within its combined bounding box
    for group_idx, bbox in group_bboxes.items():
        left, top, right, bottom = bbox

        # Path to the group's projection image
        projection_path = os.path.join(projections_dir, f"group{group_idx}_joint_max_projection.png")
        if not os.path.exists(projection_path):
            typer.echo(f"Projection image not found: {projection_path}", err=True)
            continue

        # Read and display the image
        img = mpimg.imread(projection_path)
        extent = [left, right, bottom, top]
        ax.imshow(img, extent=extent, aspect='auto', origin='lower')

        ax.text((left + right)*0.5, bottom + 40, f"Group {group_idx}", color="black", fontsize=10, ha='center', va='bottom')

    ax.set_aspect("equal", "box")
    ax.invert_yaxis()
    ax.relim()
    ax.autoscale_view()
    ax.set_xlabel("X (pixels)")
    ax.set_ylabel("Y (pixels)")
    ax.set_title("Max Projections")
    fig.tight_layout()
    plot_path = os.path.join(plots_dir, "plot_projections.png")
    plt.savefig(plot_path)
    plt.close()
    typer.echo(f"Saved composite projections plot at '{plot_path}'.")


def update_channel_color_settings(channel_colors_str: str, num_channels: int, lut_min: str, lut_max: str):
    if channel_colors_str:
        try:
            channel_color_list = channel_colors_str.split(",")
            channel_colors = [to_hex(color) for color in channel_color_list]
        except ValueError:
            typer.echo("Error: Color values must be valid matplotlib colors ('blue' or '#0000ff' for example)'.", err=True)
            raise typer.Exit(code=1)

        if len(channel_color_list) != num_channels:
            typer.echo(
                "Error: The number of colors must match the number of channels.",
                err=True
            )
            raise typer.Exit(code=1)
    else:
        channel_colors = []
        cmap = colormaps.get_cmap("tab10")
        num_colors_available = cmap.N
        for idx in range(num_channels):
            color = cmap(idx % num_colors_available)
            color_hex = mpl_colors.to_hex(color)
            channel_colors.append(color_hex)

    typer.echo(f"Assigned colors to channels: {channel_colors}")

    if lut_min:
        try:
            lut_min_list = [float(x) for x in lut_min.split(",")]
        except ValueError:
            typer.echo("Error: LUT min and max values must be valid numbers.", err=True)
            raise typer.Exit(code=1)

        if len(lut_min_list) != num_channels:
            typer.echo(
                "Error: The number of LUT min values must match the number of channels.",
                err=True
            )
            raise typer.Exit(code=1)
    else:
        lut_min_list = [0 for _ in range(num_channels)]

    if lut_max:
        try:
            lut_max_list = [float(x) for x in lut_max.split(",")]
        except ValueError:
            typer.echo("Error: LUT max values must be valid numbers.", err=True)
            raise typer.Exit(code=1)

        if len(lut_max_list) != num_channels:
            typer.echo(
                "Error: The number of LUT max values must match the number of channels.",
                err=True
            )
            raise typer.Exit(code=1)

    else:
        lut_max_list = [2000 for _ in range(num_channels)]

    lut_ranges = list(zip(lut_min_list, lut_max_list))
    typer.echo(f"Using LUT ranges: {lut_ranges}")

    return lut_ranges, channel_colors


def compute_and_save_max_projection(
        arr: np.ndarray,
        group_idx: int,
        projections_dir: str,
        channel_names: list[str]
):
    """
    Computes and saves the maximum intensity projection for a group:
    1. Saves individual channel projections as unnormalized TIFFs.
    2. Saves the joint RGB projection as a normalized TIFF.

    Parameters:
    - arr (np.ndarray): 4D array with shape (C, Z, Y, X).
    - group_idx (int): Index of the group.
    - lut_ranges (dict): Dictionary mapping channel index to (min, max) tuples for normalization.
    - channel_colors (dict): Dictionary mapping channel index to HEX color codes.
    - projections_dir (str): Directory to save the projection images.
    """
    # Ensure the projections directory exists
    os.makedirs(projections_dir, exist_ok=True)

    # Compute max projection over Z-axis for each channel
    max_projections = np.max(arr, axis=1)  # Shape: (C, Y, X)

    # Save individual channel projections without normalization
    for c, c_name in zip(range(max_projections.shape[0]), channel_names):
        # Define the projection image path
        projection_filename = f"group{group_idx}_{c_name}_max_projection.tiff"
        projection_path = os.path.join(projections_dir, projection_filename)

        # Save the individual channel projection as TIFF
        tifffile.imwrite(projection_path, max_projections[c])
        typer.echo(f"Group {group_idx}: Saved Channel {c_name} max projection at '{projection_path}'.")


def create_joint_rgb_image_from_tiffs(
        projections_dir: str,
        group_idx: int,
        lut_ranges: list,
        channel_colors: list,
        channel_name_order: list,
        output_dir: str
):
    """
    Creates a joint RGB image from individual channel max projections using consistent normalization.

    Parameters:
    - projections_dir (str): Directory where individual channel TIFFs are stored.
    - group_idx (int): Index of the group.
    - lut_ranges (list): List mapping channel index to (min, max) tuples for normalization.
    - channel_colors (list): List mapping channel index to HEX color codes.
    - output_dir (str): Directory to save the joint RGB image.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    channels_data = []
    for channel_name in channel_name_order:
        projection_path = os.path.join(projections_dir, f"group{group_idx}_{channel_name}_max_projection.tiff")
        if os.path.exists(projection_path):
            data = tifffile.imread(projection_path).astype(np.float32)
            channels_data.append(data)
            typer.echo(f"Loaded '{projection_path}' with shape {data.shape} and dtype {data.dtype}.")
        else:
            typer.echo(f"No channel projections found for group {group_idx} in '{projection_path}'.")
            return

    channels_data = np.stack(channels_data, axis=0)  # Shape: (C, Y, X)

    # Apply normalization using lut_ranges
    normalized = []
    for c in range(channels_data.shape[0]):
        channel = channels_data[c]
        lut_min, lut_max = lut_ranges[c]
        # Prevent division by zero
        if lut_max - lut_min == 0:
            norm = np.zeros_like(channel)
        else:
            norm = (channel - lut_min) / (lut_max - lut_min)

        norm = np.clip(norm, 0, 1)
        normalized.append(norm)

    normalized = np.stack(normalized, axis=0)  # Shape: (C, Y, X)

    # Combine channels into RGB using channel_colors
    rgb_image = np.zeros((channels_data.shape[1], channels_data.shape[2], 3), dtype=np.float32)
    for c in range(channels_data.shape[0]):
        color_hex = channel_colors[c]
        rgb = mpl_colors.to_rgb(color_hex)
        rgb_image[..., 0] += normalized[c] * rgb[0]
        rgb_image[..., 1] += normalized[c] * rgb[1]
        rgb_image[..., 2] += normalized[c] * rgb[2]

    # Clip the RGB image to [0,1]
    rgb_image = np.clip(rgb_image, 0, 1)
    rgb_image_uint8 = (rgb_image * 255).astype(np.uint8)

    # Define the joint RGB projection image path
    joint_image_filename = f"group{group_idx}_joint_max_projection.png"
    joint_image_path = os.path.join(projections_dir, joint_image_filename)

    # tifffile.imwrite(joint_image_path, rgb_image_uint8)
    plt.imsave(joint_image_path, rgb_image_uint8)
    typer.echo(f"Group {group_idx}: Saved joint RGB max projection at '{joint_image_path}'.")


def generate_maximum_projections(
        index_file: str = typer.Option(..., help="Harmony XML index file from export."),
        output_dir: str = typer.Option(..., help="Directory to store all outputs."),
        colors: str = typer.Option(None, help="Channel colors (comma separated value per channel)."),
        lut_min: str = typer.Option(None, help="Minimum data range for normalization (comma separated value per channel)."),
        lut_max: str = typer.Option(None, help="Maximum data range for normalization (comma separated value per channel).")
):

    projections_dir = get_projections_dir(output_dir)
    intermediate_dir = get_intermediate_dir(output_dir)
    ensure_dirs([projections_dir, intermediate_dir])

    # Load field_to_group
    field_to_group_path = os.path.join(intermediate_dir, "field_to_group.json")
    if not os.path.exists(field_to_group_path):
        typer.echo(
            f"Field to group mapping not found at '{field_to_group_path}'. Please run 'plot-grouped-rectangles' first.",
            err=True)
        raise typer.Exit(code=1)

    with open(field_to_group_path, 'r') as f:
        field_to_group = json.load(f)

    tree = ET.parse(index_file)
    root = tree.getroot()
    # Extract namespace if present
    namespace = get_namespace(root.tag)

    images_elems = root.findall(f".//{namespace}Images/{namespace}Image")

    channel_meta = get_channel_metadata(namespace, root)

    field_planes = {}
    field_bboxes = {}

    for img_elem in images_elems:
        field_str = img_elem.findtext(f"{namespace}FieldID")
        plane_str = img_elem.findtext(f"{namespace}PlaneID")
        channel_str = img_elem.findtext(f"{namespace}ChannelID")
        tiff_name = img_elem.findtext(f"{namespace}URL")
        img_id = img_elem.findtext(f"{namespace}id")

        if not (field_str and plane_str and channel_str and tiff_name and img_id):
            continue

        fieldID = int(field_str)
        planeID = int(plane_str)
        channelID = int(channel_str)

        # Check if field is in group_to_keep
        if str(fieldID) not in field_to_group:
            continue

        # Construct full TIFF path
        tiff_path = os.path.abspath(os.path.join(index_file, os.pardir, tiff_name))
        if not os.path.exists(tiff_path):
            typer.echo(f"Missing file: {tiff_path}", err=True)
            continue

        # Organize TIFFs by field, channel, and plane
        channel_dict = field_planes.setdefault(str(fieldID), {}).setdefault(str(channelID), {})
        if planeID in channel_dict:
            typer.echo(
                f"Warning: Duplicate planeID {planeID} for fieldID {fieldID}, channelID {channelID}. Overwriting.",
                err=True)
        channel_dict[str(planeID)] = tiff_path

        # Collect bounding box information
        channel_id = img_elem.find(f"{namespace}ChannelID").text
        pos_x_m = float(img_elem.findtext(f"{namespace}PositionX"))
        pos_y_m = float(img_elem.findtext(f"{namespace}PositionY"))
        res_x_m = channel_meta[channel_id]["ImageResolutionX"]
        res_y_m = channel_meta[channel_id]["ImageResolutionY"]
        size_x_px = channel_meta[channel_id]["ImageSizeX"]
        size_y_px = channel_meta[channel_id]["ImageSizeY"]

        x_center_px = pos_x_m / res_x_m
        y_center_px = pos_y_m / res_y_m

        left_x = x_center_px - size_x_px / 2
        right_x = x_center_px + size_x_px / 2
        top_y = y_center_px - size_y_px / 2
        bottom_y = y_center_px + size_y_px / 2

        if str(fieldID) in field_bboxes:
            current_bbox = tuple(field_bboxes[str(fieldID)])
            new_bbox = (
                min(current_bbox[0], left_x),
                max(current_bbox[1], right_x),
                min(current_bbox[2], top_y),
                max(current_bbox[3], bottom_y)
            )
            field_bboxes[str(fieldID)] = new_bbox
        else:
            field_bboxes[str(fieldID)] = (left_x, right_x, top_y, bottom_y)

    typer.echo(f"Collected plane data for {len(field_planes)} fields.")
    typer.echo(f"Collected bounding boxes for {len(field_bboxes)} fields.")

    # Iterate over each group to create combined volumes
    group_indices = sorted(set(field_to_group.values()))

    for group_idx in group_indices:
        fields_in_group = [fieldID for fieldID, g in field_to_group.items() if g == group_idx]
        typer.echo(f"\nProcessing group {group_idx} with fields: {fields_in_group}")

        # Compute combined bounding box
        lefts = [field_bboxes[str(fieldID)][0] for fieldID in fields_in_group]
        rights = [field_bboxes[str(fieldID)][1] for fieldID in fields_in_group]
        tops = [field_bboxes[str(fieldID)][2] for fieldID in fields_in_group]
        bottoms = [field_bboxes[str(fieldID)][3] for fieldID in fields_in_group]

        combined_left = int(np.floor(min(lefts)))
        combined_right = int(np.ceil(max(rights)))
        combined_top = int(np.floor(min(tops)))
        combined_bottom = int(np.ceil(max(bottoms)))

        combined_y_size = combined_bottom - combined_top
        combined_x_size = combined_right - combined_left

        # Determine channels in group
        channels_in_group = set()
        for fieldID in fields_in_group:
            channels_in_group.update(field_planes[str(fieldID)].keys())
        channels_in_group = sorted(list(channels_in_group))
        channel_names = [channel_meta[channel_id]["ChannelName"].replace(" ", "_") for channel_id in channels_in_group]
        num_channels = len(channels_in_group)
        typer.echo(f"Channels in group {group_idx}: {channel_names}")

        # Verify Z size consistency
        z_sizes = []
        for fieldID in fields_in_group:
            for channelID in field_planes[str(fieldID)]:
                z_sizes.append(len(field_planes[str(fieldID)][str(channelID)]))
        z_sizes = list(set(z_sizes))
        if len(z_sizes) != 1:
            typer.echo(f"Error: Inconsistent Z sizes in group {group_idx}. Skipping.", err=True)
            continue
        z_size = z_sizes[0]

        combined_shape = (num_channels, z_size, combined_y_size, combined_x_size)
        typer.echo(f"Combined volume shape (C, Z, Y, X): {combined_shape}")

        combined_volume = np.zeros(combined_shape, dtype=np.uint16)

        # Insert each field's volume
        for fieldID in fields_in_group:
            field_bbox = field_bboxes[str(fieldID)]
            left_x, right_x, top_y, bottom_y = field_bbox
            offset_y = int(top_y - combined_top)
            offset_x = int(left_x - combined_left)

            for channel_idx, channelID in enumerate(channels_in_group):
                if channelID not in field_planes[str(fieldID)]:
                    typer.echo(f"Warning: Field {fieldID} missing channel {channelID}. Skipping.", err=True)
                    continue

                plane_dict = field_planes[str(fieldID)][str(channelID)]
                sorted_planeIDs = sorted([int(pid) for pid in plane_dict.keys()])
                slices_2d = []
                for planeID in sorted_planeIDs:
                    path_2d = plane_dict[str(planeID)]
                    img_2d = tifffile.imread(path_2d)
                    slices_2d.append(img_2d)

                field_volume = np.stack(slices_2d, axis=0)

                if field_volume.shape[0] != z_size:
                    typer.echo(
                        f"Error: Field {fieldID}, Channel {channelID} Z size {field_volume.shape[0]} does not match group Z size {z_size}. Skipping.",
                        err=True)
                    continue

                y_start = combined_y_size - (offset_y + field_volume.shape[1])
                y_end = y_start + field_volume.shape[1]
                x_start, x_end = offset_x, offset_x + field_volume.shape[2]

                if y_end > combined_y_size or x_end > combined_x_size:
                    typer.echo(f"Error: Field {fieldID}, Channel {channelID} exceeds combined volume bounds. Skipping.",
                               err=True)
                    continue

                combined_volume[channel_idx, :, y_start:y_end, x_start:x_end] = np.maximum(
                    combined_volume[channel_idx, :, y_start:y_end, x_start:x_end],
                    field_volume
                )

        group_name = group_idx

        # Compute and save projection
        lut_ranges, channel_colors = update_channel_color_settings(colors, num_channels, lut_min, lut_max)

        compute_and_save_max_projection(
            arr=combined_volume,
            group_idx=group_name,
            projections_dir=projections_dir,
            channel_names=channel_names
        )

        # Step 2: Create joint RGB image
        create_joint_rgb_image_from_tiffs(
            projections_dir=projections_dir,
            group_idx=group_name,
            lut_ranges=lut_ranges,
            channel_colors=channel_colors,
            channel_name_order=channel_names,
            output_dir=output_dir
        )

        typer.echo(
            f"Group {group_idx}: Stored combined multichannel volume at '/{group_name}' with shape {combined_volume.shape}")


def plot_joint_projections(plots_dir, annotations, images_per_row: int = 3, padding = 20):

    collage_path = os.path.join(plots_dir, "plot_joint_field_annotations.png")

    num_images = len(annotations)
    num_rows = math.ceil(num_images / images_per_row)

    # Create subplots
    fig, axes = plt.subplots(num_rows, images_per_row, figsize=(10,10))
    axes = axes.flatten()  # Flatten in case of multiple rows

    for idx, ax in enumerate(axes):
        if idx < num_images:
            img = mpimg.imread(annotations[idx])
            ax.imshow(img)
            ax.set_title(f"Group {idx}", color='white', fontsize=10, pad=5)
        ax.axis('off')

        ax.set_facecolor('black')

    fig.patch.set_facecolor('black')

    plt.subplots_adjust(wspace=padding, hspace=padding)
    plt.tight_layout()
    plt.savefig(collage_path, bbox_inches='tight', pad_inches=0)
    plt.close()
    typer.echo(f"Collage saved at '{collage_path}'.")


@app.command()
def plot_projections(
        output_dir: str = typer.Option(..., help="Directory where outputs are stored.")
):

    intermediate_dir = get_intermediate_dir(output_dir)
    projections_dir = get_projections_dir(output_dir)
    plots_dir = get_plots_dir(output_dir)

    # Load field_to_group
    field_to_group_path = os.path.join(intermediate_dir, "field_to_group.json")
    if not os.path.exists(field_to_group_path):
        typer.echo(
            f"Field to group mapping not found at '{field_to_group_path}'.",
            err=True)
        raise typer.Exit(code=1)

    with open(field_to_group_path, 'r') as f:
        field_to_group = json.load(f)

    # Load field_rects
    field_rects_path = os.path.join(intermediate_dir, "field_rects.json")
    if not os.path.exists(field_rects_path):
        typer.echo(
            f"Field rects not found at '{field_rects_path}'.",
            err=True)
        raise typer.Exit(code=1)

    with open(field_rects_path, 'r') as f:
        field_rects = json.load(f)

    plot_projections_in_rectangles(field_rects, field_to_group, projections_dir, plots_dir)

    # Identify unique groups from field_to_group
    groups = set(field_to_group.values())
    typer.echo(f"Processing {len(groups)} groups: {groups}")

    annotations = []

    for group_idx in groups:
        typer.echo(f"\nProcessing Group {group_idx}")

        annotation_path = plot_projection_with_fields(field_rects, field_to_group, group_idx, plots_dir, projections_dir)
        annotations.append(annotation_path)
        
    plot_joint_projections(plots_dir, annotations)


def plot_projection_with_fields(field_rects, field_to_group, group_idx, plots_dir, projections_dir):
    projection_path = os.path.join(projections_dir, f"group{group_idx}_joint_max_projection.png")
    # Read and display the image
    max_projection_img = mpimg.imread(projection_path)
    # Identify fields belonging to this group
    fields_in_group = [field_id for field_id, grp in field_to_group.items() if grp == group_idx]
    # Extract rectangle data for these fields
    rectangles = {}
    for field_id in fields_in_group:
        rectangles[field_id] = field_rects.get(field_id)
    # Adjust rectangle coordinates by removing min x and min y
    min_x = min(rectangles[id][0] for id in rectangles)
    min_y = min(rectangles[id][1] for id in rectangles)
    # Create annotated image
    fig, ax = plt.subplots(1, figsize=(10, 10))
    max_projection_img = np.flipud(max_projection_img)
    ax.imshow(max_projection_img, origin='lower')
    for rect_id in rectangles:
        rect = rectangles[rect_id]
        x = rect[0] - min_x
        y = rect[1] - min_y
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]

        # Create a Rectangle patch
        rectangle = patches.Rectangle((x, y), width, height, linewidth=2, edgecolor='white', facecolor='none')
        ax.add_patch(rectangle)

        # Add text annotation
        ax.text(x + width / 2, y + height / 2, rect_id, color='white', fontsize=70, ha='center', va='center')
    # Remove axes for a cleaner look
    ax.axis('off')
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    plt.tight_layout(pad=1.3)

    annotated_image_filename = f"group{group_idx}_joint_max_projection_annotated.png"
    annotated_image_path = os.path.join(plots_dir, annotated_image_filename)
    plt.savefig(annotated_image_path, bbox_inches='tight', pad_inches=0.2)
    plt.close(fig)  # Close the figure to free memory
    typer.echo(f"Group {group_idx}: Saved annotated joint RGB image at '{annotated_image_path}'.")
    return annotated_image_path


@app.command()
def generate_readme(
        output_dir: str = typer.Option(..., help="Directory where outputs are stored.")
):
    """
    Generate or regenerate the README.md file with dataset information and Neuroglancer links.
    """
    readme_path = os.path.join(output_dir, "README.md")

    # Create README content
    readme_lines = []
    readme_lines.append("")
    readme_lines.append("![Projections with fields](plots/plot_joint_field_annotations.png)")
    readme_lines.append("")
    readme_lines.append("![Grouped fields](plots/plot_grouped_fields.png)")
    readme_lines.append("")
    readme_lines.append("![Projections](plots/plot_projections.png)")
    readme_lines.append("")

    # Write to README.md
    with open(readme_path, 'w') as f:
        f.write('\n'.join(readme_lines))

    typer.echo(f"\nREADME has been successfully created at '{readme_path}'.")

    readme_html_path = os.path.join(output_dir, "README.html")
    with open(readme_path, 'r') as f:
        md_content = f.read()

    html_content = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])

    with open(readme_html_path, 'w') as f:
        f.write(html_content)

    typer.echo(f"README HTML has been successfully created at '{readme_html_path}'.")


@app.command()
def process(
        index_file: str = typer.Option(None, help="Harmony XML index file from export."),
        output_dir: str = typer.Option(None, help="Directory to store all outputs."),
        colors: str = typer.Option(None, help="Channel colors (comma separated value per channel)."),
        lut_min: str = typer.Option(None, help="Minimum data range for normalization (comma separated value per channel)."),
        lut_max: str = typer.Option(None, help="Maximum data range for normalization (comma separated value per channel).")
):
    """
    Execute all processing steps: plot grouped rectangles, generate projections, and create README.
    """

    start_time = time.perf_counter()

    typer.echo("Starting full processing pipeline...")

    typer.echo("\nStep 1: Plotting grouped fields...")
    preprocess_groups(index_file=index_file, output_dir=output_dir)

    typer.echo("\nStep 2: Generate Max Projections...")
    generate_maximum_projections(index_file=index_file, output_dir=output_dir, colors=colors, lut_min=lut_min, lut_max=lut_max)

    typer.echo("\nStep 3: Plot projections together...")
    plot_projections(output_dir=output_dir)

    typer.echo("\nStep 4: Generating README...")
    generate_readme(output_dir=output_dir)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    typer.echo(f"\nFull processing pipeline completed successfully. Total Execution Time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    app()
