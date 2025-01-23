# posecraft

**posecraft** is a Python package designed to load, manipulate, and transform pose data. It uses PyTorch to handle pose tensors, allowing you to perform operations such as centering, normalizing distances, filling missing values, and more.

---

## Features

- **Pose Loading**
  Load pose data (stored in `.npy` format) directly into a PyTorch tensor.

- **Transforms**
  A set of classes (inheriting from `torch.nn.Module`) that can be chained to modify and clean your pose data, including:
  - **CenterToKeypoint**: Center all keypoints to a chosen reference keypoint.
  - **NormalizeDistances**: Enforce a fixed distance between two chosen keypoints.
  - **FillMissing**: Interpolate and fill missing (NaN) keypoints across frames.
  - **InterpolateFrames**: Resample frames to a uniform number of frames.
  - **NormalizeFramesSpeed**: Dynamically adjust frames based on the amount of movement.
  - **FilterLandmarks**: Filter out unwanted landmarks based on a mask.
  - **PadTruncateFrames**: Pad or truncate the total number of frames.
  - **RandomSampleFrames** / **RandomSampleFrameLegacy**: Randomly sample frames with fixed intervals or by chunks.
  - **ReplaceNansWithZeros**: Replace all NaN values in the tensor with zeros.
  - **UseFramesDiffs**: Represent each frame as the difference from the previous frame.
  - **FlattenKeypoints**: Reshape and flatten the keypoints across frames.

- **Animation**
  Built-in functionality to animate the keypoints over time using `matplotlib.animation.FuncAnimation`.

---

## Installation (From PyPI)

You can install the package directly from [PyPI](https://pypi.org/project/posecraft/):

```bash
pip install posecraft
```

## Installation (From Source)

1. Clone this repository or add `posecraft` to your Python environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3.	(Optional) For development and documentation, navigate to the docs/ folder and install additional requirements.

## Usage

Below is a basic example of how to load a pose and apply some transformations:

```python
import torch
from posecraft.Pose import Pose
from posecraft.transforms import CenterToKeypoint, NormalizeDistances

# Load a pose from a .npy file
pose_data = Pose(path="path/to/pose.npy")

# Create a set of transforms
transforms = torch.nn.Sequential(
    CenterToKeypoint(center_keypoint=0),
    NormalizeDistances(indices=(11, 12), distance_factor=0.2)
)

# Apply transforms
transformed_pose = transforms(pose_data.pose)

# Now do something with 'transformed_pose', like visualizing or saving
```

You can also chain other available transforms (e.g., FillMissing, FilterLandmarks, etc.) depending on your data cleaning or preprocessing needs.

## Documentation

Full documentation can be found at https://pedroodb.github.io/posecraft/.

Also, if installed locally, comprehensive documentation can be found under the [`docs/`](docs/) folder. This includes:

- Guides on setting up a development container (`.devcontainer`).
- Instructions for running tests (`tests/`) and CI workflows.
- Explanation of each transform class and utility function.

To build and view the documentation locally, navigate to the `docs/` folder and run:

```bash
make html
```

Then open the generated HTML files from docs/_build/html/.

## Contributing

1. Fork the repository and create a new branch for your contribution.
2. Make your changes, then open a pull request (PR).
3. Ensure all tests and documentation checks pass.

Please follow the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for guidance on project etiquette and the [LICENSE](LICENSE) for usage permissions.

---

## Support and Security

For any questions or issues, please see [SUPPORT.md](SUPPORT.md).
Security concerns should be reported as outlined in [SECURITY.md](SECURITY.md).

---

## License

This project is licensed under the terms of the [MIT License](LICENSE).
