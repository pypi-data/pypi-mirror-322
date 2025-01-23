# Copyright 2023 Mario Graff Guerrero

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from dataclasses import dataclass
from typing import Any, Callable, Union
from numbers import Integral
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectFromModel
from sklearn.utils._param_validation import Interval
from sklearn.base import is_classifier, clone
from sklearn.model_selection import check_cv
from sklearn.metrics import check_scoring



class SelectFromModelCV(SelectFromModel):
    """

    >>> from IngeoML import SelectFromModelCV
    >>> from sklearn.svm import LinearSVC
    >>> from sklearn.datasets import load_wine
    >>> from sklearn.metrics import f1_score
    >>> import pandas as pd
    >>> import seaborn as sns
    >>> X, y = load_wine(return_X_y=True)
    >>> scoring = lambda y, hy: f1_score(y, hy, average='macro')
    >>> select = SelectFromModelCV(estimator=LinearSVC(dual='auto'),
                                   scoring=scoring,
                                   prefit=False).fit(X, y)
                                   
    The performance of the selection mechanisim can be seen in the following figure

    >>> perf = select.cv_results_
    >>> _ = [{'d': k, 'macro-f1': v} for k, v in perf.items()]
    >>> df = pd.DataFrame(_)
    >>> sns.set_style('whitegrid')    
    >>> sns.lineplot(df, x='d', y='macro-f1')

    .. figure:: SelectFromModelCV.png
    """
    _parameter_constraints: dict = {
        **SelectFromModel._parameter_constraints,
        "min_features_to_select": [Interval(Integral, 0, None, closed="neither")],
        "cv": ["cv_object"],
        "scoring": [None, str, callable],
        "n_jobs": [None, Integral],
    }
    _parameter_constraints.pop("threshold")
    def __init__(self, estimator: Any, *, 
                 prefit: bool = False, 
                 norm_order: Union[float, int] = 1, 
                 max_features: Union[Callable[..., Any], int, None] = None, importance_getter: Union[str, Callable[..., Any]] = 'auto',
                 min_features_to_select: int = 2,
                 cv=None,
                 scoring=None,
                 max_iter: int=10) -> None:
        super().__init__(estimator, threshold=-np.inf, 
                         prefit=prefit, norm_order=norm_order, max_features=max_features, 
                         importance_getter=importance_getter)
        self.min_features_to_select = min_features_to_select
        self.scoring = scoring
        self.cv = cv
        self.max_iter = max_iter

    @property
    def max_iter(self):
        """Number of points to sample between 2 and :py:attr:`max_features`"""
        return self._max_iter
    
    @max_iter.setter
    def max_iter(self, value):
        self._max_iter = value

    def fit(self, X, y, groups=None):
        """Choose the number of features"""
        cv = check_cv(self.cv, y, classifier=is_classifier(self.estimator))
        scorer = check_scoring(self.estimator, scoring=self.scoring)
        if self.max_features is not None:
            max_features = self.max_features
        else:
            max_features = X.shape[1] - 2
        max_split = min(self.max_iter, X.shape[1] - 2, max_features)
        dims = np.linspace(2, X.shape[1] - 1, max_split).astype(int)
        folds = [(tr, vs) 
                 for tr, vs in cv.split(X, y, groups=groups)]
        scores = []
        if not self.prefit:
            estimator = clone(self.estimator).fit(X, y)
        else:
            estimator = self.estimator
        for dim in dims:
            hy = np.empty_like(y)
            select = SelectFromModel(estimator=estimator,
                                     threshold=self.threshold,
                                     prefit=True,
                                     norm_order=self.norm_order,
                                     max_features=dim,
                                     importance_getter=self.importance_getter).fit(X, y)
            for tr, vs in folds:
                Xt = select.transform(X)
                m = clone(self.estimator).fit(Xt[tr], y[tr])
                hy[vs] = m.predict(Xt[vs])
            _ = scorer(y, hy)
            scores.append(_)
        self.max_features = dims[np.argmax(scores)]
        self.cv_results_ = {dim: score for dim, score in zip(dims, scores)}
        super().fit(X, y)
        return self

    @property
    def cv(self):
        """Crossvalidation parameters"""
        return self._cv
    
    @cv.setter
    def cv(self, value):
        self._cv = value

    @property
    def scoring(self):
        """Score function"""
        return self._scoring
    
    @scoring.setter
    def scoring(self, value):
        self._scoring = value

    @property
    def min_features_to_select(self):
        """Minimum number of features to select"""
        return self._min_features_to_select
    
    @min_features_to_select.setter
    def min_features_to_select(self, value):
        self._min_features_to_select = value

        
    # @property
    # def n_jobs(self):
    #     """Number of jobs used in multiprocessing."""
    #     return self._n_jobs
    
    # @n_jobs.setter
    # def n_jobs(self, value):
    #     self._n_jobs = value        
        


@dataclass
class SelectFromLinearSVC(TransformerMixin, BaseEstimator):
    """SelectFromLinearSVC selects features using :py:class:`~sklearn.svm.LinearSVC` with penalty 'l1'.

    >>> from sklearn.pipeline import make_pipeline
    >>> from sklearn.svm import LinearSVC
    >>> from sklearn.datasets import load_digits
    >>> from IngeoML import SelectFromLinearSVC
    >>> select = SelectFromLinearSVC()
    >>> cl = LinearSVC(class_weight='balanced')
    >>> X, y = load_digits(return_X_y=True)
    >>> pipe = make_pipeline(select, cl).fit(X, y)
    >>> pipe.steps[0][1].features
    """
    iterations: int=2

    def fit(self, X, y):
        """Estimate the parameters"""
        mask = np.ones(X.shape[1], dtype=bool)
        for _ in range(self.iterations):
            m = LinearSVC(class_weight='balanced',
                          dual=False,
                          penalty='l1', C=1).fit(X[:, mask], y)
            _ = m.coef_[0] != 0
            inner = np.zeros(X.shape[1], dtype=bool)
            inner[np.arange(X.shape[1])[mask][_]] = True
            mask[inner] = False
        self.features = ~mask
        return self
    
    @property
    def features(self):
        """Features selected"""
        return self._features
    
    @features.setter
    def features(self, value):
        self._features = value

    def transform(self, X):
        """Select features"""
        return X[:, self.features]