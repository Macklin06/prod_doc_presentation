import marimo

__generated_with = "0.9.14"
app = marimo.App(width="medium")


@app.cell
def __():
    # Interactive Data Analysis Notebook
    # Author: 24f2001048@ds.study.iitm.ac.in
    # Purpose: Demonstrate variable relationships and interactive visualization
    
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    
    mo.md("""
    # Interactive Data Analysis Dashboard
    
    **Contact:** 24f2001048@ds.study.iitm.ac.in
    
    This notebook demonstrates:
    - Variable dependencies between cells
    - Interactive widgets for parameter control
    - Dynamic visualizations based on user input
    - Self-documenting data flow
    """)
    return mo, np, pd, plt


@app.cell
def __(mo):
    # Cell 2: Interactive Controls
    # This cell defines the slider widget that controls sample size
    # Dependencies: mo (marimo module)
    # Outputs: sample_size_slider (widget), sample_size (integer value)
    
    sample_size_slider = mo.ui.slider(
        start=50,
        stop=500,
        step=10,
        value=100,
        label="Sample Size:",
        show_value=True
    )
    
    mo.md(f"""
    ## Data Configuration
    
    Use the slider below to adjust the number of data points for analysis:
    
    {sample_size_slider}
    """)
    return sample_size_slider,


@app.cell
def __(sample_size_slider):
    # Cell 3: Extract sample size value
    # This cell depends on sample_size_slider from Cell 2
    # Data flow: sample_size_slider → sample_size
    
    sample_size = sample_size_slider.value
    return sample_size,


@app.cell
def __(np, sample_size):
    # Cell 4: Generate synthetic dataset
    # This cell depends on sample_size from Cell 3
    # Data flow: sample_size → dataset generation
    # Outputs: x_data, y_data, correlation_coefficient
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate correlated data
    x_data = np.linspace(0, 10, sample_size)
    noise = np.random.normal(0, 1.5, sample_size)
    y_data = 2.5 * x_data + 3 + noise
    
    # Calculate correlation coefficient
    correlation_coefficient = np.corrcoef(x_data, y_data)[0, 1]
    
    return x_data, y_data, correlation_coefficient, noise


@app.cell
def __(mo, sample_size, correlation_coefficient):
    # Cell 5: Dynamic markdown based on widget state
    # This cell depends on sample_size and correlation_coefficient from previous cells
    # Data flow: sample_size, correlation_coefficient → dynamic documentation
    
    # Determine correlation strength
    if abs(correlation_coefficient) > 0.9:
        strength = "**very strong**"
        color = "green"
    elif abs(correlation_coefficient) > 0.7:
        strength = "**strong**"
        color = "blue"
    elif abs(correlation_coefficient) > 0.5:
        strength = "**moderate**"
        color = "orange"
    else:
        strength = "**weak**"
        color = "red"
    
    mo.md(f"""
    ## Analysis Results
    
    ### Current Configuration
    - **Sample Size:** {sample_size} data points
    - **Correlation Coefficient:** {correlation_coefficient:.4f}
    - **Correlation Strength:** <span style="color:{color}">{strength}</span>
    
    ### Interpretation
    
    With {sample_size} samples, we observe a {strength} positive correlation 
    between the variables. The relationship follows the linear model:
    
    $$y = 2.5x + 3 + \\varepsilon$$
    
    where $\\varepsilon \\sim N(0, 1.5^2)$ represents random noise.
    
    **Note:** Adjust the slider above to see how sample size affects the analysis.
    """)
    return color, strength


