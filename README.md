# DamID-Seq
DamID-Seqデータ解析のためのPythonスクリプトを置いてあります。

## GATC_TC_extraction.py
#### [使い方]  
```$ python3 GATC_TC_extraction.py [filename.sam]```

#### [目的]
読み始めの配列が"GATC"であるリードと"TC"であるリードを別々に集計します。

#### [入力ファイル]
bowtie2によって出力されたマッピング後のSAMファイルを入力ファイルとします。

#### [出力ファイル]
Bedgraph形式のファイルをふたつ出力します。
- filename.GATC.bedgraph （リードカウントは"G"の座標にアサインされます）
- filename.TC.bedgraph （リードカウントは"T"の座標にアサインされます）

## mrate.py
#### [使い方]
```$ python3 mrate.py [filename.GATC.bedgraph] [filename.TC.bedgraph] [GATCpos.bedgraph] [リード数足切り閾値]```

#### [目的]
GATC_TC_extraction.py によって出力されたふたつのファイルから各ゲノム座標でのメチル化率を計算します。

各GATCポジションについて、(GATCリード数+TCリード数)≧(リード数足切り閾値）のときだけメチル化率を出力します。（180607追加）

メチル化率が0%のときも出力に含めるようにしました。（180607追加）

#### [入力ファイル]
GATC_TC_extraction.py によって出力されたふたつのBedgraphファイル および ゲノム中のすべてのGATCの座標を格納したBedgraph の合計3ファイルを入力とします。

#### [出力ファイル]
Bedgraph形式のファイルを3つ出力します。
- filename.temp.bedgraph （一時ファイルですが念のために残しておきます）
- filename.temp.bedgraph.sorted （上記の一時ファイルを染色体順・ゲノム座標順にソートしたもの。念の為に残しておきます）
- filename.mrate.bedgraph （メチル化率の計算結果。各メチル化率は"T"の座標にアサインされます）

## readnum.py
#### [使い方]
```$ python3 readnum.py [filename.GATC.bedgraph] [filename.TC.bedgraph] [GATCpos.bedgraph]```

#### [目的]
GATC_TC_extraction.py によって出力されたふたつのファイルから各ゲノム座標でのリード数の和を計算します。

#### [入力ファイル]
GATC_TC_extraction.py によって出力されたふたつのBedgraphファイル および ゲノム中のすべてのGATCの座標を格納したBedgraph の合計3ファイルを入力とします。

#### [出力ファイル]
Bedgraph形式のファイルを3つ出力します。
- filename.temp.bedgraph （一時ファイルですが念のために残しておきます）
- filename.temp.bedgraph.sorted （上記の一時ファイルを染色体順・ゲノム座標順にソートしたもの。念の為に残しておきます）
- filename.readnum.bedgraph （リード数の集計結果。リードカウントは"G"の位置にアサインされます）
