---
name: handtracking
description: Real-time hand detection in egocentric videos using victordibia/handtracking. Outputs bounding boxes for hands, specifically trained on EgoHands dataset. Supports video input/output with labeled hand boxes. Lightweight and fast for egocentric view applications.
license: MIT license
metadata:
    skill-author: K-Dense Inc.
    original-repo: https://github.com/victordibia/handtracking
    skill-category: Computer Vision
    tags: [hand-tracking, egocentric-vision, object-detection, tensorflow]
---

# HandTracking - Real-time Hand Detection

## Overview

Real-time hand detection system designed specifically for egocentric (first-person) video views. Trained on the EgoHands dataset, this lightweight model detects hand bounding boxes in video streams and can output labeled videos with hand annotations. Ideal for quick prototyping of hand-based interaction systems in AR/VR and wearable computing applications.

**Companion JavaScript library**: Handtrack.js is available for browser-based applications (https://github.com/victordibia/handtrack.js).

## When to Use This Skill

This skill should be used when:
- Analyzing egocentric video footage from wearable cameras or smart glasses
- Detecting hand presence and location in first-person perspective videos
- Building hand gesture interfaces or interaction systems
- Annotating training data for hand detection models
- Processing egocentric videos for human-computer interaction research
- Creating labeled video outputs with hand bounding box overlays
- Implementing real-time hand detection in web applications (using Handtrack.js)
- Quick prototyping of hand-based AR/VR interfaces

**Choose this when**: You need fast, lightweight hand detection with bounding box outputs and don't require detailed joint-level pose estimation.

**Consider alternatives**: If you need 3D hand pose keypoints, hand-object segmentation, or multi-view tracking, see other skills in this category.

## Core Capabilities

### 1. Hand Detection in Egocentric Views

**EgoHands-trained model**: Specifically optimized for first-person perspective videos where hands are viewed from the wearer's viewpoint.

- **Input**: Video files (MP4, AVI) or webcam streams
- **Output**: Bounding boxes (x, y, width, height) with confidence scores
- **Model**: Lightweight TensorFlow model trained on EgoHands dataset
- **Performance**: Real-time processing on standard hardware
- **Detection types**: Left hand, right hand classification
- **Visualization**: Red/green bounding boxes overlaid on video

**Bounding box format**:
```python
{
    'bbox': [x, y, width, height],  # Pixel coordinates
    'score': confidence,              # 0.0 to 1.0
    'label': 'hand'                   # Detection label
}
```

### 2. Video Processing and Annotation

**Input video processing**: Process entire video files and export annotated results.

**Workflow**:
```bash
# Clone repository
git clone https://github.com/victordibia/handtracking.git
cd handtracking

# Install dependencies (TensorFlow 1.x compatible)
pip install tensorflow==1.15.0 opencv-python numpy

# Run hand detection on video
python run.py \
    --input_video your_egocentric.mp4 \
    --output_video output_labeled.mp4 \
    --threshold 0.5  # Confidence threshold
```

**Output video features**:
- Hands outlined with colored bounding boxes (red/green)
- Real-time frame rate display
- Confidence scores shown on boxes
- Smooth tracking across frames
-保存带标注的视频文件

### 3. Real-time Webcam Detection

**Live camera processing**: Process webcam streams in real-time for interactive applications.

```python
import handtracking

# Initialize detector
detector = handtracking.HandDetector()

# Process webcam stream
detector.detect_from_webcam(
    display=True,
    save_video=False,
    confidence_threshold=0.6
)
```

**Applications**:
- Live hand gesture interfaces
- Interactive installations
- Real-time hand presence detection
- Gesture-controlled systems

### 4. Browser-based Detection (Handtrack.js)

**JavaScript companion library**: Use the same model technology in web applications.

**Integration**:
```html
<script src="https://cdn.jsdelivr.net/npm/handtrackjs/dist/handtrack.min.js"></script>

<script>
const model = await handTrack.load();
const video = document.getElementById('video');

// Detect hands in video stream
const predictions = await model.detect(video);
predictions.forEach(prediction => {
    console.log(prediction.bbox);  // [x, y, width, height]
    console.log(prediction.score); // Confidence score
});
</script>
```

**Browser capabilities**:
- Run entirely in browser (no server required)
- Real-time webcam processing
- Canvas-based visualization
- WebGL acceleration support
- Works with video files and live streams

## Installation and Setup

### Option 1: Python Installation

```bash
# Clone repository
git clone https://github.com/victordibia/handtracking.git
cd handtracking

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install tensorflow==1.15.0
pip install opencv-python numpy pillow

# Download pre-trained model
# Model will be automatically downloaded on first run
```

**Model files**: Automatically downloaded from the repository on first use (~20MB).

### Option 2: JavaScript Installation (Handtrack.js)

```bash
# For web applications
npm install handtrackjs

# Or use directly from CDN
```

## Usage Examples

### Example 1: Process Video with Output

```python
import cv2
from handtracking import HandDetector

# Initialize detector
detector = HandDetector()

# Load video
cap = cv2.VideoCapture('egocentric_video.mp4')

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Setup video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_labeled.mp4', fourcc, fps, (width, height))

# Process frames
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detect hands
    detections = detector.detect_hands(frame)

    # Draw bounding boxes
    for det in detections:
        x, y, w, h = det['bbox']
        score = det['score']

        # Draw box
        color = (0, 255, 0) if score > 0.7 else (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

        # Add label
        label = f"Hand: {score:.2f}"
        cv2.putText(frame, label, (x, y-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Save frame
    out.write(frame)

cap.release()
out.release()
```

### Example 2: Extract Hand Regions

```python
import cv2
import numpy as np
from handtracking import HandDetector

detector = HandDetector()
cap = cv2.VideoCapture('egocentric.mp4')

frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    detections = detector.detect_hands(frame)

    # Extract and save hand regions
    for i, det in enumerate(detections):
        x, y, w, h = det['bbox']

        # Crop hand region
        hand_roi = frame[y:y+h, x:x+w]

        # Save hand image
        if det['score'] > 0.7:  # High confidence only
            cv2.imwrite(f'hand_{frame_count}_{i}.jpg', hand_roi)

    frame_count += 1

cap.release()
```

### Example 3: Real-time Detection Statistics

```python
from handtracking import HandDetector
import cv2

detector = HandDetector()
cap = cv2.VideoCapture(0)  # Webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    detections = detector.detect_hands(frame)

    # Display statistics
    num_hands = len(detections)
    avg_confidence = sum(d['score'] for d in detections) / num_hands if num_hands > 0 else 0

    # Overlay text
    cv2.putText(frame, f"Hands: {num_hands}", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Avg Conf: {avg_confidence:.2f}", (10, 70),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Hand Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### Example 4: Browser-based Detection

```javascript
// Load model
const modelParams = {
    flipHorizontal: true,
    maxNumBoxes: 2,
    iouThreshold: 0.5,
    scoreThreshold: 0.6,
};

handTrack.load(modelParams).then(model => {
    // Model loaded
    console.log("Model loaded");

    // Detect from video element
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');

    function detectFrame() {
        model.detect(video).then(predictions => {
            // Clear canvas
            context.clearRect(0, 0, canvas.width, canvas.height);

            // Draw video frame
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            // Draw predictions
            predictions.forEach(prediction => {
                const [x, y, width, height] = prediction.bbox;
                context.strokeStyle = '#00FF00';
                context.lineWidth = 4;
                context.strokeRect(x, y, width, height);

                // Add label
                context.fillStyle = '#00FF00';
                context.fillText(
                    `Hand: ${prediction.score.toFixed(2)}`,
                    x, y - 10
                );
            });

            // Continue detection
            requestAnimationFrame(detectFrame);
        });
    }

    // Start detection
    detectFrame();
});
```

## Integration with Other Skills

This skill works effectively with:
- **MediaPipe skills**: For more advanced hand pose estimation and gesture recognition
- **OpenCV-based video processing skills**: For comprehensive video analysis pipelines
- **Machine learning skills**: For building custom hand gesture classifiers
- **XR/AR framework skills**: For integrating hand detection into immersive experiences

## Model Specifications

**Architecture**: Lightweight CNN-based object detection model
- **Framework**: TensorFlow 1.x (compatible with older TF versions)
- **Training dataset**: EgoHands (4,800 egocentric images)
- **Input resolution**: Flexible (recommended: 640x480)
- **Model size**: ~20MB
- **Inference speed**: 30+ FPS on standard CPU (depends on resolution)

**Detection performance** (on EgoHands test set):
- mAP: ~85% (mean Average Precision)
- Recall: ~82%
- Precision: ~88%

## Limitations and Considerations

**Scope**: This skill provides bounding box detection only. For more detailed analysis, consider:

- **3D hand pose estimation**: Use `ap229997-hands` skill for joint keypoints
- **Hand-object segmentation**: Use `owenzlz-egohos` skill for pixel-level masks
- **Multi-view tracking**: Use `facebookresearch-hot3d` for 3D tracking

**Known limitations**:
- Trained primarily on egocentric views (first-person perspective)
- May have reduced performance on third-person views
- Bounding boxes only (no joint or finger-level details)
- Requires TensorFlow 1.x (not compatible with TF 2.x without modifications)
- Model trained on diverse hands but may have bias toward certain demographics

**When to upgrade**:
- Need 3D hand joint positions → Use ap229997-hands
- Need hand-object interaction segmentation → Use owenzlz-egohos
- Need multi-view or high-precision 3D tracking → Use facebookresearch-hot3d
- Need browser-based 3D hand tracking → Consider MediaPipe Hands

## Performance Optimization

**CPU optimization**:
```python
# Reduce input resolution for faster processing
detector = HandDetector()
frame = cv2.resize(frame, (640, 480))  # Downsample
detections = detector.detect_hands(frame)
```

**GPU acceleration** (if available):
```python
# TensorFlow with GPU support
import tensorflow as tf
# Install tensorflow-gpu for GPU acceleration
```

**Batch processing**:
```python
# Process multiple videos in parallel
from concurrent.futures import ThreadPoolExecutor

def process_video(video_path):
    detector = HandDetector()
    return detector.process_video(video_path)

with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(process_video, video_list)
```

## Troubleshooting

**Issue**: Model not downloading automatically
- **Solution**: Manually download model files from the GitHub repository and place in the models directory

**Issue**: TensorFlow version conflicts
- **Solution**: Use virtual environment with TensorFlow 1.15.0: `pip install tensorflow==1.15.0`

**Issue**: Low detection accuracy
- **Solution**: Adjust confidence threshold (try 0.5-0.7), ensure video quality is adequate, check that view is egocentric

**Issue**: Slow processing speed
- **Solution**: Reduce video resolution, close other applications, consider GPU acceleration

**Issue**: No hands detected
- **Solution**: Check if video is in egocentric view, lower confidence threshold, improve lighting conditions

## References and Resources

### Documentation
- GitHub repository: https://github.com/victordibia/handtracking
- EgoHands dataset paper: https://egohands.github.io
- Handtrack.js documentation: https://github.com/victordibia/handtrack.js

### Related Projects
- EgoHands Dataset: https://github.com/egohands/EgoHands
- MediaPipe Hands: https://google.github.io/mediapipe/solutions/hands.html
- OpenPose: https://github.com/CMU-Perceptual-Computing-Lab/openpose

### Example Applications
- Gesture-controlled interfaces
- Sign language detection
- Human-computer interaction research
- AR/VR hand tracking
- Activity recognition from egocentric video

## Citation

If you use this hand tracking implementation in research, please cite:

```bibtex
@article{betancourt2015egohands,
  title={Egohands: A dataset for egocentric hand interactions},
  author={Betancourt, Alex and Orozco, Jorge and Bolaños, Mauricio},
  journal={arXiv preprint arXiv:1509.06044},
  year={2015}
}
```

And the original repository:
```bibtex
@software{victordibia_handtracking,
  author = {Victor Dibia},
  title = {Real-time Hand Detection in Python using TensorFlow},
  url = {https://github.com/victordibia/handtracking},
  year = {2018}
}
```

## Best Practices

1. **Start with this skill** for quick prototyping and proof-of-concept
2. **Validate on your data** before committing to production use
3. **Consider GPU acceleration** for real-time applications
4. **Test confidence thresholds** on your specific use case
5. **Use appropriate resolution** - balance between speed and accuracy
6. **Handle edge cases** - no hands, occluded hands, multiple hands
7. **Post-process results** - smoothing, filtering, temporal consistency
8. **Benchmark alternatives** before final implementation

## Future Enhancements

Consider exploring these related directions:
- Fine-tune model on domain-specific egocentric data
- Integrate with gesture recognition pipelines
- Combine with object detection for hand-object interactions
- Extend to browser applications using Handtrack.js
- Upgrade to 3D pose estimation for more detailed analysis
