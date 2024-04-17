#!/bin/bash

# Start timer
start=$(date +%s)

#define source paths:
GAN="hendrix:~/GAN/checkpoints/*"

#define target path (results folder):
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

#scripts are stored in.....
SCRIPTS="$TARGET_DIR/scripts"

# python3 $SCRIPTS/clear_outdated_files.py $TARGET_DIR
# echo ""

## scp -r hendrix:~/pix2pix_cycleGan/checkpoints/* /Users/andershelbo/Desktop/hendrix-folder/output/p2p_cyc
## rsync -av --ignore-existing hendrix:~/pix2pix_cycleGan/checkpoints/* /Users/andershelbo/Desktop/hendrix-folder/output/p2p_cyc
## rsync -zarv --include="*/" --include="*.txt" --include="*.html" --include="*.png" --exclude="*" --files-from=$P2P_CYCLEGAN --files-from=$WEAK_P2P "$TARGET_DIR/"

# THIS
#rsync -zarv --include="*/" --include="*.txt" --include="*.html" --include="*.png" --exclude="*" $GAN "$TARGET_DIR/Checkpoints/GAN"

#sleep 3

python3 'C:\Users\Emily Honey\MRI2CT\LOCAL_HENDRIX\Results\Scripts\plot_losses.py' 'C:\Users\Emily Honey\MRI2CT\LOCAL_HENDRIX\Results'

python3 'C:\Users\Emily Honey\MRI2CT\LOCAL_HENDRIX\Results\Scripts\html2png.py' 'C:\Users\Emily Honey\MRI2CT\LOCAL_HENDRIX\Results'


# End time
end=$(date +%s)
execution_time=$((end - start))

echo "Finished processing output. Execution Time: $execution_time seconds"
echo ""