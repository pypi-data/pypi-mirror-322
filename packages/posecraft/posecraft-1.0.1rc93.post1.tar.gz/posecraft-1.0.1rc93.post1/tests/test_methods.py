#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a sample python file for testing functions from the source code."""
from __future__ import annotations

import torch
import numpy as np
from posecraft.Pose import Pose
from posecraft.transforms import CenterToKeypoint, NormalizeDistances, FillMissing


def test_pose_initialization():
    """
    Test initialization of the Pose class from a tensor and a file path.
    """
    # Create a mock tensor for testing
    mock_tensor = torch.rand((10, 2, 33, 3))  # (frames, people, keypoints, dimensions)
    pose = Pose(pose=mock_tensor)
    assert pose.pose.shape == mock_tensor.shape, "Pose tensor shape mismatch"

    # Save and load a mock .npy file
    np.save("test_pose.npy", mock_tensor.numpy())
    pose_from_file = Pose(path="test_pose.npy")
    assert torch.equal(pose_from_file.pose, mock_tensor), "Pose tensor load mismatch"


def test_center_to_keypoint():
    """
    Test the CenterToKeypoint transform.
    """
    mock_tensor = torch.rand((10, 1, 33, 3))
    transform = CenterToKeypoint(center_keypoint=0)
    centered_tensor = transform(mock_tensor)

    # The center keypoint should now be approximately 0.5 in each dimension
    assert torch.allclose(centered_tensor[:, :, 0, :], torch.tensor([0.5, 0.5, 0.5]), atol=1e-2), "Centering failed"


def test_fill_missing():
    """
    Test the FillMissing transform.
    """
    mock_tensor = torch.rand((10, 1, 33, 3))
    # Introduce NaNs to simulate missing values
    mock_tensor[5:, :, 0, :] = float("nan")

    transform = FillMissing()
    filled_tensor = transform(mock_tensor)

    # Ensure there are no NaNs in the filled tensor
    assert not torch.isnan(filled_tensor).any(), "FillMissing did not fill NaNs correctly"


def test_chain_transforms():
    """
    Test chaining multiple transforms using Sequential.
    """
    mock_tensor = torch.rand((10, 1, 33, 3))
    transform = torch.nn.Sequential(
        CenterToKeypoint(center_keypoint=0),
        NormalizeDistances(indices=(0, 1), distance_factor=1.0),
    )
    transformed_tensor = transform(mock_tensor)

    # Perform basic sanity checks on the transformed tensor
    assert transformed_tensor.shape == mock_tensor.shape, "Shape mismatch after transforms"


def test_int_hello():
    """
    This test is marked implicitly as an integration test because the name contains "_init_"
    https://docs.pytest.org/en/6.2.x/example/markers.html#automatically-adding-markers-based-on-test-names
    """
    print("Dummy integration test")
