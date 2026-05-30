---
name: egohos-segmentation
description: Egocentric Hand-Object Segmentation (EgoHOS) - pixel-level hand and object segmentation in egocentric videos. Outputs fine-grained segmentation masks with hand regions highlighted. Specialized for hand-object interaction scenarios with pixel-accurate masks. Ideal for detailed interaction analysis.
license: MIT license
metadata:
    skill-author: K-Dense Inc.
    original-repo: https://github.com/owenzlz/EgoHOS
    skill-category: Computer Vision
    tags: [hand-segmentation, object-segmentation, egocentric-vision, pixel-level-masks, hand-object-interaction]
---

# EgoHOS - Egocentric Hand-Object Segmentation

## Overview

Fine-grained hand-object segmentation system designed for egocentric (first-person) videos. EgoHOS provides pixel-level segmentation masks that precisely separate hands from objects and background, enabling detailed analysis of hand-object interactions. The system outputs colorful mask overlays that make hand regions visually distinct and easy to analyze.

**Key advantage**: Pixel-level accuracy for understanding hand-object boundaries and contact regions, surpassing bounding box or keypoint approaches for interaction understanding.

## When to Use This Skill

This skill should be used when:
- Need pixel-accurate hand and object masks in egocentric videos
- Analyzing hand-object manipulation and interactions
- Studying contact regions between hands and objects
- Creating training data for segmentation models
- Applications requiring precise hand shape and outline
- Research in fine-grained activity recognition
- Building systems that need to understand hand-object contact
- Generating annotated videos with segmentation overlays

**Choose this when**: You need pixel-level segmentation of hands and objects, not just bounding boxes or keypoints.

**Consider alternatives**:
- For hand detection only: Use `victordibia-handtracking`
- For 3D pose estimation: Use `hands-3d-pose`
- For multi-view 3D tracking: Use `facebookresearch-hot3d`

## Core Capabilities

### 1. Pixel-Level Segmentation

**Per-pixel classification** with multiple classes:
- Hand pixels (left/right hand)
- Object pixels (manipulated objects)
- Background
- Optional: Multiple object instances

**Mask format**:
```python
masks = {
    'hand_mask': np.array(H, W),      # Binary mask for hand
    'object_mask': np.array(H, W),    # Binary mask for objects
    'combined_mask': np.array(H, W),  # Multi-class mask
    'hand_bbox': [x, y, w, h],        # Hand bounding box
    'object_bbox': [x, y, w, h],      # Object bounding box
}
```

### 2. Video Processing with Mask Overlay

**Generate annotated videos** with colorful segmentation overlays:

```bash
# Clone repository
git clone https://github.com/owenzlz/EgoHOS.git
cd EgoHOS

# Install dependencies
pip install torch torchvision opencv-python numpy pillow

# Download pre-trained models
bash scripts/download_models.sh

# Run segmentation on video
python demo.py \
    --video egocentric_video.mp4 \
    --output_dir ./output \
    --overlay_masks \
    --save_video
```

**Output features**:
- Hand regions colored (e.g., blue/cyan)
- Object regions colored (e.g., red/orange)
- Semi-transparent overlay on original video
- Smooth masks across video frames
- Edge refinement for clean boundaries

### 3. Hand-Object Interaction Analysis

**Identify contact regions** between hands and objects:
- Compute overlap between hand and object masks
- Detect grasping and manipulation moments
- Track contact regions over time
- Analyze hand pose relative to objects

```python
def analyze_contact(hand_mask, object_mask):
    """Analyze hand-object contact"""
    overlap = hand_mask & object_mask
    contact_area = np.sum(overlap)

    # Compute contact metrics
    hand_coverage = contact_area / np.sum(hand_mask)
    object_coverage = contact_area / np.sum(object_mask)

    return {
        'contact_pixels': contact_area,
        'hand_coverage': hand_coverage,
        'object_coverage': object_coverage,
    }
```

### 4. Batch Processing

**Process multiple videos** efficiently:

```python
import os
from pathlib import Path
from egohos import EgoHOS

model = EgoHOS()
model.load_model('checkpoints/best_model.pth')

video_dir = Path('egocentric_videos')
output_dir = Path('segmentation_output')

for video_path in video_dir.glob('*.mp4'):
    output_path = output_dir / f'{video_path.stem}_segmented.mp4'
    model.process_video(
        str(video_path),
        str(output_path),
        overlay=True,
        save_masks=True
    )
```

## Installation and Setup

```bash
# Clone repository
git clone https://github.com/owenzlz/EgoHOS.git
cd EgoHOS

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install PyTorch
pip install torch torchvision

# Install other dependencies
pip install opencv-python numpy pillow matplotlib tqdm

# Download pre-trained models
python scripts/download_pretrained_models.py
```

## Usage Examples

### Example 1: Basic Video Segmentation

```python
import cv2
import numpy as np
from egohos import EgoHOS

# Initialize model
model = EgoHOS()
model.load_model('checkpoints/model.pth')

# Load video
cap = cv2.VideoCapture('egocentric_video.mp4')

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Setup output
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_segmented.mp4', fourcc, fps, (width, height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Segment frame
    masks = model.segment(frame)

    # Create overlay
    overlay = model.create_overlay(frame, masks)

    # Save
    out.write(overlay)

cap.release()
out.release()
```