@app.cell
def __(plt, x_data, y_data, sample_size, correlation_coefficient):
    # Cell 6: Create visualization
    # This cell depends on x_data, y_data, sample_size, and correlation_coefficient
    # Data flow: all previous variables → visualization output
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Scatter plot with regression line
    ax1.scatter(x_data, y_data, alpha=0.6, s=30, color='steelblue', 
                edgecolors='navy', linewidth=0.5)
    
    # Calculate and plot regression line
    z = np.polyfit(x_data, y_data, 1)
    p = np.poly1d(z)
    ax1.plot(x_data, p(x_data), "r--", linewidth=2, 
             label=f'y = {z[0]:.2f}x + {z[1]:.2f}')
    
    ax1.set_xlabel('X Variable', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Y Variable', fontsize=12, fontweight='bold')
    ax1.set_title(f'Scatter Plot (n={sample_size}, r={correlation_coefficient:.3f})', 
                  fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Histogram of residuals
    residuals = y_data - p(x_data)
    ax2.hist(residuals, bins=30, color='coral', alpha=0.7, edgecolor='black')
    ax2.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Zero')
    ax2.set_xlabel('Residuals', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax2.set_title('Residual Distribution', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    fig
    return ax1, ax2, fig, p, residuals, z


@app.cell
def __(mo, pd, x_data, y_data, residuals, p, sample_size):
    # Cell 7: Statistical summary table
    # This cell depends on data from previous cells to create summary statistics
    # Data flow: x_data, y_data, residuals → statistical summary
    
    # Calculate summary statistics
    stats_dict = {
        'Metric': ['Mean', 'Std Dev', 'Min', 'Max', 'Median'],
        'X Variable': [
            f'{x_data.mean():.3f}',
            f'{x_data.std():.3f}',
            f'{x_data.min():.3f}',
            f'{x_data.max():.3f}',
            f'{np.median(x_data):.3f}'
        ],
        'Y Variable': [
            f'{y_data.mean():.3f}',
            f'{y_data.std():.3f}',
            f'{y_data.min():.3f}',
            f'{y_data.max():.3f}',
            f'{np.median(y_data):.3f}'
        ],
        'Residuals': [
            f'{residuals.mean():.3f}',
            f'{residuals.std():.3f}',
            f'{residuals.min():.3f}',
            f'{residuals.max():.3f}',
            f'{np.median(residuals):.3f}'
        ]
    }
    
    stats_df = pd.DataFrame(stats_dict)
    
    mo.md(f"""
    ## Statistical Summary
    
    Below are descriptive statistics for the current dataset (n={sample_size}):
    
    {mo.ui.table(stats_df)}
    
    ### Model Performance
    - **R² Score:** {1 - (residuals**2).sum() / ((y_data - y_data.mean())**2).sum():.4f}
    - **Mean Absolute Error:** {np.abs(residuals).mean():.4f}
    - **Root Mean Square Error:** {np.sqrt((residuals**2).mean()):.4f}
    """)
    return stats_dict, stats_df


@app.cell
def __(mo, sample_size):
    # Cell 8: Interactive recommendations based on sample size
    # This cell depends on sample_size to provide contextual recommendations
    # Data flow: sample_size → dynamic recommendations
    
    if sample_size < 100:
        recommendation = """
        ⚠️ **Small Sample Warning:** With fewer than 100 samples, statistical 
        estimates may have higher variance. Consider increasing the sample size 
        for more reliable results.
        """
        emoji = "⚠️"
    elif sample_size < 200:
        recommendation = """
        ✓ **Adequate Sample Size:** The current sample size provides reasonable 
        statistical power for basic analysis.
        """
        emoji = "✓"
    else:
        recommendation = """
        ✓✓ **Large Sample Size:** Excellent! This sample size provides high 
        statistical power and more stable estimates.
        """
        emoji = "✓✓"
    
    mo.md(f"""
    ## Recommendations {emoji}
    
    {recommendation}
    
    ### Data Flow Summary
    
    This notebook demonstrates reactive programming with the following dependency chain:
    
    ```
    slider widget → sample_size → data generation → statistics & visualization
                                                  ↓
                                          dynamic markdown
    ```
    
    **Author Contact:** 24f2001048@ds.study.iitm.ac.in
    """)
    return emoji, recommendation


@app.cell
def __():
    # Cell 9: Footer and documentation
    # Independent cell providing additional information
    
    import marimo as mo
    
    mo.md("""
    ---
    
    ## About This Notebook
    
    This Marimo notebook demonstrates:
    
    1. **Reactive Programming**: Variables automatically update when dependencies change
    2. **Interactive Widgets**: Slider controls affect all downstream computations
    3. **Dynamic Markdown**: Content changes based on computational results
    4. **Self-Documentation**: Comments explain data flow between cells
    
    ### Cell Dependencies
    
    - **Cell 1**: Import modules (no dependencies)
    - **Cell 2**: Create slider widget (depends on Cell 1)
    - **Cell 3**: Extract slider value (depends on Cell 2)
    - **Cell 4**: Generate data (depends on Cell 3)
    - **Cell 5**: Dynamic analysis text (depends on Cells 3, 4)
    - **Cell 6**: Visualization (depends on Cells 3, 4)
    - **Cell 7**: Statistical summary (depends on Cell 4, 6)
    - **Cell 8**: Recommendations (depends on Cell 3)
    - **Cell 9**: Footer (independent)
    
    **Contact:** 24f2001048@ds.study.iitm.ac.in
    """)
    return mo,


if __name__ == "__main__":
    app.run()
