# DamID-Seq
DamID-Seqデータ解析のためのPythonスクリプトを置いてあります。

# GATC_TC_extraction.py
[使い方]
python3 GATC_TC_extraction.py [filename.sam]

[目的]
読み始めの配列が"GATC"であるリードと"TC"であるリードを別々に集計します。

[入力ファイル]
bowtie2によって出力されたマッピング後のSAMファイルを入力ファイルとします。

[出力ファイル]
Bedgraph形式のファイルをふたつ出力します。（filename.GATC.bedgraph および filename.TC.bedgraph)
