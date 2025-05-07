"""
Script to design a novel enzyme using the protein design framework.
This example designs an enzyme with a catalytic triad (HDS) and specific properties.
"""
import os
import sys
import matplotlib.pyplot as plt
from pathlib import Path

# Add the parent directory to Python path to import our package
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.core.design_target import (
    DesignTarget,
    SecondaryStructureTarget,
    PropertyTarget
)
from src.core.sequence_generator import SequenceGenerator
from src.core.structure_predictor import StructurePredictor
from src.core.fitness_evaluator import FitnessEvaluator, FitnessWeights
from src.core.optimizer import Optimizer, OptimizationParameters

def plot_optimization_progress(fitness_history, title, output_dir):
    """Plot and save optimization progress."""
    plt.figure(figsize=(10, 6))
    plt.plot(fitness_history, 'b-', label='Fitness')
    plt.xlabel('Iteration')
    plt.ylabel('Fitness Score')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    
    # Save plot
    output_path = Path(output_dir) / f"{title.lower().replace(' ', '_')}.png"
    plt.savefig(output_path)
    plt.close()
    print(f"Progress plot saved to: {output_path}")

def main():
    # Create output directories
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    # Define design target for a novel enzyme
    design_target = DesignTarget(
        desired_function="Novel enzyme with catalytic triad",
        length_range=(200, 300),
        secondary_structure=SecondaryStructureTarget(
            min_helix=0.3,
            max_helix=0.5,
            min_sheet=0.2,
            max_sheet=0.4
        ),
        properties=PropertyTarget(
            min_hydropathy=-0.5,
            max_hydropathy=0.5,
            min_charge=-5,
            max_charge=5
        ),
        # Define catalytic triad positions
        catalytic_residues={
            50: {'H'},  # Histidine
            100: {'D'},  # Aspartate
            150: {'S'}   # Serine
        },
        # Add some key structural residues
        key_residues={
            25: 'P',  # Proline for turn
            75: 'G',  # Glycine for flexibility
            125: 'W'  # Tryptophan for stability
        }
    )
    
    # Initialize components
    print("\nInitializing components...")
    sequence_generator = SequenceGenerator(design_target)
    structure_predictor = StructurePredictor()
    fitness_evaluator = FitnessEvaluator(
        design_target,
        weights=FitnessWeights(
            stability=0.3,
            function=0.5,
            structure=0.2
        )
    )
    
    # Set up optimization parameters
    parameters = OptimizationParameters(
        max_iterations=100,  # Reduced for testing
        population_size=20,
        mutation_rate=0.1,
        temperature=1.0,
        cooling_rate=0.99,
        crossover_rate=0.8,
        elite_size=2,
        patience=20
    )
    
    optimizer = Optimizer(
        design_target,
        sequence_generator,
        structure_predictor,
        fitness_evaluator,
        parameters
    )
    
    # Track optimization progress
    fitness_history = []
    
    def mc_callback(structure, fitness):
        fitness_history.append(fitness)
        if len(fitness_history) % 10 == 0:
            print(f"Iteration {len(fitness_history)}, Fitness: {fitness:.4f}")
    
    # Run Monte Carlo optimization
    print("\nRunning Monte Carlo optimization...")
    best_structure, best_fitness = optimizer.monte_carlo_optimize(callback=mc_callback)
    
    # Print results
    print("\nOptimization Results:")
    print(f"Best sequence found: {best_structure.sequence}")
    print(f"Best fitness score: {best_fitness:.4f}")
    print("\nSequence properties:")
    for prop, value in best_structure.properties['sequence_properties'].items():
        print(f"{prop}: {value:.4f}")
    print("\nSecondary structure content:")
    for ss, content in best_structure.properties['secondary_structure_content'].items():
        print(f"{ss}: {content:.4f}")
    
    # Plot optimization progress
    plot_optimization_progress(
        fitness_history,
        "Monte Carlo Optimization Progress",
        results_dir
    )
    
    # Save best structure
    structure_predictor.save_prediction_results(
        best_structure,
        str(results_dir)
    )
    
    print(f"\nResults saved to: {results_dir}")

if __name__ == "__main__":
    main() 