#!/bin/bash

# Start timer
start=$(date +%s)

#define source paths:
GAN="hendrix:~/GAN/checkpoints/*"
PALETTE="hendrix:~/diffusion/experiments/*"

#define target path (results folder):
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

#scripts are stored in.....
SCRIPTS="$TARGET_DIR/scripts"

CHECKPOINTS="$TARGET_DIR/Checkponts"

# Get checkpoint images and logs
# rsync -zarv --include="*/" --include="*.log" --include="*.tiff" --exclude="*" $PALETTE "$TARGET_DIR/Checkpoints/diffusion"
# rsync_palette=$?
# echo $rsync_palette

# rsync -zarv --include="*/" --include="*.txt" --include="*.html" --include="*.png" --exclude="*" $GAN "$TARGET_DIR/Checkpoints/GAN"
# rsync_gan=$?
# echo $rsync_gan

# if [[ $rsync_palette -ne 0 && $rsync_gan -ne 0 ]]; then
#     echo "No succesfull data transfer, exit"
#     exit 1
# fi


# plot and draw images
if [[ $rsync_palette -eq 0 || $1 -eq 1 ]]; then
    echo "Received Palette data, plotting and processing images:"
    python3 $SCRIPTS/palette_plot_losses.py $TARGET_DIR &
    # python3 $SCRIPTS/palette_images.py $TARGET_DIR &
fi

# if [[ $rsync_gan -eq 0 || $1 -eq 1 ]]; then
#     echo "Received Pix2Pix data, plotting and processing images:"
#     python3 $SCRIPTS/gan_plot_losses.py $TARGET_DIR &
#     python3 $SCRIPTS/gan_images.py $TARGET_DIR &
# fi

wait

# End time
end=$(date +%s)
execution_time=$((end - start))

echo "Finished processing output. Execution Time: $execution_time seconds"
echo ""