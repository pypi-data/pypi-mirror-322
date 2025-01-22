from bs4 import BeautifulSoup


def fb2_read(path):
    with open(path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')
        text = ""

        # Находим и выводим информацию о книге
        title = soup.title.text if soup.title else "Название книги не найдено"
        text += f'Название книги: {title}\n'

        authors = soup.find_all('author')
        authors_list = [author.get_text() for author in authors]
        text += f'Автор(ы):{', '.join(authors_list)}\n'

        # Читаем содержимое книги
        sections = soup.find_all('section')
        for section in sections:
            title = section.title.text if section.title else "Название главы не найдено"
            text += f'\n--- Глава: {title} ---\n'

            paragraphs = section.find_all('p')
            for p in paragraphs:
                text += (p.text + '\n')

    return text


if __name__ == '__main__':
    print(fb2_read('../../book.fb2'))
