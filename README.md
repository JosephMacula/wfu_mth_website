# wfu_mth_website
This is a repo to prototype things to add to the Wake Math Department's website.

## Current prototype: narrated course flowcharts

Narrated animations of the two flowcharts on page 2 of the department brochure: the **Calculus Sequence** and the **Foundational Courses**. Each course appears as a box while a narrator introduces it, and an arrow grows from each course to the courses a student can take after it. The videos are built with [manim](https://www.manim.community/), and the narration uses [manim-voiceover](https://voiceover.manim.community/).

- `animations/course_graphs.py` holds the course data. Each flowchart is a directed graph, where an edge from course A to course B means a student can take B after completing A.
- `animations/flowcharts.py` holds the scenes and the narration text for each step.

### Setup

Install the system packages (Ubuntu/Debian), then the Python packages:

```bash
sudo apt-get install ffmpeg libcairo2-dev libpango1.0-dev pkg-config sox
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

### Rendering

```bash
cd animations
../.venv/bin/manim -ql flowcharts.py CalculusSequence      # 480p preview
../.venv/bin/manim -qh flowcharts.py FoundationalCourses   # 1080p
```

The videos are written to `animations/media/videos/flowcharts/<quality>/`, along with `.srt` subtitles. The narration uses Google's Gemini text-to-speech, which needs an API key. Create one at https://aistudio.google.com/app/apikey and put it in a `.env` file at the repo root as `GEMINI_API_KEY=...`. That file is gitignored, so never commit the key. The first render needs internet access to generate the narration audio. The audio is then cached under `animations/media/`, so later renders only generate (and pay for) lines that changed.

**Viewing:** VS Code's built-in video preview plays these videos without sound. To hear the narration, download the `.mp4` (right-click it in the Explorer, then **Download…**) and play it in a regular media player.

## Next step: rework the narration

The current narration text is a placeholder: generic wording written from the flowcharts alone. The voice has already moved from Google's free, robotic-sounding gTTS to Gemini text-to-speech.

1. **Script:** replace the generated text with a narration script prepared by the department, one passage per step of each animation.
2. **Voice:** done for now with Gemini. A different Gemini voice, or a recorded human voice, is still an option. Because narration goes through manim-voiceover, changing it means changing the speech service in `FlowchartScene.setup`, not the animation code.
