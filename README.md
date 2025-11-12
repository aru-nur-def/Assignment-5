# Assignment 5 — 3D Geometry Processing with Open3D

**Author:** Saparkhankyzy Aruzhan  
**Project:** *Girl in the Dark* — 3D Geometry Operations  
**Tools:** Python, Open3D, NumPy

---

## Task Description

The goal of this assignment is to demonstrate **3D geometry processing** in Python using the **Open3D** library.  
A unique 3D model (`mun.obj`) from *Free3D.com* ("Girl in the Dark") was selected and processed through **7 sequential stages**.

Each step is visualized with `draw_geometries()` and printed metrics (points, triangles, voxels, colors, normals, intersections).

---

## Steps Implemented

### **1. Load & Visualize**
- The 3D mesh `mun.obj` is loaded and displayed.  
- Console output shows: number of vertices, triangles, colors, and normals.

### **2. Convert to Point Cloud**
- The model is sampled into ~80,000 points using Poisson disk sampling.  
- This forms a detailed *point cloud* representation of the mesh surface.

### **3. Surface Reconstruction (Poisson)**
- The point cloud is reconstructed into a smooth surface mesh with `create_from_point_cloud_poisson()`.  
- Artifacts are removed using cropping by bounding box.

### **4. Voxelization**
- The point cloud is converted into a **voxel grid** (`voxel_size = 0.05`).  
- The number of voxels (≈6284) shows model density.

### **5. Add Plane**
- A flat **plane (floor)** is added below the model for visual reference.  
- Demonstrates how to combine multiple 3D geometries in a single scene.

### **6. Clipping**
- Points below the plane are removed (right-side clipping).  
- Remaining points (≈79,905) form the upper visible structure.

### **7. Coloring & Extremes**
- A **color gradient** (Red → Blue) is applied along the Z-axis.  
- Minimum and maximum points are detected and highlighted with spheres.  
- This shows vertical distribution and geometric extremes.

---

## 📊 Console Output Example

