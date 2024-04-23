# python3 train.py --dataroot ./datasets/mr2ct_pix2pix_nc1 --name mr2ct_pix2pix_nc1 --model pix2pix --display_id -1 --load_size 266 --input_nc 1 --output_nc 1 --n_epochs 2500 --gpu_ids -1 --dataset_mode aligned






python3 train.py --dataroot ./datasets/mr2ct_pix2pix_nc1 --name mr2ct_pix2pix_nc1 --model pix2pix --display_id -1 --load_size 266 --input_nc 1 --output_nc 1 --n_epochs 2500 --gpu_ids -1 --dataset_mode aligned --norm batch --batch_size 5 #--train_schedule "[(1, 50, 50, 3),(2, 70, 50, 1)]"

