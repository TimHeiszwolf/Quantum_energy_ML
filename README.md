# Quantum_energy_ML
 
This Github repo currently doesn't contain the latest version (that one is currently being cleaned up). Please check back in around sunday July 5th.

# Code usage
The code, several databases and a few trained networks can be found on this Github page. More details can be found in the section below. If afterwards you still have questions feel free to contact the author.

The program consist of three parts. The first part generates a database (see chapter 3.2 and appendix C.1) which is outputted to a .JSON file. The next part prepares that database for machine learning (see chapter 3.3 and appendix C.2). Finally a Jupyter Notebook can be opened. In the notebook several methods for generating neural networks are already implemented and examples on how to use them are displayed.

## Database generation
The function 'makeRandomDatabaseMinimum' from 'makeRandomDatabase.py' is the hart of the database generation. But controlling it directly is not very nice (lot's of inputs and very little feedback). So a script called 'runDatabaseGeneration.py' was made in which the settings can easily be adjusted and from which some feedback and analysis of the database that is produced is done.\medskip

The script produced a database (according to the method of chapter 3.2, as a pandas DataFrame) and then saves it as a .json file which can then easily be imported as a pandas DataFrame again. The DataFrame contains details like what the particle coordinates are, what the width of the cell of each data point is, what the potential energy of the data point is and with how many depth of cells it is created (in databases generated using older versions of the software this column might be names 'numberOfSurroundingCells').

The available setting are:
* numberOfDatapoints: The number of data points the database will approximately have (since splitting the work on multiple cores or compensating for the filtrating can result in some roundup errors).
* numberOfParticlesPerCell ($N_p$): The number of particles placed in each cell.
* numberOfDimensions ($d$): The number of dimensions the space in the database has. The generation process has been tested for 2D and 3D but should also work for higher dimensions.
* potentialEnergyFunction: Is the function used to calculate the potential energy of each pair/triplet. The function must take a single array of number (the relative distance between each of the particles).
* widthOfCell ($w_c$): Is a list of size 2 containing a lower and a upper limit for the size of the cell.
* numberOfWidths: The number of steps widths represented in the database (including the lower and upper endpoints).
* depthOfSurroundingCells ($d_s$): The depth of the number of cells taken into account when calculating the potential energy. This needs to be high enough such that convergence has taken place (for each possible cell size).
* relaxationDepthOfSurroundingCells: The depth of the number of cells taken into account when calculating the potential energy for the relaxation process. It is best to make this values lower than numberOfWidths since accuracy is less important and speed is more important.
* amountOfEpochs: Is the amount of epochs the relaxation process is applied. During a epoch every particle is allowed to move in a random direction and the change is accepted if the new potential energy is lower than the original.
* maxDeltaPerEpoch: Is the maximum magnitude of the movement of a particle during a epoch. The actual amount is random between this and 0.
* cutoff: Is above which percentile the energies will be cuttoff and the configurations won't be taken into the database.
* filename: Is the name of the .json while to which the database will be saved (without the file extension).

## Database preparation
The part of the code that prepares the database for machine learning has a similar structure to the code that generates the database. The 'prepareDatabaseForMachineLearning' in 'prepareDatabaseForMachineLearning.py' is the hart of the software and does all the work while the script in 'runDatabasePreperation.py' has the adjustable settings and starts the software.

It loads the database that was generated and then adds two columns. First the eigenvalues of the proximity matrices (as specified in chapter 3.3), the second are the raw relative distances between particles within the central cell (this was used for training in the early versions of the software but generaly doesn't work very well). This part is very fast.

The available setting are:
* filename: The name of the database that needs to be prepared (without the file extension). This needs to be a .json file of a saved pandas DataFrame.
* orderOfMatrix: Is a list of the orders which the proximity matrices should have.
* R0p ($R_{0p}$): Is the distance at which the contributions of the proximity matrix should become zero (see chapter 3.3). It also determined how much depth of the surrounding cells is going to be used when calculating the proximity matrices.

To prepare a database the 'runDatabasePreperation.py' script should be run. When it ask how many processes should start the user should give the amount of (logical) threads their processor has for the fastest preparation. The resulting prepared database will then be saved as a .json file again (as the same name but with 'Prepared' added to it's name). When giving the name of a database that has already been prepared the eigenvalue of relative distance columns will be overwritten during the new preparation.

## Jupyter notebooks (for machine learning)
There are also two Jupyter notebook available. First is the 'testingPotential' in which the quality of potentials can be investigated with various graphs and tests.

The other (more important) notebook is the 'machineLearning' notebook. In this notebook several functions for making, training and investigating neural networks are displayed. Also methods for importing the data and preparing it for use in the neural network is given.

The important functions are 'plotHistory' which takes the history of a fit and makes nice plots of it, 'makeGradiantPlot' makes the plots for the test of dragging the particle trough the cell, 'makePredictionPlot' makes the scatter plot in which the predicted potential energy per particle is compared to the real energy per particle and finally 'plotAndPredict' takes a random sample for the validation data and plots the lattice for it and gives the prediction and real value of the energy per particle.

## Used modules
The following non-standard modules are used:
* MatPlotLib
* Numpy
* Pandas
* Keras (for the machine learning part)


















