import enum


class MQEventType(str, enum.Enum):
    create = "event.create"
