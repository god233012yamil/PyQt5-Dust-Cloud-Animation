# PyQt5 Dust Cloud Animation

A realistic dust cloud animation widget built with PyQt5, featuring particle-based physics simulation with wind dynamics, turbulence, and natural particle decay.

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15%2B-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## Features

- **Realistic Physics Simulation**: Particles move with natural physics including velocity, drag, wind, and turbulence
- **Dynamic Wind Patterns**: Time-based wind variations create organic movement
- **Particle System**: Efficient particle spawning, updating, and cleanup
- **Smooth Gradients**: Radial gradients give particles a soft, dusty appearance
- **60 FPS Animation**: Smooth rendering with timer-based updates
- **Object-Oriented Design**: Clean, maintainable code with proper encapsulation
- **Type Hints**: Full type annotation for better code clarity and IDE support
- **Comprehensive Documentation**: Detailed docstrings for all classes and methods

## Demo

The application displays an animated dust cloud rising from the bottom of the window, with particles that:
- Drift and swirl with simulated wind
- Gradually fade and disappear
- Vary in size for depth perception
- Move with realistic turbulence
 
https://github.com/user-attachments/assets/fc192927-2cec-4418-9bf7-ef71caa112bf

## Requirements

- Python 3.7 or higher
- PyQt5 5.15 or higher

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pyqt5-dust-cloud.git
cd pyqt5-dust-cloud
```

2. Install dependencies:
```bash
pip install PyQt5
```

Or using requirements.txt:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the application directly:
```bash
python dust_cloud.py
```

### Integrating into Your Project

You can integrate the `DustCloudWidget` into your own PyQt5 application:

```python
from PyQt5.QtWidgets import QApplication, QMainWindow
from dust_cloud import DustCloudWidget

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Application")
        
        # Add the dust cloud widget
        dust_widget = DustCloudWidget()
        self.setCentralWidget(dust_widget)

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
```

### Customization

You can customize the dust cloud behavior by modifying parameters in the `DustCloudWidget` class:

```python
dust_widget = DustCloudWidget()

# Adjust spawn rate (particles per frame)
dust_widget.spawn_rate = 10  # Default: 8

# Adjust turbulence intensity
dust_widget.turbulence = 0.1  # Default: 0.05

# Modify wind strength directly
dust_widget.wind_x = 0.2
dust_widget.wind_y = -0.1
```

## Architecture

### Class Structure

#### `DustParticle`
Represents a single particle in the dust cloud system.

**Attributes:**
- `x, y`: Position coordinates
- `vx, vy`: Velocity components
- `size`: Particle size in pixels
- `opacity`: Current opacity (0-255)
- `life`: Remaining life (0-1)
- `decay_rate`: Rate of fade per frame

**Methods:**
- `update()`: Updates particle position and properties based on physics
- `is_alive()`: Checks if the particle should continue to exist

#### `DustCloudWidget`
Main widget that manages the particle system and rendering.

**Key Methods:**
- `_create_particle()`: Spawns a new particle with randomized properties
- `_update_wind()`: Updates wind patterns over time
- `update_animation()`: Main animation loop (called ~60 times per second)
- `paintEvent()`: Renders all particles using QPainter

#### `MainWindow`
Simple container window for demonstration purposes.

## Configuration Parameters

You can adjust these parameters to change the dust cloud appearance:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `spawn_rate` | 8 | Particles spawned per frame |
| `turbulence` | 0.05 | Random movement intensity |
| `wind_x` | Dynamic | Horizontal wind force |
| `wind_y` | Dynamic | Vertical wind force |
| Particle `size` | 2-8 | Size range in pixels |
| Particle `opacity` | 30-100 | Initial opacity range |
| Particle `life` | 0.7-1.0 | Initial lifespan |
| `decay_rate` | 0.002-0.006 | Fade speed |

## Performance

The application is optimized for smooth performance:
- Efficient particle cleanup (removes off-screen and dead particles)
- Hardware-accelerated rendering with QPainter antialiasing
- Typical particle count: 100-300 active particles
- Memory efficient with automatic garbage collection

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Coding Standards

This project follows:
- PEP 8 style guidelines
- Type hints for all functions and methods
- Google-style docstrings
- Object-oriented design principles

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
- Inspired by real-world particle physics simulations
- Uses radial gradients for realistic dust rendering

## Author

Your Name - [@yourhandle](https://github.com/god233012yamil)

Project Link: [https://github.com/god233012yamil/PyQt5-Dust-Cloud-Animation](https://github.com/god233012yamil/PyQt5-Dust-Cloud-Animation)

## Screenshots

*Add screenshots of your application here*

## Roadmap

- [ ] Add color customization options
- [ ] Implement multiple cloud sources
- [ ] Add mouse interaction (blow particles with cursor)
- [ ] Export animation as video
- [ ] Create preset configurations (dust storm, gentle breeze, etc.)

## Troubleshooting

**Issue: Animation is choppy**
- Reduce `spawn_rate` to decrease particle count
- Check system resources and close unnecessary applications

**Issue: Particles disappear too quickly**
- Increase particle `life` range in `_create_particle()`
- Decrease `decay_rate` range

**Issue: Window appears blank**
- Ensure PyQt5 is properly installed
- Check that the timer is starting correctly in `__init__`

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/god233012yamil/PyQt5-Dust-Cloud-Animation/issues) on GitHub.
