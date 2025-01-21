from enum import Enum

class ReleaseTypeEnum(str, Enum):
    base = 'base'
    alpha = 'alpha'
    beta = 'beta'
    rc = 'rc'
    post = 'post'
    dev = 'dev'

