import numpy as np
import tinkermodellor.tkmcpptoolkit as tct

coords1 = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
coords2 = np.array([[1.1, 2.1, 3.1], [4.1, 5.1, 6.1], [7.1, 8.1, 9.1]])

rmsd = tct.rmsd(coords1, coords2)
print(f"RMSD: {rmsd}")

