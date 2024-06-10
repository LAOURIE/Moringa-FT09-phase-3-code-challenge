class Magazine:
    def __init__(self, name=None, id=None, category=None, conn=None):
        self._id = id
        self._name = name
        self._category = category
        self.conn = conn
        if conn:
            self.cursor = self.conn.cursor()
            self.add_to_database()

    def __repr__(self):
        return f'<Magazine {self.name}>'

    def add_to_database(self):
        sql_check = "SELECT id FROM magazines WHERE name = ? "
        result = self.cursor.execute(sql_check, (self.name,)).fetchone()
        if result:
            self.id = result[0]
        else:
            sql = "INSERT INTO magazines(name,category) VALUES (?,?)"
            self.cursor.execute(sql, (self.name, self.category))
            self.conn.commit()
            self.id = self.cursor.lastrowid

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if isinstance(id, int):
            self._id = id
        else:
            raise TypeError("ID must be an integer")

    @property
    def name(self):
        if not hasattr(self, "_name"):
            sql = "SELECT name FROM magazines WHERE id = ?"
            row = self.cursor.execute(sql, (self.id,)).fetchone()
            if row:
                self._name = row[0]
        return self._name

    @name.setter
    def name(self, name):
        if not (isinstance(name, str) and 2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        self._name = name

    @property
    def category(self):
        if not hasattr(self, "_category"):
            sql = "SELECT category FROM magazines WHERE id = ?"
            row = self.cursor.execute(sql, (self.id,)).fetchone()
            if row:
                self._category = row[0]
        return self._category

    @category.setter
    def category(self, category):
        if isinstance(category, str) and len(category) > 0:
            self._category = category
        else:
            raise ValueError("Category must be a non-empty string")

    def articles(self):
        from models.article import Article
        sql = "SELECT * FROM articles WHERE articles.magazine_id = ?"
        rows = self.cursor.execute(sql, (self.id,)).fetchall()
        return [Article(id=row[0], title=row[1], content=row[2], author_id=row[3], magazine_id=row[4], conn=self.conn)
                for row in rows]

    def contributors(self):
        from models.author import Author
        sql = "SELECT DISTINCT authors.* FROM authors INNER JOIN articles ON authors.id = articles.author_id WHERE articles.magazine_id = ?"
        rows = self.cursor.execute(sql, (self.id,)).fetchall()
        return [Author(name=author[1], conn=self.conn) for author in rows]

    @classmethod
    def get_all_magazines(cls, conn):
        sql = "SELECT * FROM magazines"
        cursor = conn.cursor()
        magazines = cursor.execute(sql).fetchall()
        return [cls(id=row[0], name=row[1], category=row[2], conn=conn) for row in magazines]

    def article_titles(self):
        articles = self.articles()
        return [item.title for item in articles] if articles else None
