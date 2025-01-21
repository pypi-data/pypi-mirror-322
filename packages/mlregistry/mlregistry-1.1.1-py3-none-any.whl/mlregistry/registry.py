from datetime import datetime
from inspect import getfullargspec
from typing import Optional
from typing import Any
from json import dumps
from logging import getLogger
from hashlib import md5
from dataclasses import dataclass
from copy import deepcopy

def type_signature(type: type, excluded_positions: list[int], excluded_parameters: set[str]) -> dict[str, str]:
    init = type.__init__
    argspec = getfullargspec(init)
    annotations = {key: (value.__name__ if value is not None else Any.__name__) for key, value in argspec.annotations.items()}
    args = [arg for index, arg in enumerate(argspec.args) if index not in excluded_positions]
    signature = {key: annotations.get(key, Any.__name__) for key in args if key not in excluded_parameters}
    return deepcopy(signature)

def object_parameters(args: list[Any], kwargs: dict[str, Any], signature: dict[str, str]):
    args_dict = { key: value for value, key in zip(args, signature.keys()) }
    kwargs_dict = { key: value for key, value in kwargs.items() if key in signature.keys() }
    return deepcopy(args_dict | kwargs_dict)

def object_hashing(object: object, args: list[Any], kwargs: list[str, Any], excluded_positions: list[int], excluded_parameters: set[str]) -> str:
    name = object.__class__.__name__
    parameters = object_parameters(args, kwargs, type_signature(object, excluded_positions, excluded_parameters))
    return md5((name + dumps(parameters, sort_keys=True)).encode()).hexdigest()

@dataclass
class Metadata:
    '''
    Metadata class to store the metadata of an object. It contains the type, hash, name, and arguments of the object.
    This is useful for tracking the initialization of objects wihtout having to modify them.

    Attributes:
        type (str): the type of the object (should be the same as T, but python does not support this yet)
        hash (str): the hash of the object
        name (str): the name of the object
        arguments (dict[str, Any]): the arguments that were passed to the object during initialization
    '''
    type: str
    hash: str
    name: str
    arguments: dict[str, Any]

class Registry[T]:
    """
    Register a type in the registry with metadata factory injected in the __init__ method. When an object that is
    registered is created, a metadata object is created and attached to the object and is accessible using the functions
    `getmetadata`, `getsignature`, and `gethash`.

    After registering a type, the objects of that type can be recreated from the registry using the `get` method.

    Methods:
        register:
            Register a type in a given category. This method injects metadata in the __init__ method of the type.

        get: 
            Get a registered type by name

        keys:
            Get the list of registered type names

        signature:
            Get the signature of a registered type by name

    Example:

        .. code-block:: python        

        from mlregistry import Registry

        registry = Registry()

        class Person:
            def __init__(self, name: str, age: int):
                self.person_name = name
                self.person_age = age
        
        registry.register(Person, 'People')

        person = Person('John', 30)

        metadata = getmetadata(person)
        print(metadata) # Metadata(type='People', hash='h72kasd..as2', name='Person', arguments={'name': 'John', 'age': 30})
    """
    def __init__(self, excluded_positions: list[int] = None, exclude_parameters: set[str] = None):

        """
        Initialize the registry with a dictionary of registered types, their states, excluded positions, and excluded parameters.
        The excluded positions are the positions are the positions to exclude in the signature of the registered types and the
        excluded parameters are the parameters to exclude in the signature of the registered types. Make sure to handle both cases
        when registering a type.
        
        Args:
            types (dict[str, Tuple[type, dict[str, str]]): a dictionary of registered types with their signatures
            states (dict[str, Any]): a dictionary of the states of the registered types
            excluded_positions (list[int]): a list of excluded positions in the signature of the registered types.
            excluded_parameters (set[str]): a set of excluded parameters in the signature of the registered types.

        Example:

        .. code-block:: python

            from mlregistry import Registry

            optimizers = Registry(excluded_positions=[0], exclude_parameters={'params'})
        """
        self.types = dict()
        self.states = dict()
        self.excluded_positions = excluded_positions or []
        self.excluded_parameters = ( exclude_parameters or set() ) | {'self', 'return'}

    def register(self, type: type, category: str = None) -> type:
        '''
        Register a type in a given category. This method injects metadata in the __init__ method of the type.

        
        Parameters:
            type (type): the type to be registered
            category (str): the category of the type, should be the same as T, but python does not support this yet

        Returns:
            type: the registered type with metadata factory injected in the __init__ method.
        '''

        signature = type_signature(type, self.excluded_positions, self.excluded_parameters)
        self.types[type.__name__] = (type, signature)
        init = type.__init__
        def wrapper(obj, *args, **kwargs):
            init(obj, *args, **kwargs)
            parameters = object_parameters(args, kwargs, signature)
            hash = object_hashing(obj, args, kwargs, self.excluded_positions, self.excluded_parameters)

            setattr(obj, '__model__metadata__',
                Metadata(
                    type=category or 'object',
                    hash=hash,
                    name=type.__name__,
                    arguments=parameters
                )
            )
            setattr(obj, '__model__signature__', signature)

        type.__init__ = wrapper
        return type    

    def get(self, name: str) -> Optional[type[T]]:
        '''
        Get a registered type by name

        Parameters:
            name (str): the name of the type to be retrieved

        Returns:
            type: the registered type
        '''
        pair = self.types.get(name)
        return pair[0] if pair is not None else None

    def keys(self) -> list[str]:
        '''
        Get the list of registered type names

        Returns:
            list[str]: the list of registered type names
        '''
        return list(self.types.keys())

    def signature(self, name: str) -> Optional[dict[str, str]]:
        '''
        Get the signature of a registered type by name

        Parameters:
            name (str): the name of the type to be retrieved

        Returns:
            dict[str, str]: the signature of the registered type
        '''

        pair = self.types.get(name)
        return pair[1] if pair is not None else None
    
