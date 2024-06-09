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

    @staticmethod
    def _get_author_by_id(author_id):
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
    def __init__(self, id=None, name=None, category=None):
        if id is None and (name is None or category is None):
            raise ValueError("id, or both name and category, must be provided")

        if id is None:
            # Insert new magazine into the database
            if not isinstance(name, str) or len(name) < 2 or len(name) > 16:
                raise ValueError("Name must be a string between 2 and 16 characters")
            if not isinstance(category, str) or len(category) == 0:
                raise ValueError("Category must be a non-empty string")

            conn = sqlite3.connect('magazine.db')
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO magazines (name, category)
                VALUES (?, ?)
            ''', (name, category))
            self._id = cursor.lastrowid
            self._name = name
            self._category = category

            conn.commit()
            conn.close()
        else:
          #  magazine = self._get_magazine_by_id(id)
            if magazine is None:
                raise ValueError(f"No magazine found with id {id}")
            self._id = magazine.id
            self._name = magazine.name
            self._category = magazine.category

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        raise AttributeError("Cannot modify the id of a magazine")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) < 2 or len(value) > 16:
            raise ValueError("Name must be a string between 2 and 16 characters")
        self._name = value
        self._update_magazine_field("name", value)

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string")
        self._category = value
        self._update_magazine_field("category", value)

    def __repr__(self):
        return f'<Magazine {self.name}>'

    def _update_magazine_field(self, field, value):
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute(f'''
            UPDATE magazines
            SET {field} = ?
            WHERE id = ?
        ''', (value, self._id))

        conn.commit()
        conn.close()

    @staticmethod
    def _get_magazine_by_id(magazine_id):
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, name, category FROM magazines WHERE id = ?
        ''', (magazine_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return Magazine(id=row[0], name=row[1], category=row[2])
        else:
            return None

    @staticmethod
    def delete_magazine(magazine_id):
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM magazines WHERE id = ?
        ''', (magazine_id,))

        conn.commit()
        conn.close()

    def articles(self):
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM articles
            JOIN magazines ON articles.magazine_id = magazines.id
            WHERE magazines.id = ?
        ''', (self.id,))

        rows = cursor.fetchall()
        conn.close()

        return [Article(id=row[0], title=row[1], content=row[2], author_id=row[3], magazine_id=row[4]) for row in rows]

    def contributors(self):
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT DISTINCT authors.id, authors.name
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self.id,))

        rows = cursor.fetchall()
        conn.close()

        return [Author(id=row[0], name=row[1]) for row in rows]

    def article_titles(self):
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT title
            FROM articles
            WHERE magazine_id = ?
        ''', (self.id,))

        rows = cursor.fetchall()
        conn.close()

        if rows:
            return [row[0] for row in rows]
        else:
            return None

    def contributing_authors(self):
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT authors.id, authors.name, COUNT(articles.id) as article_count
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id, authors.name
            HAVING COUNT(articles.id) > 2
        ''', (self.id,))

        rows = cursor.fetchall()
        conn.close()

        if rows:
            return [Author(id=row[0], name=row[1]) for row in rows]
        else:
            return None

