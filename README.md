# ProteinForge Tutorial: Designing a Novel Enzyme

This tutorial walks you through designing a novel enzyme using ProteinForge. We'll create an enzyme with a catalytic triad (Histidine-Aspartate-Serine), commonly found in hydrolases.

## 🎯 Design Goals

Our enzyme design targets:
1. **Catalytic Triad**
   - Histidine at position 50
   - Aspartate at position 100
   - Serine at position 150

2. **Structural Properties**
   - Length: 200-300 amino acids
   - Secondary structure: 30-50% helix, 20-40% sheet
   - Hydropathy index: -0.5 to 0.5
   - Net charge: -5 to +5

3. **Key Structural Elements**
   - Proline at position 25 (for turn formation)
   - Glycine at position 75 (for flexibility)
   - Tryptophan at position 125 (for stability)

## 🚀 Running the Example

1. **Setup**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Unix/macOS
   # or
   .\venv\Scripts\activate  # On Windows

   # Install requirements
   pip install -r requirements.txt
   ```

2. **Run the Design Script**
   ```bash
   python scripts/design_enzyme.py
   ```

## 📊 Understanding the Output

The script generates:

1. **Optimization Progress**
   - Real-time fitness updates
   - Progress plot saved as `monte_carlo_optimization_progress.png`

2. **Best Design**
   - Sequence with optimized properties
   - Structure prediction (PDB format)
   - Detailed analysis in JSON format

3. **Results Analysis**
   ```python
   # Example output
   Best sequence found: MKTAYIAK...
   Best fitness score: 0.3891

   Sequence properties:
   - Molecular weight: 32571.90
   - Hydropathy index: -0.37
   - Net charge: +1
   - Hydrophobic ratio: 0.39
   - Polar ratio: 0.28
   - Charged ratio: 0.23

   Secondary structure:
   - Helix: 35%
   - Sheet: 25%
   - Coil: 40%
   ```

## 🔍 Code Walkthrough

1. **Design Target Setup** ([design_enzyme.py](scripts/design_enzyme.py))
   ```python
   design_target = DesignTarget(
       desired_function="Novel enzyme with catalytic triad",
       length_range=(200, 300),
       secondary_structure=SecondaryStructureTarget(
           min_helix=0.3, max_helix=0.5,
           min_sheet=0.2, max_sheet=0.4
       ),
       properties=PropertyTarget(
           min_hydropathy=-0.5, max_hydropathy=0.5,
           min_charge=-5, max_charge=5
       ),
       catalytic_residues={
           50: {'H'}, 100: {'D'}, 150: {'S'}
       }
   )
   ```

2. **Component Initialization**
   ```python
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
   ```

3. **Optimization Setup**
   ```python
   parameters = OptimizationParameters(
       max_iterations=100,
       population_size=20,
       mutation_rate=0.1,
       temperature=1.0,
       cooling_rate=0.99
   )
   ```

## 📈 Results Interpretation

The optimization process:
1. Generates random sequences meeting basic constraints
2. Predicts structures and evaluates fitness
3. Uses Monte Carlo optimization to improve designs
4. Tracks progress and saves the best results

Key metrics to watch:
- Fitness score improvement over iterations
- Property values within target ranges
- Secondary structure content
- Presence of catalytic residues

## 🛠️ Customization

You can modify:
1. Design target parameters in `design_enzyme.py`
2. Optimization parameters for different search strategies
3. Fitness weights to prioritize different aspects
4. Number of iterations and population size

## 📝 Notes

- This example uses a mock structure predictor
- For real applications, integrate with tools like AlphaFold
- Adjust parameters based on your specific design goals
- Consider using the genetic algorithm for larger searches

## 🤔 Next Steps

1. Try different design targets
2. Experiment with optimization parameters
3. Analyze results with external tools
4. Validate designs experimentally 