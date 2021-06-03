# ScanMix

Disclaimer: We're currently in the process of refactoring and uploading code to this repository. The current version is not thoroughly tested and may break.

The pipeline for running ScanMix is the following:

For CIFAR:

Step 1:

`python simclr.py --config_env configs/env.yml --config_exp configs/pretext/<config_file.yml>`

Step 2:

`python scan.py --config_env configs/env.yml --config_exp configs/scan/<config_file.yml>`

Step 3:

(symmetric) `python ScanMix.py --r [0.2/0.5/0.8/0.9] --noise_mode sym --config_env configs/env.yml --config_exp configs/scanmix/<config_file.yml>`

(asymmetric) `python ScanMix.py --r [0.4/0.49] --noise_mode asym --config_env configs/env.yml --config_exp configs/scanmix/<config_file.yml>`

(semantic) `python ScanMix.py --r 0.4 --noise_mode semantic_[vgg/resnet/densenet] --config_env configs/env.yml --config_exp configs/scanmix/<config_file.yml>`


For Webvision

Step 0:

Use [moco-v2](https://github.com/facebookresearch/moco) to pre-train an InceptionResNetV2 on Webvision and save the model weights as `moco_pretrained/webvision.tar`.

Step 1:

`python moco.py --dataset webvision --config_env configs/env.yml --config_exp configs/pretext/<config_file.yml>`

Step 2:

`python scan.py --config_env configs/env.yml --config_exp configs/scan/<config_file.yml>`

Step 3:

`python ScanMix_parallel.py --config_env configs/env.yml --config_exp configs/scanmix/<config_file.yml> --cudaids 0 1`
