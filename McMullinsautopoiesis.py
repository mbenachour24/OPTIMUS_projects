import random

# Constants
SPACE_SIZE = 100  # Define the size of the environment
NUM_SUBSTRATES = 50
NUM_CATALYSTS = 10
NUM_LINKS = 20
STEPS = 20  # Number of simulation steps
PROXIMITY_THRESHOLD = 1  # Distance within which reactions occur

# Particle Class
class Particle:
    def __init__(self, particle_type, x, y):
        self.particle_type = particle_type
        self.x = x
        self.y = y
        self.bonded = False  # Track bonding status

    def __str__(self):
        return f"Particle(type={self.particle_type}, x={self.x}, y={self.y}, bonded={self.bonded})"

# Initialize particles
def initialize_particles():
    particles = []

    # Create Substrates
    for _ in range(NUM_SUBSTRATES):
        particles.append(Particle('substrate', random.randint(0, SPACE_SIZE), random.randint(0, SPACE_SIZE)))

    # Create Catalysts
    for _ in range(NUM_CATALYSTS):
        particles.append(Particle('catalyst', random.randint(0, SPACE_SIZE), random.randint(0, SPACE_SIZE)))

    # Create Links
    for _ in range(NUM_LINKS):
        particles.append(Particle('link', random.randint(0, SPACE_SIZE), random.randint(0, SPACE_SIZE)))

    return particles

# Move particles randomly
def move_particle(particle):
    step_x = random.choice([-1, 0, 1])
    step_y = random.choice([-1, 0, 1])
    particle.x = (particle.x + step_x) % SPACE_SIZE
    particle.y = (particle.y + step_y) % SPACE_SIZE

# Check proximity between two particles
def check_proximity(p1, p2, threshold):
    return abs(p1.x - p2.x) <= threshold and abs(p1.y - p2.y) <= threshold

# Perform reactions based on proximity
def perform_reactions(particles):
    for i, p1 in enumerate(particles):
        for j, p2 in enumerate(particles):
            if i != j and check_proximity(p1, p2, PROXIMITY_THRESHOLD):
                # Reaction: Substrate + Catalyst → Link
                if p1.particle_type == 'substrate' and p2.particle_type == 'catalyst' and not p1.bonded:
                    p1.particle_type = 'link'
                    p1.bonded = True
                    print(f"Reaction occurred: Substrate {i} bonded with Catalyst {j} -> Link")

                # Reaction: Link + Link → Break bonds
                elif p1.particle_type == 'link' and p2.particle_type == 'link':
                    p1.bonded = False
                    p2.bonded = False
                    print(f"Reaction occurred: Link {i} and Link {j} broke bonds")

# Simulate the autopoiesis system
def simulate(steps):
    particles = initialize_particles()

    for step in range(steps):
        print(f"\n--- Step {step + 1} ---")
        # Move all particles
        for particle in particles:
            move_particle(particle)

        # Perform reactions
        perform_reactions(particles)

        # Display particle states (optional)
        for idx, particle in enumerate(particles):
            print(f"Particle {idx}: {particle}")

# Run the simulation
simulate(STEPS)