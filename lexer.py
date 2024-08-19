from typing import Callable
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text.base import StyleAndTextTuples
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.formatted_text import FormattedText

SQL_WORDS = [
    'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'NOT', 'IN',
    'LIKE', 'BETWEEN', 'IS', 'NULL', 'ORDER', 'BY', 'GROUP',
    'HAVING', 'LIMIT', 'OFFSET', 'JOIN', 'INNER', 'LEFT',
    'RIGHT', 'OUTER', 'FULL', 'CROSS', 'UNION', 'ALL', 'AS',
    'ON', 'USING', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END', 'WHEN',
    'EXISTS', 'CAST', 'CONVERT', 'TO', 'AS', 'DATE', 'TIME',
    'TIMESTAMP', 'CHAR', 'VARCHAR', 'TEXT', 'BINARY', 'VARBINARY', 'BLOB',
    'INT', 'INTEGER', 'TINYINT', 'SMALLINT', 'MEDIUMINT', 'BIGINT', 'FLOAT',
    'DOUBLE', 'DECIMAL', 'NUMERIC', 'BOOLEAN', 'BOOL', 'DATE', 'TIME', 'TIMESTAMP',
    'YEAR', 'CHARACTER', 'SET', 'ENUM', 'JSON', 'ARRAY', 'OBJECT', 'NULL',
    'TRUE', 'FALSE', 'UNKNOWN', 'AUTO_INCREMENT', 'PRIMARY', 'KEY', 'FOREIGN',
    'REFERENCES', 'DEFAULT', 'CHECK', 'CONSTRAINT', 'UNIQUE', 'INDEX', 'FULLTEXT',
    'SPATIAL', 'CREATE', 'TABLE', 'DROP', 'ALTER', 'RENAME', 'TO', 'ADD', 'MODIFY',
    'CHANGE', 'COLUMN', 'IF', 'EXISTS', 'CASCADE', 'RESTRICT', 'SET', 'NULL',
    'NOT', 'DEFAULT', 'CURRENT_TIMESTAMP', 'CURRENT_DATE', 'CURRENT_TIME',
    'CURRENT_USER', 'CURRENT_ROLE', 'CURRENT_SCHEMA', 'CURRENT_CATALOG',
    'DATABASE', 'SCHEMA', 'SHOW', 'DATABASES', 'TABLES', 'COLUMNS', 'INDEXES',
    'KEYS', 'VIEWS', 'TRIGGERS', 'PROCEDURES', 'FUNCTIONS', 'EVENTS', 'USERS',
    'GRANTS', 'PRIVILEGES', 'ROLES', 'SESSION', 'VARIABLES', 'STATUS', 'GLOBAL',
    'LOCAL', 'SET', 'SHOW', 'SET', 'SESSION', 'TRANSACTION', 'COMMIT', 'ROLLBACK',
    'SAVEPOINT', 'BEGIN', 'START'
]

class SqlLexer(Lexer):
    def lex_document(self, document):
        def get_line(lineno):
            line = document.lines[lineno]
            formatted_line = []
            for word in line.split():
                if word.upper() in SQL_WORDS:
                    formatted_line.append(('class:sql-keyword', word))
                    formatted_line.append(('', ' '))
                else:
                    formatted_line.append(('', word + ' '))
            return FormattedText(formatted_line)
        return get_line

