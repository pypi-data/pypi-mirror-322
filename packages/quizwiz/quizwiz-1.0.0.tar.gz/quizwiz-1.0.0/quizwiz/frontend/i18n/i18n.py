import yaml
import os


class I18n:
    def __init__(self, lang="ko"):
        # 기본 언어를 영어로 설정, 이후 언어 변경 가능
        self.language = lang
        self.translations = self.load_translation(lang)

    # 번역 파일을 로드하는 메서드
    def load_translation(self, lang):
        # 현재 파일의 절대 경로를 기준으로 i18n 폴더 경로 설정
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, f"{lang}.yaml")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Translation file for {lang} not found.")

        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    # 번역된 텍스트를 가져오는 메서드
    def translate(self, key):
        return self.translations.get(key, key)  # 번역이 없으면 키를 그대로 반환

    # 언어를 변경하는 메서드
    def update_language(self, lang):
        self.language = lang
        self.translations = self.load_translation(lang)
