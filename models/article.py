class Article:
    def __init__(self, id=None, title=None, content=None, author=None, magazine=None, conn=None, author_id=None, magazine_id=None):
        self._id = id
        self._title = title
        self._content = content
        self._author_id = author_id if author_id else author.id
        self._magazine_id = magazine_id if magazine_id else magazine.id
        self.conn = conn

        if conn:
            self.cursor = self.conn.cursor()
            self.add_to_database()

    def __repr__(self):
        return f'<Article {self.title}>'

    def add_to_database(self):
        sql = "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)"
        self.cursor.execute(sql, (self._title, self._content, self._author_id, self._magazine_id))
        self.conn.commit()
        self._id = self.cursor.lastrowid

    @property
    def title(self):
        if not hasattr(self, "_title"):
            sql = "SELECT title FROM articles WHERE id = ?"
            row = self.cursor.execute(sql, (self._id,)).fetchone()
            if row:
                self._title = row[0]
        return self._title

    @title.setter
    def title(self, title):
        if isinstance(title, str) and 5 <= len(title) <= 50:
            self._title = title
        else:
            raise ValueError("Title must be a string between 5 and 50 characters long")

    @property
    def content(self):
        if not hasattr(self, "_content"):
            sql = "SELECT content FROM articles WHERE id = ?"
            row = self.cursor.execute(sql, (self._id,)).fetchone()
            if row:
                self._content = row[0]
        return self._content

    @content.setter
    def content(self, content):
        if isinstance(content, str) and len(content) > 0:
            self._
