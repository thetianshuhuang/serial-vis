# settings_template.py
# generalized template for program settings

import copy


class settings_template:

    """
    Settings template class; reusable
    """

    #   --------------------------------
    #
    #   initialization
    #
    #   --------------------------------
    def __init__(self, **kwargs):

        """
        Initialize sv_settings object, and merge preliminary settings

        Parameters
        ----------
        kwargs : dict
            merged with object attributes (settings).
        """

        self.attr_merge(kwargs)

    #   --------------------------------
    #
    #   update
    #
    #   --------------------------------
    def update(self, settings):
        """
        Update settings.

        Parameters
        ----------
        settings : dict
            merged with object attributes
        """

        self.attr_merge(settings)

    #   --------------------------------
    #
    #   attr_merge
    #
    #   --------------------------------
    def attr_merge(self, settings):
        """
        Update attributes of obj with corresponding values in dict.

        Parameters
        ----------
        obj
            Object to be updated
        kwargs
            dictionary to update from
        """

        for key, value in settings.items():
            if(type(value) == dict):
                destination = copy.deepcopy(getattr(self, key))
                destination.update(value)
                setattr(self, key, destination)
            else:
                setattr(self, key, value)
