import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine
import sqlite3

class TestModels(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE magazines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author_id INTEGER,
                magazine_id INTEGER,
                FOREIGN KEY (author_id) REFERENCES authors(id),
                FOREIGN KEY (magazine_id) REFERENCES magazines(id)
            )
        """)
        self.conn.commit()
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_author_init(self):
        author = Author(name="John Doe", conn=self.conn)
        self.assertEqual(author.name, "John Doe")
        self.assertIsNotNone(author.id)

    def test_author_add_author(self):
        author1 = Author(name="Jane Doe", conn=self.conn)
        author2 = Author(name="Jane Doe", conn=self.conn)
        self.assertEqual(author1.id, author2.id)

    def test_author_id_property(self):
        author = Author(id=1,name="yobra", conn=self.conn)
        self.assertEqual(author.id, 1)
        with self.assertRaises(ValueError):
            author.id = "invalid"

    def test_author_name_property(self):
        author = Author(name="John Doe", conn=self.conn)
        self.assertEqual(author.name, "John Doe")
        with self.assertRaises(ValueError):
            author.name = 123

    def test_articles(self):
        author = Author(name="Jane Doe", conn=self.conn)
        magazine = Magazine(name="Tech Review", category="Technology", conn=self.conn)
        self.cursor.execute("INSERT INTO articles (title,content, author_id,magazine_id) VALUES ('Article 1','Sports', ?,?)", (author.id,magazine.id))
        self.conn.commit()
        articles = author.articles()
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, 'Article 1')


    def test_magazines(self):
        author = Author(name="Jane Doe", conn=self.conn)
        magazine = Magazine(name="Tech Review", category="Technology", conn=self.conn)
        self.cursor.execute("INSERT INTO articles (title,content, author_id, magazine_id) VALUES ('Article 1', 'sport', ?,?)", (author.id, magazine.id))
        self.conn.commit()
        magazines = author.magazines()
        self.assertEqual(len(magazines), 1)
        self.assertEqual(magazines[0].name, "Tech Review")
        self.assertEqual(magazines[0].category, "Technology")

    def test_get_all_authors(self):
        self.cursor.execute("INSERT INTO authors (name) VALUES ('Author 1')")
        self.cursor.execute("INSERT INTO authors (name) VALUES ('Author 2')")
        self.conn.commit()
        authors = Author.get_all_authors(self.conn)
        self.assertEqual(len(authors), 2)
        self.assertEqual(authors[0].name, 'Author 1')
        self.assertEqual(authors[1].name, 'Author 2')

    def test_magazine_init(self):
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        self.assertEqual(magazine.name, "Tech Weekly")
        self.assertEqual(magazine.category, "Technology")
        self.assertIsNotNone(magazine.id)

    def test_magazine_add_to_database(self):
        magazine1 = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        magazine2 = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        self.assertEqual(magazine1.id, magazine2.id)

    def test_magazine_id_property(self):
        magazine = Magazine(id=1,name="Today Daily",category="Sports", conn=self.conn)
        self.assertEqual(magazine.id, 1)
        with self.assertRaises(TypeError):
            magazine.id = "invalid"

    def test_magazine_name_property(self):
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        self.assertEqual(magazine.name, "Tech Weekly")
        with self.assertRaises(ValueError):
            magazine.name = "T"
        with self.assertRaises(ValueError):
            magazine.name = "TooLong"*5

    def test_magazine_category_property(self):
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        self.assertEqual(magazine.category, "Technology")
        with self.assertRaises(ValueError):
            magazine.category = ""

    def test_magazine_articles(self):
        magazine = Magazine(name="Tech Review", category="Technology", conn=self.conn)
        author = Author(name="Jane Doe", conn=self.conn)
        self.cursor.execute("INSERT INTO articles (title,content,author_id, magazine_id) VALUES ('Article 1','tilapia', ?,?)", (author.id,magazine.id))
        self.conn.commit()
        articles = magazine.articles()
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, 'Article 1')
    def test_contributors(self):
        magazine = Magazine(name="Tech Review", category="Technology", conn=self.conn)
        self.cursor.execute("INSERT INTO authors (name) VALUES ('Author 1')")
        self.cursor.execute("INSERT INTO articles (title,content, author_id, magazine_id) VALUES ('Article 1','sports', 1, ?)", (magazine.id,))
        self.conn.commit()
        contributors = magazine.contributors()
        self.assertEqual(len(contributors), 1)
        self.assertEqual(contributors[0].name, 'Author 1')

    def test_get_all_magazines(self):
        self.cursor.execute("INSERT INTO magazines (name, category) VALUES ('Magazine 1', 'Category 1')")
        self.cursor.execute("INSERT INTO magazines (name, category) VALUES ('Magazine 2', 'Category 2')")
        self.conn.commit()
        magazines = Magazine.get_all_magazines(self.conn)
        self.assertEqual(len(magazines), 2)
        self.assertEqual(magazines[0].name, 'Magazine 1')
        self.assertEqual(magazines[0].category, 'Category 1')
        self.assertEqual(magazines[1].name, 'Magazine 2')
        self.assertEqual(magazines[1].category, 'Category 2')

    def test_magazine_article_titles(self):
        author = Author(name="Jane Doe", conn=self.conn)
        magazine = Magazine(name="Tech Review", category="Technology", conn=self.conn)
        self.cursor.execute("INSERT INTO articles (title,content,author_id, magazine_id) VALUES ('Article 1','Dagaa', ?,?)", (author.id,magazine.id,))
        self.cursor.execute("INSERT INTO articles (title,content,author_id, magazine_id) VALUES ('Article 2','Omena', ?,?)", (author.id,magazine.id,))
        self.conn.commit()
        titles = magazine.article_titles()
        self.assertEqual(titles, ['Article 1', 'Article 2'])

    def test_magazine_contributing_authors(self):
        magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        author1 = Author(name="John Doe", conn=self.conn)
        author2 = Author(name="Jane Doe", conn=self.conn)
        article1 = Article(title="Test Title 1", content="Test Content 1", author=author1, magazine=magazine, conn=self.conn)
        article2 = Article(title="Test Title 2", content="Test Content 2", author=author1, magazine=magazine, conn=self.conn)
        article3 = Article(title="Test Title 3", content="Test Content 3", author=author1, magazine=magazine, conn=self.conn)
        article4 = Article(title="Test Title 4", content="Test Content 4", author=author2, magazine=magazine, conn=self.conn)
        contributing_authors = magazine.contributing_authors()
        self.assertEqual(len(contributing_authors), 1)
        self.assertIn(author1, contributing_authors)

    def test_article_creation(self):
        self.author = Author(name="John Doe", conn=self.conn)
        self.magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        article = Article(title="Test Title", content="Test Content", author=self.author, magazine=self.magazine, conn=self.conn)
        self.assertIsNotNone(article.id)
        self.assertEqual(article.title,"Test Title")
        self.assertEqual(article.content,"Test Content")
        self.assertEqual(article.author_id,self.author.id)
        self.assertEqual(article.magazine_id,self.magazine.id)

    def test_article_title_setter_invalid_title(self):
        self.author = Author(name="John Doe", conn=self.conn)
        self.magazine = Magazine(name="Tech Weekly", category="Technology", conn=self.conn)
        article = Article(title="Initial Title", content="Test Content", author=self.author, magazine=self.magazine, conn=self.conn)  # Initialize with a title
        with self.assertRaises(ValueError):
            article.title = "Inv"  # Too short
        with self.assertRaises(ValueError):
            article.title = "Too Long Title" * 10  # Too long
        with self.assertRaises(ValueError):
            article.title = 123  # Not a string
        with self.assertRaises(ValueError):
            article.title = "Already Set"  # Cannot set title twice

    def test_author(self):
        author = Author(name="Jane Doe", conn=self.conn)
        magazine = Magazine(name="Tech Review", category="Technology", conn=self.conn)
        article = Article(title="Article Title", content="Article Content", author=author, magazine=magazine, conn=self.conn)
        returned_author = article.author()
        self.assertEqual(returned_author.name, "Jane Doe")


    def test_magazine(self):
        author = Author(name="Jane Doe", conn=self.conn)
        magazine = Magazine(name="Tech Review", category="Technology", conn=self.conn)
        article = Article(title="Article Title", content="Article Content", author=author, magazine=magazine, conn=self.conn)
        returned_magazine = article.magazine()
        self.assertEqual(returned_magazine.name, "Tech Review")
        self.assertEqual(returned_magazine.category, "Technology")




if __name__ == "__main__":
    unittest.main()