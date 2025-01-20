import threading
from typing import Dict, List

from duowen_huqie.nlp.query import FulltextQueryer
from duowen_huqie.nlp.rag_tokenizer import RagTokenizer
from duowen_huqie.nlp.synonym import SynonymDealer
from duowen_huqie.nlp.term_weight import TermWeightDealer, TermInfo
from functools import partial


class NLP:

    def __init__(self, tokenizer: RagTokenizer = None, tw: TermWeightDealer = None, syn: SynonymDealer = None, ):

        self.tokenizer = tokenizer if tokenizer else RagTokenizer()
        self.tw = tw if tw else TermWeightDealer(self.tokenizer)
        self.syn = syn if syn else SynonymDealer()
        self.query = FulltextQueryer(self.tokenizer, self.tw, self.syn)

        # 使用 partial 绑定 self 到方法上
        self.query_text_similarity = partial(self.text_similarity, qa=True)
        self.query_hybrid_similarity = partial(self.hybrid_similarity, qa=True)

    def tok_add_word(self, word, frequency: int, pos: str):
        self.tokenizer.add_word(word, frequency=frequency, pos=pos)

    def tok_del_word(self, word):
        self.tokenizer.del_word(word)

    def tok_update_word(self, word, frequency: int, pos: str):
        self.tokenizer.update_word(word, frequency=frequency, pos=pos)

    def ner_init_word(self) -> None:
        self.tw.init_word()

    def ner_set_word(self, word: str, term_type: str) -> None:
        self.tw.set_word(word, term_type)

    def ner_del_word(self, word: str) -> None:
        self.tw.del_word(word)

    def syn_init_word(self) -> None:
        self.syn.init_word()

    def syn_set_word(self, word: str, alias: str) -> None:
        self.syn.set_word(word, alias)

    def syn_del_word(self, word: str) -> None:
        self.syn.del_word(word)

    def content_cut(self, text: str):
        return self.tokenizer.tokenize(text)

    def content_sm_cut(self, text: str):
        return self.tokenizer.fine_grained_tokenize(self.tokenizer.tokenize(text))

    def term_weight(self, text: str):
        match, keywords = self.query.question(text)
        if match:
            return match.matching_text
        else:
            return None

    def text_similarity(self, question: str, docs: List[str], qa=False):
        return [float(i) for i in
                self.query.token_similarity(self.content_cut(self.query.rmWWW(question) if qa else question),
                    [self.content_cut(i) for i in docs])]

    def hybrid_similarity(self, question: str, docs: List[str], question_vector: List[float],
                          docs_vector: List[List[float]], tkweight: float = 0.3, vtweight: float = 0.7, qa=False):
        _h, _t, _v = self.query.hybrid_similarity(question_vector, docs_vector,
                                                  self.content_cut(self.query.rmWWW(question) if qa else question),
                                                  [self.content_cut(i) for i in docs], tkweight, vtweight)
        return [float(i) for i in _h]





class NLPWrapper:

    def __init__(self):
        self.nlp_instance: Dict[str, NLP] = {}
        self.lock = threading.Lock()

    def __contains__(self, item: str) -> bool:
        return item in self.nlp_instance

    def __getitem__(self, item: str):
        if item in self.nlp_instance:
            return self.nlp_instance[item]
        else:
            raise KeyError(f"NLPWrapper not found instance {item}")

    def __setitem__(self, key: str, value: NLP):
        if key in self.nlp_instance:
            del self.nlp_instance[key]
        self.nlp_instance[key] = value

    def __delitem__(self, key: str):
        if key in self.nlp_instance:
            del self.nlp_instance[key]


nlp_server = NLPWrapper()
