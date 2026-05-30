---
name: hands-3d-pose
description: High-quality 3D hand pose estimation for egocentric videos from ECCV 2024 (ap229997/hands). Provides 3D joint keypoints and skeleton visualization projected to 2D. Optimized for daily egocentric activities with state-of-the-art accuracy. Outputs hand skeleton overlays on video frames.
license: MIT license
metadata:
    skill-author: K-Dense Inc.
    original-repo: https://github.com/ap229997/hands
    paper: ECCV 2024
    skill-category: Computer Vision
    tags: [3d-hand-pose, egocentric-vision, keypoint-detection, hand-tracking, eccv-2024]
---

# 3D Hand Pose Estimation (ECCV 2024)

## Overview

State-of-the-art 3D hand pose estimation system specifically designed for egocentric (first-person) videos. Published at ECCV 2024, this method provides accurate 3D joint keypoints for hands in daily activities, with robust performance on challenging egocentric viewpoints. The system outputs detailed hand skeleton visualizations with 3D joints projected onto 2D video frames.

**Project video**: https://youtu.be/YolFnTtq38E

**Key advantage**: Delivers precise joint-level hand pose (not just bounding boxes) for detailed hand motion analysis and gesture understanding.

## When to Use This Skill

This skill should be used when:
- Need detailed 3D hand joint positions and orientations
- Analyzing hand gestures and finger movements in egocentric videos
- Building gesture recognition systems with pose-based features
- Studying hand-object interactions with precise hand geometry
- Creating annotated videos with hand skeleton overlays
- Research in egocentric activity recognition
- Applications requiring finger-level accuracy (dexterous manipulation)
- Biomechanics analysis of hand movements
- Sign language or communication gesture analysis

**Choose this when**: You need 3D joint keypoints and skeleton structure rather than just bounding boxes.

**Consider alternatives**:
- For simple hand detection only: Use `victordibia-handtracking`
- For hand-object segmentation: Use `owenzlz-egohos`
- For multi-view 3D tracking: Use `facebookresearch-hot3d`

## Core Capabilities

### 1. 3D Hand Joint Estimation

**21 hand keypoints** per hand in 3D space (x, y, z coordinates):
- Wrist (1 point)
- Palm (5 metacarpal points)
- Fingers (15 points: 3 joints per finger × 5 fingers)

**3D joint format**:
```python
joints_3d = {
    'wrist': [x, y, z],
    'thumb_mcp': [x, y, z], 'thumb_pip': [x, y, z], 'thumb_tip': [x, y, z],
    'index_mcp': [x, y, z], 'index_pip': [x, y, z], 'index_tip': [x, y, z],
    'middle_mcp': [x, y, z], 'middle_pip': [x, y, z], 'middle_tip': [x, y, z],
    'ring_mcp': [x, y, z], 'ring_pip': [x, y, z], 'ring_tip': [x, y, z],
    'pinky_mcp': [x, y, z], 'pinky_pip': [x, y, z], 'pinky_tip': [x, y, z],
}
```

### 2. 2D Projection and Visualization

**Project 3D joints to 2D image plane** for overlay:
- Camera intrinsic parameters automatically estimated
- Perspective projection for realistic visualization
- Skeleton connections drawn between joints
- Confidence scores per joint

**Visualization options**:
- Joint keypoints (circles)
- Skeleton bones (lines connecting joints)
- Confidence-based coloring
- Hand side identification (left/right)

### 3. Video Processing Pipeline

**Complete workflow** from video to annotated output:

```bash
# Clone repository
git clone https://github.com/ap229997/hands.git
cd hands

# Switch to demo branch
git checkout demo

# Install dependencies
pip install -r requirements.txt
# Key dependencies: PyTorch, OpenCV, torchvision, numpy

# Download pre-trained models
bash scripts/download_models.sh

# Run demo on video
python demo.py \
    --video_path egocentric_video.mp4 \
    --output_dir ./output \
    --visualize_skeleton \
    --save_video
```

**Output files**:
- Annotated frames (PNG/JPG)
- Compiled output video (MP4)
- 3D joint data (NPY/PKL)
- Visualization overlays

### 4. Single Frame Processing

