# argvを取得するためにsysモジュールをインポートする
import sys
# 正規表現を使用するためにreモジュールをインポートする
import re
# copyを使用するためにcopyモジュールをインポートする
import copy

# コマンドライン引数をargvs（リスト）に格納する
argvs = sys.argv
# コマンドライン引数の数を変数argcに格納する
argc = len(argvs)
# 末尾が".sam"という正規表現を変数regexに格納する
regex = r'\.sam$'
# SAMファイル中の文字列検索で使用する正規表現を各変数に格納する
regex_samheader = r'^\@'
regex_GATCstart = r'^GATC'
regex_GATCend = r'GATC$'
regex_TCstart = r'^TC'
regex_AGend = r'GA$'

# 末端が"GACT"のリードの位置を記録する辞書dictGATCを初期化しておく
# データ構造は入れ子の辞書
# 1st keyが染色体名
# 1st value (=2nd key) がゲノム座標
# 2nd valueがリード数
dictGATC = {}
# 末端が"CT"のリードの位置を記録する辞書dictTCを初期化しておく
dictTC = {}

# 入力samファイル名を変数inputsamに格納する
inputfilename = argvs[1]
# 出力ファイル名を変数outputGATC, outputTCに格納する
outputGATC = inputfilename.replace(".sam", ".GATC.bedgraph")
outputTC = inputfilename.replace(".sam", ".TC.bedgraph")

# 入力するSAMファイルが指定されていないときは使い方を表示して終了する
if argc < 2:
	print("Usage: python3 {} [input.sam]".format(argvs[0]))
# 入力ファイル名の末尾が".sam"でないときは使い方を表示して終了する
elif re.search(regex, inputfilename) == None:
	print("Usage: python3 {} [input.sam]".format(argvs[0]))
# 入力ファイル名の末尾が".sam"であるときは以下を実行する
else:
	# 入力ファイルをオープンする
	with open(inputfilename) as samfile:
		# 一行ずつ読み出して変数lineに格納する
		for line in samfile:
			# その行が"@"から始まっていれば何もせずに次の行に移る
			if re.search(regex_samheader, line):
				continue
			# その行が"@"以外の文字で始まっていれば以下を実行する
			else:
				# リードのアラインメントスコアが0でないときは何もせずに次の行に移る
				if (re.search("AS:i:0", line) == None):
					continue
				# 行の内容を空白文字で区切ってリストlineに格納する
				line = line.split()
				# リードがマップされていなければ何もせずに次の行に移る
				if (int(line[1]) & 4 == 4):
					continue
				# リードがマップされていれば以下を実行する
				else:
					# 染色体名を変数chrに格納する
					chr = line[2]
					# スタート位置を変数startに格納する
					start = line[3]
					# リードの配列を変数seqに格納する
					seq = line[9]
					# リードの配列長を変数readlengthに格納する
					readlength = len(seq)
				# リードが順方向にマップされていれば以下を実行する
				if (int(line[1]) & 16 != 16):
					start = int(start) - 1
					# リードの読み出しが"GATC"であれば以下を実行する
					if re.search(regex_GATCstart, seq):
						if (chr in dictGATC):
							if (start in dictGATC[chr]):
								dictTEMP = dictGATC[chr]
								dictTEMP[start] = dictTEMP[start] + 1
								dictGATC[chr] = dictTEMP
							else:
								dictTEMP = dictGATC[chr]
								dictTEMP[start] = 1
								dictGATC[chr] = dictTEMP
						else:
							dictGATC[chr] = {start:1}
					# リードの読み出しが"TC"であれば以下を実行する
					if re.search(regex_TCstart, seq):
						if (chr in dictTC):
							if (start in dictTC[chr]):
								dictTEMP = dictTC[chr]
								dictTEMP[start] = dictTEMP[start] + 1
								dictTC[chr] = dictTEMP
							else:
								dictTEMP = dictTC[chr]
								dictTEMP[start] = 1
								dictTC[chr] = dictTEMP
						else:
							dictTC[chr] = {start:1}
				# リードが相補鎖にマップされていれば以下を実行する
				else:
					# リードの読み出しが"GATC"であれば以下を実行する
					if re.search(regex_GATCend, seq):
						start = int(start) + readlength - 5
						if (chr in dictGATC):
							if (start in dictGATC[chr]):
								dictTEMP = dictGATC[chr]
								dictTEMP[start] = dictTEMP[start] + 1
								dictGATC[chr] = dictTEMP
							else:
								dictTEMP = dictGATC[chr]
								dictTEMP[start] = 1
								dictGATC[chr] = dictTEMP
						else:
							dictGATC[chr] = {start:1}
					# リードの読み出しが"GA"であれば以下を実行する
					if re.search(regex_AGend, seq):
						start = int(start) + readlength - 1
						if (chr in dictTC):
							if (start in dictTC[chr]):
								dictTEMP = dictTC[chr]
								dictTEMP[start] = dictTEMP[start] + 1
								dictTC[chr] = dictTEMP
							else:
								dictTEMP = dictTC[chr]
								dictTEMP[start] = 1
								dictTC[chr] = dictTEMP
						else:
							dictTC[chr] = {start:1}

outputGATCfile = open(outputGATC, 'w')						
for keychr in dictGATC:
	for keystart in dictGATC[keychr]:
		dictTEMP = dictGATC[keychr]
		posnext = int(keystart) + 1
		outputline = str(keychr)+"\t"+str(keystart)+"\t"+str(posnext)+"\t"+str(dictTEMP[keystart])+"\n"
		outputGATCfile.write(outputline)
outputGATCfile.close()

outputTCfile = open(outputTC, 'w')						
for keychr in dictTC:
	for keystart in dictTC[keychr]:
		dictTEMP = dictTC[keychr]
		posnext = int(keystart) + 1
		outputline = str(keychr)+"\t"+str(keystart)+"\t"+str(posnext)+"\t"+str(dictTEMP[keystart])+"\n"
		outputTCfile.write(outputline)
outputTCfile.close()