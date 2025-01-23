import os
import numpy as np
import plotly.figure_factory as ff
from sklearn.metrics import confusion_matrix

def export_confusion_matrix_to_html(predictions, trues, classes, output_path):
    """
    Creates a confusion matrix and exports it to an HTML file.

    Args:
        predictions (list or np.ndarray): The predicted class labels.
        trues (list or np.ndarray): The true class labels.
        classes (list of str): List of class names corresponding to labels.
        template_path (str): Path to the template HTML file.
        output_path (str): Path to the output HTML file.
    """
    # Path to the template HTML file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, "template.html")
    print(template_path)

    # Generate the confusion matrix
    cm = confusion_matrix(trues, predictions)
    
    # Normalize the confusion matrix to show percentages
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    
    # Create the Plotly heatmap
    fig = ff.create_annotated_heatmap(
        z=cm_normalized,
        x=classes,
        y=classes,
        annotation_text=cm.astype(str),
        colorscale='Greens',
        showscale=True,
    )
    fig.update_layout(
        title="Confusion Matrix",
        xaxis_title="Predicted Label",
        yaxis_title="True Label",
    )

    # Generate the Plotly JSON for embedding
    plot_div = fig.to_html(full_html=False, include_plotlyjs=False)

    # Read the template HTML file
    with open(template_path, "r") as template_file:
        template_html = template_file.read()

    # Insert the Plotly plot into the template
    html_content = template_html.replace("{{ plot_div }}", plot_div)

    # Write the final HTML to the output file
    with open(output_path, "w") as output_file:
        output_file.write(html_content)

    print(f"Confusion matrix exported to {output_path}")


# Example usage
if __name__ == "__main__":
    # Example data
    predictions = [0, 1, 0, 2, 1, 2, 0]
    trues = [0, 1, 0, 2, 0, 2, 2]
    classes = ["Class 0", "Class 1", "Class 2"]

    output_path = "confusion_matrix.html"

    export_confusion_matrix_to_html(predictions, trues, classes, output_path)