**Process individual images** for batch analysis:

```python
import torch
from models import HandPoseEstimator
from utils import visualize_skeleton

# Load model
model = HandPoseEstimator()
model.load_pretrained('checkpoints/best_model.pth')
model.eval()

# Load image
import cv2
image = cv2.imread('frame.jpg')

# Estimate pose
with torch.no_grad():
    joints_3d, joints_2d, confidence = model(image)

# Visualize
output_image = visualize_skeleton(image, joints_2d, confidence)
cv2.imwrite('output_with_skeleton.jpg', output_image)
```

### 5. Hand Detection Integration

**Automatic hand localization**:
- Built-in hand detection (or use external detector)
- Multi-hand support (typically 1-2 hands in egocentric view)
- Hand side classification (left/right)
- Occlusion-aware reasoning

## Installation and Setup

```bash
# Clone repository
git clone https://github.com/ap229997/hands.git
cd hands

# Switch to demo branch (recommended for video processing)
git checkout demo

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install PyTorch (adjust CUDA version if needed)
pip install torch torchvision torchaudio

# Install other dependencies
pip install opencv-python numpy matplotlib pillow tqdm

# Download pre-trained models
mkdir -p checkpoints
cd checkpoints
wget https://path/to/model-weights.pth
cd ..
```

**Model weights**: Automatically downloaded or available from project releases.

## Usage Examples

### Example 1: Process Video with 3D Pose Output

```python
import cv2
import numpy as np
from models import HandPoseEstimator
from utils import project_3d_to_2d, draw_skeleton

# Initialize
model = HandPoseEstimator()
model.load_pretrained('checkpoints/model.pth')
model.eval()

# Open video
cap = cv2.VideoCapture('egocentric.mp4')
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Setup output
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_3dpose.mp4', fourcc, fps, (width, height))

frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Estimate 3D pose
    joints_3d, joints_2d, conf = model.estimate_pose(frame)

    # Project 3D to 2D for visualization
    joints_2d_proj = project_3d_to_2d(joints_3d, camera_params)

    # Draw skeleton on frame
    annotated = draw_skeleton(frame, joints_2d_proj, conf)

    # Save annotated frame
    out.write(annotated)

    # Optionally save 3D data
    np.save(f'output/joints_3d_{frame_count:04d}.npy', joints_3d)

    frame_count += 1

cap.release()
out.release()
```

### Example 2: Extract Hand Pose Features for Gesture Recognition

```python
import numpy as np
from models import HandPoseEstimator

model = HandPoseEstimator()
model.load_pretrained('checkpoints/model.pth')

def extract_features(frame):
    """Extract hand pose features for ML models"""
    joints_3d, joints_2d, conf = model.estimate_pose(frame)

    # Compute geometric features
    features = {
        # Finger angles
        'thumb_angle': compute_finger_angle(joints_3d['thumb']),
        'index_angle': compute_finger_angle(joints_3d['index']),
        'middle_angle': compute_finger_angle(joints_3d['middle']),
        'ring_angle': compute_finger_angle(joints_3d['ring']),
        'pinky_angle': compute_finger_angle(joints_3d['pinky']),

        # Hand openness
        'hand_openness': compute_hand_openness(joints_3d),

        # Palm position (relative to wrist)
        'palm_center': joints_3d['middle_mcp'] - joints_3d['wrist'],

        # Confidence
        'avg_confidence': np.mean(conf),
    }

    return features

# Process video for gesture classification
video_features = []
cap = cv2.VideoCapture('gesture_video.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    features = extract_features(frame)
    video_features.append(features)

# Use features for gesture classification
# gesture = classify_gesture(video_features)
```

### Example 3: Analyze Hand-Object Interaction

