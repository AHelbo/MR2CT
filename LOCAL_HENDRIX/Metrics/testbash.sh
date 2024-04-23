epoch="10"
FID=("FID: 10.000000" | awk '{print $2}')
echo "EPOCH $epoch FID $FID" >> "$output_file"