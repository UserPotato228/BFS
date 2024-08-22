# CONFIG FILE

# IMPORTS
import random, os

# project directory
base_dir = os.path.abspath(os.path.dirname(__file__))
formats = {"Изображение":["webp", "jpg", "jpeg", "png", "gif", "svg", "ico", "bmp", "dib", "jpe", "jfif", "tif", "tiff", "heic"],
           "Испольнительный файл":['exe'], "Документ JavaScript":["js"], "Текстовый файл":["txt"], "Каскадная таблица стилей":["css"],
           "Документ HTML":["html"], "Аудио файл":["wav", "aiff", "ape", "flac", "mp3", "ogg", "opus"], "Rich Text Format":["rtf"], "Документ PDF":["pdf"], "Документ XML":["xml"],
           "Документ Microsoft Word":["doc", "docx", "dot", "dotm", "dotx"], "Документ CSV":["csv"],"Таблица OpenDocument":[".ods"],"":[""],"":[""],"":[""],
           "":[""],"":[""],"":[""],"":[""]}

# CONFIG Class
class Config():
    # upload content size
    MAX_CONTENT_LENGTH = 8*1000*1000
    # allowed extensions for upload
    ALLOWED_EXTENSIONS = {"webp", "jpg", "jpeg", "png", "gif", "svg", "ico"}
    # folder for files
    UPLOAD_FOLDER = os.path.join(base_dir, "app", "UPLOAD_FILES")
    # secret key for session
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(random.randint(1, 10))
    # database uri
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or "sqlite:///bfs.db"
