# For the GUI
from tkinter import ttk
from tkinter import StringVar, BOTTOM, BOTH, TOP

# For plotting
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# For the database
from back import Engine

from sqlalchemy import text
from sqlalchemy.orm import Session

# For the line types
from enum import Enum, auto

# Pixels as a unit
px = 1/plt.rcParams['figure.dpi']
matplotlib.use('TkAgg')


class LineType(Enum):
    BAR = auto()
    SCATTER = auto()
    LINE = auto()
    STACKED_BAR = auto()


# A dictionary that translates user-choices for an x-axis to SQL commands
XData = {
    "Date: daily": "_date",
    "Date: monthly": "strftime('%Y', DATE(_date)) || '-' || strftime('%m', DATE(_date))",
    "Date: yearly": "strftime('%Y', DATE(_date))"
}

# A dictionary that translates user-choices for a y-axis to SQL commands
YData = {
    "Price": "AVG(Product._price) / 100.0",
    "Frequency": "COUNT(Product.name)",
    "Bonus": "AVG(Product._bonus) / 100.0"
}


class PlotFrameFill:
    """A plot that uses a notebook to get its information and updates its view if its draw() method is called.
    The type of plot, number of subplots, axes, titles and more can be varied freely through the associated notebook.
    The plot updates its size dynamically if resized.
    """
    def __init__(self, master, size, notebook):
        """Creates a dynamic plot which relies on the information provided by a notebook.

        :param master: The frame in which this plot shall exist.
        :param size: The initial size, albeit it is automatically changed if needed.
        :param notebook: The associated notebook, has to be of class `InfoNotebook`
        """
        # Create a figure and holders for axes
        self.fig = Figure(figsize=(size[0]*px, size[1]*px), dpi=100)
        self.axs = []
        self.axs.append(self.fig.add_subplot(111))

        # Save the notebook and add self.draw as action performed if anything in the notebook is changed
        self.notebook = notebook
        self.notebook.add_trace(self.draw)

        # Add a canvas to draw upon and render it
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.draw()

        # Add a navigation toolbar and render it
        self.toolbar = NavigationToolbar2Tk(self.canvas, master, pack_toolbar=False)
        self.toolbar.update()

        # Show everything in the GUI
        self.toolbar.pack(side=BOTTOM)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

        # Draw the figure
        self.draw()

    @staticmethod
    def __convert(line_type, ax):
        """Converts line types/plot types into associated commands bound to a passed axis.

        :param line_type: The wanted line_type, should be from the associated Enum.
        :param ax: The ax which is wanted to be used for displaying.
        :return: The appropriate bound function of the axis.
        """
        if line_type == '':
            raise ValueError

        # Convert from string to Enum type
        converted_type = LineType[line_type]
        match converted_type:
            case LineType.BAR:
                return ax.bar

            case LineType.LINE:
                return ax.plot

            case LineType.SCATTER:
                return ax.scatter

            case _:
                raise ValueError("Please pass an appropriate type from the LineType class.")

    def get_data(self, product, x_type, y_type):
        """Converts a given product, x-axis and y-axis type to data from the database.

        :param product: The type of product to select for. Additionally, 'All' is accepted as option, which does not
        pre-select.
        :param x_type: How to group the data.
        :param y_type: Which metric to select from the database.
        :return:
        """
        x_data = []
        y_data = []

        x_data_sql = None
        y_data_sql = None
        product_sql = None

        # Convert x and y specifications to SQL commands using global dicts.
        try:
            x_data_sql = XData[x_type]
        except KeyError:
            # TODO: Append to error message window. In general, make error window and use globally.
            pass

        try:
            y_data_sql = YData[y_type]
        except KeyError:
            # TODO: Append to error message window. In general, make error window and use globally.
            pass

        # Get a list of products from database
        with Session(Engine) as session:
            product_names = session.execute(text("SELECT name FROM Product GROUP BY name ORDER BY name DESC"))

        product_names = list(set([str(prod_name[0]) for prod_name in product_names]))

        # Get product SQL if needed
        if product == 'All':
            product_sql = ''
        elif product in product_names:
            product_sql = f"WHERE Product.name LIKE '{product}'"
        else:
            # TODO: Show error window. In general, make error window and use globally.
            raise ValueError("Please correct a valid product category")

        # Create SQL statement and get data from database
        statement = f"SELECT {x_data_sql}, {y_data_sql} FROM Receipt INNER JOIN Product ON Receipt.id = Product.receipt_id {product_sql} GROUP BY {x_data_sql};"

        with Session(Engine) as session:
            results = session.execute(text(statement))

        # Append data and return
        for x, y in results:
            x_data.append(x)
            y_data.append(y)

        return x_data, y_data

    def draw(self, event=None):
        """Draws the canvas anew.

        :param event: Ignored.
        :return:
        """
        # If we need to change the number of plots
        if len(self.axs) != len(self.notebook.plot_pages):
            # Clear all axes to allow for good ax placement in the figure
            self.fig.clf()
            self.axs = []

            # Try to get the arrangement from the user. If illegal, use smallest square approach
            try:
                num_rows = int(self.notebook.gen_info.num_rows.get())
                num_cols = int(self.notebook.gen_info.num_cols.get())

                if num_cols * num_rows < len(self.notebook.plot_pages):
                    # User's specifications were wrong, so force other approach
                    raise ValueError

            except ValueError:
                max_len = 0
                while max_len**2 < len(self.notebook.plot_pages):
                    max_len += 1
                num_rows, num_cols = max_len, max_len

            # Create new axes for all axes wanted
            for idx in range(1, len(self.notebook.plot_pages) + 1):
                self.axs.append(self.fig.add_subplot(num_rows, num_cols, idx))

        else:
            for ax in self.axs:
                ax.clear()

        # For each plot
        for plot_idx, plot in enumerate(self.notebook.plot_pages):
            # Get the titles
            title = plot.title_var.get()
            x_title = plot.x_title_var.get()
            y_title = plot.y_title_var.get()

            show_legend = False

            # For each graph
            for graph_idx, graph in enumerate(self.notebook.graph_pages):
                # Default to showing in the first plot
                try:
                    graph_num = int(graph.plot_var.get())
                except ValueError:
                    graph_num = 1

                # We render only graphs associated with the current plot
                if graph_num != plot_idx + 1:
                    continue

                # Get the correct plot function as requested by the user
                line_type = graph.line_type.get()
                try:
                    plot_func = self.__convert(line_type, self.axs[plot_idx])
                except ValueError:
                    # Default to None if anything is wrong/unanticipated
                    plot_func = None

                # Do not render if anything went wrong
                if plot_func is not None:
                    plot_func(
                        *self.get_data(graph.choice_var.get(), graph.x_data_var.get(), graph.y_data_var.get()),
                        label=graph.title_var.get()
                    )

                    # Display legend if needed
                    if graph.title_var.get() != '':
                        show_legend = True

            # Set titles and legend appropriately
            self.axs[plot_idx].set_xlabel(x_title)
            self.axs[plot_idx].set_ylabel(y_title)

            self.axs[plot_idx].set_title(title)

            if show_legend:
                self.axs[plot_idx].legend()

        # Update the shown plot
        self.canvas.draw()


