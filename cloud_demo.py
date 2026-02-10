import viser
import numpy as np
from plyfile import PlyData
import time
import argparse


def load_ply(filepath):
    """Load point cloud from PLY file"""
    plydata = PlyData.read(filepath)
    vertices = plydata['vertex']

    positions = np.vstack([vertices['x'], vertices['y'], vertices['z']]).T

    if 'red' in vertices.data.dtype.names:
        colors = np.vstack([
            vertices['red'],
            vertices['green'],
            vertices['blue']
        ]).T
        colors = colors.astype(np.float32) / 255.0 
    else:
        colors = np.ones_like(positions) * 0.5  

    return positions, colors

def main():
    parser = argparse.ArgumentParser(
        description="Visualize a point cloud from a PLY file."
    )
    parser.add_argument(
        "ply_path",
        help="Path to the input PLY point cloud file.",
    )
    args = parser.parse_args()

    ply_path = args.ply_path

    print(f"Loading point cloud from {ply_path}...")
    positions, colors = load_ply(ply_path)
    print(f"Loaded {len(positions)} points")


    server = viser.ViserServer()

    server.add_point_cloud( name="/point_cloud", points=positions, colors=colors, point_size=0.01)

    while True:
        time.sleep(10.0)

if __name__ == "__main__":
    main()