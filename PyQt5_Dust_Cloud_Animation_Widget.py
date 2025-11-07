"""
PyQt5 Dust Cloud Animation Widget

A widget that displays a realistic dust cloud animation using particle systems.
"""

import sys
import random
import math
from typing import List, Tuple
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtCore import QTimer, Qt, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QRadialGradient, QPalette


class DustParticle:
    """
    Represents a single dust particle in the animation.

    Attributes:
        x: X-coordinate of the particle
        y: Y-coordinate of the particle
        vx: Velocity in x direction
        vy: Velocity in y direction
        size: Size of the particle
        opacity: Opacity value (0-255)
        life: Remaining life of the particle (0-1)
        decay_rate: Rate at which the particle fades
    """

    def __init__(self, x: float, y: float, vx: float, vy: float,
                 size: float, opacity: int, life: float, decay_rate: float):
        """
        Initialize a dust particle.

        Args:
            x: Initial x position
            y: Initial y position
            vx: Initial velocity in x direction
            vy: Initial velocity in y direction
            size: Particle size in pixels
            opacity: Initial opacity (0-255)
            life: Initial life value (0-1)
            decay_rate: Rate of particle decay per frame
        """
        self.x: float = x
        self.y: float = y
        self.vx: float = vx
        self.vy: float = vy
        self.size: float = size
        self.opacity: int = opacity
        self.life: float = life
        self.decay_rate: float = decay_rate
        self.base_opacity: int = opacity

    def update(self, wind_x: float, wind_y: float, turbulence: float) -> None:
        """
        Update particle position and properties.

        Args:
            wind_x: Wind force in x direction
            wind_y: Wind force in y direction
            turbulence: Random turbulence factor
        """
        # Apply wind and turbulence
        self.vx += wind_x + random.uniform(-turbulence, turbulence)
        self.vy += wind_y + random.uniform(-turbulence, turbulence)

        # Apply drag to simulate air resistance
        self.vx *= 0.98
        self.vy *= 0.98

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Update life and opacity
        self.life -= self.decay_rate
        self.opacity = int(self.base_opacity * self.life)

    def is_alive(self) -> bool:
        """
        Check if the particle is still alive.

        Returns:
            True if particle life is greater than 0, False otherwise
        """
        return self.life > 0


class DustCloudWidget(QWidget):
    """
    A widget that displays an animated dust cloud using particle systems.

    The widget creates and manages multiple dust particles that move with
    realistic physics including wind, turbulence, and natural decay.
    """

    def __init__(self, parent: QWidget = None):
        """
        Initialize the dust cloud widget.

        Args:
            parent: Parent widget (optional)
        """
        super().__init__(parent)
        self.particles: List[DustParticle] = []
        self.wind_x: float = 0.0
        self.wind_y: float = 0.0
        self.turbulence: float = 0.05
        self.spawn_rate: int = 8  # Particles per frame

        # Animation properties
        self.frame_count: int = 0

        # Set up the widget
        self.setMinimumSize(800, 600)

        # Set the background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        # palette.setColor(self.backgroundRole(), QColor(0, 0, 0))
        palette.setColor(self.backgroundRole(), QColor(160, 160, 160, 0))  # transparent background
        self.setPalette(palette)

        # Set up animation timer
        self.timer: QTimer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # ~60 FPS

        # Initialize with some particles
        self._spawn_initial_particles()

    def _spawn_initial_particles(self) -> None:
        """
        Spawn initial particles to populate the cloud.
        """
        for _ in range(100):
            self._create_particle()

    def _create_particle(self) -> None:
        """
        Create a new dust particle with random properties.
        """
        width = self.width()
        height = self.height()

        # Spawn particles from the bottom-center area
        spawn_x = width / 2 + random.uniform(-150, 150)
        spawn_y = height + random.uniform(0, 50)

        # Upward velocity with some randomness
        vx = random.uniform(-0.5, 0.5)
        vy = random.uniform(-2.5, -1.0)

        # Variable size for depth perception
        size = random.uniform(2, 8)

        # Brownish-gray dust colors with variation
        # opacity = random.randint(30, 100)
        opacity = random.randint(150, 250)

        # Life span
        life = random.uniform(0.7, 1.0)
        decay_rate = random.uniform(0.002, 0.006)

        particle = DustParticle(spawn_x, spawn_y, vx, vy, size,
                                opacity, life, decay_rate)
        self.particles.append(particle)

    def _update_wind(self) -> None:
        """
        Update wind direction and strength over time.
        """
        # Gentle, changing wind patterns
        self.wind_x = 0.1 * math.sin(self.frame_count * 0.01)
        self.wind_y = -0.05 + 0.05 * math.cos(self.frame_count * 0.015)

    def update_animation(self) -> None:
        """
        Update animation state for all particles.
        """
        self.frame_count += 1

        # Update wind
        self._update_wind()

        # Update existing particles
        for particle in self.particles:
            particle.update(self.wind_x, self.wind_y, self.turbulence)

        # Remove dead particles
        self.particles = [p for p in self.particles if p.is_alive()
                          and 0 <= p.x <= self.width()
                          and -100 <= p.y <= self.height() + 100]

        # Spawn new particles
        for _ in range(self.spawn_rate):
            self._create_particle()

        # Trigger repaint
        self.update()

    def paintEvent(self, event) -> None:
        """
        Paint the dust cloud particles.

        Args:
            event: Paint event
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Fill background with black
        # painter.fillRect(self.rect(), QColor(0, 0, 0))
        painter.fillRect(self.rect(), QColor(0, 0, 0, 0))  # transparent background

        # Draw each particle
        for particle in self.particles:
            self._draw_particle(painter, particle)

    @staticmethod
    def _draw_particle(painter: QPainter, particle: DustParticle) -> None:
        """
        Draw a single dust particle with gradient effect.

        Args:
            painter: QPainter instance
            particle: DustParticle to draw
        """
        # Create radial gradient for soft, dusty appearance
        gradient = QRadialGradient(
            QPointF(particle.x, particle.y),
            particle.size
        )

        # Brownish-gray dust color
        center_color = QColor(139, 119, 101, particle.opacity)
        edge_color = QColor(139, 119, 101, 0)

        gradient.setColorAt(0, center_color)
        gradient.setColorAt(1, edge_color)

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)

        # Draw the particle
        painter.drawEllipse(
            QPointF(particle.x, particle.y),
            particle.size,
            particle.size
        )


class MainWindow(QMainWindow):
    """
    Main window containing the dust cloud widget.
    """

    def __init__(self):
        """
        Initialize the main window.
        """
        super().__init__()
        self.setWindowTitle("Dust Cloud Animation")
        self.setGeometry(100, 100, 1080, 1920 - 400)

        # Set the background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        # palette.setColor(self.backgroundRole(), QColor(0, 0, 0))
        palette.setColor(self.backgroundRole(), QColor(160, 160, 160, 0))
        self.setPalette(palette)

        # Create and set the dust cloud widget
        self.dust_widget = DustCloudWidget()
        self.setCentralWidget(self.dust_widget)


def main() -> None:
    """
    Main entry point for the application.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
