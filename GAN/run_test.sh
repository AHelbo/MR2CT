# python3 train.py --dataroot ./datasets/mri2ct_pix2pix_nc1 --name mri2ct_pix2pix_nc1 --model pix2pix --display_id -1 --load_size 266 --input_nc 1 --output_nc 1 --n_epochs 2500 --gpu_ids -1 --dataset_mode aligned






python3 test.py --dataroot ./datasets/mri2ct_pix2pix_nc1 --name pix2pix_nc1_bn10 --model pix2pix --gpu_ids -1 --input_nc 1 --output_nc 1 --num_test -1 --epoch 30
