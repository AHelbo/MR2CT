#!/bin/bash

# Start timer
start=$(date +%s)

python3 clear_outdated_files.py "/Users/andershelbo/Desktop/hendrix-folder/output"
echo ""

# scp -r hendrix:~/pix2pix_cycleGan/checkpoints/* /Users/andershelbo/Desktop/hendrix-folder/output/p2p_cyc
# rsync -av --ignore-existing hendrix:~/pix2pix_cycleGan/checkpoints/* /Users/andershelbo/Desktop/hendrix-folder/output/p2p_cyc

rsync -zarv --include="*/" --include="*.txt" --include="*.html" --include="*.png" --exclude="*" "hendrix:~/pix2pix_cycleGan/checkpoints/*" "/Users/andershelbo/Desktop/hendrix-folder/output/p2p_cyc"

sleep 5

python3 plot_losses.py "/Users/andershelbo/Desktop/hendrix-folder/output"

python3 html2png.py "/Users/andershelbo/Desktop/hendrix-folder/output"


# End time
end=$(date +%s)
execution_time=$((end - start))

echo "Finished processing output. Execution Time: $execution_time seconds"
echo ""