# Get the current directory
current_dir=$(pwd)

# Output file
output_file="$current_dir/sbatch_output.txt"

# Get a list of all .sh files in the current directory
sh_files=$(find "$current_dir" -maxdepth 1 -type f -name "*.sh")

for file in $sh_files; do
    if [[ $file != "$current_dir/$0" ]]; then
        echo "Submitted $file to sbatch" >> "$output_file"
        sbatch "$file" >> "$output_file"
    fi
done

cat $output_file
