python3 train.py \
  --name test_nc1 \
  --dataroot ../datasets/mri2ct_nc1 \
  --gpu_ids -1 \
  --input_nc 1 \
  --batch_size 10 \
  --lr 0.00005 \
  --D_update_freq 20 \
  --display_freq 20