#!/bin/bash

# Define the source and destination directories
SOURCE_SERVER="hendrix"
GAN_SOURCE="~/GAN/checkpoints/"
DIFFUSION_SOURCE="~/diffusion/experiments/"
LOCAL_GAN_DEST="./GAN/checkpoints/"
LOCAL_DIFFUSION_DEST="./diffusion/experiments/"

# Define the rsync options
RSYNC_OPTIONS="-zarv --include='*/' --include='*.tiff' --include='*.log' --exclude='*'"

# Sync GAN checkpoints directory
rsync $RSYNC_OPTIONS -e ssh $SOURCE_SERVER:$GAN_SOURCE $LOCAL_GAN_DEST &

# Sync diffusion experiments directory
rsync $RSYNC_OPTIONS -e ssh $SOURCE_SERVER:$DIFFUSION_SOURCE $LOCAL_DIFFUSION_DEST &

# Wait for all background processes to complete
wait

echo "Sync complete."