import numpy as np

def generate_sphere(radius=1.0, lat_segments=16, lon_segments=32):
    vertices = []
    indices = []
    for i in range(lat_segments + 1):
        theta = np.pi * i / lat_segments
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)
        for j in range(lon_segments + 1):
            phi = 2 * np.pi * j / lon_segments
            sin_phi = np.sin(phi)
            cos_phi = np.cos(phi)
            # Position (x, y, z)
            x = radius * sin_theta * cos_phi
            y = radius * cos_theta
            z = radius * sin_theta * sin_phi
            # Normale (normée car sphère unitaire)
            nx = sin_theta * cos_phi
            ny = cos_theta
            nz = sin_theta * sin_phi
            # Texture coordinates (u, v)
            u = j / lon_segments
            v = i / lat_segments
            r, g, b = 1.0, 1.0, 1.0
            # Interlaced vertex: position, normal, color, uv
            vertex = [x, y, z, nx, ny, nz, r, g, b, u, v]
            vertices.append(vertex)
    # Faces
    for i in range(lat_segments):
        for j in range(lon_segments):
            a = i * (lon_segments + 1) + j
            b = a + lon_segments + 1
            indices.append((a, b, a + 1))
            indices.append((a + 1, b, b + 1))
    return {
    'interlaced': np.array(vertices, dtype=np.float32), # [pos, norm, color]
    'faces': np.array(indices, dtype=np.int32) # (i0, i1, i2)
    }
