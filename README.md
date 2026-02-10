# 3DGS Demo

3D Gaussian Splatting demo pipeline with point cloud visualization. Input photos are processed via VIPE, COLMAP, and Gaussian Splatting to produce view. The trained model can be visualized with `cloud_demo.py`.


## Pipeline
Place input photos in `~/data`, and then follow commands from COMMANDS.md 

## Result folders
ALL RESULTS COULD BE FOUND [HERE](https://icedrive.net/s/x4Cu3igk98Ww6W1xRPw1tz2BGSNP)
- **vipe_out** - Folder with result model after VIPE usage on data
- **vipe_out_colmap_bin** - VIPE result in COLMAP format
- **gauss_out** - Results after Gaussian Splatting, including checkpoing, train/test data, result model

*RESULT MODEL COULD BE FOUND IN* **./gauss_out/point_cloud/iteration_10000/point_cloud.ply** 

## Result videos
ALL RESULTS COULD BE FOUND [HERE](https://icedrive.net/s/x4Cu3igk98Ww6W1xRPw1tz2BGSNP)
- **zavod.mp4** - initial video
- **demo.mp4** - render video
- **development.mp4** - process of full flow execution
- **clouds.mp4** - render visualization

## Environment
- Tested on **runpod.io** pod. Official image **runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404** 
- RTX A4500 1x 20GB - (not enough for default or dav3 VIPE pipelines)
- vCPU 12
- Memory 62 GB
- Container disk 50 GB (not enough for full flow all in one. Use more space or delete VIPE environment after usage)

## Running cloud_demo.py
```bash
pip install viser numpy plyfile
```
`cloud_demo.py` serves a point cloud from a PLY file over the web for interactive viewing.

**Usage:**
```bash
python cloud_demo.py <path_to_ply_file>
```

**Example:**
```bash
python cloud_demo.py ~/gauss_out/point_cloud/iteration_10000/point_cloud.ply
```

After starting, open the URL shown in the terminal (typically `http://localhost:8080`) in a browser to view the point cloud.

---




## Evaluated metrics after full flow
- SSIM :    0.6767617
- PSNR :   20.8839741
- LPIPS:    0.2418534
