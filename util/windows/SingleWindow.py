from tkinter import *


def generate_window_function(func):
    """Decorator for new windows. Includes forced single existence and correct closing.

    The decorated function needs to accept two arguments, order-sensitive:
        - The window in which everything will exist
        - The function that closes the window in which it will exist


    Examples
    --------
    >>> root = Tk()
        @generate_window_function
        def test(new_window, close_window):
            ...
        open_new_window = test(root)
        open_new_window()

    :param func: The to-be-decorated function
    :return: Another decorator. Please pass the window from which the decorated function should be called
                                when using the decorated function. The function to open the new window will be returned.
    """

    def generate_new_window(root):
        """Decorator for new windows. Includes forced single existence and correct closing.

        :param root: Window from which sub-window should be spawned.
        :return: Function to be called when the new window should be opened.
        """

        NEW_ENTRY_WINDOW_OPEN = False

        def new_entry(event):
            nonlocal NEW_ENTRY_WINDOW_OPEN
            if NEW_ENTRY_WINDOW_OPEN:
                return

            NEW_ENTRY_WINDOW_OPEN = True
            entry_window = Toplevel(root)

            def close_window():
                nonlocal NEW_ENTRY_WINDOW_OPEN
                NEW_ENTRY_WINDOW_OPEN = False

                entry_window.destroy()

            entry_window.protocol("WM_DELETE_WINDOW", close_window)

            func(entry_window, close_window)

        return new_entry
    return generate_new_window
