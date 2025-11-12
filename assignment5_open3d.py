import open3d as o3d
import numpy as np

# STEP 1: Load and visualize 
mesh = o3d.io.read_triangle_mesh("mun.obj")
mesh.compute_vertex_normals()

print("=== Step 1: Original Model ===")
print("Vertices:", len(mesh.vertices))
print("Triangles:", len(mesh.triangles))
print("Has colors:", mesh.has_vertex_colors())
print("Has normals:", mesh.has_vertex_normals())

o3d.visualization.draw_geometries([mesh], window_name="Step 1: Original Mesh")

# STEP 2: Convert to point cloud 
pcd = mesh.sample_points_poisson_disk(number_of_points=80000)
print("\n=== Step 2: Point Cloud ===")
print("Points:", len(pcd.points))
print("Has colors:", pcd.has_colors())

o3d.visualization.draw_geometries([pcd], window_name="Step 2: Point Cloud")

# STEP 3: Surface reconstruction (Poisson) 
print("\n=== Step 3: Poisson Reconstruction ===")
pcd.estimate_normals(fast_normal_computation=True)
mesh_recon, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)
bbox = pcd.get_axis_aligned_bounding_box().scale(1.05, pcd.get_center())
mesh_crop = mesh_recon.crop(bbox)
mesh_crop.compute_triangle_normals()

print("Vertices:", len(mesh_crop.vertices))
print("Triangles:", len(mesh_crop.triangles))
print("Has colors:", mesh_crop.has_vertex_colors())

o3d.visualization.draw_geometries([mesh_crop], window_name="Step 3: Reconstructed Mesh")

# STEP 4: Voxelization 
print("\n=== Step 4: Voxelization ===")
voxel_size = 0.05
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=voxel_size)

print("Voxels:", len(voxel_grid.get_voxels()))

o3d.visualization.draw_geometries([voxel_grid], window_name="Step 4: Voxel Grid")

# STEP 5: Add plane 
print("\n=== Step 5: Add Plane ===")
plane = o3d.geometry.TriangleMesh.create_box(width=3.0, height=0.02, depth=3.0)
plane.paint_uniform_color([0.6, 0.6, 0.6])
plane.translate([0, -1.0, 0])  # под ногами модели

o3d.visualization.draw_geometries([mesh_crop, plane], window_name="Step 5: Mesh + Plane")

# STEP 6: Clipping 
print("\n=== Step 6: Clipping ===")
points = np.asarray(pcd.points)
plane_y = 0.0
mask = points[:, 1] > plane_y  # оставляем только выше плоскости
clipped_points = points[mask]
clipped_pcd = o3d.geometry.PointCloud()
clipped_pcd.points = o3d.utility.Vector3dVector(clipped_points)

print("Remaining points:", len(clipped_points))
o3d.visualization.draw_geometries([clipped_pcd], window_name="Step 6: Clipped Model")

# STEP 7: Coloring and Extremes 
print("\n=== Step 7: Coloring and Extremes ===")
points = np.asarray(clipped_pcd.points)
if len(points) > 0:
    z_values = points[:, 2]
    min_z, max_z = np.min(z_values), np.max(z_values)
    normalized = (z_values - min_z) / (max_z - min_z)
    colors = np.stack([normalized, np.zeros_like(normalized), 1 - normalized], axis=1)
    clipped_pcd.colors = o3d.utility.Vector3dVector(colors)

    # найти экстремумы
    min_point = points[np.argmin(z_values)]
    max_point = points[np.argmax(z_values)]

    print(f"Min Z point: {min_point}")
    print(f"Max Z point: {max_point}")

    # выделить сферами
    sphere_min = o3d.geometry.TriangleMesh.create_sphere(radius=0.05)
    sphere_min.paint_uniform_color([1, 0, 0])
    sphere_min.translate(min_point)

    sphere_max = o3d.geometry.TriangleMesh.create_sphere(radius=0.05)
    sphere_max.paint_uniform_color([0, 0, 1])
    sphere_max.translate(max_point)

    o3d.visualization.draw_geometries([clipped_pcd, sphere_min, sphere_max],
                                      window_name="Step 7: Colored + Extremes")
else:
    print("No points remaining after clipping.")

print("\n✅ DONE: All 7 steps completed successfully!")
