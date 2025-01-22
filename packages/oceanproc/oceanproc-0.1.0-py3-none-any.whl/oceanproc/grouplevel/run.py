import pathlib
import os
from glob import glob


def find_beta_maps(output_dir: pathlib.Path|str,
                   sub: str):
    beta_map_paths = [] 
    for beta_map in glob(
        os.path.join(
            output_dir,
            f"sub-{sub}",
            "func",
            "*desc-*activation*"
        )
    ):
        beta_map_paths.append(beta_map)
    return beta_map_paths
