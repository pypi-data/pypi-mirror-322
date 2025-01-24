from typing import Any, Type, TypeVar, Union
from urllib.parse import ParseResult

from sardine import _sardine

from .utils import URLType

import numpy as np

T = TypeVar('T')

# A function that takes a numpy array
def url_of_numpy_ndarray(value: Any) -> str:
    """
    @brief Generates a URL for a numpy ndarray.

    @param value The numpy ndarray for which to generate a URL.
    @return The generated URL for the numpy ndarray.
    """
    # Get the memory view of the numpy array
    memory_view = memoryview(value)
    mapping = _sardine.DefaultMapping(value.shape, value.strides)
    # Generate a URL from the memory view
    url = _sardine.url_from_bytes(memory_view)
    return _sardine.update_url(url, mapping)

def numpy_ndarray_from_url(url: str) -> Any:
    """
    @brief Instantiates a numpy ndarray from a URL.

    @param url The URL to use for instantiation.
    @return A numpy ndarray instance.
    """
    # Retreive the memory package pointed by the URL
    pkg = _sardine.MemoryPackage(url, _sardine.DeviceType.CPU)
    # Get the mapping from the URL
    mapping = pkg.mapping
    # Create a numpy array from the memory package and the mapping
    memory_view = pkg.bytes

    # Extract properties from Mapping
    shape = tuple(mapping.extents)
    strides = tuple(mapping.strides)
    dtype = mapping.dtype  # Assuming dlpack_type_to_numpy already provides correct numpy dtype
    offset = mapping.offset
    itemsize = mapping.item_size

    # Validate the buffer size
    expected_size = np.prod(shape) * itemsize
    if memory_view.nbytes < expected_size + offset:
        raise ValueError("Memoryview size is smaller than expected for the given Mapping.")

    # Create the numpy array
    buffer = memory_view.obj  # Access the buffer object
    array = np.ndarray(
        shape=shape,
        strides=strides,
        dtype=dtype,
        buffer=buffer,
        offset=offset
    )
    return array

# Dictionary of supported types as (module, type_name): (from_url_function, url_of_function)
# Lambdas are used to access `_sardine` functions only when needed, to avoid accessing non compiled functions
_supported_types = {
    ('numpy', 'ndarray'): (numpy_ndarray_from_url, url_of_numpy_ndarray),
}

# # try import _sardinecuda and add it to supported types
# try:
#     from sardine import _sardinecuda
#     _supported_types[('cupy', 'ndarray')] = (_sardinecuda.cupy_ndarray_from_url, _sardinecuda.url_of_cupy_ndarray)
# except ImportError:
#     pass


def _check_supported_type(type):
    """
    @brief Checks if a type is supported by the module and raises an exception if not.

    @param type The type to check.
    @throws TypeError if the type is not supported.
    """
    # Get module and type name of the input type
    module_name = type.__module__
    type_name = type.__name__
    # Raise TypeError if the type is not supported
    if (module_name, type_name) not in _supported_types:
        raise TypeError(f"The type '{module_name}.{type_name}' is not supported.")

def _get_type_functions(type):
    """
    @brief Retrieves the URL handling functions for a given type.

    @param type The type for which to retrieve URL functions.
    @return A tuple containing (from_url_function, url_of_function).
    @throws KeyError if the type is not supported.
    """
    # Extract module and type name of the requested type
    module_name = type.__module__
    type_name = type.__name__
    # Retrieve the corresponding functions from the dictionary
    return _supported_types[(module_name, type_name)]

def from_url(requested_type : Type[T], url : URLType) -> T:
    """
    @brief Instantiates an object of a given type from a URL.

    @param requested_type The type to instantiate.
    @param url The URL to use for instantiation.
    @return An instance of the requested type.
    @throws TypeError if the requested type is not supported by the module.
    """
    if hasattr(requested_type, '__from_url__'):
        return requested_type.__from_url__(url)

    # Check if the type has a custom __from_url__ method
    if hasattr(requested_type, 'SardineMapper'):
        requested_dt = requested_type.SardineMapper.requested_device_type

        pkg = _sardine.MemoryPackage(url, requested_dt)
        requested_type.SardineMapper.check(pkg.mapping)
        mapper = requested_type.SardineMapper(pkg.mapping, url)
        return mapper.from_memoryview(pkg.bytes)

    # Verify if the type is supported, raise otherwise
    _check_supported_type(requested_type)

    # Get the from_url function and use it to instantiate the object from the URL
    from_url_fn = _get_type_functions(requested_type)[0]

    return from_url_fn(url)


def url_of(value : Any) -> ParseResult:
    """
    @brief Generates a URL for a given value.

    @param value The value for which to generate a URL.
    @return The generated URL for the value.
    @throws TypeError if the type of the value is not supported by the module.
    """
    # Check if the value has a custom __url_of__ method
    if hasattr(value, '__url_of__'):
        return value.__url_of__()

    if hasattr(value, 'SardineMapper'):
        mapper = value.SardineMapper(value)
        mv = mapper.as_memoryview(value)
        url = _sardine.url_from_bytes(mv)
        return _sardine.update_url(url, mapper.mapping)

    # Determine the type of the value
    requested_type = type(value)

    # Verify if the type is supported, raise otherwise
    _check_supported_type(requested_type)

    # Get the url_of function and use it to generate a URL for the value
    url_of_fn = _get_type_functions(requested_type)[1]
    return url_of_fn(value)
