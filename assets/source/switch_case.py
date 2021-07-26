from types import FunctionType
from typing import Any, NoReturn


class Switcher:
    """
    class for switch and case
    """

    def __init__(self):
        self.value = ...
        self.default = True

    def switch(self, function):
        """
        wrapper for switch

        .. example-code::

         .. code-block:: python3
            # define
            s = Switcher()

            # some code

            @s.switch
            def my_switch(value):
                # code

         .. code-block:: python3
            # use
            with switch(value):
                if case(value_to_check):
                    # code to run when value == value_to_check
                if case():
                    # default

        Parameters
        ----------
        function: FunctionType
            function to run with value

        Returns
        -------
            Type[SwitchWrapper]

        """
        father_self = self

        class SwitchWrapper:
            def __init__(self, value):
                self.function = function
                self.father = father_self
                self.running = True
                self.__call__(value)

            def __call__(self, value):
                self.father.value = value
                self.function(value)

            def __enter__(self):
                if not self.running:
                    self.running = True
                return None

            def __exit__(self, exc_type, exc_val, exc_tb):
                if not self.running:
                    self.running = False
                    self.father.value = ...

            def end(self, quiet_mode: bool = True):
                if not self.running:
                    self.running = False
                    self.father.value = ...
                elif not quiet_mode:
                    raise OverflowError

        return SwitchWrapper

    def case(self, function: FunctionType):
        """
        wrapper for case

        .. example-code::

         .. code-block:: python3
            # definite
            s = Switcher()
            # some code

            # if you want to add another check you can use annotation
            @s.case
            def my_case(value) -> bool:
               check value
               return output



         .. code-block:: python3

            s = Switcher()
            # some code

            # or if you want to log you can do it in function, but without annotation with return
            @s.case
            def my_case(value):
               # without ' -> bool'!
               code

         .. code-block:: python3
            # use
            with switch(value):
                if case(value_to_check):
                    # code to run when value == value_to_check
                if case():
                    # default

        Parameters
        ----------
            function: FunctionType
                function to run when checking, and when it returns bool to check

        Raises
        ------
            ValueError
                 when you don't use switch

        Returns
        -------
            FunctionType
                wrapper
        """

        def check(value):
            if isinstance(self.value, type(...)):
                raise ValueError("First, you mast use switch")
            if isinstance(value, tuple):
                _return = []
                for val in value:
                    _return.append(self.value == val)
                _return = any(_return)
                self.default = not _return
                return _return
            else:
                if value is None:
                    return self.default
                else:
                    _return = self.value == value
                    self.default = not _return
                    return _return

        def func(*value):
            if len(value) == 0:
                value = None
            elif len(value) == 1:
                value = value[0]
            if "return" in function.__annotations__.keys() and function.__annotations__["return"] == bool:
                if function(value):
                    return check(value)
                else:
                    return False
            else:
                return check(value)

        return func


# default switch
s = Switcher()


@s.switch
def switch(_: Any) -> NoReturn:
    """
    default switch
    :param _: value for wrapper
    :type _: Any
    :return: Nothing
    :rtype: NoReturn
    """
    pass


@s.case
def case(_: Any) -> NoReturn:
    """
    default case
    :param _: value for wrapper
    :type _: Any
    :return: check value
    :rtype: bool
    """
    pass


__all__ = ["switch", "case", "Switcher"]

