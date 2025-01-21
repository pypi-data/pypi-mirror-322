import regex as re


class Normalizer:
    def __init__(
        self,
        space_correction: bool = True,
        unify_numbers: bool = True,
        unify_punctuations: bool = True,
        unify_arabic_unicode: bool = True,
        remove_emojis: bool = True,
        remove_diactrics: bool = True,
        remove_punctuations: bool = False,
    ):
        self._unify_numbers = unify_numbers
        self._unify_punctuations = unify_punctuations
        self._unify_arabic_unicode = unify_arabic_unicode
        self._remove_emojis = remove_emojis
        self._remove_diactrics = remove_diactrics
        self._remove_punctuations = remove_punctuations

        self._diacritics_mappings = [
            (r"[ًٌٍَُِّْٰٖٕٓٔؕٙٴ̒́]", ""),
        ]

        self._character_mappings = [
            (r"[ـ]", ""),
            (r"[ﺁﺂ]", "آ"),
            (r"[ٲٵﭐﭑٳﺇﺈإأٱ]", "ا"),
            (r"[ٮٻڀݐݒݔݕݖﭒﭕﺏﺒ]", "ب"),
            (r"[ﭖﭗﭘﭙﭚﭛﭜﭝ]", "پ"),
            (r"[ٹٺټٿݓﭞﭟﭠﭡﭦﭨﺕﺘ]", "ت"),
            (r"[ٽݑﺙﺚﺛﺜﭢﭤ]", "ث"),
            (r"[ڃڄﭲﭴﭵﭷﺝﺟﺠ]", "ج"),
            (r"[ڇڿﭺݘﭼﮀﮁݯ]", "چ"),
            (r"[ځڂڅݗݮﺡﺤ]", "ح"),
            (r"[ﺥﺦﺧ]", "خ"),
            (r"[ڈډڊڋڍۮݙݚﮂﮈﺩ]", "د"),
            (r"[ڌﱛﺫﺬڎڏڐﮅﮇ]", "ذ"),
            (r"[ڑڒړڔڕږۯݛﮌﺭ]", "ر"),
            (r"[ڗݫﺯﺰ]", "ز"),
            (r"[ڙﮊﮋ]", "ژ"),
            (r"[ښڛﺱﺴ]", "س"),
            (r"[ڜۺﺵﺸݜݭ]", "ش"),
            (r"[ڝڞﺹﺼ]", "ص"),
            (r"[ۻﺽﻀ]", "ض"),
            (r"[ﻁﻃﻄ]", "ط"),
            (r"[ﻅﻆﻈڟ]", "ظ"),
            (r"[ڠݝݞݟﻉﻊﻋ]", "ع"),
            (r"[ۼﻍﻎﻐ]", "غ"),
            (r"[ڡڢڣڤڥڦݠݡﭪﭫﭬﻑﻒﻓ]", "ف"),
            (r"[ٯڧڨﻕﻗ]", "ق"),
            (r"[كػؼڪګڬڭڮݢݣﮎﮐﯓﻙﻛ]", "ک"),
            (r"[ڰڱڲڳڴﮒﮔﮖ]", "گ"),
            (r"[ڵڶڷڸݪﻝﻠ]", "ل"),
            (r"[۾ݥݦﻡﻢﻣ]", "م"),
            (r"[ڹںڻڼڽݧݨݩﮞﻥﻧ]", "ن"),
            (r"[ٶٷﯗﯘﯙﯚﯜﯝﯞﯟﺅۄۅۉۊۋۏﯠﻭؤפ]", "و"),
            (r"[ھۿۀہۂۃەﮤﮦﮧﮨﮩﻩﻫة]", "ه"),
            (
                r"[ؠؽؾؿىيٸۍێېۑےۓﮮﮯﮰﮱﯤﯥﯦﯧﯼﯽﯾﯿﻯﻱﻳﯨﯩﯫﯭﯰﯳﯵﯷﯹﯻﱝ]",
                "ی",
            ),
        ]

        self._number_mappings = [
            (r"[0٠𝟢𝟬]", "۰"),
            (r"[1١𝟣𝟭⑴⒈⓵①❶𝟙𝟷ı]", "۱"),
            (r"[2٢𝟤𝟮⑵⒉⓶②❷²𝟐𝟸𝟚ᒿշ]", "۲"),
            (r"[3٣𝟥𝟯⑶⒊⓷③❸³ვ]", "۳"),
            (r"[4٤𝟦𝟰⑷⒋⓸④❹⁴]", "۴"),
            (r"[5٥𝟧𝟱⑸⒌⓹⑤❺⁵]", "۵"),
            (r"[6٦𝟨𝟲⑹⒍⓺⑥❻⁶]", "۶"),
            (r"[7٧𝟩𝟳⑺⒎⓻⑦❼⁷]", "۷"),
            (r"[8٨𝟪𝟴⑻⒏⓼⑧❽⁸۸]", "۸"),
            (r"[9٩𝟫𝟵⑼⒐⓽⑨❾⁹]", "۹"),
            (r"[⑽⒑⓾⑩]", "۱۰"),
            (r"[⑾⒒⑪]", "۱۱"),
            (r"[⑿⒓⑫]", "۱۲"),
            (r"[⒀⒔⑬]", "۱۳"),
            (r"[⒁⒕⑭]", "۱۴"),
            (r"[⒂⒖⑮]", "۱۵"),
            (r"[⒃⒗⑯]", "۱۶"),
            (r"[⒄⒘⑰]", "۱۷"),
            (r"[⒅⒙⑱]", "۱۸"),
            (r"[⒆⒚⑲]", "۱۹"),
            (r"[⒇⒛⑳]", "۲۰"),
        ]

        self._punctuation_unifiying_mappings = [
            (r"[▕❘❙❚▏│]", "|"),
            (r"[ㅡ一—–ー̶ـ]", "-"),
            (r"[▁_̲]", "_"),
            (r"[❔?�؟ʕʔ🏻\x08\x97\x9d]", "؟"),
            (r"[❕！]", "!"),
            (r"[⁉]", "!؟"),
            (r"[‼]", "!!"),
            (r"[℅%]", "٪"),
            (r"[÷]", "/"),
            (r"[×]", "*"),
            (r"[：]", ":"),
            (r"[›]", ">"),
            (r"[‹＜]", "<"),
            (r"[《]", "«"),
            (r"[》]", "»"),
            (r"[•]", "."),
            (r"[٬,]", "،"),
            (r"[;；]", "؛"),
        ]

        self._no_punctuation_mappings = [
            (r"[^\w\s\d\p{Emoji}]", ""),
        ]

        self._extra_space_mappings = [
            (r" {2,}", " "),  # remove extra spaces
            (r"\n{3,}", "\n\n"),  # remove extra newlines
            (r"\u200c{2,}", "\u200c"),  # remove extra ZWNJs
            (r"\u200c{1,} ", " "),  # remove unneded ZWNJs before space
            (r" \u200c{1,}", " "),  # remove unneded ZWNJs after space
            (r"\b\u200c*\B", ""),  # remove unneded ZWNJs at the beginning of words
            (r"\B\u200c*\b", ""),  # remove unneded ZWNJs at the end of words
            (r"[\u200b\u200d\u200e\u200f\u2066\u2067\u202a\u202b\u202d]", ""),
        ]

        self._emoji_mappings = [
            (r"[😀-😯]", ""),
            (r"[🌐-🖿]", ""),
            (r"[🚀-🛿]", ""),
            (r"[🇠-🇿]", ""),
            (r"[㠠-𯿿]", ""),
            (r"[⏰]", ""),
            (r"[♀-♂]", ""),
            (r"[☀-🔿]", ""),
            (r"[‍]", ""),
            (r"[⏏]", ""),
            (r"[⏩]", ""),
            (r"[⌚]", ""),
            (r"[️]", ""),
            (r"[💯]", ""),
            (r"[〰]", ""),
            (r"[⏱]", ""),
            (r"[⏪]", ""),
        ]

        self._unicode_mappings = [
            ("﷽", "بسم الله الرحمن الرحیم"),
            ("﷼", "ریال"),
            ("(ﷰ|ﷹ)", "صلی"),
            ("ﷲ", "الله"),
            ("ﷳ", "اکبر"),
            ("ﷴ", "محمد"),
            ("ﷵ", "صلعم"),
            ("ﷶ", "رسول"),
            ("ﷷ", "علیه"),
            ("ﷸ", "وسلم"),
            ("ﻵ|ﻶ|ﻷ|ﻸ|ﻹ|ﻺ|ﻻ|ﻼ", "لا"),
        ]

        self._all_mappings = []
        self._all_mappings.extend(self._character_mappings)

        if unify_punctuations and not remove_punctuations:
            self._all_mappings.extend(self._punctuation_unifiying_mappings)

        if remove_punctuations:
            self._all_mappings.extend(self._no_punctuation_mappings)

        if unify_numbers:
            self._all_mappings.extend(self._number_mappings)
        if unify_arabic_unicode:
            self._all_mappings.extend(self._unicode_mappings)
        if remove_emojis:
            self._all_mappings.extend(self._emoji_mappings)
        if remove_diactrics:
            self._all_mappings.extend(self._diacritics_mappings)
        if space_correction:
            self._all_mappings.extend(self._extra_space_mappings)

    def normalize(self, text):
        # unification
        for pattern, replacement in self._all_mappings:
            text = re.sub(pattern, replacement, text)

        # space correction
        text = self.space_correction(text)

        return text

    def unify_numbers(self, text):
        for pattern, replacement in self._number_mappings:
            text = re.sub(pattern, replacement, text)
        return text

    def unify_punctuations(self, text):
        for pattern, replacement in self._punctuation_unifiying_mappings:
            text = re.sub(pattern, replacement, text)
        return text

    def unify_characters(self, text):
        for pattern, replacement in self._character_mappings:
            text = re.sub(pattern, replacement, text)
        return text

    def unify_arabic_unicode(self, text):
        for pattern, replacement in self._unicode_mappings:
            text = re.sub(pattern, replacement, text)
        return text

    def remove_emojis(self, text):
        for pattern, replacement in self._emoji_mappings:
            text = re.sub(pattern, replacement, text)
        return text

    def remove_diactrics(self, text):
        for pattern, replacement in self._diacritics_mappings:
            text = re.sub(pattern, replacement, text)
        return text

    def remove_punctuations(self, text):
        for pattern, replacement in self._no_punctuation_mappings:
            text = re.sub(pattern, replacement, text)
        return text

    def remove_diacritics(self, text):
        for pattern, replacement in self._diacritics_mappings:
            text = re.sub(pattern, replacement, text)
        return text

    def remove_extra_spaces(self, text):
        for pattern, replacement in self._extra_space_mappings:
            text = re.sub(pattern, replacement, text)
        return text

    def space_correction(self, sentence):
        # copied from ParsiNorm with
        # This Function is a mixture of HAZM and ParsiVar Features

        sentence = re.sub(r"^(بی|می|نمی)( )", r"\1‌", sentence)  # verb_prefix
        sentence = re.sub(r"( )(می|نمی)( )", r"\1\2‌ ", sentence)  # verb_prefix
        sentence = re.sub(
            r"([^ ]ه) ی ", r"\1‌ی ", sentence
        )  # nouns ends with ه when having ی
        sentence = re.sub(
            r"( )(هایی|ها|های|ایی|هایم|هایت|هایش|هایمان|هایتان|هایشان|ات|ان|ین"
            r"|انی|بان|ام|ای|یم|ید|اید|اند|بودم|بودی|بود|بودیم|بودید|بودند|ست|تر|تری|ترین|گری|گر)( )",
            r"‌\2\3",
            sentence,
        )
        # Issue: some suffixes may introduce incorrect spacing!
        # A more complex solution is needed to fix this issue.
        # Example: "با کی‌داری حرف می‌زنی؟" <- "با کی داری حرف می‌زنی؟"
        # Example: "به نکته ریزی اشاره کردی!" -> "به نکته‌ریزی اشاره کردی!"

        # complex_word_suffix_pattern = (
        #     r"( )(طلبان|طلب|گرایی|گرایان|شناس|شناسی|گذاری|گذار|گذاران|شناسان|گیری|پذیری|بندی|آوری|سازی|"
        #     r"بندی|کننده|کنندگان|گیری|پرداز|پردازی|پردازان|آمیز|سنجی|ریزی|داری|دهنده|آمیز|پذیری"
        #     r"|پذیر|پذیران|گر|ریز|ریزی|رسانی|یاب|یابی|گانه|گانه‌ای|انگاری|گا|بند|رسانی|دهندگان|دار)( )"
        # )
        # sentence = re.sub(complex_word_suffix_pattern, r"‌\2\3", sentence)
        sentence = re.sub(r' "([^\n"]+)" ', r'"\1"', sentence)

        punc_after = r".\.:!،؛؟»\]\)\}"
        punc_before = r"«\[\(\{"

        sentence = re.sub(
            r" ([" + punc_after + "])|([" + punc_before + "]) ", r"\1\2", sentence
        )  # Remove/add spaces around punctuation
        sentence = re.sub(
            r"([.،:؟!])([^ {} \d۰۱۲۳۴۵۶۷۸۹])".format(punc_after), r"\1 \2", sentence
        )  # Add space after ., :
        sentence = re.sub(
            r"([^ " + punc_before + "])([" + punc_before + "])", r"\1 \2", sentence
        )  # Add space before punctuation

        sentence = self.remove_extra_spaces(sentence)
        return sentence
