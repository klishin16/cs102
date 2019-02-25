from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import session, News
from sqlalchemy import and_
import string
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    new = s.query(News).filter(News.id == request.query.id).one()
    new.label = request.query.label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    latest_news = get_news("https://news.ycombinator.com/newest", n_pages=1)
    titles = [new['title'] for new in latest_news]
    authors = [new['author'] for new in latest_news]
    existing_news = s.query(News).filter(and_((News.author.in_(authors)), (News.title.in_(titles)))).all()
    for item in latest_news:
        if item['title'] not in [n.title for n in existing_news] and item['author'] not in [n.author for n in existing_news]:
            s.add(News(**item))
    s.commit()
    redirect("/news")


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


@route("/classify")
def classify_news():
    s = session()
    labeled_news = s.query(News).filter(News.label != None).all()
    x = [clean(new.title) for new in labeled_news]
    y = [new.label for new in labeled_news]
    model = NaiveBayesClassifier()
    model.fit(x, y)
    unlabeled_news = s.query(News).filter(News.label == None).all()
    good = []
    maybe = []
    never = []
    titles = [clean(current_new.title) for current_new in unlabeled_news]
    predictions = model.predict(titles)
    for i, current_news in zip(range(len(unlabeled_news)), unlabeled_news):
        if predictions[i] == 'good':
            good.append(current_news)
        elif predictions[i] == 'maybe':
            maybe.append(current_news)
        else:
            never.append(current_news)
    return template('recommendations', good=good, maybe=maybe, never=never)


if __name__ == "__main__":
    run(host="localhost", port=8080)
