# ArtEvoViewer

This is a system for visualizing the influence relationships between Western artists.
<br>
<br>
![The system overview](./overview.png)
<br>
<br>
## How to run
1. Clone this repository
   ```
   $ git clone https://github.com/RyokoOda/ArtEvoViewer.git
   ```
2. Move to this directory
3. Create a virtual environment with conda
   ```
   $ conda create -n ArtEvoViewer python==3.11
   $ conda activate ArtEvoViewer
   ```
4. Install requirement.txt <br>
   **Please make sure that the version of Dash Cytoscape is 0.2.0.**
   ```
   $ pip install -r requirements.txt
   ```
5. Run the system
   ```
   $ python dash_viewer.py
   ```
6. Then you can show the system at http://127.0.0.1:8050/
