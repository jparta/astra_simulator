def rmtree_error_handler_disregard_file_not_found(func, path, exc_info):
    """
    Error handler for shutil.rmtree
    Do nothing if the error is a FileNotFoundError.
    Otherwise, re-raise the error.
    """
    error_type, error_object, error_traceback = exc_info
    if isinstance(error_object, FileNotFoundError):
        pass
    else:
        raise error_object