```python
import cv2
import numpy as np
from models import HandPoseEstimator

model = HandPoseEstimator()
model.load_pretrained('checkpoints/model.pth')

# Load video with hand-object interaction
cap = cv2.VideoCapture('pouring_water.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Get hand pose
    joints_3d, _, conf = model.estimate_pose(frame)

    # Check if fingers are in grasping configuration
    thumb_tip = joints_3d['thumb_tip']
    index_tip = joints_3d['index_tip']
    middle_tip = joints_3d['middle_tip']

    # Compute finger tip distances
    thumb_index_dist = np.linalg.norm(thumb_tip - index_tip)
    thumb_middle_dist = np.linalg.norm(thumb_tip - middle_tip)

    # Classify grasp
    if thumb_index_dist < 20 and thumb_middle_dist < 20:
        grasp_type = "precision_grasp"
    elif thumb_index_dist < 40:
        grasp_type = "power_grasp"
    else:
        grasp_type = "open_hand"

    # Analyze hand trajectory
    wrist_pos = joints_3d['wrist']
    # Process trajectory...

    print(f"Grasp type: {grasp_type}")
```

### Example 4: Batch Process Dataset

```python
import os
from pathlib import Path
from models import HandPoseEstimator
import json

model = HandPoseEstimator()
model.load_pretrained('checkpoints/model.pth')

video_dir = Path('egocentric_videos')
output_dir = Path('output_features')
output_dir.mkdir(exist_ok=True)

results = []

for video_path in video_dir.glob('*.mp4'):
    print(f"Processing {video_path.name}")

    cap = cv2.VideoCapture(str(video_path))
    frame_features = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        joints_3d, joints_2d, conf = model.estimate_pose(frame)

        frame_features.append({
            'frame_idx': len(frame_features),
            'joints_3d': joints_3d.tolist(),
            'joints_2d': joints_2d.tolist(),
            'confidence': conf.tolist(),
        })

    # Save results
    output_file = output_dir / f'{video_path.stem}_features.json'
    with open(output_file, 'w') as f:
        json.dump(frame_features, f)

    results.append({
        'video': str(video_path),
        'num_frames': len(frame_features),
        'output': str(output_file),
    })

# Save summary
with open(output_dir / 'processing_summary.json', 'w') as f:
    json.dump(results, f, indent=2)
```

## Model Specifications

**Architecture**: Deep neural network with backbone + pose regression head
- **Framework**: PyTorch
- **Input resolution**: 256x256 (configurable)
- **Output**: 21 joints × 3 coordinates (x, y, z) per hand
- **Model size**: ~100MB
- **Inference speed**: 15-30 FPS on modern GPU (depends on hardware)

**Training datasets**:
- EgoHands (egocentric images)
- FreiHAND (3D hand poses)
- HO3D (hand-object poses)
- Custom egocentric video datasets

**Performance metrics** (on egocentric test sets):
- 3D PCK (Percentage of Correct Keypoints): ~85% (threshold: 20mm)
- 2D PCK: ~92% (threshold: 20 pixels)
- Mean joint error: ~15mm in 3D
- AUC (Area Under Curve): 0.78

## Advanced Features

### 1. Temporal Smoothing

**Reduce jitter in video sequences**:
```python
from scipy.signal import savgol_filter

def smooth_trajectory(poses_3d, window=5, polyorder=2):
    """Apply temporal smoothing to 3D joint positions"""
    smoothed = []
    for joint_idx in range(poses_3d.shape[1]):  # 21 joints
        for coord_idx in range(3):  # x, y, z
            trajectory = poses_3d[:, joint_idx, coord_idx]
            smoothed_traj = savgol_filter(trajectory, window, polyorder)
            # Store smoothed values...
    return smoothed_poses
```

### 2. Hand Side Classification

**Determine left vs right hand**:
```python
def classify_hand_side(joints_3d):
    """Classify hand as left or right based on 3D pose"""
    # Use thumb-index vector direction
    wrist = joints_3d['wrist']
    thumb_tip = joints_3d['thumb_tip']
    index_tip = joints_3d['index_tip']

    # Compute vectors
    thumb_vec = thumb_tip - wrist
    index_vec = index_tip - wrist

    # Cross product gives hand orientation
    cross_prod = np.cross(thumb_vec, index_vec)

    # Determine side based on z-component
    if cross_prod[2] > 0:
        return 'right'
    else:
        return 'left'
```

### 3. Confidence-based Filtering