### Example 2: Extract Hand and Object ROIs

```python
import cv2
import numpy as np
from egohos import EgoHOS

model = EgoHOS()
model.load_model('checkpoints/model.pth')

frame = cv2.imread('frame.jpg')
masks = model.segment(frame)

# Extract hand ROI
hand_mask = masks['hand_mask']
contours, _ = cv2.findContours(hand_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if contours:
    x, y, w, h = cv2.boundingRect(contours[0])
    hand_roi = frame[y:y+h, x:x+w]
    cv2.imwrite('hand_roi.jpg', hand_roi)

# Extract object ROI
object_mask = masks['object_mask']
contours, _ = cv2.findContours(object_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if contours:
    x, y, w, h = cv2.boundingRect(contours[0])
    object_roi = frame[y:y+h, x:x+w]
    cv2.imwrite('object_roi.jpg', object_roi)
```

### Example 3: Track Hand-Object Contact Over Time

```python
from egohos import EgoHOS
import numpy as np
import cv2

model = EgoHOS()
model.load_model('checkpoints/model.pth')

cap = cv2.VideoCapture('interaction_video.mp4')

contact_timeline = []

frame_idx = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    masks = model.segment(frame)

    # Compute contact metrics
    hand_mask = masks['hand_mask']
    object_mask = masks['object_mask']

    overlap = hand_mask & object_mask
    contact_area = np.sum(overlap)

    hand_coverage = contact_area / np.sum(hand_mask) if np.sum(hand_mask) > 0 else 0
    object_coverage = contact_area / np.sum(object_mask) if np.sum(object_mask) > 0 else 0

    # Detect grasping (significant hand coverage)
    is_grasping = hand_coverage > 0.3

    contact_timeline.append({
        'frame': frame_idx,
        'contact_area': contact_area,
        'hand_coverage': hand_coverage,
        'object_coverage': object_coverage,
        'is_grasping': is_grasping,
    })

    frame_idx += 1

# Analyze timeline
grasping_frames = [t for t in contact_timeline if t['is_grasping']]
print(f"Grasping detected in {len(grasping_frames)} frames")
```

### Example 4: Generate Training Data

```python
from pathlib import Path
from egohos import EgoHOS
import cv2
import numpy as np

model = EgoHOS()
model.load_model('checkpoints/model.pth')

# Process dataset
input_dir = Path('raw_frames')
output_dir = Path('segmentation_masks')
output_dir.mkdir(exist_ok=True)

for img_path in input_dir.glob('*.jpg'):
    # Load image
    img = cv2.imread(str(img_path))

    # Generate masks
    masks = model.segment(img)

    # Save masks
    base_name = img_path.stem

    # Hand mask
    cv2.imwrite(str(output_dir / f'{base_name}_hand.png'), masks['hand_mask'] * 255)

    # Object mask
    cv2.imwrite(str(output_dir / f'{base_name}_object.png'), masks['object_mask'] * 255)

    # Combined mask (0: background, 128: hand, 255: object)
    combined = np.zeros_like(masks['hand_mask'], dtype=np.uint8)
    combined[masks['hand_mask']] = 128
    combined[masks['object_mask']] = 255
    cv2.imwrite(str(output_dir / f'{base_name}_combined.png'), combined)
```

## Model Specifications

**Architecture**: Deep learning segmentation network (typically U-Net or DeepLab variant)
- **Framework**: PyTorch
- **Input resolution**: 512x512 (typical)
- **Output**: Per-pixel class probabilities
- **Model size**: ~150MB
- **Inference speed**: 10-20 FPS on GPU

**Training datasets**:
- EgoHands (bounding boxes → masks)
- Custom hand-object interaction datasets
- Synthesized egocentric data

**Performance metrics**:
- mIoU (mean Intersection over Union): ~80% on hand class
- Pixel accuracy: ~92%
- Boundary F-score: ~85%

## Integration with Other Skills

This skill works effectively with:
- **victordibia-handtracking**: For initial hand detection
- **hands-3d-pose**: For combining segmentation with pose estimation
- **Object detection skills**: For identifying manipulated objects
- **Activity recognition**: For understanding manipulation actions

## Limitations

**Scope**: Specialized for egocentric hand-object interactions.

**Known limitations**:
- May struggle with heavy occlusions
- Performance depends on lighting conditions
- Requires visible hand-object boundary
- Single-frame processing (temporal consistency may need post-processing)
- Computational requirements (GPU recommended)

## Best Practices

1. **Use GPU** for real-time or large-scale processing
2. **Apply temporal smoothing** to reduce mask flicker in videos
3. **Post-process masks** (morphological operations) for cleaner edges
4. **Validate on your data** before production use
5. **Consider complementing** with pose estimation for full understanding
6. **Handle edge cases** - no hands, no objects, extreme lighting

## References

- GitHub repository: https://github.com/owenzlz/EgoHOS
- Related work: Hand segmentation in egocentric videos
- Applications: Activity recognition, HCI, robotics

## Citation

```bibtex
@software{owenzlz_egohos,
  author = {Owen [Last Name]},
  title = {EgoHOS: Egocentric Hand-Object Segmentation},
  url = {https://github.com/owenzlz/EgoHOS},
  year = {2023}
}
```
