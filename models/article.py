import sqlite3

class Article:
     def _init_(self, author=None, magazine=None, title=None, id=None):
         if id is None and (author is None or magazine is None or title is None):
             raise ValueError("Either id or author, magazine and title must be provided")
         if id is None:
             if not isinstance(title, str) or len(title) < 5 or len(title) > 50:
                 raise ValueError("Title must be a string between 5 and 50 characters")
             
             self._author_id = author.id
             self._magazine_id = magazine.id
             self._title = title
            
            
             conn = sqlite3.connect('magazine.db')
             cursor = conn.cursor()
             
             cursor.execute('''
                 INSERT INTO articles (author_id, magazine_id, title)
                            VALUES (?, ?, ?)
                            ''', (self._author_id, self._magazine_id, self._title)           )
             self._id = cursor.lastrowid
             conn.commit()
             conn.close()


         else:
             article = self._get_article_by_id(id)
             if article is None:
                 raise ValueError(f"No article found with id {id}")
             self._id = article._id
             self._author_id = article._author_id
             self._magazine_id = article._magazine_id
             self._title = article._title

     @property
     def id(self):
         return self._id
     
     @id.setter
     def id(self, value):
         raise AttributeError("Cannot modify the id of an article")

     @property
     def title(self):
         return self._title
     
     @title.setter
     def title(self, value):
         raise AttributeError("Cannot modify the title of an article after it has been set")
     
     @property
     def author(self):
         return self._get_author_by_article_id(self._id)
     
     @property
     def magazine(self):
         return self._get_magazine_by_article_id(self._id)
     def __repr__(self) :
         return f'<Article {self.title}>'
     
     @staticmethod
     def _get_article_by_id(article_id):
         conn = sqlite3.connect('magazine.db')
         cursor = conn.cursor()
         
         cursor.execute('''
             SELECT id, author_id, magazine_id, title FROM articles where id = ?
             ''', (article_id,))
         row = cursor.fetchone()
         conn.close()
         
         if row:
             return Article(id=row[0], author_id=row[1], magazine_id=row[2], title=row[3])
         else:
             return None
         @staticmethod
         def delete_article(article_id):
             conn = sqlite3.connect('magazine.db')
             cursor = conn.cursor()
             
            
             cursor.execute('''
             DELETE FROM articles
             WHERE id = ?
             ''', (article_id,))

             conn.commit()
             conn.close()
         @staticmethod
         def update_article_title(self,new_title):
              if not isinstance(new_title, str) or len(new_title) < 5 or len(new_title) > 50:
                  raise ValueError("Title must be a string between 5 and 50 characters")
              
              conn = sqlite3.connect('magazine.db')
              cursor = conn.cursor()

         cursor.execute('''
            UPDATE articles
            SET title = ?
            WHERE id = ?
            ''', (new_title, article_id))

         conn.commit()
         conn.close()

         article = Article._get_article_by_id(article_id)
         article._title = new_title
         return article
     
     @staticmethod
     def _get_author_by_article_id(article_id):
         conn = sqlite3.connect('magazine.db')
         cursor = conn.cursor()
         
         cursor.execute('''
             SELECT authors.id, authors.name
             FROM authors
                        JOIN articles ON authors.id = articles.author_id
             WHERE articles.id = ?
             ''', (article_id,))
         
         row = cursor.fetchone()
         conn.close()
         
         if row:
             return Author(id=row[0], name=row[1])
         else:
             return None
         @staticmethod
         def _get_magazine_by_article_id(article_id):
             conn = sqlite3.connect('magazine.db')
             cursor = conn.cursor()
             
             cursor.execute('''
                 SELECT magazines.id, magazines.name, magazines.category
                 FROM magazines
                            JOIN articles ON magazines.id = articles.magazine_id
                 WHERE articles.id = ?
                 ''', (article_id,))
             
             row = cursor.fetchone()
             conn.close()

             if row:
                 return Magazine(id=row[0], name=row[1], category=row[2])
             else:
                 return None