"""Turning a .txt documents into a wordcloud.

Will look into `./data/documents` for documents to convert into wordclouds.

Wordclouds are stored in `./data/wordclouds`
"""

import logging
from pathlib import Path
import re

import spacy
from wordcloud import WordCloud

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

BASE_DIR = Path(__file__).parent


def create_wordcloud(
    file: Path, background_color: str = "#3F3F3F", colormap: str = "rainbow"
) -> None:
    """Create a wordcloud from a text file.

    Args:
        file (Path): Path object of the text document.
        background_color (str): Color of wordcloud background. Defaults to
        #3F3F3F.
        colormap (str): Color of wordcloud words. Defaults to "rainbow".
    """
    spacy.prefer_gpu()
    nlp = spacy.load("en_core_web_sm")

    # opening text file
    with open(str(file), "r") as f:
        text = f.read()

    logging.info(f"Text Length (char): {len(text)}")

    # tokenisation and cleaning text
    doc = nlp(text)
    exclude_list = ["-", "/", "&"]
    clean_doc = [
        _.lemma_.lower()
        for _ in doc
        if _.pos_ != "PUNCT"
        and "\n" not in _.text
        and not _.is_stop
        and _.text not in exclude_list
        and not bool(re.search(r"^\w\.$", _.text))
    ]

    wordcloud = WordCloud(
        width=3000,
        height=2000,
        random_state=1,
        background_color="#3F3F3F",
        colormap="rainbow",
        collocations=False,
    ).generate(" ".join(clean_doc))

    wordcloud_file = BASE_DIR / "data" / "wordclouds"
    file_name = str(file).split("/")[-1].replace("txt", "png")
    wordcloud.to_file(wordcloud_file / file_name)


def main():
    """Run main function."""
    documents_file = BASE_DIR / "data" / "documents"

    logging.debug(list(documents_file.iterdir()))
    text_files = [x for x in documents_file.iterdir() if str(x).split(".")[-1] == "txt"]
    logging.debug(text_files)

    for text_file in text_files:
        create_wordcloud(text_file)


if __name__ == "__main__":
    main()
