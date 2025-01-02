from skimage.metrics import structural_similarity

from skimage.metrics import peak_signal_noise_ratio

from skimage.metrics import mean_squared_error

def torch2imarr(tensor):
    # Check if CUDA is available and move tensor to CPU if necessary
    if tensor.is_cuda:
        tensor = tensor.cpu()
    
    array = tensor.detach().numpy().mean(axis=0, keepdims=True).squeeze(0).squeeze(0)
    
    # Normalize the array to range [0, 1] (cause tiff)
    imarr = (array - array.min()) / (array.max() - array.min())
    return imarr


def torch_ssim(A,B):
    A = torch2imarr(A)
    B = torch2imarr(B)

    d_range = max(A.max(),B.max())-min(A.min(),B.min())

    ssim = structural_similarity(A,B,data_range=d_range)

    return ssim

def torch_psnr(A,B):
    A = torch2imarr(A)
    B = torch2imarr(B)

    d_range = max(A.max(),B.max())-min(A.min(),B.min())

    return peak_signal_noise_ratio(A,B,data_range=d_range)


def torch_mse(A,B):
    A = torch2imarr(A)
    B = torch2imarr(B)

    return mean_squared_error(A,B)
