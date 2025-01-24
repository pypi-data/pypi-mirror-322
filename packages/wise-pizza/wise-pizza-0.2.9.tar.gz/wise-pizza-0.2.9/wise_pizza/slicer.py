import copy
import json
import warnings
from typing import Optional, Union, List, Dict, Sequence
from collections import defaultdict

import numpy as np
import pandas as pd
from scipy.sparse import csc_matrix, diags

from wise_pizza.dataframe_with_metadata import DataFrameWithMetadata
from wise_pizza.solve.find_alpha import find_alpha
from wise_pizza.utils import clean_up_min_max, fill_string_na
from wise_pizza.make_matrix import sparse_dummy_matrix
from wise_pizza.cluster import make_clusters
from wise_pizza.preselect import HeuristicSelector
from wise_pizza.time import extend_dataframe
from wise_pizza.slicer_facades import SliceFinderPredictFacade
from wise_pizza.solve.tree import tree_solver
from wise_pizza.solve.solver import solve_lasso
from wise_pizza.solve.fitter import TimeFitterLinearModel, AverageFitter, TimeFitter


def _summary(obj) -> str:
    out = {
        "task": obj.task,
        "segments": [
            {
                k: v
                for k, v in s.items()
                if k
                in ["segment", "total", "seg_size", "naive_avg", "impact", "avg_impact"]
            }
            for s in obj.segments
        ],
        "relevant_clusters": {
            k: v for k, v in obj.relevant_cluster_names.items() if "_cluster_" in k
        },
    }
    return json.dumps(out)


