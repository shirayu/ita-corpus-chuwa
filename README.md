
# ITA Corpus Chuwa!

<a rel="license" href="https://creativecommons.org/publicdomain/zero/1.0/"><img alt="Creative Commons License" style="border-width:0" src="https://licensebuttons.net/l/publicdomain/88x31.png" /></a>
[![CircleCI](https://circleci.com/gh/shirayu/ita-corpus-chuwa.svg?style=svg)](https://circleci.com/gh/shirayu/ita-corpus-chuwa)

``ITA Corpus Chuwa!`` is **chu**nked **w**ord **a**nnotation for [ITA corpus](https://github.com/mmorise/ita-corpus), a phonemically balanced public domain corpus of Japanese text.  
``ITAコーパスChuwa!``は音素バランスを考慮したパブリックドメインの日本語テキストコーパスである[ITA corpus](https://github.com/mmorise/ita-corpus)に対する単語と句のアノテーションです．

## 概要

ITAコーパスは2種類のセットからなります

- ``EMOTION``: モノフォン・ダイフォンを考慮した100件
- ``RECITATION``: モノフォン・ダイフォンに加えてトライフォンを豊富に含むように作られた324件

本アノテーションでは，以下のようなものは複数文として扱いました．

```txt
EMOTION100_014
スミスさん、ピエール・デュボワをご紹介しますわ。私の親友なの。
```

そして，``EMOTION``は113文，``RECITATION``は331文からなるとし，単語（形態素）情報と句・構文情報の付与を行いました．

なお，アノテーション誤りを見つけられた方は[Issues](https://github.com/shirayu/ita-corpus-chuwa/issues)からお知らせいただければ幸いです．

## データ

### ``data/input``

ITA Corpusの原文を文分割したものがTSVであります

### ``data/knp``

- [京都大学テキストコーパス](https://nlp.ist.i.kyoto-u.ac.jp/index.php?%E4%BA%AC%E9%83%BD%E5%A4%A7%E5%AD%A6%E3%83%86%E3%82%AD%E3%82%B9%E3%83%88%E3%82%B3%E3%83%BC%E3%83%91%E3%82%B9)や[京都大学ウェブ文書リードコーパス](https://nlp.ist.i.kyoto-u.ac.jp/index.php?KWDLC)と同様の品詞体系（益岡・田窪品詞体系）でアノテーションしています
- 句間の係り受け関係も付与している．
- 各形態素の意味情報に``発音``を付与し，ITAコーパスの発音と一致するようにしています
- [ドキュメント](docs)
    - [処理方法](docs/processing.md)
    - [アノテーションメモ](docs/note.md)

## Developer

- [Yuta Hayashibe](https://github.com/shirayu)
    - I support [Tohoku sisters](https://zunko.jp/).
    - I supported [the crowdfunding for the creation of the ITA corpus, etc](https://greenfunding.jp/pub/projects/3891).

## Links

- [ITAコーパス](https://github.com/mmorise/ita-corpus)
- [ITAコーパス マルチモーダルデータベース](https://zunko.jp/multimodal_dev/login.php)

## Licence

[CC0 1.0 Universal (CC0 1.0)](https://creativecommons.org/publicdomain/zero/1.0/)
