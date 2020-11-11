# projects


class ProjectTitleDuplicateException(Exception):

    """Exception raised when project with the same title already exists."""


class ProjectDoesNotExistsException(Exception):

    """Exception raised when project does not exists."""


# sprints


class SprintTitleDuplicateException(Exception):

    """Exception raised when sprint with the same title already exists."""


class SprintDoesNotExistsException(Exception):

    """Exception raised when sprint does not exists."""


# users


class UserDoesNotExistsException(Exception):

    """Exception raised when user does not exists."""


# tasks


class TaskTitleDuplicateException(Exception):

    """Exception raised when task with the same title already exists."""


class TaskDoesNotExistsException(Exception):

    """Exception raised when task does not exists."""


