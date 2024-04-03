#!/bin/bash

# Start timer
start=$(date +%s)

#define source paths:
P2P_CYCLEGAN="hendrix:~/pix2pix_cycleGan/checkpoints/*"
WEAK_P2P="hendrix:~/pix2pix_weak_D/checkpoints/*"
#define target path (output folder):
TARGET_DIR="/Users/andershelbo/Desktop/MRI2CT/LOCAL_HENDRIX/output"

python3 clear_outdated_files.py $TARGET_DIR
echo ""

# scp -r hendrix:~/pix2pix_cycleGan/checkpoints/* /Users/andershelbo/Desktop/hendrix-folder/output/p2p_cyc
# rsync -av --ignore-existing hendrix:~/pix2pix_cycleGan/checkpoints/* /Users/andershelbo/Desktop/hendrix-folder/output/p2p_cyc

rsync -zarv --include="*/" --include="*.txt" --include="*.html" --include="*.png" --exclude="*" $P2P_CYCLEGAN "$TARGET_DIR/p2p_cyc"
rsync -zarv --include="*/" --include="*.txt" --include="*.html" --include="*.png" --exclude="*" $WEAK_P2P "$TARGET_DIR/p2p_weak"

# rsync -zarv --include="*/" --include="*.txt" --include="*.html" --include="*.png" --exclude="*" --files-from=$P2P_CYCLEGAN --files-from=$WEAK_P2P "$TARGET_DIR/"


sleep 3

python3 plot_losses.py $TARGET_DIR

python3 html2png.py $TARGET_DIR


# End time
end=$(date +%s)
execution_time=$((end - start))

echo "Finished processing output. Execution Time: $execution_time seconds"
echo ""