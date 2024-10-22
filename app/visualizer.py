import matplotlib.pyplot as plt


class Visualizer:
    @staticmethod
    def plot_probability_bar_chart(probs, labels=["Category 1", "Category 2"]):
        fig, ax = plt.subplots()
        classes = labels
        values = probs
        ax.barh(classes, values, color=["#1f77b4", "#ff7f0e"])
        ax.set_xlim(0, 1)
        ax.set_xlabel("Predicted Proability")
        for i in range(len(classes)):
            ax.text(values[i] + 0.02, i, f"{values[i]*100:.1f}%", va="center")
        return fig
