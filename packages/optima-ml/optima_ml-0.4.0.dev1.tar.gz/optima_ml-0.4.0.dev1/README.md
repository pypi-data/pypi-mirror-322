# OPTIMA: an Optimization Platform for Tuning Input Variables and Model Parameters

OPTIMA is a framework to perform highly parallelized hyperparameter optimization and input variable selection of arbitrary Keras
or Lightning neural networks for supervised learning tasks.

#### Table of Contents
* [Documentation](#documentation)
* [Installation](#installation)
  + [Preconfigured environments](#preconfigured-environments)
    - [Dresden (Barnard / Romeo)](#dresden-barnard-romeo)
  + [Local installation](#local-installation)
* [Usage](#usage)
  + [Overview](#overview)
  + [Running an optimization](#running-an-optimization)
    - [Local](#local)
    - [Cluster](#cluster)
  + [Run-config](#run-config)
    - [General](#general)
    - [Output](#output)
    - [Inputs](#inputs)
    - [Evaluation](#evaluation)
    - [Training](#training)
    - [Hyperparameter optimization](#hyperparameter-optimization)
      * [General](#general-1)
      * [Bayesian optimization (Optuna)](#bayesian-optimization-optuna)
      * [Population Based Training](#population-based-training)
    - [Trial selection](#trial-selection)
    - [Cross-validation](#cross-validation)
    - [Input variable selection](#input-variable-selection)
    - [Lightning](#lightning-1)
    - [Custom Keras objects](#custom-keras-objects)
    - [Cluster setup](#cluster-setup)
  + [Built-in functionality](#built-in-functionality)
    - [Keras](#keras-1)
    - [Inputs](#inputs-1)
    - [Trial selection](#trial-selection-1)
    - [Evaluation](#evaluation-1)
    - [Input variable selection](#input-variable-selection-1)

## Documentation

A quick overview and instructions on how to configure OPTIMA to perform an optimization is given in [usage](#usage).
A more detailed introduction including a description of the inner workings of OPTIMA can be found in chapter 4.2 of
https://inspirehep.net/literature/2707309. Automatically generated API documentation is published at
https://optima-docs.docs.cern.ch/.

## Installation

### Preconfigured environments

#### Dresden (Barnard / Romeo / Capella)

On Barnard, Romeo, and Capella, preconfigured conda environments for both Keras (`OPTIMA_Keras_cpu` / `OPTIMA_Keras_gpu`)
and Lightning (`OPTIMA_lightning_cpu`) are available at `/projects/materie-09/OPTIMA/conda_env`.

1. If you are using `Anaconda` for the first time, load and initialize `Anaconda`:

    ```
    module load release/23.10 Anaconda3/2023.07-2
    conda init
    ```

    This appends a new code block to your `.bashrc`. For later, it is useful to surround
    this in a function. This should look similar to:

    ```bash
    function load_anaconda {
        # >>> conda initialize >>>
        # !! Contents within this block are managed by 'conda init' !!
        __conda_setup="$('/software/rapids/r23.10/Anaconda3/2023.07-2/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
        if [ $? -eq 0 ]; then
            eval "$__conda_setup"
        else
            if [ -f "/software/rapids/r23.10/Anaconda3/2023.07-2/etc/profile.d/conda.sh" ]; then
                . "/software/rapids/r23.10/Anaconda3/2023.07-2/etc/profile.d/conda.sh"
            else
                export PATH="/software/rapids/r23.10/Anaconda3/2023.07-2/bin:$PATH"
            fi
        fi
        unset __conda_setup
        # <<< conda initialize <<<
    }
    ```

    For the changes to take effect, close and re-open your shell (or `source` your
`.bashrc`), and run:

    ```
    load_anaconda
    ```

2. Point `conda` to the existing environments by adding `/projects/materie-09/OPTIMA/conda_env`
to `envs_dirs` in your `.condarc`:

    ```
    conda config --append envs_dirs /projects/materie-09/OPTIMA/conda_env
    ```

    You should now be able to see the environments when running:

    ```
    conda env list
    ```

3. (optional) To display the environment name instead of the path, run:

    ```
    conda config --set env_prompt '({name}) '
    ```

### Local installation

#### Installation with pip

Each tagged version of OPTIMA is published to PyPI. To set up the python environment and install the most recent version
of OPTIMA, run:

- Keras:

    ```
    pip install optima-ml[keras]
    ```

- Lightning (CPU only):

    ```
    pip install optima-ml[lightning] --extra-index-url https://download.pytorch.org/whl/cpu
    ```

- Lightning (with GPU support):

    ```
    pip install optima-ml[lightning]
    ```

In case a different version of OPTIMA that has not been uploaded to PyPI is needed, clone the repository and, from the
repository's root, run:

- Keras:

    ```
    pip install .[keras]
    ```

- Lightning (CPU only):

    ```
    pip install .[lightning] --extra-index-url https://download.pytorch.org/whl/cpu
    ```

- Lightning (with GPU support):

    ```
    pip install .[lightning]
    ```

### Installation with conda

To set up the python environment and install OPTIMA with conda, clone the repository, checkout the desired version of OPTIMA (e.g. the
current master version or a tagged commit), and run:

#### Keras

- Linux:

    ```
    conda env create -n OPTIMA --file conda-requirements.yml
    conda activate OPTIMA
    pip install --no-deps .
    ```

- MacOS:

    ```
    conda env create -n OPTIMA --file conda-requirements-macos.yml
    conda activate OPTIMA
    pip install --no-deps .
    ```

#### Lightning

OPTIMA with Lightning has not yet been tested on MacOS.

- Linux (CPU only):

    ```
    conda env create -n OPTIMA --file conda-requirements_lightning.yml
    conda activate OPTIMA
    pip install --no-deps .
    ```
- Linux (with GPU support):

    ```
    conda env create -n OPTIMA --file conda-requirements_lightning_gpu.yml
    conda activate OPTIMA
    pip install --no-deps .
    ```

## Usage

### Overview

A single optimization run consists of up to three optimization steps: an input variable selection, the main
hyperparameter optimization using Bayesian optimization, and a “fine-tuning” step using Population Based Training.

The input variable selection implements a backwards elimination algorithm to remove uninformative input variables.
Since this approach is based on a trained model that is representative of the final result of the hyperparameter
optimization, the input variable selection is preceded by an initial hyperparameter optimization using the same settings
as the main hyperparameter optimization. Its results are used to perform the input variable selection whose algorithm is
described [here](https://optima-docs.docs.cern.ch/core/variable_optimization.html#OPTIMA.core.variable_optimization.perform_variable_optimization).
Inputs that are found to be uninformative are removed from the dataset for the rest of the optimization.

Both the pre- and the main hyperparameter optimization perform a Bayesian optimization based on
[Optuna's `TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html).
After a fixed number of trials, the best hyperparameters are determined, corresponding models are retrained using
cross-validation and their performance is evaluated. This evaluation after each hyperparameter optimization is documented
[here](https://optima-docs.docs.cern.ch/core/evaluation.html#OPTIMA.core.evaluation.evaluate_experiment).

The fine-tuning step uses the implementation of [Population Based Training in
Tune](https://docs.ray.io/en/releases-2.5.1/tune/examples/pbt_guide.html). Hyperparameters that do not support mutation
are fixed to the optimized value found during the main optimization step. The subsequent evaluation is identical to the
evaluation of the previous two steps.

Each part of the optimization can be controlled in great detail using a [run-config file](#run-config). Additionally,
OPTIMA provides a full suite of [built-in functions](#built-in-functionality) that can be used to optimize multilayer
perceptrons for classification tasks - no additional configuration required. For other use cases, some (or all) of these
functions can be re-defined in the run-config to modularly replace built-in functionality where needed. The remaining
built-in behavior is left unchanged, reducing the necessary configuration to a minimum.

### Running an optimization

The optimization is started by loading the python environment, executing `optima` and providing the run-config.
Run `optima --help` for an explanation of the available command line arguments.

Depending on the value of the `cluster` argument, the optimization is started locally or sent off as a cluster job.

#### Local

If the `cluster` command line argument is set to `'local'` (the default), the optimization is started locally. Relevant
command line arguments are:

- `config`: Path to the run-config file. (Required)
- `defaults`: Path to an alternative defaults-config. This overwrites the built-in default parameter values. (Default: `None`)
- `cpus`: Total number of CPUs to use. (Default: `1`)
- `gpus`: Total number of GPUs to use. (Default: `0`)
- `mem_per_cpu`: Amount of memory to allocate per CPU (in MB). (Default: `1000`)
- `cpus_per_trial`: Number of CPUs to use per trial. (Default: `1`)
- `gpus_per_trial`: Number of GPUs to use per trial. This can be a fractional number if multiple trials should share a GPU. (Default: `0`)
- `max_pending_trials`: The maximum number of trials that are allowed to be `'pending'`. (Default: `cpus / cpus_per_trial`)
- `temp_dir`: Overwrite Ray's default root temporary directory (`/tmp/ray`). This must be an absolute path.

#### Cluster

If the `cluster` command line argument is set to the name of a built-in cluster or to `'custom'`, the optimization will be
launched as a cluster job. This is done by manually launching a Ray node on each node in the job in order to build a Ray
cluster, to which OPTIMA in then connected. Ray then takes care of distributing all tasks across the cluster. It is
possible to run multiple optimizations in parallel on the same cluster; each job will consequently build its own Ray cluster.
To ensure the communication between Ray nodes is confined to be within one Ray cluster, a file will be created on a shared
file system that keeps track of the running jobs. The location of this file as well as the ports used for the communication
are set in the cluster class that is discussed below.

In order to setup the OPTIMA python environment in the job, a sourcable script is needed. This can, for example, look
like this:

```bash
#!/usr/bin/env bash

source ~/.bashrc
load_anaconda
conda activate OPTIMA_Keras_cpu
```

If the optimization is to be run on an own cluster, i.e. none of the built-in options in `OPTIMA.hardware_configs`,
`cluster` must be set to `'custom'` and a cluster config file containing a `CustomCluster` class that implements the
[abstract cluster base class](https://optima-docs.docs.cern.ch/hardware_configs/common.html#OPTIMA.hardware_configs.common.Cluster)
needs to be provided via the `cluster_config` command line argument. If you are using a Slurm-based cluster, you can
subclass the built-in `SLURMCluster` class; see [Dresden's Barnard cluster](./OPTIMA/hardware_configs/Dresden_Taurus.py#L42)
for reference. At the moment, no such class is available for HTCondor-based clusters.

Additionally, when not running on a Slurm-based cluster, it may be necessary to extend the
[cluster job class](https://optima-docs.docs.cern.ch/hardware_configs/common.html#OPTIMA.hardware_configs.common.ClusterJob)
that contains the job configuration by defining a `ClusterJob` class in the cluster configuration file.

In addition to the arguments listed in [the previous section](#local), the following command line arguments are relevant
when running on a cluster:

- `name`: Specifies the name of the job and the filename of the output log that is created in a `logs` folder in the
execution directory. (Default: `'DNN_optimization'`)
- `cluster`: Specifies which cluster the optimization should run on. (Default: `'local'`)
- `cluster_config`: Path to a cluster configuration file. Only used if `cluster` is set to `'custom'`. (Default: `None`)
- `mem_per_cpu`: Amount of memory to allocate per CPU (in MB). This overwrites the value provided in the cluster-class. (Default: `None`)
- `fixed_ray_node_size`: If provided, each worker node is forced to have the same number of CPUs and GPUs instead of
letting the cluster management software handle the allocation. This is implicitly set when using GPUs. (Default: False)
- `workers`: Sets the number of nodes to allocate. Only used if `fixed_ray_node_size` is set. (Default: `None`)
- `cpus_per_worker`: Sets the number of CPUs to allocate per node. Only used if `fixed_ray_node_size` is set. (Default: `None`)
- `gpus_per_worker`: Sets the number of GPUs to allocate per node. Only used if `fixed_ray_node_size` is set. (Default: `None`)
- `min_cpus_per_ray_node`: Sets the minimum number of CPUs to allocate per node. This is not used if `fixed_ray_node_size`
is set. (Default: `None`)
- `runtime`: The runtime in hours for which the resources should be reserved. (Default: `12.0`)
- `exclude`: Comma separated list of nodes that should be excluded from the job. (Default: `None`)

### Run-config

The run-config file serves as the central repository for all available settings of an optimization run within OPTIMA.
The following sections collect all parameters required by OPTIMA to perform a full optimization. Within the run-config,
it is only necessary to specify parameters that lack default values or whose values are to be altered from their defaults.

In addition to these required parameters, optional parameters (mostly functions and classes) can be defined in the
run-config to overwrite built-in functionality. These are discussed individually [in the next section](#built-in-functionality).

#### General

Especially for testing, it can be useful to only perform the training for a fixed set of hyperparameters without any
optimization. This is possible when setting `perform_variable_opt`, `perform_main_hyperopt` and `perform_PBT_hyperopt`
to `False`. In this case, the `search_space` is assumed to only contain fixed hyperparameter values, and only the model
training and subsequent evaluation is performed.

| Parameter                        | Default value | Explanation                                                                                                                                                                          |
|----------------------------------|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `perform_variable_opt` *(bool)*  | None          | Whether to perform the initial hyperparameter optimization and subsequent input variable selection step.                                                                             |
| `perform_main_hyperopt` *(bool)* | None          | Whether to perform the main hyperparameter optimization step with Optuna.                                                                                                            |
| `perform_PBT_hyperopt` *(bool)*  | None          | Whether to perform the hyperparameter fine-tuning step with PBT.                                                                                                                     |
| `model_type` *(str)*             | `'Keras'`     | The ML library used to build the model. Allowed values are `'Keras'` and `'Lightning'`.                                                                                              |
| `random_seed` *(int)*            | `42`          | Random seed to make the optimization reproducible. Deterministic execution is only guaranteed if model training is not parallelized, i.e. no two trainings can run at the same time. |

#### Output

| Parameter                        | Default value       | Explanation                                                                                                                                                                                             |
|----------------------------------|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `output_name` *(str)*            | `'OPTIMA_defaults'` | Name of the output directory. Unless `use_exact_name` is `True`, this is prefixed by a string describing which of the three optimization steps was performed.                                           |
| `output_path` *(str)*            | `'DNN_storage'`     | Path to the directory the output folder should be created in. This path can be absolute or relative to the directory of execution. When running on a cluster, this needs to be on a shared file system. |
| `use_exact_name` *(bool)*        | `False`             | If `True`, disables the prefix of the output folder name.                                                                                                                                               |

#### Inputs

Details on how the input data is loaded and preprocessed can be found [here](https://optima-docs.docs.cern.ch/core/inputs.html#OPTIMA.core.inputs.get_experiment_inputs).

| Parameter                                 | Default value | Explanation                                                                                                                                                                                                                                                                                                                           |
|-------------------------------------------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `produce_inputs_plots` *(bool)*           | `True`        | Whether to produce plots of the input data by calling `plot_input_data()`.                                                                                                                                                                                                                                                            |
| `use_testing_dataset` *(bool)*            | `True`        | If `True`, the input data is plot into training, validation and testing datasets. If `False`, it is split into training and validation sets. This affects both the training during hyperparameter optimization as well as the cross-validation during the experiment evaluation.                                                      |
| `fixed_testing_dataset` *(bool)*          | `True`        | If `True`, use the same testing dataset for all folds during cross-validation. If `False`, the testing dataset is rotated like the training and validation sets. Only used if `use_testing_dataset` is `True`.                                                                                                                        |
| `use_eventNums_splitting` *(bool)*        | `False`       | If `True`, use the event numbers provided by `get_inputs()` to perform the splitting of the dataset according to `(event_number + offset) % N == 0`. If `False`, use random splitting.                                                                                                                                                |
| `eventNums_splitting_N` *(int)*           | `5`           | The `N` in `(event_number + offset) % N == 0`. Controls the size of each dataset when using event number splitting. A value of `5` splits the dataset into 5 parts, 1 of which is used for validation, 1 for testing if `use_testing_dataset` is `True`, and the rest for training. Only used if `use_eventNums_splitting` is `True`. |
| `eventNums_splitting_offset_val` *(int)*  | `0`           | Controls which subset is used for validation. All events satisfying `(event_number + eventNums_splitting_offset_val) % N == 0` are used for validation. Only used if `use_eventNums_splitting` is `True`.                                                                                                                             |
| `eventNums_splitting_offset_test` *(int)* | `1`           | Controls which subset is used for testing. All events satisfying `(event_number + eventNums_splitting_offset_test) % N == 0` are used for testing. Only applied if `use_eventNums_splitting` and `use_testing_dataset` are `True`.                                                                                                    |
| `validation_fraction` *(float)*           | `0.2`         | Controls the fraction of events used for validation. Only used if `use_eventNums_splitting` is `False`.                                                                                                                                                                                                                               |
| `test_fraction` *(float)*                 | `0.2`         | Controls the fraction of events used for testing. Only used if `use_eventNums_splitting` is `False` and `use_testing_dataset` is `True`.                                                                                                                                                                                              |
| `max_num_events` *(int)*                  | `np.inf`      | Controls the number of events to be loaded from the dataset. `np.inf` corresponds to all available events.                                                                                                                                                                                                                            |

#### Evaluation

| Parameter                          | Default value | Explanation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|------------------------------------|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `monitor_name` *(str)*             | `'val_loss'`  | Controls which metric is used as the target of the optimization and for early stopping during training. Allowed are native, weighted native, custom and composite metrics as well as all metrics reported by the ML backend during training (e.g. `"val_loss"`). Make sure to add the `"val_"`-prefix when using native, weighted native or custom metrics.                                                                                                                                                                                                                                                                                                                                                                |
| `monitor_op` *(str)*               | `'min'`       | Is the target metric to be minimized (`'min'`) or maximized (`'max'`)?                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `native_metrics` *(list)*          | `[]`          | A list of references to a metric class native to the used ML backend. Each entry must be a tuple of the form `("name", (ClassReference, {"kwarg1": kwarg1, ...}))`. Their values are calculated separately on the training and validation datasets and reported as `"train_name" and "val_name". Event weights are not applied.                                                                                                                                                                                                                                                                                                                                                                                            |
| `weighted_native_metrics` *(list)* | `[]`          | A list of references to a metric class native to the used ML backend. Each entry must be a tuple of the form `("name", (ClassReference, {"kwarg1": kwarg1, ...}))`. Their values are calculated separately on the training and validation datasets and reported as `"train_name" and "val_name". Event weights are applied. Currently, weighted metrics are not supported for Lightning (see https://github.com/Lightning-AI/torchmetrics/issues/784).                                                                                                                                                                                                                                                                     |
| `custom_metrics` *(list)*          | `[]`          | A list of custom metrics. Each entry must be a tuple of the form `("name", callable)`. `callable` needs to accept target values, model prediction and sample weights and return a number or a boolean. Their values are calculated at the end of each epoch separately on the training and validation datasets and reported as `"train_name" and "val_name".                                                                                                                                                                                                                                                                                                                                                               |
| `composite_metrics` *(list)*       | `[]`          | A list of composite metrics. These are metrics that combine the values of already existing metrics. Each entry must be a tuple of the form `("name", (metric_name1, metric_name2, ...), callable)` where `callable` accepts the same number of positional arguments as the number of provided metric names and returns a number or a boolean. They are calculated at the end of each epoch and allow all native, weighted native and custom metrics as well as metrics directly reported by the ML backend (e.g. validation loss) as inputs. It is possible to mix training and validation metrics, allowing e.g. to assess the generalization gap. The value of composite metrics is reported as "name" without a prefix. |
| `overtraining_conditions` *(list)* | `[]`          | A list of overtraining conditions. These are special composite metrics that should return `True` when overtraining is detected and `False` otherwise. Each entry must be a tuple of the form `("name", (metric_name1, metric_name2, ...), callable)` where `callable` accepts the same number of positional arguments as the number of provided metric names and returns a boolean. They are calculated at the end of each epoch and allow all native, weighted native, custom and composite metrics as well as metrics directly reported by the ML backend (e.g. validation loss) as inputs. Naturally, it is possible to mix training and validation metrics. The value of overtraining conditions is not reported.      |

#### Training

| Parameter                                | Default value | Explanation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|------------------------------------------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `max_epochs` *(int)*                     | `200`         | The maximal number of epochs until the training is terminated. Early stopping may terminate the training earlier.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `early_stopping_patience` *(int)*        | `6`           | The maximal number of consecutive epochs without an improvement of the target metric before early-stopping the training.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `overtraining_patience` *(int)*          | `6`           | The maximal number of consecutive epochs with overtraining detected (i.e. at least one overtraining condition detected overtraining) before early-stopping the training. This is ignored if no overtraining conditions are defined.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `callbacks` *(list)*                     | `[]`          | A list of references to a callback class native to the used ML backend (i.e. a subclass of `keras.callbacks.Callback` for Keras or `lightning.pytorch.callbacks.Callback` for Lightning. Each entry must be a tuple of the form `(ClassReference, {"kwarg1": kwarg1, ...})`. The callbacks are only used during the training.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `checkpoint_frequency` *(int)*           | `1`           | The number of epochs to wait between consecutive checkpoints for each model. Since this is only useful to restore the training progress if the optimization is interrupted, this should be set so that, on average, a checkpoint is created every few minutes. For the initial and main hyperparameter optimization, the first checkpoint for each trial is created after `checkpoint_frequency` epochs. Since for Population Based Training, a checkpoint must be created after the last epoch in each perturbation interval, the `checkpoint_frequency` is overwritten with the `perturbation_interval`, unless it is divisible by the `checkpointing_frequency`. The first checkpoint will be created after `checkpointing_frequency` epochs if the `burn_in_period` is divisible by the `checkpointing_frequency`, and after `burn_in_period` epochs otherwise. |
| `crossvalidation_for_fixed_hps` *(bool)* | `True`        | If only a fixed set of hyperparameter is to be used (e.g. for testing purposes), this parameter controls if the training of a single model (`False`) or a full cross-validation (`True`) is performed.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |

#### Hyperparameter optimization

##### General

| Parameter                             | Default value                                                                                                                 | Explanation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|---------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `optimize_on_best_value` *(bool)*     | `False`                                                                                                                       | Controls how each trial is evaluated during the hyperparameter optimization. While the target metric is calculated every epoch, *Tune* only allows accepts a single value to evaluate a trial. If `True`, the best epoch that passes all overtraining conditions (which is usually representative of the best performance possible with these hyperparameters, but may also be an outlier) is used. If `False`, the last epoch that passed all overtraining conditions (which is less likely an outlier but may be degraded due to overtraining) is used.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `restore_on_best_checkpoint` *(bool)* | `True`                                                                                                                        | When resuming a trial (e.g. during Population Based Training), resume from the best epoch (`True`) or last epoch (`False`)?                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `num_samples_variableOpt` *(int)*     | `1`                                                                                                                           | The number of trials (hyperparameter combinations) to try during the initial hyperparameter optimization step.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `num_samples_main` *(int)*            | `1`                                                                                                                           | The number of trials (hyperparameter combinations) to try during the main hyperparameter optimization step.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `num_samples_PBT` *(int)*             | `4`                                                                                                                           | The number of trials in the population for the hyperparameter fine-tuning step with Population Based Training.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `search_space` *(dict)*               | see [here](https://gitlab.cern.ch/atlas-germany-dresden-vbs-group/optima/-/blob/master/OPTIMA/defaults.py?ref_type=heads#L42) | Defines the hyperparameter search space. Each dictionary entry corresponds to a hyperparameter, and the corresponding search space is defined using a dictionary with the following allowed key-value pairs:<br><ul><li>`'type'`: Specifies if a range of values (`'range'`) or a list of allowed values (`'choice'`) defines the search space.</li><li>`'bounds'`: Specifies the lower and upper bounds for range search spaces. This can be given as a list or tuple of type `(lower_bound, upper_bound)`. Alternatively, conditional bounds that depend on the values of other hyperparameters can be specified as a tuple of type `(hp_depends_tuple, callable)`. Here, `hp_depends_tuple` is a tuple of hyperparameters the bounds depend on (i.e. each entry must correspond to another key in the search space). The `callable` will be provided with the values of the hyperparameters specified in `hp_depends_tuple` as positional arguments and needs to return a list or tuple of type `(lower_bound, upper_bound)`. Conditional bounds are not supported for Population Based Training. This is only used for range search spaces.</li><li>`'value_type'`: Specifies if an integer (`'int'`) or float (`'float'`) value should be suggested. Defaults to `'float'`. This is only used for range search spaces.</li><li>`'sampling'`: Specifies if the search space should be sampled uniformly (`'uniform'`), logarithmically (`'log'`) or gaussian distributed (`'normal'`). Gaussian sampled integer search spaces are not supported. Defaults to `'uniform'`. This is only used for range search spaces.</li><li>`'mean'`: Specifies the mean of the gaussian sampling. This can be given as a float or integer. Only used for range search spaces and `'sampling'` set to `'normal'`.</li><li>`'std'`: Specifies the standard deviation of the gaussian sampling. This can be given as a float or integer. Only used for range search spaces and `'sampling'` set to `'normal'`.</li><li>`'step'`: Used to quantize range search spaces. For integer search spaces, this must be an integer. For float search spaces, this can be an integer or a float. For log-sampled search spaces, setting a step size is not supported. Defaults to `None` (i.e. unquantized) for float and `1` for integer parameters. This is only used for range search spaces.</li><li>`'values'`: Specifies the allowed values for choice search spaces. This can be a list or a tuple. Alternatively, conditional values that depend on the values of other hyperparameters can be specified as a tuple of type `(hp_depends_tuple, callable)`. Here, `hp_depends_tuple` is a tuple of hyperparameters the values depend on (i.e. each entry must correspond to another key in the search space). The `callable` will be provided with the values of the hyperparameters specified in `hp_depends_tuple` as positional arguments and needs to return a list or tuple of allowed values. Conditional values are not supported for Population Based Training. This is only used for choice search spaces.</li><li>`'supports_mutation'`: A `bool` that specifies if this hyperparameter can be altered during the training without loosing the training state. Only these hyperparameters can be optimized with Population Based Training. The remaining hyperparameters will be fixed to the best value found during the previous hyperparameter optimization step. If only the Population Based Training step is performed, all hyperparameters need to be fixed or mutatable.</li><li>`'only'`: Used to build hierarchical search spaces where not all hyperparameters are always needed (e.g. the number of neurons in the fourth layer are only needed if the number of layers is at least four). If provided, this needs to be a tuple of type `(hp_depends_tuple, callable)`. Here, `hp_depends_tuple` is a tuple of hyperparameters that are necessary to decide if this hyperparameter is needed (i.e. each entry must correspond to another key in the search space). The `callable` will be provided with the values of the hyperparameters specified in `hp_depends_tuple` as positional arguments and needs to return a `bool` that signifies if a value should be suggested for this hyperparameter. If the condition is evaluated as `False`, the value if the hyperparameter is explicitly set to `None` and provided as such to all conditions that depend on this hyperparameter. This allows defining multiple dependency layers where, e.g., `B` is only needed if `A > 0` and `C` is only needed if `B` exists and `B > 0`. Rejected hyperparameters will, however, not be added to the `model_config`. Hierarchical search spaces are not supported for Population Based Training.</li></ul>Any search space entry that is not a dictionary is considered fixed and the corresponding hyperparameter will not be optimized but still added to the `model_config`. Being independent of the particular task, the batch size (with key `'batch_size'`) must always be provided as a hyperparameter, either as a fixed integer or as an integer range search space. |


##### Bayesian optimization (Optuna)

| Parameter                       | Default value | Explanation                                                                                                                                |
|---------------------------------|---------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| `use_TPESampler` *(bool)*       | `True`        | Use Optuna's Tree-structured Parzen Estimator algorithm or random sampling?                                                                |
| `use_multivariate_TPE` *(bool)* | `False`       | Use the multivariate or the independent version of the TPESampler?                                                                         |
| `use_ASHAScheduler` *(bool)*    | `True`        | Use the Asynchronous HyperBand scheduler (ASHA) to prune trials or not?                                                                    |
| `ASHA_grace_period` *(int)*     | `15`          | The minimum number of epochs to wait before the ASHA scheduler is allowed to prune a trial. Only used if `use_ASHAScheduler` is `True`.    |
| `ASHA_max_t` *(int)*            | `max_epochs`  | The end point of the reduction with ASHA. Only used if `use_ASHAScheduler` is `True`.                                                      |
| `ASHA_reduction_factor` *(int)* | `2`           | Controls which fraction of trials is terminated at each point by ASHA. A value of `2` corresponds to the termination of 50% of all trials. |

##### Population Based Training

| Parameter                          | Default value | Explanation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|------------------------------------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `use_fit_results_for_PBT` *(bool)* | `True`        | PBT is only applied to hyperparameters that are marked with `'supports_mutation'` set to `True`. If the initial and/or main hyperparameter optimization step was run before, all unsupported hyperparameters are fixed to their optimized values from the previous optimization step. If `use_fit_results_for_PBT` is `True`, the best-fit results are used, otherwise the best-value results are used. If only the PBT step is performed, all provided hyperparameters need to be fixed or support mutation. |
| `perturbation_interval` *(int)*    | `6`           | The number of epochs to train between each perturbation of a trial.                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `burn_in_period` *(int)*           | `6`           | The number of epochs to wait before the first perturbation of a trial.                                                                                                                                                                                                                                                                                                                                                                                                                                        |

#### Trial selection

To select the best set of hyperparameters and the number of epochs to train from the pool of tested trials, two
independent algorithms are used:

- **best-value**: the best trial is given by the best reported value of the target metric (i.e. best single epoch) while
passing all overtraining conditions.
- **best-fit**: the evolution of all reported metrics of all trials is fitted. The best trial is given by the best-fit
function value of the fitted target metric while passing all overtraining conditions.

| Parameter                              | Default value | Explanation                                                                                                                                                                                                                                                   |
|----------------------------------------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `check_overtraining_with_fit` *(bool)* | `True`        | Controls how the overtraining conditions are evaluated during the best-fit selection. If `True`, the fit function values of all metrics are given to the overtraining conditions. If `False`, the raw metric values are given to the overtraining conditions. |

#### Cross-validation

| Parameter                                         | Default value | Explanation                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|---------------------------------------------------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `use_early_stopping_for_crossvalidation` *(bool)* | `False`       | If `True`, the maximum number of epochs is kept unchanged (`max_epochs`) and the training can be terminated by early stopping with the same settings as used during the hyperparameter optimization (see [here](#training)). If `False`, early stopping only monitors the overtraining conditions but ignores the evolution of the target metric. In this case, the maximum number of epochs is set to the best-value found during the trail selection. |
| `use_OT_conditions_for_crossvalidation` *(bool)*  | `False`       | If `True`, the overtraining conditions are evaluated like during the hyperparameter optimization. If `False`, the overtraining conditions are not evaluated.                                                                                                                                                                                                                                                                                            |
| `reuse_seed_for_crossvalidation` *(bool)*         | `False`       | If `True`, will use the same random seed as during the hyperparameter optimization for all folds. For the fold that was used during the hyperparameter optimization, this should reproduce the same training progression. If `False`, new seeds are generated.                                                                                                                                                                                          |
| `fixed_seed_for_crossvalidation` *(bool)*         | `False`       | If `True`, each fold will use the same random seed. If `False`, a new random seed is generated for each fold. Only used if `reuse_seed_for_crossvalidation` is `False`.                                                                                                                                                                                                                                                                                 |

#### Input variable selection

Since all training during the input variable selection is done by performing a cross-validation, the [corresponding
settings](#cross-validation) also affect the result of the input variable selection.

| Parameter                                      | Default value   | Explanation                                                                                                                                                                                                                                                                                                   |
|------------------------------------------------|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `var_metric` *(str)*                           | `'loss'`        | Which metric should be used to check the DNN performance during the input variable selection? Allowed are `'loss', which uses binary crossentropy loss, or the name of any native, weighted native or custom metric.                                                                                          |
| `var_metric_op` *(str)*                        | `'min'`         | Is the target metric for the input variable selection to be minimized (`'min'`) or maximized (`'max'`)?                                                                                                                                                                                                       |
| `variable_optimization_mode` *(str)*           | `'hybrid'`      | Which algorithm to use to evaluate the variable importance. Possible values are `'retrain'`, `'shuffle'`, `'hybrid'` and `'custom'`. See [here](https://optima-docs.docs.cern.ch/core/variable_optimization.html#OPTIMA.core.variable_optimization.perform_variable_optimization) for more details.           |
| `acceptance_criterion` *(str)*                 | `'improvement'` | Which criterion to use for deciding if an iteration should be accepted. Possible values are `'theshold'`, `'improvement'` and `'degradation'`. See [here](https://optima-docs.docs.cern.ch/core/variable_optimization.html#OPTIMA.core.variable_optimization.perform_variable_optimization) for more details. |
| `max_rel_change` *(float)*                     | `0.5`           | The threshold for how much the metric value is allowed to degrade before the input variable selection is stopped (relative difference). Positive values correspond to worse metric values. Only used if `acceptance_criterion` is set to `'theshold'`.                                                        |
| `var_opt_patience` *(int)*                     | `3`             | Early-stopping-like patience to terminate the input variable selection once a certain number of consecutive iterations were not accepted.                                                                                                                                                                     |
| `choose_best_var_set` *(bool)*                 | `True`          | If `True`, the set of input variables that resulted in the best target metric will be used as the result of the input variable selection. If `False`, the last accepted set will be used.                                                                                                                     |
| `hybrid_revert_to_best_before_switch` *(bool)* | `True`          | If `True`, the input variable selection is reverted to the best iteration before switching to the retrain-phase. If `False`, only revert to the last accepted iteration. Only used if `variable_optimization_mode` is `'hybrid'`.                                                                             |
| `num_repeats` *(int)*                          | `5`             | How often should each variable set be evaluated per iteration?                                                                                                                                                                                                                                                |
| `num_repeats_hybrid_retrain` *(int)*           | `1`             | How often should each variable set be evaluated per iteration in the retrain-phase of hybrid mode? Only used if `variable_optimization_mode` is `'hybrid'`.                                                                                                                                                   |
| `reevaluate_candidate_to_drop` *(bool)*        | `True`          | If `True`, the best variable set in each iteration is re-evaluated before deciding if the iteration should be accepted. If `False`, the metric values from the original evaluation are used.                                                                                                                  |
| `retrain_for_reevaluation` *(bool)*            | `True`          | If `True`, the retrain-method is used to evaluate the best variable set during the re-evaluation instead of the original evaluation method. Only used if `reevaluate_candidate_to_drop` is `True`.                                                                                                            |
| `num_repeats_for_reevaluation` *(int)*         | `2`             | The often should the best variable set be re-evaluated? Only used if `reevaluate_candidate_to_drop` is `True`.                                                                                                                                                                                                |
| `use_median_for_averages` *(bool)*             | `False`         | If `True`, use the median and MAD to calculate averages and uncertainties across the `k` folds, otherwise use mean and standard deviation.                                                                                                                                                                    |
| `use_fit_results_for_varOpt` *(bool)*          | `True`          | Whether to use the best-fit (`True`) or best-value (`False`) results of the trial selection of the initial hyperparameter optimization as the basis of the input variable selection.                                                                                                                          |

#### Lightning

When using Lightning, the Lightning model, i.e. the `LightningModule`-subclass, must be defined with name `LitModel`
in the run-config. Its constructor must accept the following parameters:

- `model_config`: a dictionary containing the values of the hyperparameters using the same keys as used in the `search_space`
- `input_shape`: the shape of the input features. The first axis corresponds to the number of entries in the training dataset.
- `output_shape`: the shape of the model output. The first axis corresponds to the number of entries in the training dataset.
- `metrics`: a list of initialized metrics and corresponding names. Each entry is a tuple of the form `(name, metric)`
where `name` is the name given in `native_metrics` plus a `'train_'` / `'val_'` prefix and `metric` is the corresponding
initialized metric.
- `weighted_metrics`: a list of initialized weighted metrics and corresponding names. Each entry is a tuple of the form
`(name, metric)` where `name` is the name given in `native_metrics` plus a `'train_'` / `'val_'` prefix and `metric` is
the corresponding initialized metric.

Within the constructor, `self.save_hyperparameters()` needs to be called in order to include the hyperparameters in the
saved checkpoints.

In addition to the usual functions (`configure_optimizers`, `forward`, `training_step`, `validation_step`, `test_step`,
`predict_step`, `on_train_epoch_end`, `on_validation_epoch_end`), `LitModel` must implement a `prepare()`-function which
needs to accept the following parameters:

- `input_handler`: a reference to the InputHandler instance
- `inputs_train`: a numpy array of the input features of the training dataset
- `targets_train`: a numpy array of the target labels of the training dataset
- `first_prepare`: a bool, signifying if this is the first time calling this model's `prepare()`-function

This function is called after creating a model (with `first_prepare` set to `True`) and after reloading a model from a
checkpoint (with `first_prepare` set to `False`). It can e.g. be used to adapt a normalization layer.

It is expected that the validation loss is logged with key `'val_loss'` and all metrics and weighted metrics are
logged with the name provided in `metrics` and `weighted_metrics`, respectively.

#### Custom Keras objects

If your Keras model uses custom objects, they cannot be defined directly in the run-config for technical reasons. Instead,
define your custom objects in a separate module and import it into your run-config. Additionally, all custom objects need
to be registered to Keras using the `@tf.keras.saving.register_keras_serializable(...)`-decorator in order to allow
loading the saved checkpoints.

#### Cluster setup

These options are only used when running on a cluster.

| Parameter                        | Default value | Explanation                                                                                                                         |
|----------------------------------|---------------|-------------------------------------------------------------------------------------------------------------------------------------|
| `path_to_setup_file` *(str)*     | None          | Path to a sourceable file that sets up the python environment. This path can be absolute or relative to the directory of execution. |

### Built-in functionality

---

Built-in functionality can be overwritten by defining a new function or class in the run-config with the same name as the
component that should be overwritten.

All functions defined in the run-config must accept the same arguments and return the same type of return value as the
built-in function they are replacing unless otherwise specified.

All classes defined in the run-config must implement the same methods as the built-in class they are replacing. Like
functions, the constructor and all class methods must accept the same arguments and return the same type of return value
as the built-in counterpart, unless otherwise specified.

All overwritable components are collected in the following sections. If a built-in components uses parameters in the
run-config, they are collected in a table in the corresponding section.

#### Keras

Both the built-in `build_model` and `compile_model` functions provide default values for their required hyperparameters.
If a hyperparameter is omitted from the search space, it will be fixed to its default value. Additionally, for
hyperparameters that support mutation (all hyperparameters of the `compile_model` function and those updated by the
`update_model` function), search space entries that do not explicitly set the `supports_mutation` flag will be updated
with this flag set to `True`. If either of the two functions is overwritten, this behavior is of cause disabled for the
corresponding hyperparameters.

##### build_model

A function that builds a Functional Keras multilayer perceptron for provided hyperparameter values. Supported
hyperparameters and corresponding default values are:

- `'num_layers'`: the number of hidden layers. Default: `3`
- `'units'`: the number of neurons per hidden layer (constant for all layers). Default: `32`
- `'units_i'`: the number of neurons in hidden layer `i`, counting from 1 (has higher priority than `'units'`). Default: `None`
- `'activation'`: the activation function. Default: `'swish'`
- `'kernel_initializer'` and `'bias_initializer'`: initializers of the weights and biases of the hidden layers. Defaults: `'auto'`
- `'l1_lambda'` and `'l2_lambda'`: the strength of the L1 and L2 regularizations. Defaults: `0.0`
- `'dropout'`: the dropout rate. Default: `0.1`

The input variables are normalized using a custom non-linear normalization layer, whose documentation can be found
[here](https://optima-docs.docs.cern.ch/keras/tools.html#OPTIMA.keras.tools.NonLinearNormalization). This layer first
applies the non-linear transformations returned by the `get_nonlinear_scaling`-function of the [InputHandler](#inputhandler);
supported are $\sqrt{\bullet}$, $\log_{10}(\bullet)$ or the identity. After that, a linear transformation to achieve
zero mean and unit variance for all input features on the training dataset is applied. A batch normalization layer is
added between each hidden layer unless the SELU activation function is used. The number of nodes in the output layer is
controlled by the provided `output_shape` parameter. For a single output node, a sigmoid activation is applied while a
softmax activation is used for more than one output node. As such, this MLP is suitable for classification tasks. The
returned Keras model is not yet compiled. More details can be found
[here](https://optima-docs.docs.cern.ch/keras/model.html#OPTIMA.keras.model.build_model).

##### compile_model

A function that compiles the provided Keras model. It is called after creating a new model by executing the
`build_model`-function (with parameter `first_compile` set to `True`) and after reloading a model from a checkpoint
(with parameter `first_compile` set to `False`). It uses the Adam optimizer with the following tunable hyperparameters
(see https://arxiv.org/abs/1412.6980v9 for the Adam update rule):

- `'learning_rate'`: $\alpha$. Default: `0.001`
- `'Adam_beta_1'`: $\beta_1$. Default: `0.9`
- `'one_minus_Adam_beta_2''`: $1 - \beta_2$. Default: `0.001`
- `'Adam_epsilon'`: $\varepsilon$. Default: `1e-7`

Supported loss functions, set using the hyperparameter `'loss_function'`, are binary crossentropy loss
(`'BinaryCrossentropy'`), categorical crossentropy loss (`'CategoricalCrossentropy'`), and Kullback–Leibler divergence
loss (`'KLDivergence'`). By default, binary crossentropy loss is used. For all available loss functions, the loss values
can be weighted using class weights, controlled via hyperparameters of type `'loss_weight_class_N'` with `N`
corresponding to the `N`-th class.

If an already compiled model is provided, the loss function and the parameters of the Adam optimizer are updated without
losing the training state of the model. This functionality is needed to allow mutations during the Population Based
Training step.

For more details, see the documentation [here](https://optima-docs.docs.cern.ch/keras/model.html#OPTIMA.keras.model.compile_model)

##### update_model

A function that updates all updatable hyperparameters (besides the ones that are updated in the `compile_model` function)
of a given pretrained Keras model without losing the training state. It is called only after reloading a model from a
checkpoint. This is needed to allow mutations during the Population Based Training step. This function is specific to
the MLP built with the built-in `build_model` function and, as such, allows to update the following hyperparameters:

- `'l1_lambda'`
- `'l2_lambda'`
- `'dropout'`

After the update, the model is compiled for the changes to take effect. For more details, see the documentation
[here](https://optima-docs.docs.cern.ch/keras/model.html#OPTIMA.keras.model.update_model).

#### Inputs

##### InputHandler

A helper class that keeps track of which input variables are currently used and which non-linear scalings are being
applied to each of them. It supports arbitrary N-dimensional numpy arrays as inputs per event. Individual input
variables can be referenced via a name or an index. Details can be found
[here](https://optima-docs.docs.cern.ch/builtin/inputs.html#OPTIMA.builtin.inputs.InputHandler).

| Parameter                | Default value | Explanation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|--------------------------|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `input_vars` *(list)*    | None          | A list of strings corresponding to the input variables that should be given to the model (before the input variable selection). If provided, this is the list that is returned by the `get_vars()`-method of the `InputHandler` (before the input variable selection). If not provided, all available input variables are used.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `input_scaling` *(dict)* | None          | A dictionary of scalings to be applied to each input variable. The key of each item must either be a variable name present in `input_vars` or encode the index of an input (e.g. `'1_2_3'` encodes the input variable with index `(1, 2, 3)`). The value must be a tuple of type `(scale_type, (scale, offset))` where `scale_type` specifies the type of non-linear scaling to apply (e.g. $\log_{10}(\bullet)$) and `scale` and `offset` specify a linear transformation to apply before applying the non-linearity. For each variable in `input_vars` (if provided) without an entry in `input_scaling`, the value is set to `('linear', (1., 0.))`. The resulting dictionary is returned when calling the `InputHandler`'s `get_nonlinear_scaling`-function. Which values are supported for `scale_type` depends on the implementation used to perform the input scaling. When using the built-in non-linear normalization layer, refer to [the documentation](https://optima-docs.docs.cern.ch/keras/tools.html#OPTIMA.keras.tools.NonLinearNormalization) for details. |

##### get_inputs

A function that loads the input dataset from a `.pickle`-file. It expects a vector of input variables per event, event
weights, event numbers and binary or one-hot encoded target labels for classification to be present in the dataset. The
documentation can be found [here](https://optima-docs.docs.cern.ch/builtin/inputs.html#OPTIMA.builtin.inputs.get_inputs).

| Parameter                     | Default value | Explanation                                                                                                                                                                      |
|-------------------------------|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `inputs_file` *(str)*         | None          | A path to the `.pickle`-file containing the input dataset.                                                                                                                       |
| `max_event_weight` *(float)*  | `np.inf`      | The maximum relative event weight. Events with a weight larger than `max_event_weight` times the median weight are repeatedly duplicated and the corresponding weight is halved. |

##### get_training_data

A function that splits the input dataset into training, validation and testing samples. It supports arbitrary
N-dimensional numpy arrays as inputs and targets. For both, the first axis is expected to separate different events. It
implements random splitting or splitting based on event numbers and a callable splitting condition. In both cases, a
single splitting or k-fold splitting is possible. Documentation can be found
[here](https://optima-docs.docs.cern.ch/builtin/inputs.html#OPTIMA.builtin.inputs.get_training_data). While still
present in the built-in function, the `preprocessor` argument is not used anymore and does not need to be present in the
overwritten version.

##### plot_input_data

A function that creates histograms of the distributions of each input variable for each target class. It can only be
used for classification tasks and expects a vector of input variables and corresponding binary or one-hot encoded target
label per event. Documentation can be found
[here](https://optima-docs.docs.cern.ch/builtin/inputs.html#OPTIMA.builtin.inputs.plot_input_data).

| Parameter                          | Default value              | Explanation                                                                                                             |
|------------------------------------|----------------------------|-------------------------------------------------------------------------------------------------------------------------|
| `evaluation_class_labels` *(list)* | `["Signal", "Background"]` | A list of labels for each of the classes in the order of the target label vector. This is only used to label the plots. |

##### LightningDataset

A class that stores the input features, target labels and event weights that is needed when performing an optimization with Lightning.
By default, pytorch's `torch.utils.data.TensorDataset` is used. If the `LightningDataset` is defined in the run-config,
its constructor is provided with the dictionary containing the model parameters (including the batch size) as well as
two (inputs and targets) or three (inputs, targets and event weights) tensors as positional arguments. OPTIMA also
provides a built-in tensor dataset with in-memory batching at `OPTIMA.lightning.inputs.LightningDataset` which is,
however, not used by default.

##### DataLoader

A class that retrieves the features, labels and weights from the dataset that is needed when performing an optimization with Lightning.
By default, pytorch's `torch.utils.data.DataLoader` is used. If the `DataLoader` is defined in the run-config, its
constructor is provided with the dataset and the dictionary of hyperparameters (including the batch size) as positional
arguments.

##### DataModule

A subclass of Lightning's `LightningDataModule` that encapsulates all steps needed to process data that is needed when performing an
optimization with Lightning. The built-in `DataModule` provides a bare-bones implementation by combining input features,
target labels and event weights for training, validation and testing into dataset and wrapping them in dataloaders. The
documentation can be found [here](https://optima-docs.docs.cern.ch/lightning/inputs.html#OPTIMA.lightning.inputs.DefaultDataModule).

#### Trial selection

##### fit_function

To perform the best-fit trial selection, the function

$$
f(x) = \frac{a}{x^2} + \frac{b}{x} + c x^2 + d x + \mathrm{const.}
$$

is fitted to the evolution of each metric as a function of epochs using least-squares as implemented by scipy's
`curve_fit` function. All trials with less than 10 metric values (i.e. trained for less than 10 epochs) are skipped to
prevent overfitting of the fit function. This behaviour can be overwritten by defining a `fit_function` function in the
run-config that accepts the following parameters as positional arguments:

- `df`: A pandas dataframe of metric values. All reported metrics are contained as columns. The epoch is contained as
column `training_iteration`.
- `metric_to_fit`: A string containing the name of the metric to fit.
- `metric_to_fit_op`: Either `'min'`, `'max'` or `None`. If `metric_to_fit` is the target metric `monitor_name`, this
is equal to `monitor_op`. For any other metric, this parameter will be `None`.
- `overtraining_conditions`: The list of overtraining conditions `overtraining_conditions` as defined in the run-config.

`fit_function` is expected to return a callable that returns the fit function value when called and provided with an epoch
number as a positional argument.

| Parameter                              | Default value | Explanation                                                                                                                                                                                                                 |
|----------------------------------------|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `fit_min_R_squared` *(float)*          | `0.9`         | To evaluate the goodness of fit, the R-squared value of each fit is calculated. If any of the fits for a trial have an R-squared value lower than `fit_min_R_squared`, the trial is disregarded for the best-fit selection. |

#### Evaluation

##### evaluate

A function that evaluates the performance of the trained models. Supported are classification tasks with binary or
one-hot encoded target labels. While the model predictions are calculated using the batched inputs as during the
training of the model, it is assumed that the aggregated model predictions for the entire dataset can fit into memory,
and that all metrics can be calculated without batching. The evaluation functions draws histograms of:

- **stacked output distributions**: The model predictions for each output are calculated on the testing dataset (if present,
on the validation dataset otherwise) and stacked for each target class. The contribution of each class is normalized to
its total weight in the event weights.
- **normalized output distributions**: The model predictions for each output are calculated on the training, validation
and (if present) testing datasets. The output distributions for each target class is normalized to area 1. For each
class, a ratio of the validation and testing distributions to the training distributions is calculated.
- **ROC-curves**: A ROC-curve is calculated for each output in a One-vs-Rest scheme on the training, validation and
testing datasets. Since negative weights can cause the ROC-curve to be non-monotonic, all events with negative event
weights are ignored.

Additionally, the loss and all metric values are calculated on the training, validation and testing datasets. The `evaluate`
function is expected to return a results string with placeholders `{}` in place of metric values (e.g.
`"Loss (training): {}"`) as well as a list of corresponding metric values. This allows to average the results over the
individual crossvalidation folds.

Further documentation can be found [here](https://optima-docs.docs.cern.ch/builtin/evaluation.html#OPTIMA.builtin.evaluation.evaluate).

| Parameter                           | Default value              | Explanation                                                                                                              |
|-------------------------------------|----------------------------|--------------------------------------------------------------------------------------------------------------------------|
| `evaluation_class_labels` *(list)*  | `["Signal", "Background"]` | A list of labels for each of the classes in the order of the target label vector. This is only used to label the plots.  |

##### finalize_model

A helper function that can be used to perform finalization tasks, e.g. exporting the model to a different format. The
`finalize` function is called for each crossvalidation model and is provided with the following arguments:

- `run_config`: A reference to the run-config.
- `inputs_split`: A list of Ray `ObjectReference`s to the input features on the training, validation and (if present)
testing datasets. Calling `ray.get(inputs_split)` will return the list of corresponding numpy arrays.
- `targets_split`: A list of Ray `ObjectReference`s to the target values on the training, validation and (if present)
testing datasets. Calling `ray.get(inputs_split)` will return the list of corresponding numpy arrays.
- `weights_split`: A list of Ray `ObjectReference`s to the event weights on the training, validation and (if present)
testing datasets. Calling `ray.get(inputs_split)` will return the list of corresponding numpy arrays.
- `normalized_weights_split`: A list of Ray `ObjectReference`s to the normalized event weights on the training,
validation and (if present) testing datasets. Calling `ray.get(inputs_split)` will return the list of corresponding
numpy arrays.
- `results_dir`: A path to the results directory for this optimization step.
- `model_dir`: A path to the directory the current model is saved in. This directory is shared by all crossvalidation
models of the same trial (i.e. all best-value and all best-fit models).
- `model_info`: A dictionary containing information of the current model:
  * `'name'`: The file name of the current model. This must be appended with `'.keras'` for Keras models and `'.ckpt'`
    for lightning models.
  * `'split`: An index denoting which of the `k` crossvalidation model this is. This ranges from `0` to `k-1`.
  * `'config'`: A dictionary containing the hyperparameter values of the current model.
- `input_handler`: A reference to the InputHandler instance.

#### Input variable selection

##### create_variable_sets_to_try

A function that generates the sets of input variables to evaluate for each iteration of the input variable selection.
By default, each leave-one-out subset of the remaining set of input variables is tested. To overwrite this behavior, a
`create_variable_sets_to_try` function that accepts the following parameters needs to be defined in the run-config:

- `model_config`: The dictionary of hyperparameters.
- `models_with_inputs`: A list of tuples, with one entry for each crossvalidation model. Each tuples is of the form
`(model_path, input_vars, (inputs, targets, normalized_weights))` where
    * `model_path`: The full path to the saved model file.
    * `input_vars`: The list of input variables that are needed for this model, in the correct order.
    * `inputs`: A Ray `ObjectReference` to the numpy array of input features of this model's validation dataset.
    * `targets`: A Ray `ObjectReference` to the numpy array of target labels of this model's validation dataset.
    * `normalized_weights`: A Ray `ObjectReference` to the numpy array of normalized event weights of this model's
    validation dataset.
- `metric`: A callable that, given numpy arrays of target labels, model predictions and optimal event weights as positional
arguments, returns the value of the target metric.
- `all_vars`: A list of all input variables that were available at the beginning of the input variable selection.
- `vars_remaining`: A list of input variables that is still remaining in the current iteration.

The `create_variable_sets_to_try` must return a dictionary containing all sets of input variables that should be tried
this iteration. The keys for each variable set are used to label the obtained results.

##### evaluate_variable_importance

A function that evaluates the model performance for a given list of input variable sets. Two built-in algorithms for this
are available, based on shuffling the input values (see
[here](https://optima-docs.docs.cern.ch/core/variable_optimization.html#OPTIMA.core.variable_optimization.evaluate_vars_shuffle))
and based on retraining the models with different input variables (see
[here](https://optima-docs.docs.cern.ch/core/variable_optimization.html#OPTIMA.core.variable_optimization.evaluate_vars_retrain)).
To use a different evaluation algorithm, a `evaluate_variable_importance` function needs to be defined in the run-config
and `variable_optimization_mode` must be set to `'custom'`. The `evaluate_variable_importance` is expected to accept the
same parameters as `OPTIMA.core.variable_optimization.evaluate_vars_shuffle` and
`OPTIMA.core.variable_optimization.evaluate_vars_retrain`. It must return a dictionary contains the values of the
target metric for each tested input variable set. For further details, see the documentations of the two built-in
algorithms linked above.

##### update_models_with_inputs

A function that updates the `models_with_inputs` object at the end of each iteration. This is necessary if the existing
models are altered, e.g. by retraining, to make sure that the evaluation is based on the most recent model version in
each iteration. For the built-in algorithms, this is done automatically if a re-evaluation using the retrain method is
performed. If this is necessary for a custom evaluation method, a `update_models_with_inputs` function needs to be
defined in the run-config that accepts the following arguments:

- `run_config`: A reference to the run-config.
- `model_config`: The dictionary of hyperparameters.
- `input_handler`: A reference to the InputHandler instance.
- `all_vars`: A list of all input variables that were available at the beginning of the input variable selection.
- `best_var_set`: A dictionary containing the best performing input variable set of this iteration. The same key is used
as in the dictionary of input variable sets to try.
- `output_path_evaluation`: The path to the temporary output directory of this iteration that was given to the
`evaluate_variable_importance` function as parameter `temp_output_path`.

It is expected to return an updated `models_with_inputs` dictionary of the same form as created by
`OPTIMA.core.variable_optimization.get_models_with_inputs`.
