# Contents
The project contains the companion code to paper "Strategic Cost Selection in
Participatory Budgeting" by [Piotr
Faliszewski](https://home.agh.edu.pl/~faliszew/), Łukasz Janeczko, [Andrzej
Kaczmarczyk](https://akaczmarczyk.com), [Grzegorz
Lisowski](https://scholar.google.com/citations?user=oGo467wAAAAJ&hl=en), [Piotr
Skowron](https://duch.mimuw.edu.pl/~ps219737/), [Stanisław
Szufa](https://szufa.simple.ink), and Mateusz Szwagierczak.

# Replicating Experiments

## Data
No data was collected in the course of this project. All used datasets, that we
provide with this repository for convinience, come
from a publically accessible library of participatory
budgeting datasets [Pabulib](https://pabulib.org/).

## Preparation
Install the following packages

```
pip install pabutools==1.1.11
```
```
pip install tqdm
```
```
pip install matplotlib
```

## Getting Figure 1

To compute the experiments with winning and losing margins run
```
python script_01.py
```

Then to plot the figure run
```
python script_02.py paperplot
```

## Getting Figure 2

To compute the experiments simulating our dynamics (for 10000 iterations) run
```
python script_03.py
```

Then to plot the figure run
```
python script_04.py paperplot
```

## Getting charts from Figure 5

Apply the computation step from Figure 1


Then to plot the charts run
```
python script_02.py
```

## Getting charts from Figure 6

Apply the computation step from Figure 2


Then to plot the charts run
```
python script_04.py
```


## Getting charts from Figure 7

o compute the experiments simulating our dynamics (for 10000 iterations) and the delivery costs equal to 80% of the original costs run
```
python script_05.py
```

Then to plot the charts run
```
python script_06.py
```


# Acknowledgments

This research is part of the [PRAGMA project](https://home.agh.edu.pl/~pragma/)
which has received funding from the [European Research Council
(ERC)](https://erc.europa.eu/homepage) under the European Union’s Horizon 2020
research and innovation programme ([grant agreement No
101002854](https://erc.easme-web.eu/?p=101002854)) and the [PRO-DEMOCRATIC
project](https://duch.mimuw.edu.pl/~ps219737/projects/pro-democratic/). Piotr
Skowron was supported by the European Union
([ERC](https://erc.europa.eu/homepage), [PRO-DEMOCRATIC
project](https://duch.mimuw.edu.pl/~ps219737/projects/pro-democratic/), 101076570).
Views and opinions expressed are however those of the authors only and do not
necessarily reflect those of the European Union or the European Research
Council. Neither the European Union nor the granting authority can be held
responsible for them.
Grzegorz Lisowski acknowledges support by the European Union under the Horizon
Europe project [Perycles](https://perycles-project.eu/) (Participatory Democracy
that Scales). This research has been supported by the French government under
the management of [Agence Nationale de la Recherche](https://anr.fr/) as part of
the France 2030 program, reference ANR-23-IACL-0008.
