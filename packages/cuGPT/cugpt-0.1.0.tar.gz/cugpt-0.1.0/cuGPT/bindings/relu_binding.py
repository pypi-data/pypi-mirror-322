# import ..kernels import relu_cuda

# cuGPT/bindings/relu.py

import torch
from ..kernels import relu_ext  # Import the compiled CUDA extension
from typing import Optional

def relu_fp32(input_tensor: torch.Tensor) -> torch.Tensor:
    """
    Apply ReLU using the fp32 kernel.
    
    Args:
        input_tensor (torch.Tensor): Input tensor of type float32.
        
    Returns:
        torch.Tensor: Output tensor after applying ReLU.
    """
    if not input_tensor.is_cuda:
        raise ValueError("Input tensor must be on CUDA device.")
    if input_tensor.dtype != torch.float32:
        raise TypeError("Input tensor must be of type float32.")
    
    return relu_ext.relu_fp32_launcher(input_tensor)

def relu_fp32x4(input_tensor: torch.Tensor) -> torch.Tensor:
    """
    Apply ReLU using the fp32x4 kernel.
    
    Args:
        input_tensor (torch.Tensor): Input tensor of type float32.
        
    Returns:
        torch.Tensor: Output tensor after applying ReLU.
    """
    if not input_tensor.is_cuda:
        raise ValueError("Input tensor must be on CUDA device.")
    if input_tensor.dtype != torch.float32:
        raise TypeError("Input tensor must be of type float32.")
    
    return relu_ext.relu_fp32x4_launcher(input_tensor)

def relu_fp16(input_tensor: torch.Tensor) -> torch.Tensor:
    """
    Apply ReLU using the fp16 kernel.
    
    Args:
        input_tensor (torch.Tensor): Input tensor of type float16.
        
    Returns:
        torch.Tensor: Output tensor after applying ReLU.
    """
    if not input_tensor.is_cuda:
        raise ValueError("Input tensor must be on CUDA device.")
    if input_tensor.dtype != torch.float16:
        raise TypeError("Input tensor must be of type float16.")
    
    return relu_ext.relu_fp16_launcher(input_tensor)

def relu_fp16x2(input_tensor: torch.Tensor) -> torch.Tensor:
    """
    Apply ReLU using the fp16x2 kernel.
    
    Args:
        input_tensor (torch.Tensor): Input tensor of type float16.
        
    Returns:
        torch.Tensor: Output tensor after applying ReLU.
    """
    if not input_tensor.is_cuda:
        raise ValueError("Input tensor must be on CUDA device.")
    if input_tensor.dtype != torch.float16:
        raise TypeError("Input tensor must be of type float16.")
    
    return relu_ext.relu_fp16x2_launcher(input_tensor)

def relu_fp16x2o(input_tensor: torch.Tensor) -> torch.Tensor:
    """
    Apply ReLU using the fp16x2o kernel.
    
    Args:
        input_tensor (torch.Tensor): Input tensor of type float16.
        
    Returns:
        torch.Tensor: Output tensor after applying ReLU.
    """
    if not input_tensor.is_cuda:
        raise ValueError("Input tensor must be on CUDA device.")
    if input_tensor.dtype != torch.float16:
        raise TypeError("Input tensor must be of type float16.")
    
    return relu_ext.relu_fp16x2o_launcher(input_tensor)

def relu_fp16x8(input_tensor: torch.Tensor) -> torch.Tensor:
    """
    Apply ReLU using the fp16x8 kernel.
    
    Args:
        input_tensor (torch.Tensor): Input tensor of type float16.
        
    Returns:
        torch.Tensor: Output tensor after applying ReLU.
    """
    if not input_tensor.is_cuda:
        raise ValueError("Input tensor must be on CUDA device.")
    if input_tensor.dtype != torch.float16:
        raise TypeError("Input tensor must be of type float16.")
    
    return relu_ext.relu_fp16x8_launcher(input_tensor)


# Optional: Expose all functions in __all__
__all__ = [
    'relu_fp32',
    'relu_fp32x4',
    'relu_fp16',
    'relu_fp16x2',
    'relu_fp16x2o',
    'relu_fp16x8',
]