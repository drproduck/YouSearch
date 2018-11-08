from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from YouSearch.settings import DOCUMENT_ROOT
from .forms import SearchForm
import os
import numpy as np
from scipy.io import loadmat
import pandas as pd
import pickle

no_display = 20
data = None


# use sessions?

@login_required
def main(request):
    if data is None:
        load()

    if request.method == 'POST':
        # papers by keywords

        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            keys = tokenize(search_form.cleaned_data['keywords'])
            inds = search(keys)
            titles, authors, abstracts = query(inds)

    else:
        # default list of papers
        inds = np.random.choice(data['no_paper'], size=no_display)
        titles, authors, abstracts = query(inds)

    user = request.user
    username = user.username
    # path = os.path.join(DOCUMENT_ROOT, username)
    # if not os.path.exists(path):
    #     os.makedirs(path)
    # file_list = [f for f in os.listdir(path)]
    search_form = SearchForm()

    list = zip(titles, authors, abstracts, inds)

    return render(request, template_name='dashboard/main.djt', context={'user': user, 'search_form': search_form,
                                                                        'list': list})

@login_required
def get_similar_papers(request, paper_id, knn=20):
    """

    :param id:
    :return:
    """
    if data is None:
        load()

    paper_id = int(paper_id)
    doc_vector = data['doc_embedding'][paper_id]
    distance = doc_vector.dot(data['doc_embedding'].T)
    rank = np.argsort(distance)

    inds = [paper_id]
    inds.extend(rank[-knn:])

    titles, authors, abstracts = query(inds)
    user = request.user.username
    search_form = SearchForm()

    list = zip(titles, authors, abstracts, inds)

    return render(request, template_name='dashboard/main.djt', context={'user': user, 'search_form': search_form,
                                                                        'list':list})


def tokenize(search_string):
    """
    possibly lemmatize here?
    """
    return search_string.strip().split()


def query(inds):
    """

    :param inds:
    :return titles:
    :return authors:
    :return abstracts:
    """
    return data['papers']['title'][inds], data['authors']['name'][inds], data['papers']['abstract'][inds]


def search(keywords, knn=20):
    """

    :param keywords:
    :return:
    """
    keywords_vectors = []
    for k in keywords:
        try:
            keywords_vectors += [data['word_embedding'][k]]
        except KeyError:
            continue

    rep_vector = np.array(keywords_vectors).mean(axis=0)
    # normlize
    rep_vector = rep_vector / np.sqrt(np.sum(rep_vector ** 2))
    distance = data['doc_embedding'].dot(rep_vector)
    rank = np.argsort(distance)

    return rank[-knn:]


def load():
    """
    load all necessary data and embeddings
    temporary method
    """
    global data
    data = dict()
    with open('nips/w_embs.pkl', 'rb') as handle:
        data['word_embedding'] = pickle.load(handle)
    data['papers'] = pd.read_csv('nips/papers.csv')
    data['authors'] = pd.read_csv('nips/authors.csv')
    data['no_paper'] = len(data['papers'])
    data['doc_embedding'] = loadmat('nips/embedding.mat', mat_dtype=True)['doc_embedding']
