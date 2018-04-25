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

# mrate.py
[使い方] python3 mrate.py [filename.GATC.bedgraph] [filename.TC.bedgraph]

[目的]
GATC_TC_extraction.py によって出力されたふたつのファイルから各ゲノム座標でのメチル化率を計算します。

[入力ファイル]
GATC_TC_extraction.py によって出力されたふたつのファイルを入力ファイルとします。

[出力ファイル]
Bedgraph形式のファイルを3つ出力します。（filename.temp.bedgraph および filename.temp.bedgraph.sorted および filename.mrate.bedgraph)
