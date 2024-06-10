import numpy as np
import pandas as pd
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import sklearn.model_selection
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix




# Load Data


ratings = pd.read_csv('https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/ratings.csv')


books = pd.read_csv('https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/books.csv')
books.drop(['small_image_url', 'image_url'], axis=1, inplace=True)


book_tags = pd.read_csv('https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/tags.csv')

to_read = pd.read_csv('https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/to_read.csv')
to_read = to_read.groupby('book_id').size().reset_index(name='to_read_count')


# merging book_tags (for future maybe???)
# merged_df = pd.merge(books, book_tags, on='goodreads_book_id', how='left')
# grouped_df = merged_df.groupby('goodreads_book_id')['tag_id'].agg(list).reset_index()
# books = pd.merge(books, grouped_df, on='goodreads_book_id', how='left')
books = pd.merge(books, to_read, on='book_id', how='left')


"""# Exploratory Data Analysis"""

n_ratings = len(ratings)
n_books = ratings['book_id'].nunique()
n_users = ratings['user_id'].nunique()
print(f"Number of ratings: {n_ratings}")
print(f"Number of unique bookId's: {n_books}")
print(f"Number of unique users: {n_users}")
print(f"Average number of ratings per user: {round(n_ratings/n_users, 2)}")
print(f"Average number of ratings per book: {round(n_ratings/n_books, 2)}")

"""## Ratings"""

ratings.rating.hist( bins = 5 )

"""## Books"""

authors_counts = books['authors'].value_counts()
print("Top 10 Authors:")
print(authors_counts.head(10))

books['original_publication_year'].hist(bins=30)
plt.title('Distribution of Publication Years')
plt.xlabel('Publication Year')
plt.ylabel('Frequency')
plt.xlim(1900, 2020)

ratings_breakdown = books[['ratings_1', 'ratings_2', 'ratings_3', 'ratings_4', 'ratings_5']].sum()
print("Ratings Breakdown:")
print(ratings_breakdown)

print("line 68")

"""## Tags"""

tags = pd.read_csv("https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/tags.csv")
book_tags = book_tags.merge( tags, on = 'tag_id' )
print(book_tags)
tag_counts = book_tags.groupby( 'tag_name_x' ).tag_name_x.count().sort_values( ascending = False )

tag_counts.head(10)

print("line 76")

"""## Correlation Matrix"""

corr_df = books.copy()
corr_df.drop(['authors', 'book_id', 'goodreads_book_id', 'best_book_id', 'work_id', 'original_title', 'books_count', 'title', 'language_code', 'isbn', 'isbn13', 'ratings_1', 'ratings_2', 'ratings_3', 'ratings_4', 'ratings_5', 'ratings_count'], axis=1, inplace=True)
corr_df.head()

correlation_matrix = corr_df.corr()
mask = np.zeros_like(correlation_matrix)
mask[np.triu_indices_from(mask)] = True
sns.heatmap(correlation_matrix, vmax=1, vmin=-1, annot=True, mask=mask, cmap=sns.diverging_palette(20,220, as_cmap=True))

"""# Collaborative Filtering"""

train_data, test_data = sklearn.model_selection.train_test_split(ratings, test_size=0.2)


def create_X(df):
    """
    Generates a sparse matrix from ratings dataframe.

    Args:
        df: pandas dataframe

    Returns:
        X: sparse matrix
        user_mapper: dict that maps user id's to user indices
        user_inv_mapper: dict that maps user indices to user id's
        book_mapper: dict that maps book id's to book indices
        book_inv_mapper: dict that maps book indices to book id's
    """
    N = df['user_id'].nunique()
    M = df['book_id'].nunique()

    user_mapper = dict(zip(np.unique(df["user_id"]), list(range(N))))
    book_mapper = dict(zip(np.unique(df["book_id"]), list(range(M))))

    user_inv_mapper = dict(zip(list(range(N)), np.unique(df["user_id"])))
    book_inv_mapper = dict(zip(list(range(M)), np.unique(df["book_id"])))

    user_index = [user_mapper[i] for i in df['user_id']]
    book_index = [book_mapper[i] for i in df['book_id']]

    X = csr_matrix((df["rating"], (book_index, user_index)), shape=(M, N))

    return X, user_mapper, book_mapper, user_inv_mapper, book_inv_mapper

X, user_mapper, book_mapper, user_inv_mapper, book_inv_mapper = create_X(train_data)

sparsity = X.count_nonzero()/(X.shape[0]*X.shape[1])
print(f"Matrix sparsity: {round(sparsity*100,2)}%") # ideally we should have < 0.5% matrix sparsity for collaborative filtering to work best (i think)


similar_books_cache = {}
similar_distances_cache = {}

def find_similar_books(book_id, X, k, metric='cosine', show_distance=True):
    """
    Finds k-nearest neighbours for a given book id.

    Args:
        book_id: id of the book of interest
        X: user-item utility matrix
        k: number of similar books to retrieve
        metric: distance metric for kNN calculations

    Returns:
        list of k similar book ID's
    """
    if book_id in similar_books_cache:
      return similar_books_cache[book_id], similar_distances_cache[book_id]

    neighbour_ids = []
    neighbour_distances = []

    book_ind = book_mapper[book_id]
    book_vec = X[book_ind]
    k+=1
    kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
    kNN.fit(X)
    if isinstance(book_vec, (np.ndarray)):
        book_vec = book_vec.reshape(1,-1)
    neighbour = kNN.kneighbors(book_vec, return_distance=show_distance)
    for i in range(0,k):
        book_index = neighbour[1][0][i]
        neighbour_ids.append(book_inv_mapper[book_index])

        book_distance = neighbour[0][0][i]
        neighbour_distances.append(book_distance)

    neighbour_ids.pop(0)

    similar_books_cache[book_id] = neighbour_ids
    similar_distances_cache[book_id] = neighbour_distances
    return neighbour_ids, neighbour_distances

book_titles = dict(zip(books['book_id'], books['original_title']))

book_id = 1

similar_ids, similar_distances = find_similar_books(book_id, X, k=10)

book_title = book_titles[book_id]

print(f"Because you read {book_title}")
for index, id in enumerate(similar_ids):
    print(index + 1, book_titles[id], "- Distance: ", round(similar_distances[index], 3))

def create_book_id_list():
    book_id_list_df = pd.read_csv("https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/books.csv")
    print(book_id_list_df.columns)
    return book_id_list_df

book_id_list = create_book_id_list()

def find_similar_books_wrapper(book_title):
    book_id_from_title = book_id_list.loc[book_id_list['original_title'] == book_title]['book_id'].values[0]
    # book_id_from_title = book_id_list.where(book_id_list.book_title == book_title)
    # print(book_id_from_title.values[0])
    return find_similar_books(book_id_from_title, X, k=10)


def test_find_similar_books_wrapper(book_title):
    book_titles = dict(zip(books['book_id'], books['original_title']))

    book_id = book_id_list.loc[book_id_list['original_title'] == book_title]['book_id'].values[0]

    similar_ids, similar_distances = find_similar_books_wrapper(book_title)

    book_title = book_titles[book_id]

    results = []

    print(f"Because you read {book_title}")
    for index, id in enumerate(similar_ids):
        result = f"{book_titles[id]} - Distance: {round(similar_distances[index], 3)}"
        results.append(result)
        print(index + 1, book_titles[id], "- Distance: ", round(similar_distances[index], 3))
    
    print("results:", results)
    return results