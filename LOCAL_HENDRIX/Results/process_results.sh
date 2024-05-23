#!/bin/bash

# Start timer
start=$(date +%s)

#define source paths:
GAN="hendrix:~/GAN/checkpoints/*"
PALETTE="hendrix:~/PALETTE/experiments/*"

#define target path (results folder):
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

#scripts are stored in.....
SCRIPTS="$TARGET_DIR/scripts"

CHECKPOINTS="$TARGET_DIR/Checkponts"


# Get checkpoint images and logs
rsync -zarv --include="*/" --include="*.log" --include="*.png" --exclude="*" $PALETTE "$TARGET_DIR/Checkpoints/PALETTE"
rsync -zarv --include="*/" --include="*.txt" --include="*.html" --include="*.png" --exclude="*" $GAN "$TARGET_DIR/Checkpoints/GAN"


# plot and draw images
python3 $SCRIPTS/gan_plot_losses.py $TARGET_DIR &
python3 $SCRIPTS/gan_images.py $TARGET_DIR &

python3 $SCRIPTS/palette_plot_losses.py $TARGET_DIR &
python3 $SCRIPTS/palette_images.py $TARGET_DIR &

wait

# End time
end=$(date +%s)
execution_time=$((end - start))

echo "Finished processing output. Execution Time: $execution_time seconds"
echo ""