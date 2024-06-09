import sqlite3

class Author:
    def __init__(self, id=None, name=None):
        if id is None and name is None:
            raise ValueError("Either id or name must be provided")

        if id is None:
            # Insert new author into the database
            if not isinstance(name, str) or len(name) == 0:
                raise ValueError("Name must be a non-empty string")

            conn = sqlite3.connect('magazine.db')
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO authors (name)
                VALUES (?)
            ''', (name,))
            self._id = cursor.lastrowid
            self._name = name

            conn.commit()
            conn.close()
        else:
            author = self._get_author_by_id(id)
            if author is None:
                raise ValueError(f"No author found with id {id}")
            self._id = author.id
            self._name = author.name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        raise AttributeError("Cannot modify the id of an author")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError("Cannot modify the name of an author after it has been set")

    def __repr__(self):
        return f'<Author {self.name}>'

    def _get_author_by_id(self, author_id):
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, name FROM authors WHERE id = ?
        ''', (author_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return Author(id=row[0], name=row[1])
        else:
            return None

    @staticmethod
    def delete_author(author_id):
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM authors WHERE id = ?
        ''', (author_id,))

        conn.commit()
        conn.close()

    def update_author_name(self, new_name):
        if not isinstance(new_name, str) or len(new_name) == 0:
            raise ValueError("Name must be a non-empty string")

        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE authors
            SET name = ?
            WHERE id = ?
        ''', (new_name, self._id))

        conn.commit()
        conn.close()
        self._name = new_name

    def articles(self):
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM articles
            JOIN authors ON articles.author_id = authors.id
            WHERE authors.id = ?
        ''', (self.id,))

        rows = cursor.fetchall()
        conn.close()

        return [Article(id=row[0], title=row[1], content=row[2], author_id=row[3], magazine_id=row[4]) for row in rows]

    def magazines(self):
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT DISTINCT magazines.id, magazines.name, magazines.category
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self.id,))

        rows = cursor.fetchall()
        conn.close()

        return [Magazine(id=row[0], name=row[1], category=row[2]) for row in rows]

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f'<Article {self.title}>'

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f'<Magazine {self.name}>'
