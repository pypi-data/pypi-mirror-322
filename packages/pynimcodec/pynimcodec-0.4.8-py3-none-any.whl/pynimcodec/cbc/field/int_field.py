"""Signed integer field class and methods."""

from pynimcodec.bitman import BitArray, append_bits_to_buffer, extract_from_buffer
from pynimcodec.utils import snake_case

from ..constants import FieldType
from .base_field import Field
from .calc import calc_decode, calc_encode

FIELD_TYPE = FieldType.INT


class IntField(Field):
    """A signed integer field.
    
    Attributes:
        name (str): The unique field name.
        type (FieldType): The field type.
        description (str): Optional description for the field.
        optional (bool): Flag indicates if the field is optional in the message.
        size (int): The size of the encoded field in bits.
        encalc (str): Optional pre-encoding math expression to apply to value.
        decalc (str): Optional post-decoding math expression to apply to value.
        clip (bool): Allows encoding of values to clip to the limit of `size`.
    """
    
    def __init__(self, name: str, **kwargs) -> None:
        kwargs['type'] = FIELD_TYPE
        self._add_kwargs(['size'], ['encalc', 'decalc', 'clip'])
        super().__init__(name, **kwargs)
        self._size = 0
        self.size = kwargs.get('size')
        self._encalc: 'str|None' = None
        self.encalc = kwargs.get('encalc')
        self._decalc: 'str|None' = ''
        self.decalc = kwargs.get('decalc')
        self._clip: bool = False
        self.clip = kwargs.get('clip', False)
    
    @property
    def size(self) -> int:
        return self._size
    
    @size.setter
    def size(self, value: int):
        if not isinstance(value, int) or value < 1:
            raise ValueError('Invalid size must be greater than 0.')
        self._size = value
    
    @property
    def encalc(self) -> 'str|None':
        return self._encalc
    
    @encalc.setter
    def encalc(self, expr: 'str|None'):
        if expr is None or expr == '':
            self._encalc = None
        else:
            try:
                calc_encode(expr, -1)
                self._encalc = expr
            except TypeError as exc:
                raise ValueError('Invalid expression.') from exc
    
    @property
    def decalc(self) -> 'str|None':
        return self._decalc
    
    @decalc.setter
    def decalc(self, expr: 'str|None'):
        if expr is None or expr == '':
            self._decalc = None
        else:
            try:
                calc_decode(expr, -1)
                self._decalc = expr
            except TypeError as exc:
                raise ValueError('Invalid expression.') from exc
    
    @property
    def _max_value(self) -> int:
        return int(2**self.size / 2) - 1
    
    @property
    def _min_value(self) -> int:
        return -int(2**self.size / 2)
    
    @property
    def clip(self) -> bool:
        return self._clip
    
    @clip.setter
    def clip(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError('Invalid clip boolean')
        self._clip = value
    
    def decode(self, buffer: bytes, offset: int) -> 'tuple[int|float, int]':
        """Extracts the signed integer value from a buffer."""
        return decode(self, buffer, offset)
    
    def encode(self,
               value: 'int|float',
               buffer: bytearray,
               offset: int,
               ) -> tuple[bytearray, int]:
        "Appends the signed integer value to the buffer at the bit offset."
        return encode(self, value, buffer, offset)


def create(**kwargs) -> IntField:
    """Create an IntField."""
    return IntField(**{snake_case(k): v for k, v in kwargs.items()})


def decode(field: Field, buffer: bytes, offset: int) -> 'tuple[int|float, int]':
    """Decode a signed integer field value from a buffer at a bit offset.
    
    If the field has `decalc` attribute populated it will apply the math
    expression.
    
    Args:
        field (Field): The field definition, with `size` attribute.
        buffer (bytes): The encoded buffer to extract from.
        offset (int): The bit offset to extract from.
    
    Returns:
        tuple(int|float, int): The decoded value and the offset of the next
            field in the buffer.
    
    Raises:
        ValueError: If field is invalid.
    """
    if not isinstance(field, IntField):
        raise ValueError('Invalid IntField definition.')
    value = extract_from_buffer(buffer, offset, field.size, signed=True)
    if field.decalc:
        value = calc_decode(field.decalc, value)
    return ( value, offset + field.size )


def encode(field: IntField,
           value: 'int|float',
           buffer: bytearray,
           offset: int,
           ) -> 'tuple[bytearray, int]':
    """Append a signed integer field value to a buffer at a bit offset.
    
    Args:
        field (IntField): The field definition.
        value (int|float): The value to encode. Floats are only allowed if
            'encalc' specifies an integer conversion.
        buffer (bytearray): The buffer to modify/append to.
        offset (int): The bit offset to append from.
    
    Returns:
        tuple(bytearray, int): The modified buffer and the offset of the next
            field.
    
    Raises:
        ValueError: If the field or value is invalid for the field definition.
    """
    if not isinstance(field, IntField):
        raise ValueError('Invalid IntField definition.')
    if (not isinstance(value, int) and
        not (isinstance(value, float) and field.encalc)):
        raise ValueError(f'Invalid {field.name} value.')
    if field.encalc:
        value = calc_encode(field.encalc, value)
    elif not isinstance(value, int):
        raise ValueError(f'Invalid {field.name} value.')
    if (value < field._min_value or value > field._max_value) and not field.clip:
        raise ValueError(f'{field.name} value exceeds size {field.size} bits.')
    if value < field._min_value:
        value = field._min_value
    elif value > field._max_value:
        value = field._max_value
    bits = BitArray.from_int(value, field.size)
    return ( append_bits_to_buffer(bits, buffer, offset), offset + field.size )
