from scipy.spatial.distance import cosine
from slack_channels import data
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd
from sklearn.preprocessing import scale
import matplotlib
import matplotlib.pyplot as plt
from adjustText import adjust_text
import seaborn as sns

def run(number_of_clusters):
    return Analysis(number_of_clusters)

class Analysis(object):
    def __init__(self,number_of_clusters):
        self.number_of_clusters = number_of_clusters
        self.run()

    def run(self):
        self.slack_data = data.read()
        self.slack_data = self.slack_data.apply(scale, axis=1)
        self.reduced_data = PCA(n_components=2).fit_transform(self.slack_data)
        self.cluster_predictions = self.predict_clusters()

    def channel_similarity(self,channel1, channel2):
        return 1 - cosine(self.slack_data[channel1], self.slack_data[channel2])

    def predict_clusters(self):
        self.__kmeans = KMeans(n_clusters=self.number_of_clusters).fit(self.reduced_data)
        cluster_predictions = self.__kmeans.predict(self.reduced_data)

        names = self.slack_data.index.get_values()
        return pd.DataFrame({'name' : names, 'cluster' : cluster_predictions})

    def plot_clusters(self):
        fig = plt.figure(figsize=(15,15))
        ax = fig.add_subplot(111)

        centroids = self.__kmeans.cluster_centers_
        colors = sns.color_palette("Paired", 10)
        cmap=matplotlib.colors.ListedColormap(colors)
        plt.scatter(self.reduced_data[:, 0], self.reduced_data[:, 1], cmap=cmap, c=self.cluster_predictions.cluster,)

        plt.xticks(())
        plt.yticks(())

        coordinates = zip(self.reduced_data[:, 0],self.reduced_data[:, 1], self.cluster_predictions.name)
        texts = []
        for (x,y, name) in coordinates:
            texts.append(plt.text(x, y, name))
        adjust_text(texts, arrowprops=dict(arrowstyle="->", color='black'))
        plt.grid()
