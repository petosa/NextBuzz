from sklearn.cluster import KMeans

def kmeans(data, k):
    kmeans = KMeans(n_clusters=k).fit(data)
    clustered = kmeans.predict(data)
    return clustered