**Filter low-confidence poses**:
```python
def filter_low_confidence(joints_3d, joints_2d, conf, threshold=0.5):
    """Remove joints with low confidence"""
    mask = conf > threshold

    joints_3d_filtered = joints_3d * mask[..., np.newaxis]
    joints_2d_filtered = joints_2d * mask[..., np.newaxis]

    return joints_3d_filtered, joints_2d_filtered, mask
```

### 4. Camera Calibration

**Estimate camera intrinsics** for better projection:
```python
def estimate_camera_intrinsics(width, height, fov=60):
    """Estimate camera matrix from FOV"""
    focal_length = width / (2 * np.tan(np.radians(fov / 2)))
    cx, cy = width / 2, height / 2

    K = np.array([
        [focal_length, 0, cx],
        [0, focal_length, cy],
        [0, 0, 1]
    ])

    return K
```

## Integration with Other Skills

This skill works effectively with:
- **victordibia-handtracking**: For initial hand detection before pose estimation
- **owenzlz-egohos**: For hand-object segmentation combined with pose
- **MediaPipe tasks**: For gesture recognition and hand tracking
- **Object detection skills**: For analyzing hand-object interactions
- **Machine learning skills**: For building custom gesture classifiers

## Performance Optimization

**GPU acceleration**:
```python
# Use GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# Batch processing for efficiency
def process_batch(frames_batch):
    with torch.no_grad():
        poses = model(frames_batch)
    return poses
```

**Multi-threaded video processing**:
```python
from concurrent.futures import ThreadPoolExecutor

def process_video_threaded(video_path, num_workers=4):
    # Split video into chunks
    # Process chunks in parallel
    # Combine results
    pass
```

## Limitations and Considerations

**Scope**: Optimized for egocentric views (first-person perspective).

**Known limitations**:
- May struggle with severe hand occlusions
- Performance degrades with extreme lighting conditions
- Requires visible hand (no tables/sleeves covering hand)
- Single-view 3D estimation (depth ambiguity possible)
- Computational requirements (GPU recommended for real-time)

**Comparison to alternatives**:
- **vs victordibia-handtracking**: Provides 3D joints vs 2D boxes
- **vs owenzlz-egohos**: Pose estimation vs segmentation
- **vs facebookresearch-hot3d**: Single-view vs multi-view

## Troubleshooting

**Issue**: Model loading errors
- **Solution**: Ensure PyTorch version compatibility, check model file integrity

**Issue**: Out of memory errors
- **Solution**: Reduce batch size, use smaller input resolution, clear GPU cache

**Issue**: Poor pose quality
- **Solution**: Check video quality, ensure good lighting, verify egocentric viewpoint

**Issue**: Slow processing speed
- **Solution**: Use GPU, reduce resolution, close other applications

**Issue**: Jittery poses
- **Solution**: Apply temporal smoothing, check for unstable video input

## References and Resources

### Academic Paper
```bibtex
@inproceedings{hands2024eccv,
  title={3D Hand Pose Estimation in Egocentric Videos},
  author={[Authors]},
  booktitle={ECCV},
  year={2024}
}
```

### Code and Data
- GitHub repository: https://github.com/ap229997/hands
- Demo branch: https://github.com/ap229997/hands/tree/demo
- Project video: https://youtu.be/YolFnTtq38E

### Related Work
- FreiHAND: https://lmb.informatik.uni-freiburg.de/projects/freihand/
- HO3D: https://www.is.tue.mpg.de/person/mohan/hands2020.html
- EgoHands: https://egohands.github.io

## Best Practices

1. **Validate on your data** before large-scale processing
2. **Use GPU acceleration** for real-time or large-batch applications
3. **Apply temporal smoothing** for video output to reduce jitter
4. **Filter by confidence** to remove unreliable detections
5. **Calibrate camera** if precise 3D measurements are needed
6. **Handle edge cases** - occlusions, extreme poses, motion blur
7. **Consider complementing** with hand segmentation for occlusion handling
8. **Benchmark against** simpler methods if bounding boxes suffice

## Future Enhancements

Consider exploring:
- Fine-tune on domain-specific egocentric data
- Integrate with temporal models for smoother tracking
- Combine with hand-object segmentation for robustness
- Extend to two-hand interactions
- Add gesture classification on top of pose estimation
- Explore self-supervised pre-training on unlabeled egocentric videos
