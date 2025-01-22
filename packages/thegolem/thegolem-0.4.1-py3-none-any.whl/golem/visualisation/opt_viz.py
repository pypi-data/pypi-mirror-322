from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from golem.core.log import default_log
from golem.visualisation.opt_history.diversity import DiversityLine, DiversityPopulation
from golem.visualisation.opt_history.fitness_box import FitnessBox
from golem.visualisation.opt_history.fitness_line import FitnessLine, FitnessLineInteractive
from golem.visualisation.opt_history.genealogical_path import GenealogicalPath
from golem.visualisation.opt_history.operations_animated_bar import OperationsAnimatedBar
from golem.visualisation.opt_history.operations_kde import OperationsKDE

if TYPE_CHECKING:
    from golem.core.optimisers.opt_history_objects.opt_history import OptHistory


class PlotTypesEnum(Enum):
    fitness_box = FitnessBox
    fitness_line = FitnessLine
    fitness_line_interactive = FitnessLineInteractive
    operations_kde = OperationsKDE
    operations_animated_bar = OperationsAnimatedBar
    diversity_line = DiversityLine
    diversity_population = DiversityPopulation
    genealogical_path = GenealogicalPath

    @classmethod
    def member_names(cls):
        return cls._member_names_


class OptHistoryVisualizer:
    """ Implements optimization history visualizations available via `OptHistory.show()`.

    `OptHistory.show` points to the initialized instance of this class.
    Thus, supported visualizations can be called directly via `OptHistory.show.<vis_name>(...)` or
    indirectly via `OptHistory.show(...)`.

    This implies that all supported visualizations are listed in two places:
        1. `PlotTypesEnum` members

        `<vis_name> = <VisClass>`

        2. assigned as the class attributes in `OptHistoryVisualizer.__init__`

        `self.<vis_name> = <VizClass>(self.history).visualize`
    """

    def __init__(self, history: OptHistory, visuals_params: Optional[Dict[str, Any]] = None):
        visuals_params = visuals_params or {}
        default_visuals_params = dict(dpi=100)
        default_visuals_params.update(visuals_params)

        self.visuals_params = default_visuals_params
        self.history = history

        self.fitness_box = FitnessBox(history, self.visuals_params).visualize
        self.fitness_line = FitnessLine(history, self.visuals_params).visualize
        self.fitness_line_interactive = FitnessLineInteractive(history, self.visuals_params).visualize
        self.operations_kde = OperationsKDE(history, self.visuals_params).visualize
        self.operations_animated_bar = OperationsAnimatedBar(history, self.visuals_params).visualize
        self.diversity_line = DiversityLine(history, self.visuals_params).visualize
        self.diversity_population = DiversityPopulation(history, self.visuals_params).visualize
        self.genealogical_path = GenealogicalPath(history, self.visuals_params).visualize

        self.log = default_log(self)

    def __call__(self, plot_type: Union[PlotTypesEnum, str] = PlotTypesEnum.fitness_line, **kwargs):
        """ Visualizes the OptHistory with one of the supported methods.

        :param plot_type: visualization to show. Expected values are listed in
            'golem.core.visualisation.opt_viz.PlotTypesEnum'.
        :keyword save_path: path to save the visualization. If set, then the image will be saved, and if not,
            it will be displayed. Essential for animations.
        :keyword dpi: DPI of the output figure.
        :keyword best_fraction: fraction of the best individuals of each generation that included in the
            visualization. Must be in the interval (0, 1].
        :keyword show_fitness: if False, visualizations that support this argument will not display fitness.
        :keyword per_time: Shows time axis instead of generations axis. Currently, supported for plot types:
            'show_fitness_line', 'show_fitness_line_interactive'.
        :keyword use_tags: if True (default), all operations in the history are colored and grouped based on
            operation repository tags. If False, operations are not grouped, colors are picked by fixed colormap
            for every history independently.
        """

        if isinstance(plot_type, str):
            try:
                visualize_function = vars(self)[plot_type]
            except KeyError:
                raise NotImplementedError(
                    f'Visualization "{plot_type}" is not supported. Expected values: '
                    f'{", ".join(PlotTypesEnum.member_names())}.')
        else:
            visualize_function = vars(self)[plot_type.name]
        visualize_function(**kwargs)
