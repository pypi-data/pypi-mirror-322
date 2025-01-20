.. image:: https://img.shields.io/pypi/v/UnPaAc.svg
    :target: https://pypi.python.org/pypi/UnPaAc
    :alt: Latest Version


# UnPaAc - Uncertainties Pandas Accessors

This python package provides accessors to handle quantities with uncertainties in
pandas `Series` and `DataFrame` objects using the packages [`Pint`](https://github.com/hgrecco/pint)
and [`Uncertainties`](https://github.com/lebigot/uncertainties).
The accessors combine some of the functionalities provided by the pandas
integrations [`pint-pandas`](https://github.com/hgrecco/pint-pandas) and
[`uncertainties-pandas`](https://github.com/andrewgsavage/uncertainties-pandas/tree/main).


```{warning}
The project is currently under development and changes in its behaviour might be introduced.
```

## Installation

<!-- Install UnPaAc simply via `pip`: -->

<!-- ```sh -->
<!-- $ pip install unpaac -->
<!-- ``` -->

The package is currently not available via PyPI, but can be installed it from
[its Git repository](https://codeberg.org/Cs137/unpaac) using pip:

```sh
# Via https
pip install git+https://codeberg.org/Cs137/unpaac.git

# Via ssh
pip install git+ssh://git@codeberg.org:Cs137/unpaac.git
```

### Installing for development

To install the package in development mode, clone the Git repository and install
the package using Poetry, as shown in the code block underneath. To install Poetry,
which is required for virtual environment and dependency management, follow the
instructions on the [Poetry website](https://python-poetry.org/docs/#installation).

```bash
git clone https://codeberg.org/Cs137/unpaac.git
cd unpaac
poetry install
```

This will create a virtual environment and install the package dependencies and
the package itself in editable mode, allowing you to make changes to the code and
see the effects immediately in the corresponding virtual environment. Alternatively,
you can install it via `pip install -e` in an existing virtual environment.


## Usage

Import `unpaac.uncrts` in order to make use of the `Series` and/or `DataFrame`
accessors. They are available via the `uncrts` attribute of instances of the
aforementioned object classes.

If you have any questions or need assistance, feel free to
[open an issue on the repository](https://codeberg.org/Cs137/unpaac/issues).

### Examples

#### Create a Pint Series

A pandas Series that holds a PintArray can be created via the `create_pint_series` function.
The creation with the mandatory attributes `values` and `unit`, is shown underneath.

```python
from unpaac.uncrts import create_pint_series

p_series = create_pint_series([1.0, 2.0, 3.0], "mg")
print(p_series)
0    1.0
1    2.0
2    3.0
dtype: pint[milligram][Float64]
```

Optionally, you can declare `uncertainties` and/or further keyword arguments that
are passed to the pandas Series constructor, like e.g. a `name`.
If uncertainties are provided, an UncertaintyArray is created, which is nested
in the PintArray that is assigned to the values of the created series.

```python
pu_series = create_pint_series([1.0, 2.0, 3.0], "m", uncertainties=[0.1, 0.2, 0.3], name="length")
print(pu_series)
0    1.00+/-0.10
1    2.00+/-0.20
2    3.00+/-0.30
Name: length, dtype: pint[meter][UncertaintyDtype]
```

#### Access nominal values and standard deviations in a Pint Uncertainty Series

You can access the nominal values and standard deviations via the series accessors
properties `nominal_values` and `std_devs`, or their shortcuts `n` and `s`, respectively.

```python
pu_series.uncrts.n
0    1.0
1    2.0
2    3.0
Name: length, dtype: pint[meter][Float64]

pu_series.uncrts.s
0    0.1
1    0.2
2    0.3
Name: δ(length), dtype: pint[meter][Float64]
```

The method `to_series` returns a tuple with both pint series, nominal values and
standard deviations.

#### Add Uncertainties to a pint Series in a DataFrame

The DataFrame accessor allows to assign uncertainties to a column that holds a
pint series via the `add` method, as shows underneath.

```python
df = pd.DataFrame({"mass": p_series})
df.uncrts.add("mass", [0.1, 0.2, 0.3])
print(df)
          mass
0  1.00+/-0.10
1  2.00+/-0.20
2  3.00+/-0.30
```

#### Deconvolute Columns

The `deconvolute` method allows to split a column with a pint uncertainty series
into separate columns for nominal values and uncertainties.

```python
deconv_df = df.uncrts.deconvolute()
print(deconv_df)
   mass  δ(mass)
0   1.0      0.1
1   2.0      0.2
2   3.0      0.3
```

#### Convolute Columns

The `convolute` method allows to to combine nominal value and uncertainty columns
from separate columns into a single column.

```python
deconv_df.uncrts.convolute()
          mass
0  1.00+/-0.10
1  2.00+/-0.20
2  3.00+/-0.30
```

### Save a DataFrame to CSV and restore DataFrame from CSV

After using the `deconvolute` method to split a column with a `PintArray` into
nominal values and uncertainties, you can save the data to CSV. However, you must
first apply `pint.dequantify()` to add units to the columns before saving.
When reading the data back, use `pint.quantify()` to restore the units, followed
by the `convolute` method to combine the nominal values and uncertainties again.

#### Example Workflow

```python
# Dequantify deconvoluted DataFrame to add units to it before saving as CSV
df_dequantified = deconv_df.pint.dequantify()
df_dequantified.to_csv("data_with_uncertainties_and_units.csv")

# Read back
df_read = pd.read_csv("data_with_uncertainties_and_units.csv", header=[0,1], index_col=0)
print(df_read)
          mass   δ(mass)
unit milligram milligram
0          1.0       0.1
1          2.0       0.2
2          3.0       0.3

# Restore units
df_quantified = df_deconvoluted.pint.quantify(level=-1)
print(df_quantified)
   mass  δ(mass)
0   1.0      0.1
1   2.0      0.2
2   3.0      0.3

# Reapply convolute to restore uncertainty data
df_restored = df_quantified.uncrts.convolute()
print(df_restored)
          mass
0  1.00+/-0.10
1  2.00+/-0.20
2  3.00+/-0.30
```


## License

UnPaAc is open source software released under the MIT License.
See [LICENSE](https://codeberg.org/Cs137/UnPaAc/src/branch/main/LICENSE) file for details.


## Contributing

Contributions to the `UnPaAc` package are very welcomed. Feel free to submit a
pull request, if you would like to contribute to the project. In case you are
unfamiliar with the process, consult the
[forgejo documentation](https://forgejo.org/docs/latest/user/pull-requests-and-git-flow/)
and follow the steps using this repository instead of the `example` repository.

Create your [pull request (PR)](https://codeberg.org/Cs137/unpaac/pulls) to
inform that you start working on a contribution. Provide a clear description
of your envisaged changes and the motivation behind them, prefix the PR's title
with ``WIP: `` until your changes are finalised.

All kind of contributions are appreciated, whether they are
bug fixes, new features, or improvements to the documentation.


---

This package was created and is maintained by Christian Schreinemachers, (C) 2025.

