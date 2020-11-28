import enum


class StatusEnum(enum.Enum):

    todo = 'todo'
    progress = 'progress'
    review = 'review'
    testing = 'testing'
    done = 'done'


class PriorityEnum(enum.Enum):

    lowest = 'lowest'
    low = 'low'
    medium = 'medium'
    high = 'high'
    highest = 'highest'


class RoleEnum(enum.Enum):

    admin = 'admin'
    user = 'user'
    product_owner = 'product owner'
