<!--Start-->

<h2 class="bg-gradient rounded-2 p-0"> <img src="https://kwokcb.github.io/materialxMaterials/documents/icons/logo_large_blue_teapot_no_text.png" width=32px>MaterialX Materials</h2>

<div class="container p-2 rounded-4 border border-secondary border-rounded">

<h3>Introduction</h3>

Welcome to MaterialX Materials.

This site hosts a set of libraries and command line utilities to query remote databases for MaterialX materials.

<h4> > Visit the <b><a href="https://kwokcb.github.io/materialxMaterials" target="_blank">Home Page</a></b>
</h4>

<p>
Related utilities and libraries can be found at the:
<div class="btn btn-outline-secondary">
<a href="https://kwokcb.github.io/MaterialXLab" target="_blank">
<img src="https://kwokcb.github.io/MaterialXLab/documents/icons/teapot_logo.svg"
width=32px>
MaterialXLab home page</a>
</a>
</div>
</p>

The current utilities support:

<div style="display: flex; align-items: center;">
<img src="https://physicallybased.info/images/renders/cycles/600/aluminum.webp" width="64px" style="margin-right: 5px;">
<a href="https://physicallybased.info/">PhysicallyBased database</a> Material descriptions can be downloaded with additional utilities to create materials using either: Autodesk Standard Surface, OpenPBR, or glTF PBR shading model shaders.
</div>
<br>
<div style="display: flex; align-items: center;">
<img src="https://image.matlib.gpuopen.com/afff0c66-dba8-4d79-b96b-459fbd9cbef5.jpeg" width="64px" style="margin-right: 5px;">
<a href="https://matlib.gpuopen.com/main/materials/all">AMD GPUOpen database</a> MaterialX packages can be downloaded (as zip files). Images and MaterialX documents can be extracted for any of the posted materials in the database.
</div>
<br>
<div style="display: flex; align-items: center;">
<img src="https://acg-media.struffelproductions.com/file/ambientCG-Web/media/thumbnail/2048-JPG-242424/PavingStones142.jpg" width="64px" style="margin-right: 5px;">
<a href="https://ambientcg.com/list?type=material&sort=popular">ambientCG database</a> MaterialX packages can be downloaded (as zip files). Images and MaterialX documents can be extracted for any of the posted materials in the database.
</div>

Each currently has <code>Python</code> implementations.
</p>

<iframe
  src="https://www.youtube.com/embed/4KiPW9IUR6U?rel=0&vq=hd1080"
  title="Using Material Libraries" width="100%"
  height="600px" frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  allowfullscreen>
</iframe>

<h3>Usage Examples</h3>

<h4>A. PhysicallyBased</h4>
An <a href="https://kwokcb.github.io/MaterialXLab/javascript/PhysicallyBasedMaterialX_out.html" target="_blank">interactive page: 
<br>
<img src="https://kwokcb.github.io/MaterialXLab/documents/help/images/physicallyBased_material_fetch.png" width=50%/>
</a> 

for extracting <code>PhysicallyBased</code> uses a Javascript implementation found <a href="https://github.com/kwokcb/materialxMaterials/blob/main/javascript/JsMaterialXPhysicallyBased.js">here</a>
</p>

<p>
<hr>
<h4>B. AMD GPUOpen</h4>
A command line utility is available <a href="https://github.com/kwokcb/materialxMaterials/tree/main/javascript/JsGPUOpenLoaderPackage">here</a>. This uses <code>Node.js</code> to allow access to fetch materials from the <code>GPU Open</code> site(which is not available via a web page).
<p>

<p><a href="https://github.com/kwokcb/materialxWeb/blob/main/flask/gpuopen/README.md">A <b>Flask</b> application</a> is also available which uses the Python package with a Web based front here.
<img src="https://raw.githubusercontent.com/kwokcb/materialxWeb/refs/heads/main/flask/gpuopen/images/extract_material_1.png" width=50%>
</p>

<hr>
<h4>C. Loading into Web Editor</h4>

<p>
Below are screenshots of materials fetched from from <code>PhysicallyBased</code> and <code>GPU Open</code> and <code>ambientCg></code> (left to right  images respectively). Note that the material zip from <code>GPU Open</code> and <code>ambientCg</code> is directly read into the editor via it's zip loading option. 
<table>
<tr>
<td><img src="https://kwokcb.github.io/MaterialXLab/documents/help/images/load_phybased_node_editor.png" width=100%></td>
<td><img src="https://kwokcb.github.io/MaterialXLab/documents/help/images/load_zip_node_editor_3.png" width=100%></td>
<td><img src="https://kwokcb.github.io/MaterialXLab/documents/help/images/load_ambientCG_node_editor.png" width=100%></td>
</tr>
</table>
</p>
<p></p>

<h3>Library Dependencies</h3>

The Python utilities require:

1. The MaterialX 1.39 or greater package for PhysicallyBased OpenPBR shader creation
2. The `requests` package.
3. The `pillow` package for image handling for GPUOpen package handling

The GPUOpen Javascript logic requires:
1. `node-fetch` if fetch is not available in the version of Node.js used. 
2. `yargs` for the command line utility 

<h3>Package Building</h3>

The <a href="https://github.com/kwokcb/materialxMaterials"><img src="https://raw.githubusercontent.com/kwokcb/materialxMaterials/4125d04c73fc2b1755f5b6054b25b6d1bdabcf6b/documents/icons/github-mark-white.svg" width=16px> GitHub repository</a> can be cloned.

