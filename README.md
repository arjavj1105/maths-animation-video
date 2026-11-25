# Gaussian Elimination: Solving a 3×3 System of Linear Equations

**Mathematics 3 (Linear Algebra and Calculus) — Internal Assessment Animation Video**

---

## Student Credentials

- **Student Name:** Arjav Jain
- **Student ID:** E25B070861
- **Batch:** Ramanujan
- **Course:** Mathematics 3 (Linear Algebra and Calculus)
- **Project Option:** Option 1 — Animation Video
- **GitHub Repository:** [https://github.com/arjavj1105/maths-animation-video](https://github.com/arjavj1105/maths-animation-video)

---

## Project Overview & Learning Objective

This project is an educational mathematical animation teaching Gaussian Elimination to fellow engineering students. It connects formal matrix algebra with 3D geometric intuition, demonstrating how elementary row operations transform a system of three intersecting planes into upper-triangular row echelon form to reveal a unique intersection point.

### Official Learning Objective
> *"By the end of this video, the viewer will be able to explain how Gaussian elimination uses row operations to reduce a 3×3 system to row echelon form, why those operations do not change the solution set, and what the solution means geometrically."*

---

## The Mathematical Problem & Verified Solution

### 1. System of Linear Equations
$$\begin{aligned}
x + y + z &= 6 \\
2x + 3y + z &= 11 \\
x + 2y + 3z &= 14
\end{aligned}$$

### 2. Matrix Representation ($Ax = b$)
$$\begin{bmatrix} 1 & 1 & 1 \\ 2 & 3 & 1 \\ 1 & 2 & 3 \end{bmatrix} \begin{bmatrix} x \\ y \\ z \end{bmatrix} = \begin{bmatrix} 6 \\ 11 \\ 14 \end{bmatrix}$$

Initial Augmented Matrix:
$$\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 2 & 3 & 1 & 11 \\ 1 & 2 & 3 & 14 \end{array}\right]$$

### 3. Step-by-Step Elementary Row Operations

1. **Operation 1 ($R_2 \to R_2 - 2R_1$):**
   $$[2, 3, 1 \mid 11] - 2[1, 1, 1 \mid 6] = [0, 1, -1 \mid -1]$$
   $$\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & -1 & -1 \\ 1 & 2 & 3 & 14 \end{array}\right]$$

2. **Operation 2 ($R_3 \to R_3 - R_1$):**
   $$[1, 2, 3 \mid 14] - [1, 1, 1 \mid 6] = [0, 1, 2 \mid 8]$$
   $$\left[\begin{array}{ccc|c} 1 & 1 & 1 & 6 \\ 0 & 1 & -1 & -1 \\ 0 & 1 & 2 & 8 \end{array}\right]$$

3. **Operation 3 ($R_3 \to R_3 - R_2$):**
   $$[0, 1, 2 \mid 8] - [0, 1, -1 \mid -1] = [0, 0, 3 \mid 9]$$
   $$\left[\begin{array}{ccc|c} \mathbf{1} & 1 & 1 & 6 \\ 0 & \mathbf{1} & -1 & -1 \\ 0 & 0 & \mathbf{3} & 9 \end{array}\right]$$

### 4. Row Echelon Form (REF) & Pivots
- **Pivot 1:** $1$ at Row 1, Column 1
- **Pivot 2:** $1$ at Row 2, Column 2
- **Pivot 3:** $3$ at Row 3, Column 3
- All entries below each pivot are zero, and pivots advance strictly to the right.

### 5. Back Substitution
- **From Row 3:** $3z = 9 \implies \mathbf{z = 3}$
- **From Row 2:** $y - z = -1 \implies y - 3 = -1 \implies \mathbf{y = 2}$
- **From Row 1:** $x + y + z = 6 \implies x + 2 + 3 = 6 \implies \mathbf{x = 1}$

### 6. Final Verified Solution
$$(x, y, z) = (1, 2, 3)$$

All three original equations are satisfied with zero residuals:
- $1 + 2 + 3 = 6 \implies 6 = 6$ ✓
- $2(1) + 3(2) + 3 = 2 + 6 + 3 = 11 \implies 11 = 11$ ✓
- $1 + 2(2) + 3(3) = 1 + 4 + 9 = 14 \implies 14 = 14$ ✓

---

## Six-Scene Video Structure

