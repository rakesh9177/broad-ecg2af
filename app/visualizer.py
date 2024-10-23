import matplotlib.pyplot as plt


class Visualizer:
    """
    A class used to visualize model predictions by generating bar charts.

    Methods:
        plot_probability_bar_chart(probs, labels=["Category 1", "Category 2"]):
            Creates a horizontal bar chart to display prediction probabilities for given categories.
    """

    @staticmethod
    def plot_probability_bar_chart(probs, labels=["Category 1", "Category 2"]):
        """
        Plot a horizontal bar chart to visualize the predicted probabilities.

        Args:
            probs (list): A list of probabilities corresponding to the categories.
            labels (list): A list of category labels to display on the chart. Defaults to ["Category 1", "Category 2"].

        Returns:
            matplotlib.figure.Figure: The generated figure containing the bar chart.
        """
        fig, ax = plt.subplots()
        classes = labels
        values = probs

        # Plot the horizontal bar chart with specified colors for each class
        ax.barh(classes, values, color=["#1f77b4", "#ff7f0e"])

        # Set the x-axis limits and label
        ax.set_xlim(0, 1)
        ax.set_xlabel("Predicted Probability")

        # Add text annotations to display percentage values for each bar
        for i in range(len(classes)):
            ax.text(values[i] + 0.02, i, f"{values[i]*100:.1f}%", va="center")

        return fig
