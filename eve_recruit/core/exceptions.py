class ProfileNotLoaded(Exception):
    def __init__(self):
        super().__init__('Cant load profile')


class ProfileCreationError(Exception):
    def __init__(self):
        super().__init__('Cant create profile')
