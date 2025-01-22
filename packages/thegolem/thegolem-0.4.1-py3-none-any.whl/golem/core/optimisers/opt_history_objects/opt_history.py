from __future__ import annotations

import csv
import io
import itertools
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union, TYPE_CHECKING

from golem.core.log import default_log
from golem.core.optimisers.objective.objective import ObjectiveInfo
from golem.core.optimisers.opt_history_objects.generation import Generation

from golem.core.paths import default_data_dir
from golem.serializers.serializer import default_load, default_save
from golem.visualisation.opt_viz import OptHistoryVisualizer

if TYPE_CHECKING:
    from golem.core.dag.graph import Graph
    from golem.core.optimisers.opt_history_objects.individual import Individual


class OptHistory:
    """
    Contains optimization history, saves history to csv.
    Can be used for any type of graph that is serializable with Serializer.

    Args:
        objective: information about metrics (metric names and if it's multi-objective)
        default_save_dir: default directory used for saving history when not explicit path is provided.
    """

    def __init__(self,
                 objective: Optional[ObjectiveInfo] = None,
                 default_save_dir: Optional[os.PathLike] = None):
        self._objective = objective or ObjectiveInfo()
        self._generations: List[Generation] = []
        self.archive_history: List[List[Individual]] = []
        self._tuning_result: Optional[Graph] = None

        # init default save directory
        if default_save_dir:
            default_save_dir = Path(default_save_dir)
            if not default_save_dir.is_absolute():
                # if path is not absolute, treat it as relative to data dir
                default_save_dir = Path(default_data_dir()) / default_save_dir
        else:
            default_save_dir = default_data_dir()
        self._default_save_dir = str(default_save_dir)

    @property
    def objective(self):
        return self._objective

    def is_empty(self) -> bool:
        return not self.generations

    def add_to_history(self, individuals: Sequence[Individual], generation_label: Optional[str] = None,
                       generation_metadata: Optional[Dict[str, Any]] = None):
        generation = Generation(individuals, self.generations_count, generation_label, generation_metadata)
        self.generations.append(generation)

    def add_to_archive_history(self, individuals: Sequence[Individual]):
        self.archive_history.append(list(individuals))

    def to_csv(self, save_dir: Optional[os.PathLike] = None, file: os.PathLike = 'history.csv'):
        save_dir = save_dir or self._default_save_dir
        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)

        with open(Path(save_dir, file), 'w', newline='') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)

            # Write header
            metric_str = 'metric'
            if self.objective.is_multi_objective:
                metric_str += 's'
            header_row = ['index', 'generation', metric_str, 'quantity_of_operations', 'depth', 'metadata']
            writer.writerow(header_row)

            # Write history rows
            idx = 0
            for gen_num, gen_inds in enumerate(self.generations):
                for ind_num, ind in enumerate(gen_inds):
                    row = [idx, gen_num, ind.fitness.values, ind.graph.length, ind.graph.depth, ind.metadata]
                    writer.writerow(row)
                    idx += 1

    def save_current_results(self, save_dir: Optional[os.PathLike] = None):
        # Create folder if it's not exists
        save_dir = save_dir or self._default_save_dir
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
            self._log.info(f"Created directory for saving optimization history: {save_dir}")

        try:
            last_gen_id = self.generations_count - 1
            last_gen = self.generations[last_gen_id]
            for individual in last_gen:
                ind_path = Path(save_dir, str(last_gen_id), str(individual.uid))
                ind_path.mkdir(exist_ok=True, parents=True)
                individual.save(json_file_path=ind_path / f'{str(individual.uid)}.json')
        except Exception as ex:
            self._log.exception(ex)

    def save(self, json_file_path: Union[str, os.PathLike] = None, is_save_light: bool = False) -> Optional[str]:
        """ Saves history to specified path.
        Args:
            json_file_path: path to json file where to save history.
            is_save_light: bool parameter to specify whether there is a need to save full history or a light version.
            NB! For experiments and etc. full histories must be saved. However, to make the analysis of results faster
            (show fitness plots, for example) the light version of histories can be saved too.
        """
        history_to_save = lighten_history(self) if is_save_light else self
        return default_save(obj=history_to_save, json_file_path=json_file_path)

    @staticmethod
    def load(json_str_or_file_path: Union[str, os.PathLike] = None) -> OptHistory:
        return default_load(json_str_or_file_path)

    @staticmethod
    def clean_results(dir_path: Optional[str] = None):
        """Clearn the directory tree with previously dumped history results."""
        if dir_path and os.path.isdir(dir_path):
            shutil.rmtree(dir_path, ignore_errors=True)
            os.mkdir(dir_path)

    @property
    def historical_fitness(self) -> Sequence[Sequence[Union[float, Sequence[float]]]]:
        """Return sequence of histories of generations per each metric"""
        if self.objective.is_multi_objective:
            historical_fitness = []
            num_metrics = len(self.generations[0][0].fitness.values)
            for objective_num in range(num_metrics):
                # history of specific objective for each generation
                objective_history = [[ind.fitness.values[objective_num] for ind in generation]
                                     for generation in self.generations]
                historical_fitness.append(objective_history)
        else:
            historical_fitness = [[ind.fitness.value for ind in pop]
                                  for pop in self.generations]
        return historical_fitness

    @property
    def all_historical_fitness(self) -> List[float]:
        historical_fitness = self.historical_fitness
        if self.objective.is_multi_objective:
            all_historical_fitness = []
            for obj_num in range(len(historical_fitness)):
                all_historical_fitness.append(list(itertools.chain(*historical_fitness[obj_num])))
        else:
            all_historical_fitness = list(itertools.chain(*historical_fitness))
        return all_historical_fitness

    def all_historical_quality(self, metric_position: int = 0) -> List[float]:
        """
        Return fitness history of population for specified metric.

        Args:
            metric_position: Index of the metric for multi-objective optimization.
             By default, choose first metric, assuming it is primary quality metric.

        Returns:
            List: all historical fitness
        """
        if self.objective.is_multi_objective:
            all_historical_quality = self.all_historical_fitness[metric_position]
        else:
            all_historical_quality = self.all_historical_fitness
        return all_historical_quality

    @property
    def show(self):
        return OptHistoryVisualizer(self)

    # def analyze_online(self, url='https://fedot.onti.actcognitive.org'):
    #     case_id = FILE_NAME.replace('.json', '') + str(uuid4())
    #     history_url = f'{DOMAIN}/ws/sandbox/custom_{case_id}/history'
    #     post_url = f"{DOMAIN}/api/showcase/add"
    #
    #     history_json = json.load(open(BASE_PATH.joinpath(FILE_NAME)))
    #     new_case = {
    #         'case': {
    #             'case_id': case_id,
    #         },
    #         'history': history_json
    #     }
    #     response = requests.post(post_url, json=new_case)
    #
    #     print(response.text, response.status_code, )
    #     print(f'IMPORTANT! Save this url.\n{history_url}')

    def get_leaderboard(self, top_n: int = 10) -> str:
        """
        Prints ordered description of the best solutions in history
        :param top_n: number of solutions to print
        """
        # Take only the first graph's appearance in history
        individuals_with_positions \
            = list({ind.graph.descriptive_id: (ind, gen_num, ind_num)
                    for gen_num, gen in enumerate(self.generations)
                    for ind_num, ind in reversed(list(enumerate(gen)))}.values())

        top_individuals = sorted(individuals_with_positions,
                                 key=lambda pos_ind: pos_ind[0].fitness, reverse=True)[:top_n]

        output = io.StringIO()
        separator = ' | '
        header = separator.join(['Position', 'Fitness', 'Generation', 'Graph'])
        print(header, file=output)
        for ind_num, ind_with_position in enumerate(top_individuals):
            individual, gen_num, ind_num = ind_with_position
            positional_id = f'g{gen_num}-i{ind_num}'
            print(separator.join([f'{ind_num:>3}, '
                                  f'{str(individual.fitness):>8}, '
                                  f'{positional_id:>8}, '
                                  f'{individual.graph.descriptive_id}']), file=output)

        # add info about initial assumptions (stored as zero generation)
        for i, individual in enumerate(self.generations[0]):
            ind = f'I{i}'
            positional_id = '-'
            print(separator.join([f'{ind:>3}'
                                  f'{str(individual.fitness):>8}',
                                  f'{positional_id}',
                                  f'{individual.graph.descriptive_id}']), file=output)
        return output.getvalue()

    @property
    def initial_assumptions(self) -> Optional[Generation]:
        if not self.generations:
            return None
        for gen in self.generations:
            if gen.label == 'initial_assumptions':
                return gen

    @property
    def final_choices(self) -> Optional[Generation]:
        if not self.generations:
            return None
        for gen in reversed(self.generations):
            if gen.label == 'final_choices':
                return gen

    @property
    def generations_count(self) -> int:
        return len(self.generations)

    @property
    def tuning_result(self):
        if hasattr(self, '_tuning_result'):
            return self._tuning_result
        else:
            return None

    @tuning_result.setter
    def tuning_result(self, val):
        self._tuning_result = val

    @property
    def generations(self):
        return self._generations

    @generations.setter
    def generations(self, value):
        self._generations = value

    @property
    def individuals(self):
        self._log.warning(
            '"OptHistory.individuals" is deprecated and will be removed later. '
            'Please, use "OptHistory.generations" to access generations.')
        return self.generations

    @individuals.setter
    def individuals(self, value):
        self.generations = value

    @property
    def _log(self):
        return default_log(self)


def lighten_history(history: OptHistory) -> OptHistory:
    """ Keeps the most informative field in OptHistory object to show most of the visualizations
    without excessive memory usage. """
    light_history = OptHistory()
    light_history._generations = \
        [Generation(iterable=gen, generation_num=i) for i, gen in enumerate(history.archive_history)]
    light_history.archive_history = history.archive_history
    light_history._objective = history.objective
    light_history._tuning_result = history.tuning_result
    return light_history
