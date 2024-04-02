#!/bin/bash

# Start timer
start=$(date +%s)


bash create_dataset.sh CUT 3 1
# bash create_dataset.sh cycleGan 1
# bash create_dataset.sh cycleGan 3


# End time
end=$(date +%s)
execution_time=$((end - start))

echo "Finished creating datasets. Execution Time: $execution_time seconds"