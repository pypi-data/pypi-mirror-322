"""Parser module to parse gear config.json."""

from pathlib import Path
from typing import Tuple

from flywheel_gear_toolkit.context import GearToolkitContext


# This function mainly parses gear_context's config.json file and returns relevant inputs and options.
def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[str, str]:
    """Get seg_only flag and debug option"""

    seg_only = gear_context.config.get("seg-only")
    debug = gear_context.config.get("debug")

    input_file = Path(gear_context.get_input_path("T1w"))
    file_name = input_file.name

    if not (file_name.endswith(".nii.gz") or file_name.endswith(".nii")):
        raise ValueError(
            f"input_file must be of type nifti (.nii) or nifti gz (.nii.gz), "
            f"({input_file} found)"
        )

    return seg_only, debug
