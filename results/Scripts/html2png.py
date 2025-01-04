import sys
import os
import glob
import subprocess

def find_files_by_extension(root_folder, extension):
    
    search_pattern = os.path.join(root_folder, f'**/*.{extension}')

    files = glob.glob(search_pattern, recursive=True)
    
    return files

def gen_pdf(root_folder, htmls):

    for elm in htmls:
        try:
            new_dir = elm[:-10]
            # FLYT UDKOMMENTERING WINDOWS/MAC STIER
            pdf_path = elm.split("/")[-3]
            # pdf_path = elm.split("\\")[-3]

            os.chdir(new_dir)

            images_per_epoch = 3 if (pdf_path.count("pix2pix") > 0) else 8

            image_height =  67 if (pdf_path.count("pix2pix") > 0) else 85

            rows = len(os.listdir(f"{new_dir}/images/")) / images_per_epoch

            width = 50 * images_per_epoch

            subprocess.run(f"wkhtmltopdf --enable-local-file-access --page-height {rows*image_height} --page-width {width} index.html {root_folder}/{pdf_path}.pdf", shell=True)
        except subprocess.CalledProcessError as e:
            return None
    

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: _____")

    else:

        print("Running html2png.py")

        root_folder = sys.argv[1]

        html_files = find_files_by_extension(os.path.join(root_folder,"Checkpoints"), "html")

        gen_pdf(root_folder, html_files)

