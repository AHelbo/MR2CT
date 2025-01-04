python3 train.py \
  --name GAN_nc1 \
  --dataroot ../datasets/mri2ct_nc1 \
  --input_nc 1 \
  --output_nc 1 \
  --norm batch \
  --batch_size 10 \
  --lr 0.00005 \
  --D_update_freq 10 \
  --gpu_ids -1
