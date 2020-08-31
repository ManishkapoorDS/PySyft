# DOs and Don's of this class:
# - Do NOT use absolute syft imports (i.e. import syft.core...) Use relative ones.
# - Do NOT put multiple imports on the same line (i.e. from <x> import a, b, c). Use separate lines
# - Do sort imports by length
# - Do group imports by where they come from

# external class imports
from typing import List
from typing import Type
from typing import Optional
from nacl.signing import VerifyKey
from typing_extensions import final
from google.protobuf.reflection import GeneratedProtocolMessageType

# syft class imports
from .....proto.core.node.common.service.repr_service_pb2 import (
    ReprMessage as ReprMessage_PB,
)
from ....common.message import ImmediateSyftMessageWithoutReply
from .....decorators.syft_decorator_impl import syft_decorator
from .node_service import ImmediateNodeServiceWithoutReply
from ....common.serde.deserialize import _deserialize
from ...abstract.node import AbstractNode
from ....io.address import Address
from ....common.uid import UID
from .auth import service_auth


@final
class ReprMessage(ImmediateSyftMessageWithoutReply):
    def __init__(self, address: Address, msg_id: Optional[UID] = None):
        super().__init__(address=address, msg_id=msg_id)

    @syft_decorator(typechecking=True)
    def _object2proto(self) -> ReprMessage_PB:
        """Returns a protobuf serialization of self.

        As a requirement of all objects which inherit from Serializable,
        this method transforms the current object into the corresponding
        Protobuf object so that it can be further serialized.

        :return: returns a protobuf object
        :rtype: ReprMessage_PB

        .. note::
            This method is purely an internal method. Please use object.serialize() or one of
            the other public serialization methods if you wish to serialize an
            object.
        """

        return ReprMessage_PB(
            msg_id=self.id.serialize(), address=self.address.serialize(),
        )

    @staticmethod
    def _proto2object(proto: ReprMessage_PB) -> "ReprMessage":
        """Creates a ReprMessage from a protobuf

        As a requirement of all objects which inherit from Serializable,
        this method transforms a protobuf object into an instance of this class.

        :return: returns an instance of ReprMessage
        :rtype: ReprMessage

        .. note::
            This method is purely an internal method. Please use syft.deserialize()
            if you wish to deserialize an object.
        """

        return ReprMessage(
            msg_id=_deserialize(blob=proto.msg_id),
            address=_deserialize(blob=proto.address),
        )

    @staticmethod
    def get_protobuf_schema() -> GeneratedProtocolMessageType:
        """Return the type of protobuf object which stores a class of this type

        As a part of serialization and deserialization, we need the ability to
        lookup the protobuf object type directly from the object type. This
        static method allows us to do this.

        Importantly, this method is also used to create the reverse lookup ability within
        the metaclass of Serializable. In the metaclass, it calls this method and then
        it takes whatever type is returned from this method and adds an attribute to it
        with the type of this class attached to it. See the MetaSerializable class for details.

        :return: the type of protobuf object which corresponds to this class.
        :rtype: GeneratedProtocolMessageType

        """

        return ReprMessage_PB


class ReprService(ImmediateNodeServiceWithoutReply):
    @staticmethod
    @service_auth(root_only=True)
    def process(node: AbstractNode, msg: ReprMessage, verify_key: VerifyKey) -> None:
        print(node.__repr__())

    @staticmethod
    def message_handler_types() -> List[Type[ReprMessage]]:
        return [ReprMessage]
