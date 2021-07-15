# Examples

After checking out the code using git you can run:

```bash
pip install -e .
```

## Sample

_Sample_ represents the project described in [Build your project](https://github.com/francescobarbarulo/pysim#build-your-project) section.

```bash
python examples/sample/main.py
```

## TicToc

_TicToc_ simulates two modules that keep passing the same message back and forth.

```bash
python examples/tictoc/main.py
```

## Airport

_Airport_ simulates the arrival of passengers at the terminal and their wait for doing the check-in.
The inter-arrival time between passengers is modeled by the exponential distribution (see [Random variates](https://github.com/francescobarbarulo/pysim#generating-random-variates)).
When a passenger arrives it enqueues itself at the gate having the minimum queue length.
The check-in time is determined by the number of luggages they have.

```bash
python examples/airport/main.py
```