from src.utils import print_hierarchical
from src.get_logs import *
from src.process_logs import *
from src.plot_dicts import *

def main():
    print_hierarchical("Processing train/validation metrics:")

    print_hierarchical("Getting GAN loss logs:")
    gan_logs = get_gan_logs()

    # dict from log
    print_hierarchical("Converting GAN losses to dictionary")
    gan_dicts = process_gan_logs(gan_logs)

    # plot from dict
    print_hierarchical("Plotting from dicts:")
    plot_gan_dicts(gan_dicts)
    return
    # diff 0
    print_hierarchical("Getting diffusion loss logs:")
    diffusion_logs = get_diffusion_logs()

    # dict from log
    print_hierarchical("Converting GAN losses to dictionary")
    process_diffusion_logs(diffusion_logs)

    # plot from dict



if __name__ == "__main__":
    main()