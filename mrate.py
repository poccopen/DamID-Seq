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

# ひとつめの入力Bedgraphファイル名を変数inputGATCfilenameに格納する
inputGATCfilename = argvs[1]
# ふたつめ入力Bedgraphファイル名を変数inputTCfilenameに格納する
inputTCfilename = argvs[2]
# 出力ファイル名を変数outputfilenameに格納する
outputfilename = inputGATCfilename.replace(".GATC.bedgraph", ".mrate.bedgraph")
# 一時出力ファイル名を変数tempoutputに格納する
tempoutput = inputGATCfilename.replace(".GATC.bedgraph", ".temp.bedgraph")

# 入力するBegraphファイルふたつが指定されていないときは使い方を表示して終了する
if argc < 3:
	print("Usage: python3 {} [input.GATC.bedgraph] [input.TC.bedgraph]".format(argvs[0]))
# ひとつめの入力ファイル名の末尾が".GATC.bedgraph"でないときは使い方を表示して終了する
elif re.search(r'\.GATC\.bedgraph$', inputGATCfilename) == None:
	print("Usage: python3 {} [input.GATC.bedgraph] [input.TC.bedgraph]".format(argvs[0]))
# ふたつめの入力ファイル名の末尾が".TC.bedgraph"でないときは使い方を表示して終了する
elif re.search(r'\.TC\.bedgraph$', inputTCfilename) == None:
	print("Usage: python3 {} [input.GATC.bedgraph] [input.TC.bedgraph]".format(argvs[0]))
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
	tempoutputfile.close()
	
	# 一時出力ファイルをソートし、ソート結果を変数sortedに格納する
	# Linux内のsortコマンドを利用します
	# sort [ソートしたいファイル] [オプション] の順でリストに格納されている必要がありそうです
	cmd = ['sort', tempoutput, '-k1,1d', '-k2,2n']
	" sort結果はbytes型で返ってくるので、str型にデコードする
	sorted = subprocess.check_output(cmd).decode()
	
	
	sortedoutputfilename = tempoutput + ".sorted"
	sortedoutputfile = open(sortedoutputfilename, 'w')
	sortedoutputfile.write(sorted)
	sortedoutputfile.close()
	
	outputfile = open(outputfilename, 'a')
	pl = []
	cl = []
	
	sorted = sorted.split("\n")
	for cl in sorted:
		
		cl = cl.split("\t")
		
		if (len(pl) != 5 or len(cl) != 5):
			pl = cl
			continue
		if (pl[4] == "GATC" and cl[4] == "TC" and int(cl[1]) == int(pl[1])+2):
			cl[3] = int(cl[3]) / (int(pl[3]) + int(cl[3]))
			outputfile.write(str(cl[0]) + "\t" + str(cl[1]) + "\t" + str(cl[2]) + "\t" + str(cl[3]) + "\t" + str(cl[4]) + "\n")
			pl = cl
			continue
		else:
			pl = cl
			continue
