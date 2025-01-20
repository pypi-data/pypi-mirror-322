import sys
import numpy as np
from collections import OrderedDict
from pathlib import Path
from argparse import ArgumentParser

from MDAnalysis import AtomGroup, Universe
from MDAnalysis.coordinates.base import Timestep

from sklearn.cluster import DBSCAN


def read_ndx_file(ndx_file_path: str, universe: Universe) -> AtomGroup:

    ndx_content = OrderedDict()

    with open(ndx_file_path, "r") as f:
        ndx_file = f.read()
    ndx_file = ndx_file.split("\n")

    current_key = None
    for line in ndx_file:

        if line.startswith("[ "):
            current_key = line[2:-2]
            ndx_content[current_key] = list()
        elif line.startswith(";"):
            pass
        else:
            ndx_content[current_key] += list(map(int, line.split()))

    max_name_length = max(map(len, ndx_content.keys()))
    max_len_length = max(map(lambda x: len(str(len(x))), ndx_content.values()))
    print("Select group for rigid body analysis")
    for group_idx, group_name in enumerate(ndx_content):
        print("Group", end="")
        print((6 - len(str(group_idx))) * " " + str(group_idx) + " ( ", end="")
        print((max_name_length - len(group_name)) * " " + group_name + ") has ", end="")

        str_len = str(len(ndx_content[group_name]))
        print((max_len_length - len(str_len)) * " " + str_len + " elements")

    selected_idx = int(input("Select a group: "))
    atom_group = universe.atoms[list(ndx_content.values())[selected_idx]]

    return atom_group