def getdatehash(datetime: datetime) -> str:
    '''
    Get the hash of a datetime object

    Parameters:
        datetime (datetime): the datetime object to get the hash from

    Returns:
        str: the hash of the datetime object   
    '''
    return md5(datetime.isoformat().encode()).hexdigest()


    
def getmetadata(object: object, raises: Optional[type[Exception]] = None) -> Optional[Metadata]:
    """
    Get the metadata of an object.

    Parameters:
        obj (object): The object to retrieve the metadata from.
        raises (Optional[Type[Exception]]): An exception to raise if the object does not have metadata.

    Returns:
        Optional[Metadata]: The metadata of the object if available, or None if no exception is raised.

    Raises:
        raises: If the object does not have metadata and `raises` is specified.
    """
    try:
        return getattr(object, '__model__metadata__')
    except AttributeError as error:
        if raises is not None:
            if isinstance(raises, type) and issubclass(raises, Exception):
                raise raises from error
            else:
                raise TypeError("`raises` must be an exception type.") from error
        return None
        

def getsignature(object: object, raises: Optional[type[Exception]] = None) -> dict[str, str]:
    '''
    Get the signature of an object. Return a dictionary with parameter names and annotations.

    Parameters:
        object (object): the object to get the signature from

    Returns:
        dict[str, str]: the signature of the object if available, or None if no exception is raised

    Raises:
        raises: If the object does not have a signature and `raises` is specified. 

    '''
    try:
        return getattr(object, '__model__signature__')
    except AttributeError as error:
        if raises is not None:
            if isinstance(raises, type) and issubclass(raises, Exception):
                raise raises from error
            else:
                raise TypeError("`raises` must be an exception type.") from error
        return None

def gethash(object: object, raises: Optional[type[Exception]] = None) -> str:
    '''
    Get the local identifier of an object

    Parameters:
        object (object): the object to get the hash from

    Returns:
        str: the hash of the object if available, or None if no exception is raised
        
    Raises:
        raises: If the object does not have a hash and `raises` is specified
    '''
    metadata = getmetadata(object, raises)
    return metadata.hash if metadata is not None else None