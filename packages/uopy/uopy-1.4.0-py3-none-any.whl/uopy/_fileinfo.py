# Copyright 2020 - 2023 Rocket Software, Inc. or its affiliates. All Rights Reserved.
#
"""
This class is used for the fileInfoEx method of File class.
Its fields, such as VOCNAME, are defined as the list index of the return value
split by the \xff character from the server. The index values are from 0 to 22.
The field LIST_COUNT is the total item count of the list. It is a fixed value.
"""


class FileInfoEx:
    IS_FILEVAR = 0
    VOCNAME = 1
    PATHNAME = 2
    TYPE = 3
    HASHALG = 4
    MODULUS = 5
    MINMODULUS = 6
    GROUPSIZE = 7
    LARGERECORDSIZE = 8
    MERGELOAD = 9
    SPLITLOAD = 10
    CURRENTLOAD = 11
    NODENAME = 12
    IS_AKFILE = 13
    CURRENTLINE = 14
    PARTNUM = 15
    STATUS = 16
    RECOVERYTYPE = 17
    RECOVERYID = 18
    IS_FIXED_MODULUS = 19
    NLSMAP = 20
    ENCRYPTION = 21  # In fact 22 in server side
    REPSTATUS = 22  # In fact 24 in server side
    LIST_COUNT = 23


class UDFileInfoEx:
    FINFO_IS_FILEVAR = 0
    FINFO_VOCNAME = 1
    FINFO_FULLNAME = 2
    FINFO_TYPE = 3
    FINFO_HASH_ALGORITHM = 4
    FINFO_MODULUS = 5
    FINFO_MIN_MODULUS = 6
    FINFO_GROUPSIZE = 7
    FINFO_LARGE_RECSIZE = 8
    FINFO_MERGE_FACTOR = 9
    FINFO_SPLIT_FACTOR = 10
    FINFO_CURRENT_LOAD = 11
    FINFO_NODE_NAME = 12
    FINFO_IS_ALTKEY_FILE = 13
    FINFO_CURRENT_LINE = 14
    FINFO_PART_NUM = 15
    FINFO_STATUS = 16
    FINFO_REL_NAME = 17
    FINFO_BLKSIZE = 18
    FINFO_PRIVILEGE = 19
    FINFO_WHICH_INDEX = 20
    FINFO_WHAT_XVALUE = 21
    FINFO_IS_RECOVERABLE = 22
    FINFO_IS_NUMERICAL = 23
    FINFO_IS_REPLICATED = 24
    FINFO_BEFORE_UPDATE_TRIGGER = 25
    FINFO_BEFORE_DELETE_TRIGGER = 26
    FINFO_IS_ENCRYPTED = 27
    FINFO_ENCINFO = 28
    FINFO_AFTER_UPDATE_TRIGGER = 29
    FINFO_AFTER_DELETE_TRIGGER = 30
    FINFO_IS64BIT = 31
    LIST_COUNT = 32