class SliceFinder:
    """
    SliceFinder class to find unusual slices
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.min_depth = kwargs.get("min_depth", None)
        self.max_depth = kwargs.get("max_depth", None)
        self.dims = None
        self.X = None
        self.col_defs = None
        self.reg = None
        self.nonzeros = None
        self.weights = None
        self.verbose = 0
        self.task = ""

    def _init_mat(
        self,
        dim_df: pd.DataFrame,
        min_depth: int,
        max_depth: int,
        max_cols: int = 300,
        force_dim: Optional[str] = None,
        clusters: Optional[Dict[str, Sequence[str]]] = None,
        time_basis: Optional[pd.DataFrame] = None,
    ):
        """
        Function to initialize sparse matrix
        @param dim_df: Dataset with dimensions
        @param min_depth: Minimum number of dimension to constrain in segment definition
        @param max_depth: Maximum number of dimension to constrain in segment definition
        @param max_cols: Maxumum number of segments to consider
        @param force_dim: To add dim
        @param clusters: groups of same-dimension values to be considered as candidate segments
        @param time_basis: the set of time profiles to scale the candidate segments by
        @return:
        """
        sel = HeuristicSelector(
            max_cols=max_cols,
            weights=self.weights,
            totals=self.totals,
            time_basis=time_basis,
            verbose=self.verbose,
        )

        # This returns the candidate vectors in batches
        basis_iter = sparse_dummy_matrix(
            dim_df,
            min_depth=min_depth,
            max_depth=max_depth,
            verbose=self.verbose,
            force_dim=force_dim,
            clusters=clusters,
            cluster_names=self.cluster_names,
            time_basis=time_basis,
        )

        # do pre-filter recursively
        for i in basis_iter:
            this_X, these_col_defs = i
            if this_X is not None:
                X_out, col_defs_out = sel(this_X, these_col_defs)

        if self.verbose:
            print("Preselection done!")
        return X_out, col_defs_out

    def fit(
        self,
        dim_df: pd.DataFrame,
        totals: pd.Series,
        weights: pd.Series = None,
        time_col: pd.Series = None,
        time_basis: pd.DataFrame = None,
        min_segments: int = None,
        max_segments: int = None,
        min_depth: int = 1,
        max_depth: int = 3,
        solver: str = "lp",
        verbose: Union[bool, None] = None,
        force_dim: Optional[str] = None,
        force_add_up: bool = False,
        constrain_signs: bool = True,
        cluster_values: bool = True,
        groupby_dims: Optional[List[str]] = None,
        n_jobs: int = 1,
    ):
        """
        Function to fit slicer and find segments
        @param dim_df: Dataset with dimensions
        @param totals: Column with totals
        @param weights: Column with sizes
        @param min_segments: Minimum number of segments to find
        @param max_segments: Maximum number of segments to find, defaults to min_segments
        @param min_depth: Minimum number of dimension to constrain in segment definition
        @param max_depth: Maximum number of dimensions to constrain in segment definition; also max depth pf tree in tree solver
        @param solver: Valid values are "lasso" (default), "tree" (for non-overlapping segments), "omp", or "lp"
        @param verbose: If set to a truish value, lots of debug info is printed to console
        @param force_dim: To add dim
        @param force_add_up: To force add up
        @param constrain_signs: To constrain signs
        @param cluster_values In addition to single-value slices, consider slices that consist of a
        group of segments from the same dimension with similar naive averages

        """
        dim_df = dim_df.copy()
        if groupby_dims is None:
            groupby_dims = []

        assert solver.lower() in ["lasso", "tree", "omp", "lp"]
        min_segments, max_segments = clean_up_min_max(min_segments, max_segments)
        if verbose is not None:
            self.verbose = verbose

        totals = np.array(totals).astype(np.float64)

        if weights is None:
            weights = np.ones_like(totals)
        else:
            weights = np.array(weights).astype(np.float64)

        assert min(weights) >= 0
        assert np.sum(np.abs(totals[weights == 0])) == 0

        # Cast all dimension values to strings
        for c in dim_df.columns:
            if c not in groupby_dims + ["total_adjustment"]:
                dim_df[c] = dim_df[c].astype(str)

        dims = list(dim_df.columns)
        if groupby_dims:
            dims = [d for d in dims if d not in groupby_dims + ["total_adjustment"]]
        # sort the dataframe by dimension values,
        # making sure the other vectors stay aligned
        dim_df = dim_df.reset_index(drop=True)
        dim_df["totals"] = totals
        dim_df["weights"] = weights

        if groupby_dims:
            dim_df = pd.merge(dim_df, time_basis, on=groupby_dims)
            sort_dims = dims + groupby_dims
        else:
            sort_dims = dims

        dim_df = dim_df.sort_values(sort_dims)
        dim_df = dim_df[dim_df["weights"] > 0]

        if groupby_dims is not None and len(groupby_dims) == 2:
            source_df = dim_df[dim_df["chunk"] == "Average"]
        else:
            source_df = dim_df

        # Transform the time basis from table by date to matrices by dataset row
        if time_col is not None:
            self.basis_df = time_basis
            # self.time_basis = {}
            # for c in time_basis.columns:
            #     this_ts = dim_df[c].values.reshape((-1, 1))
            #     max_val = np.abs(this_ts).max()
            #     # take all the values a nudge away from zero so we can divide by them later
            #     this_ts[np.abs(this_ts) < 1e-6 * max_val] = 1e-6 * max_val
            #     self.time_basis[c] = csc_matrix(this_ts)
            self.time = source_df["__time"].values
        # else:
        #     self.time_basis = None

        self.weights = source_df["weights"].values
        self.totals = source_df["totals"].values

        # While we still have weights and totals as part of the dataframe, let's produce clusters
        # of dimension values with similar outcomes
        clusters = defaultdict(list)
        self.cluster_names = {}

        self.avg_prediction = None
        if solver == "tree":
            if cluster_values:
                warnings.warn(
                    "Ignoring cluster_values argument as tree solver makes its own clusters"
                )
            if time_basis is None:
                self.X, self.col_defs, self.cluster_names, _, _ = tree_solver(
                    dim_df=dim_df,
                    dims=dims,
                    num_leaves=max_segments,
                    max_depth=max_depth,
                    fitter=AverageFitter(),
                    n_jobs=n_jobs,
                    verbose=verbose,
                )

                Xw = csc_matrix(diags(self.weights) @ self.X)
                self.reg = solve_lasso(
                    Xw.toarray(),
                    self.totals,
                    alpha=1e-5,
                    verbose=self.verbose,
                    fit_intercept=False,
                )
                print("")

            else:
                time_fitter_model = TimeFitterLinearModel(
                    basis=time_basis,
                    time_col="__time",
                    groupby_dims=groupby_dims,
                )
                fitter = TimeFitter(
                    dims=dims,
                    time_col="__time",
                    time_fitter_model=time_fitter_model,
                    groupby_dims=groupby_dims,
                )
                (
                    self.X,
                    self.col_defs,
                    self.cluster_names,
                    self.avg_prediction,
                    self.weight_total_prediction,
                ) = tree_solver(
                    dim_df=dim_df,
                    dims=dims,
                    fitter=fitter,
                    num_leaves=max_segments,
                    max_depth=max_depth,
                    n_jobs=n_jobs,
                    verbose=verbose,
                )
            self.nonzeros = np.array(range(self.X.shape[1]))

        else:
            if cluster_values:
                self.cluster_names = make_clusters(dim_df, dims)
                for dim in dims:
                    clusters[dim] = [
                        c for c in self.cluster_names.keys() if c.startswith(dim)
                    ]

            dim_df = dim_df[dims]  # if time_col is None else dims + ["__time"]]
            self.dim_df = dim_df
            # lazy calculation of the dummy matrix (calculation can be very slow)
            if (
                list(dim_df.columns) != self.dims
                or max_depth != self.max_depth
                or self.X is not None
                and len(dim_df) != self.X.shape[1]
            ):
                self.X, self.col_defs = self._init_mat(
                    dim_df,
                    min_depth,
                    max_depth,
                    force_dim=force_dim,
                    clusters=clusters,
                )
                assert len(self.col_defs) == self.X.shape[1]
                self.min_depth = min_depth
                self.max_depth = max_depth
                self.dims = list(dim_df.columns)

            Xw = csc_matrix(diags(self.weights) @ self.X)

            if self.verbose:
                print("Starting solve!")
            self.reg, self.nonzeros = find_alpha(
                Xw,
                self.totals,
                max_nonzeros=max_segments,
                solver=solver,
                min_nonzeros=min_segments,
                verbose=self.verbose,
                adding_up_regularizer=force_add_up,
                constrain_signs=constrain_signs,
            )

        if self.verbose:
            print("Solver done!!")

        self.segments = [
            {"segment": self.col_defs[i], "index": int(i)} for i in self.nonzeros
        ]

        # wgts = np.array((np.abs(Xw[:, self.nonzeros]) > 0).sum(axis=0))[0]

        for i, s in enumerate(self.segments):
            segment_def = s["segment"]
            this_vec = (
                self.X[:, s["index"]]
                .toarray()
                .reshape(
                    -1,
                )
            )
            if "time" in segment_def and solver != "tree":
                # Divide out the time profile mult - we've made sure it's always nonzero
                time_mult = (
                    self.time_basis[segment_def["time"]]
                    .toarray()
                    .reshape(
                        -1,
                    )
                )
                dummy = (this_vec / time_mult).astype(int).astype(np.float64)
            else:
                dummy = this_vec.astype(int)

            this_wgts = self.weights * dummy
            wgt = this_wgts.sum()
            # assert wgt == wgts[i]
            s["orig_i"] = i
            s["total"] = (self.totals * dummy).sum()
            s["seg_size"] = wgt
            s["naive_avg"] = s["total"] / wgt
            s["dummy"] = dummy

        if hasattr(self.reg, "coef_"):
            for i, s in enumerate(self.segments):
                this_vec = (
                    self.X[:, s["index"]]
                    .toarray()
                    .reshape(
                        -1,
                    )
                )
                s["coef"] = self.reg.coef_[i]
                # TODO: does not taking the abs of coef here break time series?
                s["impact"] = s["coef"] * (np.abs(this_vec) * self.weights).sum()
                s["avg_impact"] = s["impact"] / sum(self.weights)

            self.segments = self.order_segments(self.segments)

        if (
            time_basis is not None and self.reg is not None
        ):  # it's a time series not fitted with tree
            # Do we need this bit at all?
            predict = self.reg.predict(self.X[:, self.nonzeros]).reshape(
                -1,
            )
            davg = (predict * self.weights).sum() / self.weights.sum()
            self.reg.intercept_ = -davg

            # And this is the version to use later in TS plotting
            self.predict_totals = self.reg.predict(Xw[:, self.nonzeros]).reshape(
                -1,
            )

            # self.enrich_segments_with_timeless_reg(self.segments, self.y_adj)

        # In some cases (mostly in a/b exps we have a situation where there is no any diff in totals/sizes)
        if len(self.segments) == 0:
            self.segments.append(
                {
                    "segment": {"No unusual segments": "No unusual segments"},
                    "coef": 0,
                    "impact": 0,
                    "avg_impact": 0,
                    "total": 0,
                    "seg_size": 0,
                    "naive_avg": 0,
                }
            )

    @staticmethod
    def order_segments(segments: List[Dict[str, any]]):
        pos_seg = [s for s in segments if s["impact"] > 0]
        neg_seg = [s for s in segments if s["impact"] < 0]

        return sorted(pos_seg, key=lambda x: abs(x["impact"]), reverse=True) + sorted(
            neg_seg, key=lambda x: abs(x["impact"]), reverse=True
        )

    @staticmethod
    def segment_to_str(segment: Dict[str, any]):
        s = {
            k: v
            for k, v in segment.items()
            if k not in ["coef", "impact", "avg_impact"]
        }
        return str(s)

    @property
    def segment_labels(self):
        return [self.segment_to_str(s["segment"]) for s in self.segments]

    def summary(self):
        return _summary(self)

    @property
    def relevant_cluster_names(self):
        relevant_clusters = {}
        for s in self.segments:
            for c in s["segment"].values():
                if c in self.cluster_names and ";" not in c:
                    # Then cluster names containing ; are snumerations, don't need explanation
                    relevant_clusters[c] = self.cluster_names[c].replace("@@", ", ")
        return relevant_clusters

    def segment_impact_on_totals(self, s: Dict) -> np.ndarray:
        return s["seg_total_vec"]

    @property
    def actual_totals(self):
        return self.totals + self.y_adj

    @property
    def predicted_totals(self):
        return self.predict_totals + self.y_adj

    def predict(
        self,
        steps: Optional[int] = None,
        basis: Optional[pd.DataFrame] = None,
        weight_df: Optional[pd.DataFrame] = None,
    ):
        """
        Predict the totals using the given basis
        :param basis: Time profiles going into the future, time as index
        :param weight_df: dataframe with all dimensions and time, plus weight column
        :return:
        """
        if basis is None:
            if weight_df is None:
                if steps is None:
                    steps = 6
            else:
                steps = len(weight_df[self.time_name].unique())
                warnings.warn(
                    "Ignoring steps argument, using weight_df to determine forecast horizon"
                )
            basis = extend_dataframe(self.basis_df, steps)
        else:
            if steps is not None:
                raise ValueError("Can't specify both basis and steps")

        last_ts = self.time.max()
        new_basis = basis[basis.index > last_ts]

        dims = [c for c in self.dim_df.columns if c != "__time"]
        if weight_df is None:
            pre_dim_df = self.dim_df[dims].drop_duplicates()
            pre_dim_df[self.size_name] = 1

            # Do a Cartesian join of the time basis and the dimensions
            b = new_basis.reset_index().rename(columns={"index": self.time_name})
            b["key"] = 1
            pre_dim_df["key"] = 1

            # Perform the merge operation
            new_dim_df = pd.merge(b, pre_dim_df, on="key").drop("key", axis=1)
        else:
            # This branch is as yet untested
            assert self.time_name in weight_df.columns
            for d in dims:
                assert d in weight_df.columns

            new_dim_df = pd.merge(
                new_basis, weight_df, left_index=True, right_on=self.time_name
            )

        # Join the (timeless) averages to these future rows
        new_dim_df = pd.merge(new_dim_df, self.avg_df, on=dims, how="left").rename(
            columns={"avg": "avg_future"}
        )
        # TODO: replace with a simple regression for more plausible baselines
        global_avg = (
            new_dim_df[self.total_name].sum() / new_dim_df[self.size_name].sum()
        )
        new_dim_df["avg_future"] = new_dim_df["avg_future"].fillna(global_avg)

        # Construct the dummies for predicting

        segments = copy.deepcopy(self.segments)
        new_X = np.zeros((len(new_dim_df), len(segments)))

        new_totals = np.zeros(len(new_dim_df))
        for s in segments:
            dummy, Xi = make_dummy(s["segment"], new_dim_df)
            new_X[:, s["orig_i"]] = Xi
            s["dummy"] = np.concatenate([s["dummy"], dummy], axis=0)
            future_impact = new_dim_df[self.size_name].values * Xi * s["coef"]
            new_totals += future_impact
            s["seg_total_vec"] = np.concatenate([s["seg_total_vec"], future_impact])

        # Evaluate the regression
        new_avg = self.reg.predict(new_X)

        # Add in the constant averages and multiply by the weights
        new_totals = (new_avg + new_dim_df["avg_future"].values) * new_dim_df[
            self.size_name
        ].values

        # Return the dataframe with totals and weights
        new_dim_df[self.total_name] = pd.Series(data=new_totals, index=new_dim_df.index)

        out = SliceFinderPredictFacade(self, new_dim_df, segments)
        return out

    @property
    def nice_summary(self):

        return nice_summary(
            self.summary(),
            self.total_name,
            self.size_name,
            self.average_name,
            self.data_attrs if hasattr(self, "data_attrs") else None,
        )

    @property
    def markdown_summary(self):
        return markdown_summary(self.nice_summary)

    def descriptive_prompt(
        self, prompt_template: Optional["BasePromptTemplate"] = None
    ):
        if prompt_template is not None:
            return prompt_template.format(
                total_name=self.total_name,
                size_name=self.size_name,
                average_name=self.average_name,
                summary=self.markdown_summary,
            )
        else:
            return f"""
