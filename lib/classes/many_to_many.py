class Article:
    all = []  # Change from all_articles to all

    def __init__(self, author, magazine, title):
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise Exception("Title must be a string 5-50 characters")
        if not isinstance(author, Author) or not isinstance(magazine, Magazine):
            raise Exception("Author and Magazine must be correct instances")

        self._title = title
        self._author = author
        self._magazine = magazine
        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        pass

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise Exception("Must be an Author instance")
        self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):  # Changed parameter name to 'value'
        if not isinstance(value, Magazine):
            raise Exception("Must be a Magazine instance")
        self._magazine = value  # Use 'value' consistently
        
class Author:
    all_authors = []

    def __init__(self, name):
        if not isinstance(name, str) or len(name) == 0:
            raise Exception("Name must be a non-empty string")
        self._name = name
        Author.all_authors.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Silently ignore attempts to change the name
        # This makes it effectively immutable for external access
        pass

    def articles(self):
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        return list({article.magazine for article in self.articles()})

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        mags = self.magazines()
        if not mags:
            return None
        return list({mag.category for mag in mags})

class Magazine:
    all_magazines = []

    def __init__(self, name, category):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise Exception("Name must be a string 2-16 characters")
        if not isinstance(category, str) or len(category) == 0:
            raise Exception("Category must be a non-empty string")
        self._name = name
        self._category = category
        Magazine.all_magazines.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Only set the name if it's valid, otherwise silently ignore
        if isinstance(value, str) and (2 <= len(value) <= 16):
            self._name = value
        # If invalid, do nothing (silently ignore)

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        # Only set the category if it's valid, otherwise silently ignore
        if isinstance(value, str) and len(value) > 0:
            self._category = value

    def articles(self):
        return [article for article in Article.all if article.magazine == self]  # Changed from all_articles to all

    def contributors(self):
        return list({article.author for article in self.articles()})

    def article_titles(self):
        arts = self.articles()
        if not arts:
            return None
        return [article.title for article in arts]

    def contributing_authors(self):
        authors = self.contributors()
        qualified = [author for author in authors if len([a for a in self.articles() if a.author == author]) > 2]
        return qualified if qualified else None

    @classmethod
    def top_publisher(cls):
        if not Article.all:  # Changed from all_articles to all
            return None
        counts = {mag: len(mag.articles()) for mag in cls.all_magazines}
        return max(counts, key=counts.get)