class InfoNotebook:
    def __init__(self, master):
        self.details_notebook = ttk.Notebook(master)
        self.details_notebook.grid(column=0, row=0, sticky="NWES")

        self.gen_info = GeneralPage(self.details_notebook)
        self.details_notebook.add(self.gen_info.general_frame, text="General")
        self.gen_info.add_button(self.add_plot, self.add_graph)

        self.plot_pages = [PlotPage(self.details_notebook)]
        for idx, plot in enumerate(self.plot_pages):
            self.details_notebook.add(plot.plot_frame, text=f"Plot {idx + 1}")

        self.graph_pages = [GraphPage(self.details_notebook)]
        for idx, page in enumerate(self.graph_pages):
            self.details_notebook.add(page.plot_frame, text=f"Graph {idx + 1}")

    def add_plot(self, event=None):
        self.plot_pages.append(PlotPage(self.details_notebook))
        self.plot_pages[-1].add_trace(self.draw)
        self.details_notebook.insert(PlotPage.count, self.plot_pages[-1].plot_frame,
                                     text=f"Plot {PlotPage.count}")

        for page in self.graph_pages:
            page.change_plot_num(PlotPage.count)

        self.draw()

    def add_graph(self, event=None):
        self.graph_pages.append(GraphPage(self.details_notebook))
        self.graph_pages[-1].change_plot_num(PlotPage.count)
        self.graph_pages[-1].add_trace(self.draw)
        self.details_notebook.add(self.graph_pages[-1].plot_frame, text=f"Graph {GraphPage.count}")

        self.draw()

    def add_trace(self, draw):
        self.draw = lambda *x: draw()

        for page in self.plot_pages:
            page.add_trace(self.draw)

        for page in self.graph_pages:
            page.add_trace(self.draw)


class GeneralPage:
    def __init__(self, master):
        self.general_frame = ttk.Frame(master)
        self.general_frame.grid(column=0, row=0, sticky="NWES")

        self.tight_layout = StringVar()
        ttk.Checkbutton(self.general_frame, text="Tight Layout", variable=self.tight_layout).grid(row=0, column=0, sticky="W")

        ttk.Label(self.general_frame, text="Number of Rows: ").grid(row=1, column=0, sticky="W")
        self.num_rows = StringVar()
        ttk.Entry(self.general_frame, textvariable=self.num_rows, width=20).grid(row=1, column=1, sticky="W")

        ttk.Label(self.general_frame, text="Number of Columns: ").grid(row=2, column=0, sticky="W")
        self.num_cols = StringVar()
        ttk.Entry(self.general_frame, textvariable=self.num_cols, width=20).grid(row=2, column=1, sticky="W")

    def add_button(self, cmd_plt, cmd_gph):
        self.new_plot_button = ttk.Button(self.general_frame, text="Add Plot", command=cmd_plt)
        self.new_plot_button.grid(row=0, column=4, sticky="W")
        self.new_graph_button = ttk.Button(self.general_frame, text="Add Graph", command=cmd_gph)
        self.new_graph_button.grid(row=1, column=4, sticky="W")



