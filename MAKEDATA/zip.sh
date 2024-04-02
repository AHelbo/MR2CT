input_channels="1"

MAKEDATA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

TARGET_DIR="$MAKEDATA_DIR/mr2ct_pic2pix_nc$input_channels"

zip -r "$TARGET_DIR/mr2ct_pix2pix_nc$input_channels.zip" "mr2ct_pic2pix_nc$input_channels" > /dev/null 2>&1