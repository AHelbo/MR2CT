from src.utils import print_hierarchical
from src.get_logs import *
from src.process_logs import *
from src.plot_dicts import *

def main():
    print_hierarchical("Processing train/validation metrics:")

    # print_hierarchical("Getting GAN loss logs:")
    # gan_logs = get_gan_logs()

    # print_hierarchical("Converting GAN losses to dictionary")
    # gan_dicts = process_gan_logs(gan_logs)

    # print_hierarchical("Plotting from dicts:")
    #plot_gan_dicts(gan_dicts)
    
    print_hierarchical("Getting diffusion loss logs:")
    diffusion_logs = get_diffusion_logs()

    print_hierarchical("Converting diffusion losses to dictionary")
    diffusion_dicts=process_diffusion_logs(diffusion_logs)

    print_hierarchical("Plotting diffusion")
    plot_diffusion_dicts(diffusion_dicts)



if __name__ == "__main__":
    main()