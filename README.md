# Contents
The project contains the companion code to paper "Strategic Cost Selection in
Participatory Budgeting" by [Piotr
Faliszewski](https://home.agh.edu.pl/~faliszew/), Łukasz Janeczko, [Andrzej
Kaczmarczyk](https://akaczmarczyk.com), [Grzegorz
Lisowski](https://scholar.google.com/citations?user=oGo467wAAAAJ&hl=en), [Piotr
Skowron](https://duch.mimuw.edu.pl/~ps219737/), [Stanisław
Szufa](https://szufa.simple.ink), and Mateusz Szwagierczak.

# Replicating Experiments

To replicate our experiments you need to install several packages
>> pip install pabutools==1.1.11
>> pip install tqdm
>> pip install matplotlib

///-----------------------\\\
|||To get Figures 2 and 6.|||
\\\-----------------------///

To compute data for Figures 2 and 6 run the following code.
-----------------------------------------------------------

# Compute winning and losing margins
>> python script_01.py

To plot Figure 2
----------------

# Plot the results as images/PAPERPLOT_margins.png
>> python script_02.py paperplot

To plot the pictures from Figure 6 run the following code.
----------------------------------------------------------

# Plot the results in the folder images/
>> python script_02.py


///-----------------------\\\
|||To get Figures 3 and 7.|||
\\\-----------------------///

To compute data for Figures 3 and 7 run the following code.
-----------------------------------------------------------

# Simulation 10000 iterations of the game
>> python script_03.py

To plot Figure 3
----------------

# Plot the results as images/PAPERPLOT_games.png
>> python script_04.py paperplot

To plot the pictures from Figure 7
----------------------------------

# Plot the results in images/
>> python script_04.py

///----------------\\\
|||To get Figure 8.|||
\\\----------------///

To compute data for Figure 8 run the following code.
----------------------------------------------------

# Simulation 10000 iterations of the game
>> python script_05.py

To plot the pictures from Figure 8
----------------------------------
# Plot the results to the directory /images.
>> python script_06.py

The files contain:
 - jupyter notebooks with the code used to generate the figures
 - the python package we implemented, in directory `cvrpy`
 - the datasets we used, in directory `datasets` 
 - raw data of our experiments, in directory `data_out`

> ❗ No data was collected in the course of this project. All used datasets come
from [Pabulib](https://pabulib.org/). 


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
Council. Neither the European Union nor the grant- ing authority can be held
responsible for them.
Grzegorz Lisowski acknowledges support by the European Union under the Horizon
Europe project [Perycles](https://perycles-project.eu/) (Participatory Democracy
that Scales).  This research has been supported by the French government under
the management of Agence Na- tionale de la Recherche as part of the France 2030
program, reference ANR-23-IACL-0008.
