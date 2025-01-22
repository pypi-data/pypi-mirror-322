"""Custom exceptions for SHARK."""


class DuplicateSequenceIdError(Exception):
    """Exception for cases when a duplicate sequence ID was identified."""

    def __init__(self, seq_id):
        self.seq_id = seq_id
        self.message = (
            f"Duplicate sequence ID: {seq_id}, detected! Please make sure that your input sequence set does not"
            f" contain any duplicated sequence IDs."
        )
        super(Exception, self).__init__(self.message)
