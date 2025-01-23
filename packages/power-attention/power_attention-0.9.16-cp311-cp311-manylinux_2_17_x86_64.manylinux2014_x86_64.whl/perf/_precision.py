import torch
from typing import Any, Dict, Literal
from torch.utils._pytree import tree_map

def compare_tensors(ref: torch.Tensor, test: torch.Tensor, relative: bool = False) -> float:
    """Calculate maximum absolute difference between two tensors."""
    if ref.numel() == 0 and test.numel() == 0:
        return 0.
    if relative:
        diffs = (ref - test).abs() / (ref.abs() + 1e-8)
    else:
        diffs = (ref - test).abs()
    return diffs.max().item()
    
def compare_numbers(a: float, b: float, relative: bool = False) -> float:
    """Calculate maximum absolute or relative difference between two numbers."""
    if relative:
        return abs(a - b) / (abs(b) + 1e-8)
    else:
        return abs(a - b)

def compare(a: Any, b: Any, relative: bool = False) -> float:
    """Calculate maximum absolute or relative difference between tensors or pairs of tensors."""
    if isinstance(a, torch.Tensor) and isinstance(b, torch.Tensor):
        return compare_tensors(a, b, relative)
    elif a is None and b is None:
        return 0.
    elif isinstance(a, (float, int, bool)) and isinstance(b, (float, int, bool)):
        return compare_numbers(a, b, relative)
    elif isinstance(a, dict) and isinstance(b, dict):
        if a.keys() != b.keys():
            raise ValueError(f"Dict keys don't match: {a.keys()} vs {b.keys()}")
        return max([compare(a[k], b[k], relative) for k in a.keys()])

    try:
        return max([compare(_a, _b, relative) for _a, _b in zip(a, b, strict=True)])
    except TypeError as e:
        if "zip" not in str(e):
            raise
        raise TypeError(f"Inputs must both be tensors, dicts, or iterables of tensors. Got types: {type(a)} and {type(b)}")

def measure_forward_precision(ref_fn: callable, fn: callable, ref_inputs: Dict[str, torch.Tensor], test_inputs: Dict[str, torch.Tensor]) -> float:
    """Measure precision difference between reference and test implementations on forward pass.
    
    Args:
        fn: Function to test
        ref_inputs: Reference inputs (typically fp32)
        test_inputs: Test inputs (typically lower precision)
    
    Returns:
        float: Maximum absolute difference between reference and test outputs
    """
    with torch.no_grad():
        ref_output = ref_fn(**ref_inputs)
        test_output = fn(**test_inputs)
    return compare(ref_output, test_output)

def measure_backward_precision(ref_fn: callable, fn: callable, ref_inputs: Dict[str, torch.Tensor], test_inputs: Dict[str, torch.Tensor]) -> float:
    """Measure precision difference between reference and test implementations on backward pass.
    
    Args:
        ref_fn: Reference function
        fn: Function to test
        ref_inputs: Reference inputs (typically fp32)
        test_inputs: Test inputs (typically lower precision)
    
    Returns:
        float: Maximum absolute difference between reference and test gradients
    """
    # Forward pass
    ref_output = ref_fn(**ref_inputs)
    test_output = fn(**test_inputs)
    
    # Backward pass with same gradient
    grad = torch.ones_like(ref_output)
    ref_output.backward(grad)
    test_output.backward(grad.to(test_output.dtype))
    
    # Collect gradients into dictionaries
    ref_grads = {
        k: ref_inputs[k].grad 
        for k in ref_inputs.keys() 
        if isinstance(ref_inputs[k], torch.Tensor) and ref_inputs[k].requires_grad
    }
    test_grads = {
        k: test_inputs[k].grad
        for k in test_inputs.keys()
        if isinstance(test_inputs[k], torch.Tensor) and test_inputs[k].requires_grad
    }
    
    return tree_map(compare, ref_grads, test_grads)


def benchmark_precision(direction : Literal['fwd', 'bwd'], ref_fn : callable, fn : callable, create_inputs : callable, ref_create_inputs_kwargs : Dict[str, Any], test_create_inputs_kwargs : Dict[str, Any]) -> float:
    # Create reference inputs - always fp32, no chunking
    ref_inputs = create_inputs(**ref_create_inputs_kwargs, requires_grad=True)
    # Create test inputs with specified parameters
    test_inputs = create_inputs(**test_create_inputs_kwargs, requires_grad=True)
    
    # Measure forward and backward precision
    if direction == 'fwd':
        return measure_forward_precision(ref_fn, fn, ref_inputs, test_inputs)
    elif direction == 'bwd':
        return measure_backward_precision(ref_fn, fn, ref_inputs, test_inputs)
