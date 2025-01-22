import numpy as np
import matplotlib.pyplot as plt
import threading

# internal
from .data_read import read_metadata, load_file
from .data_process import get_bin_edges, project_data
from .Transformer import ARTOFTransformer



# def process_data(dir, i, load_as, transformer):
#     raw_data = load_file(dir, i)
#     transformer.transform(raw_data, load_as)

class ARTOFLoader:
    """Class to load ARTOF data."""

    def __init__(self):
        """Initialize ARTOFLoader class"""
        self.binned_data = None
        self.bin_edges = list()
        self.axes = None
        self.metadata = None
        self.transformer = None

    def load_run(self, dir: str, load_as: str, x0: int = None, y0: int = None, t0: int = None, bin_confs: list = None):
        """
        Load ARTOF data for given run.

        Args:
            dir: Path to run directory.
            load_as: Load parameters in given format ('raw': x,y,t).
            bin_confs: List of 3 binning configurations for the 3 parameters (type defined by 'load_as').
        """
        # aquire metadata and configure transformer
        self.metadata = read_metadata(dir)
        self.transformer = ARTOFTransformer(self.metadata, x0, y0, t0)
        self.axes, def_bin_confs = self.transformer.get_axis_and_bins(load_as, self.metadata)
        bin_confs = def_bin_confs if bin_confs is None else bin_confs

        # transform data to desired format via multithreading
        data_pieces = []
        threads = []
        for i in range(self.metadata.general.lensIterations):
            thread = threading.Thread(target=self.__process_data, args=(dir, i, data_pieces, load_as))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        data = np.concatenate(data_pieces, axis=0)

        # create bin edges based on the passed bin configs
        for i in range(3):
            self.bin_edges.append(get_bin_edges(data[:,i], bin_confs[i], data_id=self.axes[i]))
        # bin data in 3D histogram
        self.binned_data, _ = np.histogramdd(data, bins=self.bin_edges) 

    def __process_data(self, dir: str, i: int, data_pieces: list, load_as: str):        
        """
        Load and transform single data file in given format (needed for multithreading).

        Args:
            dir: Directory where data files are located.
            i: Index of the data to be loaded.
            data_pieces: List of transformed data pieces to which the newly transformed data should be appended.
            load_as: Desired transformation format.
        """
        raw_data = load_file(dir, i)
        data_pieces.append(self.transformer.transform(raw_data, load_as))



    def plot(self, axes: list, ranges: list = [None, None, None], width: float = 5.5, height: float = 5.5):
        """
        Plot loaded data as projection onto given axes. Projections are possible onto 1 or 2 axes.

        Args:
            axes: List containing all axes onto which the projection is performed, e.g., [0,1].
            ranges: List containing ranges for axes (e.g., [[50, 101], [0,50], None]), if None entire range of axes is used (default entire range of each axis).
            width: Width of plot (default 5).
            height: Height of plot (default 5).
        """
        
        proj_data = project_data(self.binned_data, axes, ranges)

        if len(axes) == 2: # plot data in 2D as image
            img_fig, img_ax = plt.subplots(figsize=(width, height))
            img_fig.subplots_adjust(bottom=0.2, left=0.2)
            img_ax.imshow(proj_data, cmap='terrain', norm='linear', origin='lower', extent=[self.bin_edges[axes[0]][0], self.bin_edges[axes[0]][-1], self.bin_edges[axes[1]][0], self.bin_edges[axes[1]][-1]], aspect="auto")
            img_ax.set_xlabel(self.__axis_label(self.axes[axes[0]]))
            img_ax.set_ylabel(self.__axis_label(self.axes[axes[1]]))
        elif len(axes) == 1: # plot data in 1D as line
            x_values = [(self.bin_edges[axes[0]][i] + self.bin_edges[axes[0]][i+1])/2 for i in range(len(self.bin_edges[axes[0]])-1)]            

            line_fig, line_ax = plt.subplots(figsize=(width, height))
            line_fig.subplots_adjust(bottom=0.2, left=0.2)
            line_ax.plot(x_values, proj_data)
            line_ax.set_xlabel(self.__axis_label(self.axes[axes[0]]))
            line_ax.set_ylabel('Counts')


        else:
            raise Exception(f'A projection along {len(axes)} axes is not possible.')
        
    def export_to_csv(self, path: str, axes: list, ranges: list = [None, None, None], delimiter: str = ','):
        """
        Export loaded data as projection onto given axes. Projections are possible onto 1 or 2 axes.

        Args:
            path: Path including file name to which the data is saved.
            axes: List containing all axes onto which the projection is performed, e.g., [0,1].
            ranges: List containing ranges for axes (e.g., [[50, 101], [0,50], None]), if None entire range of axes is used (default entire range of each axis).
            delimiter: Delimiter by which the data is separated (default ',').
        """  
        data_to_export = project_data(self.binned_data, axes, ranges)        
        np.savetxt(path, data_to_export, delimiter=delimiter)

    def __axis_label(self, axis: str) -> str:
        """
        Build string for matplotlib axis label including Greek characters.

        Args:
            axis: String containing the axis label and unit separated by '_'.

        Returns:
            Formatted string for matplotlib.
        """
        name, unit = axis.split('_')
        match name:
            case 'phi':
                name = '$\\varphi$'
            case 'theta':
                name = '$\\theta$'
        return f'{name} [{unit}]'