class PlotPage:
    count = 0

    def __init__(self, master):
        self.plot_frame = ttk.Frame(master)
        self.plot_frame.grid(column=0, row=0, sticky="NWES")

        ttk.Label(self.plot_frame, text="Plot Title: ").grid(row=0, column=0, sticky="W")
        self.title_var = StringVar()
        ttk.Entry(self.plot_frame, textvariable=self.title_var, width=20).grid(row=0, column=1, sticky="W")

        ttk.Label(self.plot_frame, text="Y-Axis Label: ").grid(row=1, column=0, sticky="W")
        self.y_title_var = StringVar()
        ttk.Entry(self.plot_frame, textvariable=self.y_title_var, width=20).grid(row=1, column=1, sticky="W")

        ttk.Label(self.plot_frame, text="X-Axis Label: ").grid(row=2, column=0, sticky="W")
        self.x_title_var = StringVar()
        ttk.Entry(self.plot_frame, textvariable=self.x_title_var, width=20).grid(row=2, column=1, sticky="W")

        PlotPage.count += 1

    def add_trace(self, draw):
        self.x_title_var.trace("w", draw)
        self.y_title_var.trace("w", draw)
        self.title_var.trace("w", draw)


class GraphPage:
    count = 0

    def __init__(self, master):
        GraphPage.count += 1

        self.plot_frame = ttk.Frame(master)
        self.plot_frame.grid(column=0, row=0, sticky="NWES")

        ttk.Label(self.plot_frame, text="Plot Num: ").grid(row=0, column=0, sticky="W")
        self.plot_var = StringVar()
        self.choice_combobox = ttk.Combobox(self.plot_frame, textvariable=self.plot_var, width=20, values=["1"])
        self.choice_combobox.grid(row=0, column=1, sticky="W")
        self.choice_combobox.set("1")

        ttk.Label(self.plot_frame, text="Graph Title: ").grid(row=1, column=0, sticky="W")
        self.title_var = StringVar()
        ttk.Entry(self.plot_frame, textvariable=self.title_var, width=20).grid(row=1, column=1, sticky="W")

        ttk.Label(self.plot_frame, text="Graph Color: ").grid(row=2, column=0, sticky="W")
        self.graph_colour = StringVar()
        ttk.Entry(self.plot_frame, textvariable=self.graph_colour, width=20).grid(row=2, column=1, sticky="W")

        with Session(Engine) as session:
            product_names = session.execute(text("SELECT name FROM Product GROUP BY name ORDER BY name DESC"))

        product_names = list(set([str(prod_name[0]) for prod_name in product_names]))
        product_names.sort(reverse=False)
        product_names.insert(0, "All")

        ttk.Label(self.plot_frame, text="Product: ").grid(row=0, column=2, sticky="W")
        self.choice_var = StringVar()
        choice_cbb = ttk.Combobox(self.plot_frame, textvariable=self.choice_var, values=product_names,
                     width=20)
        choice_cbb.grid(row=0, column=3, sticky="W")
        choice_cbb.set(product_names[0])

        ttk.Label(self.plot_frame, text="Store: ").grid(row=1, column=2, sticky="W")
        self.store = StringVar()
        ttk.Entry(self.plot_frame, textvariable=self.store, width=20).grid(row=1, column=3, sticky="W")

        ttk.Label(self.plot_frame, text="Y Data: ").grid(row=0, column=4, sticky="W")
        self.y_data_var = StringVar()
        y_data_cbb = ttk.Combobox(self.plot_frame, textvariable=self.y_data_var, values=[data for data in YData.keys()],
                     width=20)
        y_data_cbb.grid(row=0, column=5, sticky="W")
        y_data_cbb.set(list(YData.keys())[0])

        ttk.Label(self.plot_frame, text="X Data: ").grid(row=1, column=4, sticky="W")
        self.x_data_var = StringVar()
        x_data_cbb = ttk.Combobox(self.plot_frame, textvariable=self.x_data_var, values=[data for data in XData.keys()],
                     width=20)
        x_data_cbb.grid(row=1, column=5, sticky="W")
        x_data_cbb.set(list(XData.keys())[0])

        ttk.Label(self.plot_frame, text="Graph Type: ").grid(row=2, column=4, sticky="W")
        self.line_type = StringVar()
        graph_cbb = ttk.Combobox(self.plot_frame, textvariable=self.line_type, values=[line.name for line in LineType],
                     width=20)
        graph_cbb.grid(row=2, column=5, sticky="W")
        graph_cbb.set([line.name for line in LineType][0])

    def change_plot_num(self, new_num):
        self.choice_combobox["values"] = [i + 1 for i in range(0, new_num)]

    def add_trace(self, draw):
        self.plot_var.trace("w", draw)
        self.x_data_var.trace("w", draw)
        self.y_data_var.trace("w", draw)
        self.line_type.trace("w", draw)
        self.title_var.trace("w", draw)
        self.choice_var.trace("w", draw)