def main():

    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f", "--trajectory_file", type=str, required=True,
                            help="The trajectory file.")
    arg_parser.add_argument("-s", "--structure_file", type=str, required=True,
                            help="The structure (pdb) file.")
    arg_parser.add_argument("-o", "--output_file", type=str, required=True,
                            help="The b-labelled output pdb file.")
    arg_parser.add_argument("-n", "--index_file", type=str, default=None,
                            help="The index file containing the atoms for the RBS if mode is \"index\".")
    arg_parser.add_argument("-clr", "--cluster_radius", type=float, default=0.25,
                            help="The epsilon value for the DBSCAN clustering algorithm.")
    arg_parser.add_argument("-cln", "--cluster_neighbours", type=int, default=5,
                            help="The min_samples value for the DBSCAN clustering algorithm.")
    arg_parser.add_argument("-b", "--begin_time", type=int, default=0,
                            help="The time (in ps) from the algorithm reads the trajectory.")
    arg_parser.add_argument("-e", "--end_time", type=int, default=None,
                            help="The time (in ps) until the algorithm reads the trajectory.")
    arg_parser.add_argument("-dt", "--delta_time", type=int, default=None,
                            help="The time (in ps) interval the algorithm reads the trajectory.")
    arg_parser.add_argument("-m", "--mode", type=str, default="CA",
                            help="Either \"CA\", \"CB\", or \"index\".")
    args = arg_parser.parse_args()

    assert Path(args.trajectory_file).exists(), "Path to trajectory file does not exist!"
    assert Path(args.trajectory_file).is_file(), "Path to trajectory file is not a file!"
    assert args.trajectory_file.endswith(".xtc"), "Trajectory file is not a .xtc file!"

    assert Path(args.structure_file).exists(), "Path to structure file does not exist!"
    assert Path(args.structure_file).is_file(), "Path to structure file is not a file!"
    assert args.structure_file.endswith(".pdb"), "Structure file is not a .pdb file!"

    if args.index_file is not None and args.mode == "index":
        assert Path(args.index_file).exists(), "Path to index file does not exist!"
        assert Path(args.index_file).is_file(), "Path to index file is not a file!"
        assert args.index_file.endswith(".ndx"), "Index file is not an .ndx file!"

    if not args.output_file.endswith(".pdb"):
        args.output_file += ".pdb"

    universe = Universe(args.structure_file, args.trajectory_file)
    print("Trajectory and structure file OK!")

    ref_selection: AtomGroup
    if args.mode == "CA":
        ref_selection = universe.select_atoms("name CA")
    elif args.mode == "CB":
        ref_selection = universe.select_atoms("name CB or (name CA and resname GLY)")
    elif args.mode == "index":
        ref_selection = read_ndx_file(args.index_file, universe)
    else:
        raise Exception("Invalid mode! Use either \"CA\", \"CB\", or \"index\"!")

    begin_frame = int(args.begin_time / universe.trajectory.dt)

    if args.delta_time is None:
        delta_frame = 1
        args.delta_time = universe.trajectory.dt
    else:
        delta_frame = int(args.delta_time / universe.trajectory.dt)

    if args.end_time is None:
        end_frame = "end"
        trajectory = universe.trajectory[begin_frame::delta_frame]
    else:
        end_frame = int(args.end_time / universe.trajectory.dt)
        trajectory = universe.trajectory[begin_frame:end_frame:delta_frame]

    print(f"Reading frames from {begin_frame} to {end_frame} with a delta frame of {delta_frame}.\n")

    dmx_mean = None
    dmx_variance = None

    frame: Timestep
    for frame_idx, frame in enumerate(trajectory):

        ca_positions: np.ndarray = ref_selection.positions
        dmx = ca_positions[:, np.newaxis, :] - ca_positions[np.newaxis, :, :]
        dmx = np.sqrt(np.sum(dmx ** 2, axis=2))

        if dmx_mean is None:
            dmx_mean = np.copy(dmx)
            dmx_variance = np.zeros(dmx.shape)
        else:
            new_dmx_mean = dmx_mean + (dmx - dmx_mean) / (frame_idx + 1)
            dmx_variance += (dmx - dmx_mean) * (dmx - new_dmx_mean)
            dmx_mean = np.copy(new_dmx_mean)

        sys.stdout.write("\033[F")  # go up one line
        current_time = args.begin_time + frame_idx * args.delta_time
        print(f"Time: {current_time} ps")

    dmx_variance = np.sqrt(dmx_variance / len(trajectory))  # this is dmx std now

    print(f"RMSD matrix constructed with shape: {dmx_variance.shape}.")
    flattened_variance = dmx_variance[np.tril_indices(len(dmx_variance), -1)]
    print(f"\tMin RMSD: {np.min(flattened_variance):.3f} nm")
    print(f"\tMax RMSD: {np.max(flattened_variance):.3f} nm")
    print(f"\tAvg RMSD: {np.mean(flattened_variance):.3f} nm")
    print(f"\tMedian RMSD: {np.median(flattened_variance):.3f} nm")
    print(f"\tStd of RMSDs: {np.std(flattened_variance):.3f} nm")
    print(f"\tMedian RMSD of {args.cluster_neighbours}th closest neighbour: "
          f"{np.median(np.sort(dmx_variance, axis=1)[:, args.cluster_neighbours]):.3f}")

    clustering = DBSCAN(eps=args.cluster_radius,
                        min_samples=args.cluster_neighbours,
                        metric="precomputed").fit(dmx_variance)

    print(f"Clustering done! Found {len(np.unique(clustering.labels_))} clusters.")
    for idx in np.sort(np.unique(clustering.labels_)):
        current_size = np.sum(clustering.labels_ == idx)
        print(f"\tSize of cluster {idx}: {current_size}")

    print("Resetting atom bfactors...")
    universe.add_TopologyAttr("tempfactors")  # needed to set the tempfactors of the atoms
    for atom in universe.atoms:
        atom.tempfactor = -1.

    if args.mode == "index":
        for idx, atom in enumerate(ref_selection.atoms):
            atom.tempfactor = clustering.labels_[idx]
    else:
        for idx, atom in enumerate(ref_selection.atoms):
            tempfactor_array = clustering.labels_[idx] * np.ones(len(atom.residue.atoms))
            atom.residue.atoms.tempfactors = tempfactor_array

    universe.select_atoms("all").write(args.output_file)
    print(f"B-labelled pdb file saved as {args.output_file}")
    print("Everything is done! Have a nice day!")


if __name__ == "__main__":
    main()