You are a helpful research assistant. You are given a summary analysis of a dataset, 
highlighting the key segments that drove the change in total volume. 
The logic behind choosing those segments is the following: a segment's impact equals the segment's size
({self.size_name}) multiplied by the difference between the segment' average ({self.average_name}) and 
the average of the whole dataset, that describes the change in the total volume ({self.total_name}) due 
to the segment's average deviation from the dataset's average. We look for the segments that have the
larges absolute impact on the total volume. 

Please summarize that data BRIEFLY in a few sentences. 
Here is the summary:
{self.markdown_summary}"""


def make_dummy(segment_def: Dict[str, str], dim_df: pd.DataFrame) -> np.ndarray:
    """
    Function to make dummy vector from segment definition
    @param segment_def: Segment definition
    @param dim_df: Dataset with dimensions
    @return: Dummy vector
    """
    dummy = np.ones((len(dim_df)))
    for k, v in segment_def.items():
        if k != "time":
            dummy = dummy * (dim_df[k] == v).values

    if "time" in segment_def:
        Xi = dummy * dim_df[segment_def["time"]].values
    else:
        raise ValueError("Segments for time series prediction must contain time!")

    assert np.abs(dummy).sum() > 0
    return dummy, Xi


def nice_summary(
    x: str,
    total_name: str,
    size_name: Optional[str] = None,
    average_name: Optional[str] = None,
    attrs: Optional[Dict[str, str]] = None,
) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    x = json.loads(x)
    for xx in x["segments"]:
        xx.update(xx["segment"])

    df = pd.DataFrame(x["segments"])

    # These columns are pretty much self-explanatory, don't need descriptions

    df = fill_string_na(df, "All")
    df = df[[c for c in df.columns if c != "segment"] + ["segment"]]

    if not average_name:
        average_name = "average " + total_name.replace("total", "").replace(
            "Total", ""
        ).replace("TOTAL", "").replace("  ", " ")

    df.rename(
        columns={
            "seg_size": size_name + " of segment",
            "total": total_name + " in segment",
            "impact": "Segment impact on overall total",
            "avg_impact": f"Segment impact on overall {average_name}",
            "naive_avg": average_name + " over segment",
        },
        inplace=True,
    )

    if attrs and "column_descriptions" in attrs:
        column_desc = {
            k: v for k, v in attrs["column_descriptions"].items() if k in df.columns
        }

        df = DataFrameWithMetadata(df, column_descriptions=column_desc)

    out = df

    # TODO: cast cluster definitions to dataframe too
    if "relevant_clusters" in x and x["relevant_clusters"]:
        out = {"summary": df, "clusters": x["relevant_clusters"]}

    return out


def markdown_summary(x: Union[dict, pd.DataFrame]):
    if isinstance(x, pd.DataFrame):
        x = x.drop(columns="segment")
        return x.to_markdown(index=False)
    elif isinstance(x, dict):
        xx = x["summary"].drop(columns="segment")
        table = xx.to_markdown(index=False)
        if "clusters" in x and x["clusters"]:
            clusters = x["clusters"]
            table += "\n\nDefinitions of clusters: \n"
            for k, v in clusters.items():
                table += f"\n{k}: {v}"
        return table
    else:
        raise ValueError("Invalid input, expected either a pd.DataFrame or a dict")


class SlicerPair:
    def __init__(self, s1: SliceFinder, s2: SliceFinder):
        self.s1 = s1
        self.s2 = s2
        self.task = ""

    def summary(self):
        return _summary(self)