| Scene | Scene Title | Purpose & Visual Progression | Mathematics Covered | Duration |
|:---:|:---|:---|:---|:---:|
| **1** | **Hook / Context** | Opening credentials card; sequential reveal of the 3 simultaneous equations; tangled trial & error vs systematic algorithms. | System definition; motivation for Gaussian elimination. | **34.5s** |
| **2** | **Concept Introduction** | Matrix form $Ax = b$; augmented matrix $[A \mid b]$; mandatory learning objective; 3 elementary row operations and reversibility. | Compact notation; row swaps, scaling, and replacements; REF criteria. | **46.0s** |
| **3** | **Visual Intuition** | 3D coordinate system; three semi-transparent intersecting planes; unique point $(1, 2, 3)$; 360° orbiting camera; plane tilt invariance. | Plane equations in $\mathbb{R}^3$; line of intersection; geometric invariance under row operations. | **46.0s** |
| **4** | **Worked Example** | The core algorithm: step-by-step matrix row operations; side-by-side arithmetic; highlighted pivots; REF staircase; back substitution. | $R_2 \to R_2 - 2R_1$, $R_3 \to R_3 - R_1$, $R_3 \to R_3 - R_2$; pivots $1, 1, 3$; back substitution. | **89.5s** |
| **5** | **Interpretation** | Verification by direct substitution with green checkmarks; 3D point reconnection; special cases (inconsistent vs dependent). | Verification: $6=6, 11=11, 14=14$; inconsistent $[0\ 0\ 0 \mid 5]$; dependent $[0\ 0\ 0 \mid 0]$. | **61.0s** |
| **6** | **Summary & Credits** | Three key takeaways; final solution restatement; academic citations; AI disclosure; academic closing credentials. | Core principles summary; solution $(1, 2, 3)$; full references and disclosures. | **55.0s** |

**Total Video Duration:** ~332 seconds (**5.5 minutes**) — strictly adheres to the ~5-minute recommendation and $\le 7$-minute ceiling.

---

## Repository Structure

```
maths-animation-video/
├── _Video.mp4                      # Final 1080p 30 FPS narrated MP4 video
├── Storyboard.pdf                  # Official 6-scene storyboard table and plan
├── Narration_Script.pdf            # Complete verbatim narration script with timings
├── Code_Walkthrough.pdf            # Beginner-friendly code explanation for viva prep
├── Viva_Prep.pdf                   # 15 likely viva questions with detailed answers
├── README.md                       # Comprehensive project documentation
├── .gitignore                      # Git ignore rules for caches and media temp files
│
└── _Code/
    ├── scenes/                     # Manim animation scene scripts
    │   ├── scene_01_hook.py
    │   ├── scene_02_concepts.py
    │   ├── scene_03_geometry.py
    │   ├── scene_04_worked_example.py
    │   ├── scene_05_interpretation.py
    │   └── scene_06_summary.py
    │
    ├── helpers/                    # Shared styling and layout helper modules
    │   ├── matrix_helpers.py
    │   ├── animation_helpers.py
    │   └── audio_helpers.py
    │
    ├── narration/                  # Scene-by-scene narration text files
    │   ├── scene_01.txt
    │   ├── scene_02.txt
    │   ├── scene_03.txt
    │   ├── scene_04.txt
    │   ├── scene_05.txt
    │   └── scene_06.txt
    │
    ├── audio/                      # Original recordings, processed audio & manifest
    │   ├── human_voiceovers/       # Arjav Jain's original audio recordings (scene_01.m4a ... scene_06.m4a)
    │   ├── processed/              # Standardized 44.1kHz 16-bit EBU R128 WAV files
    │   ├── scene_audio_manifest.json # Audio metadata, durations, and loudness analysis
    │   ├── scene_audio_manifest.md   # Markdown summary of audio analysis
    │   └── durations.txt           # Measured audio durations per scene
    │
    ├── scripts/                    # Automation and pipeline scripts
    │   ├── verify_mathematics.py   # NumPy automated verification suite
    │   ├── process_audio.py        # Human audio processing and loudness normalization
    │   ├── render_scenes.py        # 1080p Manim batch rendering (synchronized to human voice)
    │   ├── merge_video_audio.py    # FFmpeg audio-video synchronization & final concatenation
    │   ├── generate_documents.py   # ReportLab academic PDF documentation builder
    │   └── quality_check.py        # Technical ffprobe verification & frame extraction
    │
    └── requirements.txt            # Python dependencies
```