The Python package can be built using:

```shell
pip install .
```

This will pull down the dependent Python packages as needed.

Build scripts can be found in the `utilities` folder.

- `build.sh` will install the package and run package commands to update package data.
- `buildDocs.sh` will prepare documents and run Doxygen to build API docs.

The GPUOpen Javascript utility requires Node.js to be installed. From the package folder (`javascript\JsGPUOpenLoaderPackage`) the following should be run:

```shell
npm install     # Install dependent packages
npm run build   # Setup runtime area
```

<h3>Usage</h3>

<h4>Python Commands</h4>

- Query all materials fom PhysicallyBased and convert them to all  support shading models. Save the material list and corresponding MaterialX files in the default output location. The build will include this information Python package under the <code>data</code> folder.

  ```sh
  python physicallyBasedMaterialXCmd.py
  ```
  or 

  ```sh
  materialxMaterials physbased
  ```

- Query all materials fom GPUOpen. Extract out a few material packages (zip). Save the material lists, material names and unzipped packages (MaterialX and images) in the default output location. The build will include this information Python package under the <code>data</code> folder.

  ```sh
  materialxMaterials gpuopen --materialNames=1 --saveMaterials=1
  ```

- Download the materials list fom ambientCG: 

  ```sh
  materialxMaterials acg --saveMaterials True
  ```

- Extract out a material package for the "WoodFloor038" material from ambientCG requesting the 
package where the images are 2K PNG files:

  ```sh
  materialxMaterials acg --downloadMaterial "WoodFloor038" --downloadResolution 2
  ```

<h4>GPU Open Node.js Utility</h4>

The utility can be run from the `javascript\JsGPUOpenLoaderPackage` folder as follows:

```
npm start -- [<arguments>]
```
or:
```
node gpuOpenFetch.js [<arguments>]
```
with the appropriate arguments. It supports the same options as the Python utility -- namely material information, and package (zip) downloads. For the following 2 lines are equivalent to download a material called "Moss Green Solid Granite".
```
node gpuOpenFetch.js  -n "Moss Green Solid Granite"
npm start -- -n "Moss Green Solid Granite"
```

<h3>Library</h3>

A `Jupyter` notebook demonstrates the direct usage of the Python library. The output of the notebook can be found <a href="https://kwokcb.github.io/materialxMaterials/examples/materialxMaterials_tutorial_out_iframe.html">here</a>. The notebook can found in the Github repository under the `examples` folder.

<h3>Results</h3>

The following are some samples which have been rendered using the `MaterialXView` utility which is part of the MaterialX binary distribution. 

<h4>Examples</h4>
Details about some examples can be found in the <a href="https://kwokcb.github.io/materialxMaterials/examples/index.html">Examples pages</a>

<table>
<tr >
<th >
Emerald Peaks Wallpaper
<th >
Indigo Palm Wallpaper
<th >
Oliana Blue Painted Wood
<tr >
<td >
<img src="https://kwokcb.github.io/materialxMaterials/src/materialxMaterials/data/GPUOpenMaterialX/Emerald Peaks Wallpaper/Emerald_Peaks_Wallpaper.png" width=100%>
</td>
<td >
<img src="https://kwokcb.github.io/materialxMaterials/src/materialxMaterials/data/GPUOpenMaterialX/Indigo Palm Wallpaper/Indigo_Palm_Wallpaper.png" width=100%>
</td>
<td >
<img src="https://kwokcb.github.io/materialxMaterials/src/materialxMaterials/data/GPUOpenMaterialX/Oliana Blue Painted Wood/Oliana_Blue_Painted_Wood.png" width=100%>
</td>
</tr>
</table>

<table>
<tr >
<th>
Ketchup
<th>
Cooking Oil
<th>
Brass
</th>
<tr >
<td >
<img src="https://kwokcb.github.io/materialxMaterials/src/materialxMaterials/data/PhysicallyBasedMaterialX/Ketchup.png" width=100%>
</td>
<td >
<img src="https://kwokcb.github.io/materialxMaterials/src/materialxMaterials/data/PhysicallyBasedMaterialX/Cooking_Oil.png" width=100%>
</td>
<td >
<img src="https://kwokcb.github.io/materialxMaterials/src/materialxMaterials/data/PhysicallyBasedMaterialX/Brass.png" width=100%>
</td>
</table>

<table>
<tr >
<th>
Metal (53)
<th>
Paving Stones (142)
<th>
Wood Floor (38)
</th>
<tr >
<td >
<img src="https://kwokcb.github.io/materialxMaterials/src/materialxMaterials/data/ambientCgMaterials/Metal053C_1K-PNG.png" width=100%>
</td>
<td >
<img src="https://kwokcb.github.io/materialxMaterials/src/materialxMaterials/data/ambientCgMaterials/PavingStones142_1K-PNG.png" width=100%>
</td>
<td >
<img src="https://kwokcb.github.io/materialxMaterials/src/materialxMaterials/data/ambientCgMaterials/WoodFloor038_1K-PNG.png" width=100%>
</td>
</table>
<sub>The rows of materials are from `GPUOpen` `PhysicallyBased`, and `ambientCG` from top to bottom respectively.</sub>

<p></p>

<h3>API Reference</h3>

The API reference can be found <a href="https://kwokcb.github.io/materialxMaterials/documents/html/index.html">here</a>

</div>
<!--End-->

