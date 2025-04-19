### RUSLE: Soil erosion modelling of eucalyptus plantations across the south of Portugal
Aims: Model soil erosion using the RUSLE model for eucalyptus plantations in the south of Portugal. The model will use experimental results collected during the trip to improve accuracy. We will investigate how management decisions/land cover change (e.g. felling, forest fires) may affect soil erosion rates and determine if climate change plays a role. 
Materials: 
•	The presentation from the workshop on 25/03/25 RUSLE2025.pptx will help the understanding and implementation of the model.
•	A Jupyter Notebook which contains python code of the model and instructions on how to use it: ./Notebooks/RUSLE2025.ipynb. Jupyter Notebook is a web-browser based programming platform which integrates code, text and visualisation. 
•	Some parts have been left as an exercise for students to complete which should be completed during the workshop/before the trip. A guide on how to run the notebook on Google Colab or install Python and launch the notebook comes in the following section.
•	The data folder contains a digital elevation map of the region at 25m resolution and a database of soil measurements in Portugal which might be useful when we are on the trip.
•	Field measurements of soil properties will be needed to parameterise the equation. 
The Jupyter Notebook RUSLE2025.ipynb contains further guidance and tasks to complete on the trip for this project which we will go over in the workshop.

# Option 1: Running Jupyter Notebook on google colab
With this option we will run the model on google’s computers using google colab. This avoids having to install anything.
1.	Go to https://colab.research.google.com/ 
2.	Upload the Notebook by pressing File -> Upload in google colab



 
3) Navigate to where the RUSLE2025.ipnb file in the “Notebooks” sub directory in the “RUSLE2024” folder and open it.
 
4) If it looks like this you are ready to go. Remember you have run each cell (by pressing the play button) sequentially for it to work.
 
# Option 2: Running the Jupyter Notebook on your own computer (recommended for people on this project)
1)	If you do not have python installed: Download and install the ‘Anaconda Distribution’ of python https://www.anaconda.com/download. This is a python installation which comes with a number of modules that are useful for data science and modelling. If you do not have admin rights on your computer make sure and install it in your personal directory. For example I have it in C:\Users\dfletcher\Anaconda3
If you do have python installed already: Check if the Jupyter notebook package is installed, if not install it with >> pip install notebook in the command line
2)	Save RUSLE2025.ipynb in a folder on your computer
3)	Launch Jupyter Notebook:
 

A command prompt should open and after a few seconds your web-browser will open with Jupyter
4)	Navigate to where you have saved RUSLE2025.ipynb on the browsers file explorer:
 
5)	Once you have found RUSLE2025.ipynb, click it and a new tab should open with the notebook in it:
 

6)	You can now ‘run’ each cell sequentially to work through the notebook.
