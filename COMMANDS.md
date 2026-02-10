### photos in ~/data folder
### Go to the folder with input photos
```bash
cd ~/data
```
### make video from photos
### Create a 720p MP4 video from all JPG images at 5 fps. 720p significantly reduces memory usage
```bash
ffmpeg -framerate 5 -pattern_type glob -i '*.jpg' -vf scale=-1:720 -c:v libx264 -pix_fmt yuv420p output.mp4
```

### miniconda
### Create target folder for Miniconda installation
### Download the latest Miniconda installer for Linux x86_64
### Run the installer silently into ~/miniconda3
```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
```

### Remove installer script to save space
### Activate the newly installed Miniconda
### Go to home directory
```bash
rm ~/miniconda3/miniconda.sh
source ~/miniconda3/bin/activate
cd ~
```

### Clone the VIPE repository. Enter the VIPE project folder
```bash
git clone https://github.com/nv-tlabs/vipe.git
cd vipe
```

### Create the VIPE Conda environment from base config. Activate the VIPE environment
```bash
conda env create -f envs/base.yml
conda activate vipe
```

### Install Python dependencies with CUDA 12.8 wheels
```bash
pip install -r envs/requirements.txt --extra-index-url https://download.pytorch.org/whl/cu128
```

### Install VIPE in editable mode
```bash
pip install --no-build-isolation -e .
```
### or 
### Install VIPE with additional `dav3` extras
```bash
pip install --no-build-isolation -e .[dav3]
```

### Install missing hf_transfer
```bash
pip install hf_transfer
```


### Create output folder for VIPE results. Go back to home directory
### Copy generated video to a simpler name used by the pipeline
```bash
mkdir ~/vipe_out
cd ~
cp ~/data/output.mp4 zavod.mp4
```


### Run VIPE pipeline on input video and save slam map and artifacts
```bash
python vipe/run.py pipeline=no_vda streams=raw_mp4_stream streams.base_path=zavod.mp4 pipeline.output.path="vipe_out/" pipeline.output.save_slam_map=true pipeline.output.save_artifacts=true
```

### Create folder for converting VIPE output to COLMAP format
### Convert VIPE output to COLMAP-compatible structure
```bash
mkdir vipe_out_colmap
python vipe/scripts/vipe_to_colmap.py vipe_out/ --use_slam_map --output vipe_out_colmap/
```

### Install COLMAP
### Create binary COLMAP project folder
### Create sparse reconstruction folder
### Create first sparse model subfolder
```bash
apt install colmap
mkdir vipe_out_colmap_bin
mkdir vipe_out_colmap_bin/sparse
mkdir vipe_out_colmap_bin/sparse/0
```

### Copy images from COLMAP export into binary project
### Copy COLMAP text models into sparse/0
```bash
cp -r vipe_out_colmap/images vipe_out_colmap_bin/
cp vipe_out_colmap/*.txt vipe_out_colmap_bin/sparse/0/
```

### Enter the binary COLMAP project directory
### Convert COLMAP text model to binary format
```bash
cd vipe_out_colmap_bin
colmap model_converter --input_path sparse/0 --output_path sparse/0 --output_type BIN
```

### Remove temporary COLMAP text files
### Return to home directory
```bash
rm sparse/0/*.txt
cd ~
```



### downgrade gcc and g++ for CUDA 11.8
### Update package lists to get latest versions
### Install GCC/G++ version 11 required by CUDA 11.8
```bash
apt update
apt install gcc-11 g++-11
```

### Register gcc-11 as an alternative with high priority
### Register g++-11 as an alternative with high priority
```bash
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 110
update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 110
```

### Interactively select default gcc version (choose gcc-11)
### Interactively select default g++ version (choose g++-11)
```bash
update-alternatives --config gcc
update-alternatives --config g++
```


### CUDA 11.8 (NEED for Gaussian Splatting)
### Download CUDA 11.8 local installer for Linux
### Run the CUDA installer (follow prompts to install toolkit/driver)
```bash
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run
sh cuda_11.8.0_520.61.05_linux.run
```


### Clone the Gaussian Splatting repository
### Initialize and update all submodules
```bash
git clone https://github.com/graphdeco-inria/gaussian-splatting.git
git submodule update --init --recursive
```


### Create Conda environment for Gaussian Splatting
### Activate Gaussian Splatting environment
```bash
conda env create --file environment.yml
conda activate gaussian_splatting
```

### Train model
```bash
python train.py --source_path ~/vipe_out_colmap_bin --model_path ~/gauss_out -r 2 --iterations 10000 --checkpoint_iterations 5000 --eval
```

### Render novel views from the trained model
### Compute quality metrics for the trained model
```bash
python render.py --model_path ~/gauss_out
python metrics.py --model_path ~/gauss_out
```


### Turn rendered PNG frames into a demo MP4 video
```bash
ffmpeg -framerate 5 -i /root/gauss_out/train/ours_10000/renders/%05d.png -c:v libx264 -pix_fmt yuv420p demo.mp4
```


