import json
import os
import pandas as pd
from collections import defaultdict
from tabulate import tabulate
from tqdm import tqdm
from typing import List

from evalscope.benchmarks import Benchmark
from evalscope.collections.sampler import DatasetEntry
from evalscope.config import TaskConfig
from evalscope.constants import DataCollection, DumpMode
from evalscope.evaluator import Evaluator
from evalscope.models import get_local_model, initialize_model_adapter
from evalscope.report import ReportGenerator
from evalscope.utils.io_utils import OutputsStructure, dump_jsonl_data, jsonl_to_list
from evalscope.utils.logger import get_logger

logger = get_logger()


class SimpleEvaluator(Evaluator):

    def __init__(self, dataset_name, data_adapter, model_adapter, task_cfg, outputs):
        super().__init__(
            dataset_name_or_path=dataset_name,
            data_adapter=data_adapter,
            model_adapter=model_adapter,
            task_cfg=task_cfg,
            outputs=outputs)

    def get_answer(self, input_prompt, subset_name, infer_cfg) -> dict:
        answer_d: dict = self.model_adapter.predict(inputs=input_prompt, infer_cfg=infer_cfg)
        answer_id = self._generate_answer_id(self.model_adapter.model_cfg, input_prompt, infer_cfg)
        processed_answer = self._process_answer(answer_d, input_prompt, subset_name, answer_id)
        return processed_answer

    def get_review(self, answer_d) -> dict:
        review_id, reviewer_spec = self._generate_review_id(answer_d)
        review_d = self._get_review(answer_d=answer_d, review_id=review_id, reviewer_spec=reviewer_spec)
        return review_d

    def get_score(self, review_d) -> float:
        metric_score: List[dict] = self.compute_metrics(reviews_list=[review_d])
        # use the first metric by default
        score = metric_score[0]['score']
        return score


