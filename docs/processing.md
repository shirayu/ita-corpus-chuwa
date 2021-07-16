
# How to annotate

## Generate text files

```bash
python3 ./scripts/ita-corpus-extract.py -i ./ita-corpus/emotion_transcript_utf8.txt -o input/emotion.tsv
python3 ./scripts/ita-corpus-extract.py -i ./ita-corpus/recitation_transcript_utf8.txt -o input/recitation.tsv
find input -type f | xargs cat | python3 ./scripts/generate_txt.py -o txt
```

## Manual fix

```bash
mkdir -p jumanpp-fixed
find txt -type f | sort | parallel -t 'jumanpp < {} > jumanpp-fixed/{/.}.jpp'  
# Work in jumanpp-fixed until the following script outputs no errors
poetry run python3 ./scripts/check_jumanpp.py -i txt-jumanpp-fixed -r ./input/emotion.tsv -r input/recitation.tsv 
```

## Annotate

Work with [Kyoto Corpus Annotation Tool](https://github.com/ku-nlp/KyotoCorpusAnnotationTool)

## Export

```bash
python3 ./scripts/katool2dist.py -i /path/to/kyoto_tool/data/files/ita/ -o knp
```

## Import

```bash
python3 ./scripts/dist2katool.py -i ./knp -o ./tmpdir
```
