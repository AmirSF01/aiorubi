from enum import Enum

class UpdateEndpointStatusType(str, Enum):
    DONE = "Done"
    INVALID_URL = "InvalidUrl"