class EvaluatorCollection:

    def __init__(self, task_cfg: TaskConfig, outputs: OutputsStructure):
        self.task_cfg = task_cfg
        self.outputs = outputs
        self.model = get_local_model(task_cfg)
        self.dataset, self.dataset_name = self.load()
        self.dataset_name_map, self.dataset_id_map = self._parse_dataset()
        self.evaluators = self._initialize_evaluators()

    def load(self) -> tuple[list[DatasetEntry], str]:
        dataset_path = self.task_cfg.dataset_args[DataCollection.NAME]['local_path']
        dataset_name = os.path.basename(dataset_path).split('.')[0]
        raw_dataset = jsonl_to_list(dataset_path)
        datasets = []
        for sample in raw_dataset:
            datasets.append(DatasetEntry(**sample))
        return datasets, dataset_name

    def _parse_dataset(self):
        dataset_name_map = defaultdict(lambda: defaultdict(list))
        dataset_id_map = {}
        for sample in self.dataset:
            dataset_name, subset_name = sample.dataset_name, sample.subset_name
            dataset_name_map[dataset_name][subset_name].append(sample.index)
            dataset_id_map[sample.index] = sample
        return dataset_name_map, dataset_id_map

    def _initialize_evaluators(self):
        evaluators = {}
        for dataset_name in self.dataset_name_map.keys():
            benchmark = Benchmark.get(dataset_name)
            data_adapter = benchmark.get_data_adapter()
            model_adapter = initialize_model_adapter(self.task_cfg, benchmark.model_adapter, self.model)
            evaluators[dataset_name] = SimpleEvaluator(dataset_name, data_adapter, model_adapter, self.task_cfg,
                                                       self.outputs)
        return evaluators

    def get_report(self, scores):

        def get_dataframe(scores):
            data = []
            for dataset_name, data_map in self.dataset_name_map.items():
                for subset_name, ids in data_map.items():
                    for _id in ids:
                        row_data: DatasetEntry = self.dataset_id_map[_id]
                        score = scores[_id]
                        data.append(
                            dict(
                                task_type=row_data.task_type,
                                categories=tuple(row_data.categories),
                                dataset_name=dataset_name,
                                subset_name=subset_name,
                                tags=row_data.tags,
                                score=score))
            return pd.DataFrame(data)

        def aggregate_and_sort(df, group_by_cols):
            # aggregate by group_by_cols, and calculate average_score and count
            report_df = df.groupby(group_by_cols) \
                .agg(average_score=('score', 'mean'), count=('score', 'size')) \
                .reset_index()
            report_df['average_score'] = report_df['average_score'].round(4)
            report_df = report_df.sort_values(by='count', ascending=False) \
                .to_dict(orient='records')
            return report_df

        df = get_dataframe(scores)

        # multi-level aggregation
        subset_report_df = aggregate_and_sort(df, ['task_type', 'dataset_name', 'subset_name'])
        dataset_report_df = aggregate_and_sort(df, ['task_type', 'dataset_name'])
        task_report_df = aggregate_and_sort(df, ['task_type'])

        # explode tags to multiple rows
        df_exploded_tags = df.explode('tags')
        tag_report_df = aggregate_and_sort(df_exploded_tags, ['tags'])

        # process multi-level categories
        df_categories = df.copy()
        # multi-level aggregation for categories
        max_depth = df_categories['categories'].apply(len).max()
        for level in range(max_depth):
            df_categories[f'category{level}'] = df_categories['categories'].apply(lambda x: x[level]
                                                                                  if len(x) > level else '')
        category_report_df = aggregate_and_sort(df_categories, [f'category{level}' for level in range(max_depth)])

        # convert to dict format
        report_dict = {
            'subset_level': subset_report_df,
            'dataset_level': dataset_report_df,
            'task_level': task_report_df,
            'tag_level': tag_report_df,
            'category_level': category_report_df,
        }

        # record report
        for level, data in report_dict.items():
            table = tabulate(data, headers='keys', tablefmt='pretty', showindex=False)
            logger.info(f'{level} Report:\n{table}')

        report = ReportGenerator.gen_collection_report(df, self.dataset_name, self.task_cfg.model_id)
        # save report to JSON file
        report_file_path = os.path.join(self.outputs.reports_dir, self.task_cfg.model_id, f'{self.dataset_name}.json')
        os.makedirs(os.path.dirname(report_file_path), exist_ok=True)
        with open(report_file_path, 'w', encoding='utf-8') as f:
            json.dump(report.to_dict(), f, ensure_ascii=False, indent=4)

    def get_answers(self):
        pred_file_path = os.path.join(self.outputs.predictions_dir, self.task_cfg.model_id,
                                      f'{self.dataset_name}.jsonl')
        os.makedirs(os.path.dirname(pred_file_path), exist_ok=True)
        answers = defaultdict(dict)
        for sample in tqdm(self.dataset, desc='Getting answers'):
            evaluator = self.evaluators[sample.dataset_name]
            answer_d = evaluator.get_answer(sample.prompt, sample.subset_name, self.task_cfg.generation_config)
            answers[sample.index] = answer_d
            dump_jsonl_data(answer_d, pred_file_path, dump_mode=DumpMode.APPEND)
        return answers

    def get_reviews(self, answers):
        review_file_path = os.path.join(self.outputs.reviews_dir, self.task_cfg.model_id)
        os.makedirs(review_file_path, exist_ok=True)
        reviews = defaultdict(dict)
        for sample in tqdm(self.dataset, desc='Getting reviews'):
            evaluator = self.evaluators[sample.dataset_name]
            review_d = evaluator.get_review(answers[sample.index])
            reviews[sample.index] = review_d
            dump_jsonl_data(
                review_d,
                os.path.join(review_file_path, f'{self.dataset_name}_{sample.dataset_name}_{sample.subset_name}.jsonl'),
                dump_mode=DumpMode.APPEND)
        return reviews

    def get_scores(self, reviews) -> float:
        scores = defaultdict(dict)
        for sample in tqdm(self.dataset, desc='Getting scores'):
            evaluator = self.evaluators[sample.dataset_name]
            review_d = reviews[sample.index]
            score = evaluator.get_score(review_d)
            scores[sample.index] = score

        return scores

    def eval(self, **kwargs):
        answers = self.get_answers()
        reviews = self.get_reviews(answers)
        scores = self.get_scores(reviews)
        self.get_report(scores)
