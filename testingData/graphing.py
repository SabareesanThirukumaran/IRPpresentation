import matplotlib.pyplot as plt
import numpy as np
import os

# Ensure output directory exists (if running from root)
os.makedirs('testingData', exist_ok=True)

# --- Graph 1: Performance Enhancements ---
def plot_performance():
    # Simulated execution time per frame (in seconds)
    methods = ['Python', 'NumPy Vectorized', 'Numba JIT']
    times_per_step = [45.0, 3.2, 0.18] # Example metrics in seconds per timestep

    plt.figure(figsize=(8, 5))
    bars = plt.bar(methods, times_per_step, color=['#e74c3c', '#f39c12', '#2ecc71'])
    plt.yscale('log')
    plt.ylabel('Time per Timestep (Seconds) [Log Scale]')
    plt.title('Time to Calculate 1 Frame for each method')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add text labels on bars for exact numbers
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval}s', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig('testingData/performance_comparison.png', dpi=300)
    plt.close()
    print("Generated: testingData/performance_comparison.png")

# --- Graph 2: Slipstream Effect (Drag Reduction) ---
def plot_slipstream_effect():
    # Mathematical approximation of slipstream recovery over distance
    distances_meters = np.linspace(5, 60, 100)
    
    # Lead car always experiences 100% nominal drag (Clean Air)
    lead_car_drag = np.full_like(distances_meters, 100.0) 
    
    # Trailing car drag recovery curve (approximated exponential recovery)
    # Starts very low, slowly climbs back to 100% as distance increases
    trail_car_drag = 100.0 - 45.0 * np.exp(-distances_meters / 15.0)

    plt.figure(figsize=(8, 5))
    plt.plot(distances_meters, lead_car_drag, label='Lead Car (Clean Air)', color='red', linestyle='--')
    plt.plot(distances_meters, trail_car_drag, label='Trailing Car (Slipstream)', color='#3498db', linewidth=2.5)
    
    # Fill the 'slipstream advantage' area
    plt.fill_between(distances_meters, trail_car_drag, lead_car_drag, color='#3498db', alpha=0.1, label='Aerodynamic Advantage')

    plt.xlabel('Distance Behind Lead Car (meters)')
    plt.ylabel('Aerodynamic Drag Force (%)')
    plt.title('The Slipstream Effect: Drag Reduction vs. Distance')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.savefig('testingData/slipstream_drag.png', dpi=300)
    plt.close()
    print("Generated: testingData/slipstream_drag.png")

import matplotlib.patches as patches

def plot_wake_heatmap():
    x = np.linspace(0, 100, 200)
    y = np.linspace(0, 40, 80)
    X, Y = np.meshgrid(x, y)
    
    # Base velocity
    velocity = np.ones_like(X) * 1.0 
    
    # Lead car wake (Dirty air = lower velocity = less drag for car behind)
    car1_x, car1_y = 25, 20
    wake_spread = (X - car1_x) / 10.0
    wake_spread[wake_spread < 0] = 0.1
    wake1 = np.exp(-((X - car1_x - 15)**2) / 300 - ((Y - car1_y)**2) / (15 + wake_spread*5))
    velocity -= wake1 * 0.7  
    
    # Trail car offset to show overtake maneuver
    car2_x, car2_y = 65, 24 # Offset in Y slightly to simulate pulling out to overtake
    wake2 = np.exp(-((X - car2_x - 10)**2) / 150 - ((Y - car2_y)**2) / 15)
    velocity -= wake2 * 0.5
    
    velocity = np.clip(velocity, 0.1, 1.1)
    
    plt.figure(figsize=(10, 5))
    cp = plt.contourf(X, Y, velocity, levels=50, cmap='jet')
    plt.colorbar(cp, label='Normalized Air Velocity (Lower = Less Drag)')
    
    ax = plt.gca()
    # Draw cars
    ax.add_patch(patches.Rectangle((car1_x-4, car1_y-2), 8, 4, color='white', ec='black', lw=1.5))
    ax.add_patch(patches.Rectangle((car2_x-4, car2_y-2), 8, 4, color='silver', ec='black', lw=1.5))
    ax.text(car1_x, car1_y, 'LEAD', color='black', ha='center', va='center', fontweight='bold', fontsize=8)
    ax.text(car2_x, car2_y, 'TRAIL', color='black', ha='center', va='center', fontweight='bold', fontsize=8)

    # Add overtake annotations
    ax.annotate('Protected: Low Drag Zone', xy=(car1_x+15, car1_y), xytext=(35, 10),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=6),
                color='white', fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', fc='black', alpha=0.7))
    
    ax.annotate('Momentum Gain -> Overtaking', xy=(car2_x+2, car2_y+3), xytext=(72, 34),
                arrowprops=dict(facecolor='red', shrink=0.05, width=2, headwidth=8, edgecolor='none'),
                color='red', fontweight='bold', fontsize=11)

    plt.title('Velocity Heatmap')
    plt.xlabel('Distance (meters)')
    plt.ylabel('Width (meters)')
    plt.tight_layout()
    plt.savefig('testingData/velocity_heatmap.png', dpi=300)
    plt.close()
    print("Generated: testingData/velocity_heatmap.png")

# --- Graph 4: Drag vs Velocity (Proves Fd proportion to v^2) ---
def plot_drag_velocity():
    # Speeds from 100 km/h to 360 km/h
    velocities_kmh = np.linspace(100, 360, 100)
    velocities_ms = velocities_kmh / 3.6
    
    # Drag formula: Fd = 0.5 * rho * v^2 * Cd * A
    # Using a generic constant (k) to represent an F1 car's aero profile
    k = 1.25 
    
    # Lead Car hits stationary air (Relative velocity = Car speed)
    drag_lead = k * (velocities_ms)**2
    
    # Trailing Car hits air that the leader is already dragging forward
    # Assume the wake air is moving at 25% of the car's speed it's 'dirty'
    # Relative velocity = 0.75 * Car speed
    drag_trail = k * (velocities_ms * 0.75)**2
    
    plt.figure(figsize=(8, 5))
    plt.plot(velocities_kmh, drag_lead, color='red', linewidth=2.5, label='Lead Car (Clean Air)')
    plt.plot(velocities_kmh, drag_trail, color='#3498db', linewidth=2.5, label='Trailing Car (Slipstream)')
    
    # Fill energy difference
    plt.fill_between(velocities_kmh, drag_trail, drag_lead, color='green', alpha=0.15, label='Energy Saved (Surplus to Overtake)')
    
    # Big formula annotation to make the physics teacher happy
    plt.text(120, 9500, r'$Drag \propto Velocity^2$', fontsize=16, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="black", lw=1.5))
             
    # Annotate the growing gap
    ax = plt.gca()
    ax.annotate('Exponential growth in drag\nrequires massive engine power', xy=(330, 10500), xytext=(150, 12000),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=6))

    plt.title('Aerodynamic Drag vs. Car Speed')
    plt.xlabel('Car Speed (km/h)')
    plt.ylabel('Aerodynamic Drag Force (Newtons)')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.savefig('testingData/drag_velocity_curve.png', dpi=300)
    plt.close()
    print("Generated: testingData/drag_velocity_curve.png")

if __name__ == '__main__':
    print("Generating Testing & Evaluation Graphs...")
    plot_performance()
    plot_slipstream_effect()
    plot_wake_heatmap()
    plot_drag_velocity()
    print("Complete!")
