from globox import COCOEvaluator
from .constants import *
from math import isclose
import pytest


@pytest.fixture
def evaluator() -> COCOEvaluator:
    coco_gt = AnnotationSet.from_coco(coco_gts_path)
    coco_det = coco_gt.from_results(coco_results_path)

    return COCOEvaluator(
        ground_truths=coco_gt, 
        predictions=coco_det,
    )


def test_evaluation(evaluator: COCOEvaluator):
    # Official figures returned by pycocotools (see pycocotools_results.py)
    assert isclose(evaluator.ap(), 0.503647, abs_tol=1e-6)
    assert isclose(evaluator.ap_50(), 0.696973, abs_tol=1e-6)
    assert isclose(evaluator.ap_75(), 0.571667, abs_tol=1e-6)

    assert isclose(evaluator.ap_small(), 0.593252, abs_tol=1e-6)
    assert isclose(evaluator.ap_medium(), 0.557991, abs_tol=1e-6)
    assert isclose(evaluator.ap_large(), 0.489363, abs_tol=1e-6)

    assert isclose(evaluator.ar_1(), 0.386813, abs_tol=1e-6)
    assert isclose(evaluator.ar_10(), 0.593680, abs_tol=1e-6)
    assert isclose(evaluator.ar_100(), 0.595353, abs_tol=1e-6)

    assert isclose(evaluator.ar_small(), 0.654764, abs_tol=1e-6)
    assert isclose(evaluator.ar_medium(), 0.603130, abs_tol=1e-6)
    assert isclose(evaluator.ar_large(), 0.553744, abs_tol=1e-6)

    assert evaluator.evaluate.cache_info().currsize == 60


def test_evaluation_no_confidence():
    coco_gt = AnnotationSet.from_coco(coco_gts_path)

    COCOEvaluator(
        ground_truths=coco_gt, 
        predictions=coco_gt,
    ).evaluate(
        iou_threshold=0.5,
        max_detections=100,
        size_range=COCOEvaluator.ALL_RANGE
    )

def test_evaluate_defaults(evaluator: COCOEvaluator):
    evaluator.evaluate(iou_threshold=0.6)
