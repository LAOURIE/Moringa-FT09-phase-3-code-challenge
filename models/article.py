class Article:
    all = {}
    def __init__(self,id=None, title=None, content=None, author=None, magazine=None,conn = None,author_id=None,magazine_id=None):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id if author_id else author.id
        self.magazine_id = magazine_id if magazine_id else magazine.id
        self.conn = conn

        if conn:
            self.cursor = self.conn.cursor()
            self.add_to_database()

    def __repr__(self):
        return f'<Article {self.title}>'
    

    def add_to_database(self):
        sql_check = "SELECT id FROM articles WHERE title = ? "
        result = self.cursor.execute(sql_check,(self.title,)).fetchone()
        if result:
            self.id = result[0]
        else:
            sql = "INSERT INTO articles (title,content,author_id,magazine_id) VALUES (?,?,?,?)"
            self.cursor.execute(sql,(self.title,self.content,self.author_id,self.magazine_id))
            self.conn.commit()
            self.id = self.cursor.lastrowid
            type(self).all[self.id] = self

    @property
    def title(self):
        if not hasattr(self,"_title"):
            sql = "SELECT title FROM articles WHERE id = ?"
            row = self.cursor.execute(sql,(self.id,)).fetchone()
            if row:
                self._title = row[0]
        return self._title
        
    @title.setter
    def title(self,title):
        if isinstance(title,str) and 5 <= len(title) <= 50 and not hasattr(self,"_title") :
            self._title = title
        else:
            raise ValueError("Title must be a string between 5 and 50 characters long and can only be set once.")

    def author(self):
        from models.author import Author
        sql = "SELECT authors.* FROM articles INNER JOIN authors ON articles.author_id = authors.id WHERE articles.id = ?"
        row = self.cursor.execute(sql,(self.id,)).fetchone()
        if row:
            return Author(id=row[0], name=row[1], conn=self.conn)
        else:
            return None

    
    def magazine(self):
        from models.magazine import Magazine
        sql = "SELECT magazines.* FROM articles INNER JOIN magazines ON articles.magazine_id = magazines.id WHERE articles.id = ?"
        row = self.cursor.execute(sql,(self.id,)).fetchone()
        if row:
            return Magazine(id=row[0],name=row[1],category=row[2],conn=self.conn)
        else:
            return None

    @classmethod
    def instance_from_db(cls,row,conn):
        article = cls.all.get(row[0])
        if article:
            article.content = row[2]

        else:
            article = cls(title = row[1],content = row[2], author_id = row[3], magazine_id = row[4],conn = conn)
            article.id = row[0]
            cls.all[article.id] = article
        return article

    @classmethod
    def find_by_id(cls, conn, id):
        sql = """
            SELECT *
            FROM articles
            WHERE id is ?
        """
        cursor = conn.cursor()

        row = cursor.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row,conn) if row else None
    
    @classmethod
    def get_all_articles(cls,conn):
        sql = "SELECT * FROM articles"
        cursor = conn.cursor()
        articles = cursor.execute(sql).fetchall()
        return [cls.instance_from_db(row,conn) for row in articles]

    