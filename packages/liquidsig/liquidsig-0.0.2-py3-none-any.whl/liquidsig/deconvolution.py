""" Perform hierarchical deconvolution of cfRNA data. """

# Third party modules
import pandas as pd
import numpy as np
from scipy.optimize import nnls
from scipy.stats import pearsonr
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

matplotlib.rcParams["figure.max_open_warning"] = (
    0  # Suppress warning about too many open figures
)


# TODO: Extensively modularize this very long function into smaller functions
def hierarchical_deconvolution(
    mixture_data, training_data, top_tissue_markers=50, top_cell_markers=30
):
    """
    Performs hierarchical deconvolution of RNA-seq mixture data, calculates extended statistics, and generates enhanced figures.

    Args:
        mixture_data (pd.DataFrame): DataFrame containing mixture RNA-seq data with columns 'GeneName' and 'TPM'.
        training_data (pd.DataFrame): DataFrame containing training data with columns
                                      'Tissue', 'Cell', 'GeneName', 'GeneMarkerScore',
                                      'GeneMeanExpression', 'GenePercentExpressing'.
        top_tissue_markers (int): Number of top marker genes to use for tissue deconvolution.
        top_cell_markers (int): Number of top marker genes to use for cell deconvolution within each tissue.

    Returns:
        dict: A dictionary containing:
              'tissue_proportions': pd.DataFrame with columns 'Tissue', 'Proportion'.
              'cell_proportions': pd.DataFrame with columns 'Tissue', 'Cell', and 'Proportion'.
              'tissue_deconvolution_r2': R-squared value for tissue deconvolution.
              'tissue_deconvolution_rmse': RMSE value for tissue deconvolution.
              'tissue_deconvolution_pearson_r': Pearson correlation coefficient for tissue deconvolution.
              'cell_deconvolution_r2': dict, R-squared values for cell deconvolution per tissue.
              'cell_deconvolution_rmse': dict, RMSE values for cell deconvolution per tissue.
              'cell_deconvolution_pearson_r': dict, Pearson correlation coefficients for cell deconvolution per tissue.
              'tissue_proportion_figure': matplotlib.figure.Figure object for tissue proportions bar plot.
              'cell_proportion_figures': dict, matplotlib.figure.Figure objects for cell proportions bar plots per tissue.
              'tissue_scatter_figure': matplotlib.figure.Figure object for tissue deconvolution scatter plot.
              'cell_scatter_figures': dict, matplotlib.figure.Figure objects for cell deconvolution scatter plots per tissue.
              'tissue_marker_heatmap_figure': matplotlib.figure.Figure object for tissue marker heatmap.
              'cell_marker_heatmap_figures': dict, matplotlib.figure.Figure objects for cell marker heatmaps per tissue.
              'tissue_residual_figure': matplotlib.figure.Figure object for tissue deconvolution residual plot.
              'cell_residual_figures': dict, matplotlib.figure.Figure objects for cell deconvolution residual plots per tissue.

    Raises:
        ValueError: If required columns are missing in the input data.
    """

    required_columns_mixture = ["GeneName", "TPM"]
    if not set(required_columns_mixture).issubset(mixture_data.columns):
        raise ValueError(
            f"Mixture data must contain columns: {required_columns_mixture}"
        )

    required_columns_training = [
        "Tissue",
        "Cell",
        "GeneName",
        "GeneMarkerScore",
        "GeneMeanExpression",
        "GenePercentExpressing",
    ]
    if not set(required_columns_training).issubset(training_data.columns):
        raise ValueError(
            f"Training data must contain columns: {required_columns_training}"
        )

    # 1. Tissue Deconvolution

    print("Starting tissue-level deconvolution...")

    tissue_list = training_data["Tissue"].unique()
    print(f"\tNumber of Tissues: {len(tissue_list)}")
    tissue_marker_expression_profiles = {}
    tissue_markers = {}

    # Subset to the top marker genes for each tissue (based on top_tissue_markers)
    for tissue in tissue_list:
        tissue_specific_markers = (
            training_data[training_data["Tissue"] == tissue]
            .sort_values("GeneMarkerScore", ascending=False)
            .drop_duplicates(subset=["GeneName"])
        )

        top_markers = tissue_specific_markers.head(top_tissue_markers)
        tissue_markers[tissue] = top_markers["GeneName"].tolist()
        tissue_marker_expression_profiles[tissue] = top_markers.set_index("GeneName")[
            "GeneMeanExpression"
        ].to_dict()

    # Ensure we have overlap of the top marker genes between training and mixture data
    tissue_marker_genes = list(
        set(gene for markers in tissue_markers.values() for gene in markers)
    )
    tissue_marker_genes_intersection = list(
        set(tissue_marker_genes) & set(mixture_data["GeneName"])
    )
    if not tissue_marker_genes_intersection:
        raise ValueError(
            "No overlapping marker genes found between training and mixture data for tissue deconvolution."
        )

    # Prepare the reference tissue expression matrix
    reference_tissue_expression = []
    tissue_names_for_matrix = []
    for tissue in tissue_list:
        profile = tissue_marker_expression_profiles[tissue]
        expression_vector = [
            profile.get(gene, 0) for gene in tissue_marker_genes_intersection
        ]
        reference_tissue_expression.append(expression_vector)
        tissue_names_for_matrix.append(tissue)

    # Prepare the matrices for constrained least squares
    reference_tissue_expression_matrix = np.array(reference_tissue_expression).T
    # Extract the mixture expression vector for the marker genes, filling with 0 if gene not present
    mixture_tissue_expression_vector = np.array(
        [
            (
                mixture_data[mixture_data["GeneName"] == gene]["TPM"].iloc[0]
                if gene in mixture_data["GeneName"].values
                else 0
            )
            for gene in tissue_marker_genes_intersection
        ]
    )

    # Constrained Least Squares for Tissue Deconvolution
    # NNLS seems to outperform L-BFGS-B and SLSQP for our use case
    tissue_proportions, residuals = nnls(
        reference_tissue_expression_matrix, mixture_tissue_expression_vector
    )
    tissue_proportions_normalized = (
        tissue_proportions / tissue_proportions.sum()
        if tissue_proportions.sum() > 0
        else tissue_proportions
    )

    # Use the NNLS residuals to calculate the proportion of unexplained variance -- this is not the same as R-squared, but a useful metric for NNLS
    # Note we are not comparing the same values -- specifically we have TPM data from our mixture, but mean expression data from our training data
    # TODO: Consider normalizing the data before calculating residuals or fitting the model?
    total_variance = np.sum(
        (mixture_tissue_expression_vector - np.mean(mixture_tissue_expression_vector))
        ** 2
    )
    unexplained_variance = np.sum(residuals**2)
    proportion_unexplained_variance = unexplained_variance / total_variance
    print(
        f"\tProportion of Unexplained Variance: {proportion_unexplained_variance:.3f}"
    )

    tissue_proportion_df = pd.DataFrame(
        {"Tissue": tissue_names_for_matrix, "Proportion": tissue_proportions_normalized}
    )

    # Calculate Statistics for tissue deconvolution
    reconstructed_tissue_expression = (
        reference_tissue_expression_matrix @ tissue_proportions
    )
    tissue_r2 = r2_score(
        mixture_tissue_expression_vector, reconstructed_tissue_expression
    )
    tissue_rmse = np.sqrt(
        mean_squared_error(
            mixture_tissue_expression_vector, reconstructed_tissue_expression
        )
    )
    tissue_pearson_r, _ = pearsonr(
        mixture_tissue_expression_vector, reconstructed_tissue_expression
    )

    print("Completed tissue deconvolution.\n\nStarting cell-level deconvolution...")

    # 2. Cell Deconvolution within each Tissue

    cell_proportions_dict = {}
    cell_r2_dict = {}
    cell_rmse_dict = {}
    cell_pearson_r_dict = {}
    cell_proportion_figures_dict = {}
    cell_scatter_figures_dict = {}
    cell_marker_heatmap_figures_dict = {}
    cell_residual_figures_dict = {}

    for tissue in tissue_list:
        print(f"Cell-level deconvoluting: {tissue}")

        cells_in_tissue = training_data[training_data["Tissue"] == tissue][
            "Cell"
        ].unique()
        cell_marker_expression_profiles = {}
        cell_markers = {}

        for cell in cells_in_tissue:
            cell_specific_markers = (
                training_data[
                    (training_data["Tissue"] == tissue)
                    & (training_data["Cell"] == cell)
                ]
                .sort_values("GeneMarkerScore", ascending=False)
                .drop_duplicates(subset=["GeneName"])
            )

            top_markers = cell_specific_markers.head(top_cell_markers)
            cell_markers[cell] = top_markers["GeneName"].tolist()
            cell_marker_expression_profiles[cell] = top_markers.set_index("GeneName")[
                "GeneMeanExpression"
            ].to_dict()

        cell_marker_genes = list(
            set(gene for markers in cell_markers.values() for gene in markers)
        )
        cell_marker_genes_intersection = list(
            set(cell_marker_genes) & set(mixture_data["GeneName"])
        )

        if not cell_marker_genes_intersection:
            print(
                f"Warning: No overlapping marker genes found for cell deconvolution in Tissue: {tissue}. Skipping this tissue."
            )
            cell_proportions_dict[tissue] = pd.DataFrame(
                {"Cell": cells_in_tissue, "Proportion": np.nan}
            )
            cell_r2_dict[tissue] = np.nan
            cell_rmse_dict[tissue] = np.nan
            cell_pearson_r_dict[tissue] = np.nan
            cell_proportion_figures_dict[tissue] = None
            cell_scatter_figures_dict[tissue] = None
            cell_marker_heatmap_figures_dict[tissue] = None
            cell_residual_figures_dict[tissue] = None
            continue

        reference_cell_expression = []
        cell_names_for_matrix = []
        for cell in cells_in_tissue:
            profile = cell_marker_expression_profiles[cell]
            expression_vector = [
                profile.get(gene, 0) for gene in cell_marker_genes_intersection
            ]
            reference_cell_expression.append(expression_vector)
            cell_names_for_matrix.append(cell)

        reference_cell_expression_matrix = np.array(reference_cell_expression).T
        mixture_cell_expression_vector = np.array(
            [
                (
                    mixture_data[mixture_data["GeneName"] == gene]["TPM"].iloc[0]
                    if gene in mixture_data["GeneName"].values
                    else 0
                )
                for gene in cell_marker_genes_intersection
            ]
        )

        # Constrained Least Squares for Cell Deconvolution
        cell_proportions, _ = nnls(
            reference_cell_expression_matrix, mixture_cell_expression_vector
        )
        cell_proportions_normalized = (
            cell_proportions / cell_proportions.sum()
            if cell_proportions.sum() > 0
            else cell_proportions
        )

        cell_proportions_dict[tissue] = pd.DataFrame(
            {
                "Tissue": [tissue] * len(cell_names_for_matrix),
                "Cell": cell_names_for_matrix,
                "Proportion": cell_proportions_normalized,
            }
        )

        # Calculate Statistics for cell deconvolution
        reconstructed_cell_expression = (
            reference_cell_expression_matrix @ cell_proportions
        )
        cell_r2 = r2_score(
            mixture_cell_expression_vector, reconstructed_cell_expression
        )
        cell_rmse = np.sqrt(
            mean_squared_error(
                mixture_cell_expression_vector, reconstructed_cell_expression
            )
        )
        cell_pearson_r, _ = pearsonr(
            mixture_cell_expression_vector, reconstructed_cell_expression
        )

        cell_r2_dict[tissue] = cell_r2
        cell_rmse_dict[tissue] = cell_rmse
        cell_pearson_r_dict[tissue] = cell_pearson_r

        print(
            f"\tR-squared: {cell_r2:.3f}, RMSE: {cell_rmse:.3f}, Pearson r: {cell_pearson_r:.3f}\n"
        )

    cell_proportion_df = pd.concat(cell_proportions_dict.values(), ignore_index=True)

    print("All deconvolutions complete. Generating figures...")

    # 3. Figure Generation

    # Tissue Proportion Bar Plot (same as before)
    tissue_fig_prop, ax_tissue_prop = plt.subplots(figsize=(10, 12))
    sns.barplot(
        x="Proportion",
        y="Tissue",
        data=tissue_proportion_df.sort_values("Proportion", ascending=False),
        hue="Tissue",
        dodge=False,
        legend=False,
        palette="viridis",
        ax=ax_tissue_prop,
    )
    ax_tissue_prop.set_title("Estimated Tissue Proportions")
    ax_tissue_prop.set_xlabel("Proportion")
    ax_tissue_prop.set_ylabel("Tissue")
    tissue_fig_prop.tight_layout()
    tissue_proportion_figure = tissue_fig_prop

    cell_proportion_figures_dict = {}
    cell_scatter_figures_dict = {}
    cell_marker_heatmap_figures_dict = {}
    cell_residual_figures_dict = {}

    # Tissue Scatter Plot (Reconstructed vs. Original)
    tissue_fig_scatter, ax_tissue_scatter = plt.subplots(figsize=(8, 8))
    sns.scatterplot(
        x=mixture_tissue_expression_vector,
        y=reconstructed_tissue_expression,
        ax=ax_tissue_scatter,
    )
    ax_tissue_scatter.set_xlabel("Original Mixture Expression (Marker Genes)")
    ax_tissue_scatter.set_ylabel("Reconstructed Tissue Expression (Marker Genes)")
    ax_tissue_scatter.set_title("Tissue Deconvolution: Reconstructed vs. Original")
    ax_tissue_scatter.plot(
        [min(mixture_tissue_expression_vector), max(mixture_tissue_expression_vector)],
        [min(mixture_tissue_expression_vector), max(mixture_tissue_expression_vector)],
        color="red",
        linestyle="--",
    )  # Diagonal line
    tissue_fig_scatter.tight_layout()
    tissue_scatter_figure = tissue_fig_scatter

    # Tissue Marker Heatmap
    tissue_marker_heatmap_fig, ax_tissue_heatmap = plt.subplots(figsize=(10, 10))
    tissue_marker_expression_df = pd.DataFrame(
        reference_tissue_expression_matrix,
        index=tissue_marker_genes_intersection,
        columns=tissue_names_for_matrix,
    )
    sns.heatmap(
        tissue_marker_expression_df,
        cmap="viridis",
        ax=ax_tissue_heatmap,
        cbar_kws={"label": "Mean Expression"},
    )
    ax_tissue_heatmap.set_title("Tissue Marker Gene Expression Heatmap")
    ax_tissue_heatmap.set_xlabel("Tissues")
    ax_tissue_heatmap.set_ylabel("Marker Genes")
    tissue_marker_heatmap_fig.tight_layout()
    tissue_marker_heatmap_figure = tissue_marker_heatmap_fig

    # Tissue Residual Plot
    tissue_fig_residual, ax_tissue_residual = plt.subplots(figsize=(8, 8))
    residuals_tissue = (
        reconstructed_tissue_expression - mixture_tissue_expression_vector
    )
    sns.scatterplot(
        x=mixture_tissue_expression_vector, y=residuals_tissue, ax=ax_tissue_residual
    )
    ax_tissue_residual.axhline(0, color="red", linestyle="--")  # Zero line
    ax_tissue_residual.set_xlabel("Original Mixture Expression (Marker Genes)")
    ax_tissue_residual.set_ylabel("Residuals (Reconstructed - Original)")
    ax_tissue_residual.set_title("Tissue Deconvolution: Residual Plot")
    tissue_fig_residual.tight_layout()
    tissue_residual_figure = tissue_fig_residual

    generate_detailed_figures = False

    # We generate per-tissue figures for cell deconvolution
    for tissue in tissue_list:
        cell_props_tissue = cell_proportions_dict.get(tissue)
        if (
            cell_props_tissue is not None
            and not cell_props_tissue["Proportion"].isnull().all()
            and generate_detailed_figures
        ):
            cell_props_tissue_valid = cell_props_tissue.dropna(
                subset=["Proportion"]
            ).sort_values("Proportion", ascending=False)

            # Cell Proportion Bar Plot
            cell_fig_prop, ax_cell_prop = plt.subplots(figsize=(8, 8))
            sns.barplot(
                x="Proportion",
                y="Cell",
                data=cell_props_tissue_valid,
                hue="Cell",
                dodge=False,
                legend=False,
                palette="viridis",
                ax=ax_cell_prop,
            )
            ax_cell_prop.set_title(f"Cell Proportions within {tissue} Tissue")
            ax_cell_prop.set_xlabel("Proportion")
            ax_cell_prop.set_ylabel("Cell Type")
            cell_fig_prop.tight_layout()
            cell_proportion_figures_dict[tissue] = cell_fig_prop

            # Cell Scatter Plot (Reconstructed vs. Original)
            cell_fig_scatter, ax_cell_scatter = plt.subplots(figsize=(8, 8))
            mixture_cell_expression_vector = np.array(
                [
                    (
                        mixture_data[mixture_data["GeneName"] == gene]["TPM"].iloc[0]
                        if gene in mixture_data["GeneName"].values
                        else 0
                    )
                    for gene in cell_marker_genes_intersection
                ]
            )  # Re-calculate inside the loop to ensure correct genes
            reference_cell_expression_matrix = np.array(
                reference_cell_expression
            ).T  # Re-calculate inside the loop
            reconstructed_cell_expression = (
                reference_cell_expression_matrix @ cell_proportions
            )  # Re-calculate inside the loop
            sns.scatterplot(
                x=mixture_cell_expression_vector,
                y=reconstructed_cell_expression,
                ax=ax_cell_scatter,
            )
            ax_cell_scatter.set_xlabel("Original Mixture Expression (Marker Genes)")
            ax_cell_scatter.set_ylabel("Reconstructed Cell Expression (Marker Genes)")
            ax_cell_scatter.set_title(
                f"Cell Deconvolution in {tissue}: Reconstructed vs. Original"
            )
            ax_cell_scatter.plot(
                [
                    min(mixture_cell_expression_vector),
                    max(mixture_cell_expression_vector),
                ],
                [
                    min(mixture_cell_expression_vector),
                    max(mixture_cell_expression_vector),
                ],
                color="red",
                linestyle="--",
            )  # Diagonal line
            cell_fig_scatter.tight_layout()
            cell_scatter_figures_dict[tissue] = cell_fig_scatter

            # Cell Marker Heatmap
            cell_marker_heatmap_fig, ax_cell_heatmap = plt.subplots(figsize=(8, 8))
            reference_cell_expression_matrix = np.array(
                reference_cell_expression
            ).T  # Re-calculate inside the loop
            cell_marker_expression_df = pd.DataFrame(
                reference_cell_expression_matrix,
                index=cell_marker_genes_intersection,
                columns=cell_names_for_matrix,
            )
            sns.heatmap(
                cell_marker_expression_df,
                cmap="viridis",
                ax=ax_cell_heatmap,
                cbar_kws={"label": "Mean Expression"},
            )
            ax_cell_heatmap.set_title(
                f"Cell Marker Gene Expression Heatmap in {tissue}"
            )
            ax_cell_heatmap.set_xlabel("Cell Types")
            ax_cell_heatmap.set_ylabel("Marker Genes")
            cell_marker_heatmap_fig.tight_layout()
            cell_marker_heatmap_figures_dict[tissue] = cell_marker_heatmap_fig

            # Cell Residual Plot
            cell_fig_residual, ax_cell_residual = plt.subplots(figsize=(8, 8))
            residuals_cell = (
                reconstructed_cell_expression - mixture_cell_expression_vector
            )
            sns.scatterplot(
                x=mixture_cell_expression_vector, y=residuals_cell, ax=ax_cell_residual
            )
            ax_cell_residual.axhline(0, color="red", linestyle="--")  # Zero line
            ax_cell_residual.set_xlabel("Original Mixture Expression (Marker Genes)")
            ax_cell_residual.set_ylabel("Residuals (Reconstructed - Original)")
            ax_cell_residual.set_title(f"Cell Deconvolution in {tissue}: Residual Plot")
            cell_fig_residual.tight_layout()
            cell_residual_figures_dict[tissue] = cell_fig_residual

        else:
            cell_proportion_figures_dict[tissue] = None
            cell_scatter_figures_dict[tissue] = None
            cell_marker_heatmap_figures_dict[tissue] = None
            cell_residual_figures_dict[tissue] = None

    print("Figure generation complete.")

    return {
        "tissue_proportions": tissue_proportion_df,
        "cell_proportions": cell_proportion_df,
        "tissue_deconvolution_r2": tissue_r2,
        "tissue_deconvolution_rmse": tissue_rmse,
        "tissue_deconvolution_pearson_r": tissue_pearson_r,
        "cell_deconvolution_r2": cell_r2_dict,
        "cell_deconvolution_rmse": cell_rmse_dict,
        "cell_deconvolution_pearson_r": cell_pearson_r_dict,
        "tissue_proportion_figure": tissue_proportion_figure,
        "cell_proportion_figures": cell_proportion_figures_dict,
        "tissue_scatter_figure": tissue_scatter_figure,
        "cell_scatter_figures": cell_scatter_figures_dict,
        "tissue_marker_heatmap_figure": tissue_marker_heatmap_figure,
        "cell_marker_heatmap_figures": cell_marker_heatmap_figures_dict,
        "tissue_residual_figure": tissue_residual_figure,
        "cell_residual_figures": cell_residual_figures_dict,
    }