---

## Technology Stack

- **Animation Engine:** [Manim Community Edition (v0.22.1)](https://www.manim.community/) — Python programmatic mathematical animation engine.
- **3D Geometry:** Manim `ThreeDScene`, `ThreeDAxes`, and `Surface` parametric plotting.
- **Mathematical Verification:** [NumPy (v2.5.5)](https://numpy.org/) — Linear algebra verification (`det`, `solve`, array operations, residuals).
- **Voiceover Narration:** Original human narration recorded by **Arjav Jain** (Student ID: E25B070861, Batch: Ramanujan) — standardized and gently normalized using FFmpeg EBU R128 loudness standards (-18 LUFS, -1.5 dB true peak headroom).
- **Video & Audio Processing:** [FFmpeg (v9.0.2)](https://ffmpeg.org/) — Audio-video synchronization, H.264/AAC encoding, and concatenation.
- **Document Generation:** [ReportLab (v4.5.1)](https://www.reportlab.com/) — Programmatic PDF generation with professional typography.

---

## Visual Design & Color Palette

A strict, accessible mathematical color scheme is maintained throughout:
- **Row 1 / Plane 1:** Bright Blue (`#3B82F6`)
- **Row 2 / Plane 2:** Emerald Green (`#10B981`)
- **Row 3 / Plane 3:** Vivid Orange (`#F97316`)
- **Pivot Elements:** Golden Yellow (`#FBBF24`)
- **Background:** Deep Navy / Charcoal (`#0B1120`)
- **Explanatory Typography:** Crisp White (`#F8FAFC`) / Slate Muted (`#94A3B8`)
- **Verification Checks:** Bright Green (`#22C55E`)

---

## Reproduction & Build Workflow

Follow these steps to reproduce the complete project from source:

### 1. Install System Dependencies
Ensure `ffmpeg` and `manim` are installed:
```bash
brew install ffmpeg manim
```

### 2. Install Python Dependencies
```bash
pip install -r _Code/requirements.txt
```

### 3. Verify Mathematics
Execute the automated NumPy verification suite:
```bash
python3 _Code/scripts/verify_mathematics.py
```

### 4. Process Human Voiceover Narration
Standardize human voice recordings and generate audio manifest:
```bash
python3 _Code/scripts/process_audio.py
```

### 5. Render All Scenes in 1080p
Batch render all six Manim scenes at 1080p 30 FPS:
```bash
python3 _Code/scripts/render_scenes.py
```

### 6. Merge Audio & Video
Synchronize audio and concatenate scenes into the final video:
```bash
python3 _Code/scripts/merge_video_audio.py
```

### 7. Run Quality Assurance
Run technical specification checks (H.264, AAC, 1920×1080, 30 FPS) and extract sample inspection frames:
```bash
python3 _Code/scripts/quality_check.py
```

### 8. Generate Supporting PDFs
Build all four academic documentation PDFs:
```bash
python3 _Code/scripts/generate_documents.py
```

---

## Technical Video Specifications

- **Container:** MP4
- **Video Codec:** H.264 (AVC)
- **Audio Codec:** AAC (192 kbps, 44.1 kHz, mono)
- **Resolution:** 1920 × 1080 (1080p Full HD)
- **Aspect Ratio:** 16:9 Landscape
- **Frame Rate:** 30.0 FPS
- **Duration:** ~316.6 seconds (5 minutes 16.6 seconds) — safely under the 7-minute ceiling
- **Audio:** Original human voiceover by Arjav Jain, zero clipping, EBU R128 normalized, synchronized visual transitions.

---

## References

1. **Strang, Gilbert.** *Introduction to Linear Algebra.* 5th Edition, Wellesley-Cambridge Press, 2016.
2. **Lay, David C., Lay, Steven R., & McDonald, Judi J.** *Linear Algebra and Its Applications.* 5th Edition, Pearson, 2016.
3. **Manim Community Developers.** *Manim – Mathematical Animation Framework.* Documentation & API Reference (v0.22.1), 2026. [https://docs.manim.community](https://docs.manim.community)

---

## AI Disclosure

AI tools assisted in preparing the script, animation code and visual design. Voiceover: Original narration recorded by Arjav Jain. All mathematical calculations were independently verified.
