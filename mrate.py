# -*- coding: utf-8 -*-
# argvを取得するためにsysモジュールをインポートする
import sys
# 正規表現を使用するためにreモジュールをインポートする
import re
# 外部コマンドを使用するためにsubprocessモジュールをインポートする
import subprocess

# コマンドライン引数をargvs（リスト）に格納する
argvs = sys.argv
# コマンドライン引数の数を変数argcに格納する
argc = len(argvs)

# 入力するBegraphファイルふたつが指定されていないときは使い方を表示して終了する
if argc < 5:
	print("Usage: python3 {} [input.GATC.bedgraph] [input.TC.bedgraph] [GATCpos.bedgraph] [Read number threshold]".format(argvs[0]))
	sys.exit()

# ひとつめの入力Bedgraphファイル名を変数inputGATCfilenameに格納する
inputGATCfilename = argvs[1]
# ふたつめ入力Bedgraphファイル名を変数inputTCfilenameに格納する
inputTCfilename = argvs[2]
# みっつめの入力Bedgraphファイル名を変数inputPosfilenameに格納する
inputPosfilename = argvs[3]
# リード数足切りのための閾値を変数readNumberThresholdに格納する
readNumberThreshold = int(argvs[4])
# 出力ファイル名を変数outputfilenameに格納する
outputfilename = inputGATCfilename.replace(".GATC.bedgraph", ".mrate.bedgraph")
# 一時出力ファイル名を変数tempoutputに格納する
tempoutput = inputGATCfilename.replace(".GATC.bedgraph", ".temp.bedgraph")


# ひとつめの入力ファイル名の末尾が".GATC.bedgraph"でないときは使い方を表示して終了する
if re.search(r'\.GATC\.bedgraph$', inputGATCfilename) == None:
	print("Usage: python3 {} [input.GATC.bedgraph] [input.TC.bedgraph] [GATCpos.bedgraph]".format(argvs[0]))
	sys.exit()
# ふたつめの入力ファイル名の末尾が".TC.bedgraph"でないときは使い方を表示して終了する
elif re.search(r'\.TC\.bedgraph$', inputTCfilename) == None:
	print("Usage: python3 {} [input.GATC.bedgraph] [input.TC.bedgraph] [GATCpos.bedgraph]".format(argvs[0]))
	sys.exit()
# みっつめの入力ファイル名の末尾が"GATCpos.bedgraph"でないときは使い方を表示して終了する
elif re.search(r'GATCpos\.bedgraph$', inputPosfilename) == None:
	print("Usage: python3 {} [input.GATC.bedgraph] [input.TC.bedgraph] [GATCpos.bedgraph]".format(argvs[0]))
	sys.exit()
# 入力ファイル名の末尾に問題がないときは以下を実行する
else:
	# 一時出力ファイルを追加書き込み用にオープンする
	tempoutputfile = open(tempoutput, 'a')	
	# ひとつめの入力ファイルをオープンする
	with open(inputGATCfilename) as input1:
		# 一行ずつ読み出して変数lineに格納する
		for line in input1:
			# 各行の末尾に"GATC"を追記して一時出力ファイルに追記する
			list1 = line.split()
			list1.append("GATC")
			string = ""
			for s in list1:
				string = string + "\t" + str(s)
			string = re.sub(r'^\t', "", string)
			string = string + "\n"
			tempoutputfile.write(string)

	# ふたつめの入力ファイルをオープンする		
	with open(inputTCfilename) as input2:
		# 一行ずつ読み出して変数lineに格納する
		for line in input2:
			# 各行の末尾に"TC"を追記して一時出力ファイルに追記する
			list1 = line.split()
			list1.append("TC")
			string = ""
			for s in list1:
				string = string + "\t" + str(s)
			string = re.sub(r'^\t', "", string)
			string = string + "\n"
			tempoutputfile.write(string)
	
	# みっつめの入力ファイルをオープンし、一時出力ファイルに内容を追記する
	with open(inputPosfilename) as input3:
		for line in input3:
			list1 = line.split()
			string = ""
			for s in list1:
				string = string + "\t" + str(s)
			string = re.sub(r'^\t', "", string)
			string = string + "\n"
			tempoutputfile.write(string)
	
	tempoutputfile.close()
	
	# 一時出力ファイルをソートし、ソート結果を変数sortedに格納する
	# Linux内のsortコマンドを利用します
	# sort [ソートしたいファイル] [オプション] の順でリストに格納されている必要がありそうです
	cmd = ['sort', tempoutput, '-k1,1d', '-k2,2n', '-k4,4n']
	# sort結果はbytes型で返ってくるので、str型にデコードする
	sorted = subprocess.check_output(cmd).decode()
	
	# sort結果をふたつめの一時ファイルに書き出す
	sortedoutputfilename = tempoutput + ".sorted"
	sortedoutputfile = open(sortedoutputfilename, 'w')
	sortedoutputfile.write(sorted)
	sortedoutputfile.close()
	
	# 最終出力ファイル（メチル化率計算結果）を追記モードでオープンする
	outputfile = open(outputfilename, 'a')
	# 配列pl (previous line)を初期化しておく
	pl = []
	# 配列cl (current line)を初期化しておく
	cl = []
	
	# sort結果全体を改行文字でスプリットする
	sorted = sorted.split("\n")
	# sort結果の各行について以下の処理を実行する
	for cl in sorted:
		# 各行をタブ区切り文字でスプリットする
		cl = cl.split("\t")
		# listの要素数が5でないときはclの内容をplに代入して次の行に移る
		if (len(pl) != 5 or len(cl) != 5):
			pl = cl
			continue
		# 以下の3条件が同時に成立するときのみ以下の処理を実行する
		# 条件1 plの末尾の要素が"posG_in_GATC"である
		# 条件2 clの末尾の要素が"TC"である
		# 条件3 plの座標とclの座標の差が2である
		if (pl[4] == "posG_in_GATC" and cl[4] == "TC" and int(cl[1]) == int(pl[1])+2):
			# メチル化率=100%、clの第4カラムの値と入れ替える
			cl[3] = 1
			outputfile.write(str(cl[0]) + "\t" + str(cl[1]) + "\t" + str(cl[2]) + "\t" + str(cl[3]) + "\t" + str(cl[4]) + "\n")
			# clの内容をplに代入して次の行に移る
			pl = cl
			continue		
		# 以下の3条件が同時に成立するときのみ以下の処理を実行する
		# 条件1 plの末尾の要素が"GATC"である
		# 条件2 clの末尾の要素が"TC"である
		# 条件3 plの座標とclの座標の差が2である
		elif (pl[4] == "GATC" and cl[4] == "TC" and int(cl[1]) == int(pl[1])+2):
			# メチル化率を計算し、clの第4カラムの値と入れ替える
			cl[3] = int(cl[3]) / (int(pl[3]) + int(cl[3]))
			# 分母がリード数足切り閾値以上ならば最終出力ファイルにclの内容を書き出す
			if ((int(pl[3]) + int(cl[3])) >= readNumberThreshold):
				outputfile.write(str(cl[0]) + "\t" + str(cl[1]) + "\t" + str(cl[2]) + "\t" + str(cl[3]) + "\t" + str(cl[4]) + "\n")
			# clの内容をplに代入して次の行に移る
			pl = cl
			continue
		# 上記の3条件のいずれかが成立しないときはclの内容をplに代入して次の行に移る
		else:
			pl = cl
			continue
